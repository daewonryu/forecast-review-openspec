"""
Simulation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.llm import get_llm_service, LLMService
from app.services.persona import PersonaService
from app.services.simulation import SimulationService
from app.schemas import (
    SimulationRunRequest,
    SimulationResponse,
    PersonaResultResponse,
    PersonaDrillDownResponse
)

router = APIRouter(prefix="/api/simulations", tags=["Simulations"])


def get_simulation_service(
    llm_service: LLMService = Depends(get_llm_service)
) -> SimulationService:
    """Dependency to get simulation service"""
    persona_service = PersonaService(llm_service)
    return SimulationService(llm_service, persona_service)


@router.post("/run", response_model=SimulationResponse)
async def run_simulation(
    request: SimulationRunRequest,
    db: Session = Depends(get_db),
    simulation_service: SimulationService = Depends(get_simulation_service)
):
    """
    Run simulation with a persona set on draft content.
    
    - **draft_content**: Text content to test (10-5000 chars)
    - **persona_set_id**: ID of the persona set to use
    
    Returns simulation results with persona reactions and aggregate scores.
    Simulations run in parallel and complete in under 20 seconds.
    Handles partial failures gracefully.
    
    Insights are automatically generated in the background after simulation completes.
    """
    user_id = 1  # MVP: default user
    
    try:
        result = await simulation_service.run_simulation(
            draft_content=request.draft_content,
            persona_set_id=request.persona_set_id,
            user_id=user_id,
            db=db
        )
        
        # Automatically trigger insights generation in the background
        # This happens asynchronously so it doesn't block the response
        from app.services.insights import InsightsService
        from app.services.llm import LLMService
        import asyncio
        
        async def generate_insights_background():
            try:
                llm_service = LLMService()
                insights_service = InsightsService(db=db, llm_service=llm_service)
                
                # Get simulation results
                from app.db.models import SimulationResult
                simulation_results = db.query(SimulationResult).filter(
                    SimulationResult.draft_id == result["draft_id"]
                ).all()
                
                await insights_service.generate_insights(
                    draft_id=result["draft_id"],
                    simulation_results=simulation_results
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Background insights generation failed: {str(e)}", exc_info=True)
        
        # Start background task
        asyncio.create_task(generate_insights_background())
        
        # Convert to response format
        persona_results = [
            PersonaResultResponse(**r) for r in result["results"]
        ]
        
        return SimulationResponse(
            draft_id=result["draft_id"],
            simulation_id=result["simulation_id"],
            results=persona_results,
            aggregate=result["aggregate"],
            completed_at=result["completed_at"],
            duration_seconds=result["duration_seconds"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running simulation: {str(e)}"
        )


@router.get("/{simulation_id}")
async def get_simulation(
    simulation_id: str,
    db: Session = Depends(get_db),
    simulation_service: SimulationService = Depends(get_simulation_service)
):
    """
    Retrieve a previously run simulation by ID.
    """
    user_id = 1  # MVP: default user
    
    result = simulation_service.get_simulation_results(simulation_id, user_id, db)
    
    if not result:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return result


@router.get("/")
async def list_simulations(
    user_id: int = 1,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all simulations for a user with pagination.
    Returns the most recent simulation result for each draft.
    """
    from app.db.models import Draft, SimulationResult
    from sqlalchemy import func
    
    skip = (page - 1) * page_size
    
    # Get most recent simulation for each draft
    subquery = (
        db.query(
            SimulationResult.draft_id,
            func.max(SimulationResult.id).label('max_id')
        )
        .join(Draft, Draft.id == SimulationResult.draft_id)
        .filter(Draft.user_id == user_id)
        .group_by(SimulationResult.draft_id)
        .subquery()
    )
    
    simulations = (
        db.query(SimulationResult, Draft)
        .join(Draft, Draft.id == SimulationResult.draft_id)
        .join(subquery, SimulationResult.id == subquery.c.max_id)
        .order_by(SimulationResult.created_at.desc())
        .offset(skip)
        .limit(page_size)
        .all()
    )
    
    total = db.query(func.count(func.distinct(Draft.id))).join(
        SimulationResult, Draft.id == SimulationResult.draft_id
    ).filter(Draft.user_id == user_id).scalar()
    
    # Calculate aggregate scores from results with the same simulation_id
    result_list = []
    for sim_result, draft in simulations:
        # Get all results for this simulation_id to calculate aggregate
        all_results = db.query(SimulationResult).filter(
            SimulationResult.simulation_id == sim_result.simulation_id
        ).all()
        
        avg_trust = sum(r.trust_score for r in all_results) / len(all_results) if all_results else 0
        avg_excitement = sum(r.excitement_score for r in all_results) / len(all_results) if all_results else 0
        avg_backlash = sum(r.backlash_risk_score for r in all_results) / len(all_results) if all_results else 0
        
        result_list.append({
            "simulation_id": sim_result.simulation_id,
            "draft_id": draft.id,
            "draft_content": draft.content,
            "completed_at": sim_result.created_at.isoformat(),
            "duration_seconds": 0,  # Field not stored in database
            "aggregate": {
                "avg_trust": round(avg_trust, 2),
                "avg_excitement": round(avg_excitement, 2),
                "avg_backlash": round(avg_backlash, 2)
            }
        })
    
    return {
        "simulations": result_list,
        "total": total or 0,
        "page": page,
        "page_size": page_size
    }


@router.get("/{simulation_id}/personas/{persona_id}", response_model=PersonaDrillDownResponse)
async def get_persona_drill_down(
    simulation_id: str,
    persona_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed drill-down view for a specific persona in a simulation.
    
    Compares persona scores to group average and identifies outliers.
    """
    from app.db.models import SimulationResult, Persona
    
    # Get this persona's result
    persona_result = db.query(SimulationResult).filter(
        SimulationResult.simulation_id == simulation_id,
        SimulationResult.persona_id == persona_id
    ).first()
    
    if not persona_result:
        raise HTTPException(
            status_code=404,
            detail=f"Persona {persona_id} not found in simulation {simulation_id}"
        )
    
    # Get all results for this simulation
    all_results = db.query(SimulationResult).filter(
        SimulationResult.simulation_id == simulation_id
    ).all()
    
    if not all_results:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    # Get persona details
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    # Calculate group averages
    group_avg_trust = sum(r.trust_score for r in all_results) / len(all_results)
    group_avg_excitement = sum(r.excitement_score for r in all_results) / len(all_results)
    group_avg_backlash = sum(r.backlash_risk_score for r in all_results) / len(all_results)
    
    # Calculate deltas
    delta_trust = persona_result.trust_score - group_avg_trust
    delta_excitement = persona_result.excitement_score - group_avg_excitement
    delta_backlash = persona_result.backlash_risk_score - group_avg_backlash
    
    # Determine if outlier (> 2.5 points difference on any metric)
    is_outlier = (
        abs(delta_trust) > 2.5 or
        abs(delta_excitement) > 2.5 or
        abs(delta_backlash) > 2.5
    )
    
    return PersonaDrillDownResponse(
        persona_details={
            "id": persona.id,
            "name": persona.name,
            "archetype": persona.archetype,
            "loyalty_level": persona.loyalty_level,
            "core_values": persona.core_values
        },
        persona_scores={
            "trust": persona_result.trust_score,
            "excitement": persona_result.excitement_score,
            "backlash_risk": persona_result.backlash_risk_score
        },
        group_averages={
            "avg_trust": round(group_avg_trust, 2),
            "avg_excitement": round(group_avg_excitement, 2),
            "avg_backlash_risk": round(group_avg_backlash, 2)
        },
        delta={
            "trust": round(delta_trust, 2),
            "excitement": round(delta_excitement, 2),
            "backlash_risk": round(delta_backlash, 2)
        },
        is_outlier=is_outlier,
        reactions={
            "internal_monologue": persona_result.internal_monologue,
            "public_comment": persona_result.public_comment,
            "reasoning": persona_result.reasoning
        }
    )
