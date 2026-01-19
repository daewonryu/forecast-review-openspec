"""
Simulation service for running persona reactions to content
"""
import asyncio
import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.llm import LLMService
from app.services.persona import PersonaService
from app.db.models import Draft, SimulationResult, Persona
from app.schemas import PersonaResultResponse, AggregateScores

logger = logging.getLogger(__name__)


class SimulationService:
    """Service for running content simulations with personas"""
    
    def __init__(self, llm_service: LLMService, persona_service: PersonaService):
        self.llm_service = llm_service
        self.persona_service = persona_service
    
    async def run_simulation(
        self,
        draft_content: str,
        persona_set_id: str,
        user_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Run simulation with all personas in a set
        
        Args:
            draft_content: Content to test
            persona_set_id: ID of persona set to use
            user_id: User ID
            db: Database session
        
        Returns:
            Complete simulation results with aggregated scores
        """
        start_time = datetime.utcnow()
        simulation_id = str(uuid.uuid4())
        
        logger.info(f"Starting simulation {simulation_id} with persona set {persona_set_id}")
        
        # Create draft record
        draft = Draft(user_id=user_id, content=draft_content)
        db.add(draft)
        db.commit()
        db.refresh(draft)
        
        # Get personas
        personas = self.persona_service.get_persona_set(persona_set_id, user_id, db)
        if not personas or len(personas) != 5:
            raise ValueError(f"Persona set not found or incomplete (expected 5, got {len(personas) if personas else 0})")
        
        # Prepare requests for parallel execution
        requests = []
        for persona in personas:
            persona_dict = {
                "id": persona.id,
                "name": persona.name,
                "archetype": persona.archetype,
                "loyalty_level": persona.loyalty_level,
                "core_values": persona.core_values
            }
            requests.append({
                "persona": persona_dict,
                "audience_description": persona.audience_description
            })
        
        # Run all simulations in parallel with error handling
        results = await self._run_parallel_simulations(
            draft_content,
            requests,
            simulation_id,
            draft.id,
            db
        )
        
        # Calculate aggregate scores
        aggregate = self._calculate_aggregate_scores(results)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(
            f"Simulation {simulation_id} completed in {duration:.2f}s. "
            f"Success: {sum(1 for r in results if r['status'] == 'success')}/{len(results)}"
        )
        
        return {
            "draft_id": draft.id,
            "simulation_id": simulation_id,
            "results": results,
            "aggregate": aggregate,
            "completed_at": end_time,
            "duration_seconds": round(duration, 2)
        }
    
    async def _run_parallel_simulations(
        self,
        content: str,
        requests: List[Dict[str, Any]],
        simulation_id: str,
        draft_id: int,
        db: Session
    ) -> List[Dict[str, Any]]:
        """
        Run multiple persona simulations in parallel
        
        Handles partial failures gracefully - returns whatever succeeded
        """
        tasks = []
        for req in requests:
            task = self._run_single_simulation_with_timeout(
                persona=req["persona"],
                content=content,
                audience_description=req["audience_description"]
            )
            tasks.append(task)
        
        # Gather results with exception handling
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and save to database
        processed_results = []
        for i, result in enumerate(raw_results):
            persona = requests[i]["persona"]
            
            if isinstance(result, Exception):
                # Handle error case
                error_result = {
                    "persona_id": persona["id"],
                    "persona_name": persona["name"],
                    "status": "error",
                    "error_message": str(result),
                    "internal_monologue": "",
                    "public_comment": "",
                    "scores": {"trust": 5, "excitement": 5, "backlash_risk": 5},
                    "reasoning": None
                }
                processed_results.append(error_result)
                
                # Save error to database
                sim_result = SimulationResult(
                    simulation_id=simulation_id,
                    draft_id=draft_id,
                    persona_id=persona["id"],
                    trust_score=5,
                    excitement_score=5,
                    backlash_risk_score=5,
                    internal_monologue="[Error occurred]",
                    public_comment="[Error occurred]",
                    reasoning=None,
                    status="error",
                    error_message=str(result)
                )
                db.add(sim_result)
            
            elif result.get("status") == "success":
                # Success case
                processed_results.append(result)
                
                # Save to database
                sim_result = SimulationResult(
                    simulation_id=simulation_id,
                    draft_id=draft_id,
                    persona_id=result["persona_id"],
                    trust_score=result["scores"]["trust"],
                    excitement_score=result["scores"]["excitement"],
                    backlash_risk_score=result["scores"]["backlash_risk"],
                    internal_monologue=result["internal_monologue"],
                    public_comment=result["public_comment"],
                    reasoning=result.get("reasoning"),
                    status="success"
                )
                db.add(sim_result)
            else:
                # Error from persona service
                processed_results.append(result)
                
                sim_result = SimulationResult(
                    simulation_id=simulation_id,
                    draft_id=draft_id,
                    persona_id=result["persona_id"],
                    trust_score=5,
                    excitement_score=5,
                    backlash_risk_score=5,
                    internal_monologue="[Error occurred]",
                    public_comment="[Error occurred]",
                    reasoning=None,
                    status="error",
                    error_message=result.get("error_message", "Unknown error")
                )
                db.add(sim_result)
        
        db.commit()
        
        return processed_results
    
    async def _run_single_simulation_with_timeout(
        self,
        persona: Dict[str, Any],
        content: str,
        audience_description: str
    ) -> Dict[str, Any]:
        """
        Run single persona simulation with timeout
        
        Timeout is handled by the LLM service, but we add an extra safety layer
        """
        try:
            # Add 5 second buffer to LLM timeout
            result = await asyncio.wait_for(
                self.persona_service.generate_persona_reaction(
                    persona, content, audience_description
                ),
                timeout=65  # 60s LLM timeout + 5s buffer
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Timeout for persona {persona['name']}")
            raise Exception(f"Simulation timeout for {persona['name']}")
        except Exception as e:
            logger.error(f"Error in simulation for {persona['name']}: {e}")
            raise
    
    def _calculate_aggregate_scores(self, results: List[Dict[str, Any]]) -> AggregateScores:
        """Calculate average scores from all successful results"""
        successful_results = [r for r in results if r.get("status") == "success"]
        
        if not successful_results:
            # All failed - return neutral scores
            return AggregateScores(
                avg_trust=5.0,
                avg_excitement=5.0,
                avg_backlash_risk=5.0
            )
        
        total_trust = sum(r["scores"]["trust"] for r in successful_results)
        total_excitement = sum(r["scores"]["excitement"] for r in successful_results)
        total_backlash = sum(r["scores"]["backlash_risk"] for r in successful_results)
        
        count = len(successful_results)
        
        return AggregateScores(
            avg_trust=round(total_trust / count, 1),
            avg_excitement=round(total_excitement / count, 1),
            avg_backlash_risk=round(total_backlash / count, 1)
        )
    
    def get_simulation_results(
        self,
        simulation_id: str,
        user_id: int,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """Retrieve simulation results by ID"""
        results = db.query(SimulationResult).filter(
            SimulationResult.simulation_id == simulation_id
        ).all()
        
        if not results:
            return None
        
        # Verify user owns the draft
        draft = db.query(Draft).filter(Draft.id == results[0].draft_id).first()
        if not draft or draft.user_id != user_id:
            return None
        
        # Convert to response format
        persona_results = []
        for r in results:
            persona_results.append({
                "persona_id": r.persona_id,
                "persona_name": r.persona.name if r.persona else "Unknown",
                "internal_monologue": r.internal_monologue,
                "public_comment": r.public_comment,
                "scores": {
                    "trust": r.trust_score,
                    "excitement": r.excitement_score,
                    "backlash_risk": r.backlash_risk_score
                },
                "reasoning": r.reasoning,
                "status": r.status,
                "error_message": r.error_message
            })
        
        # Calculate aggregate
        aggregate = self._calculate_aggregate_scores(persona_results)
        
        return {
            "simulation_id": simulation_id,
            "draft_id": results[0].draft_id,
            "results": persona_results,
            "aggregate": aggregate,
            "created_at": results[0].created_at
        }
