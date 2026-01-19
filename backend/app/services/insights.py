"""
Insights Service - Generate analytics, pain points, and improvement tips
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
import logging

from app.db.models import SimulationResult, Draft, Persona, Insight
from app.services.llm import LLMService
from app.services.prompts import PAIN_POINT_EXTRACTION_PROMPT, IMPROVEMENT_TIPS_PROMPT

logger = logging.getLogger(__name__)


class InsightsService:
    def __init__(self, db: Session, llm_service: LLMService):
        self.db = db
        self.llm_service = llm_service
    
    def calculate_aggregate_analytics(self, simulation_results: List[SimulationResult]) -> Dict[str, Any]:
        """
        Calculate aggregate analytics from simulation results.
        
        Returns:
            - average_scores: Dict with avg trust, excitement, backlash
            - overall_sentiment: "positive" | "neutral" | "negative"
            - score_distribution: breakdown by persona
        """
        if not simulation_results:
            return {
                "average_scores": {"trust": 0, "excitement": 0, "backlash": 0},
                "overall_sentiment": "neutral",
                "score_distribution": []
            }
        
        # Calculate averages
        total_trust = sum(r.trust_score for r in simulation_results)
        total_excitement = sum(r.excitement_score for r in simulation_results)
        total_backlash = sum(r.backlash_risk_score for r in simulation_results)
        count = len(simulation_results)
        
        avg_trust = total_trust / count
        avg_excitement = total_excitement / count
        avg_backlash = total_backlash / count
        
        # Determine overall sentiment
        # Logic: positive if (trust + excitement) > backlash + threshold
        positive_score = avg_trust + avg_excitement
        negative_score = avg_backlash * 2  # Weight backlash more heavily
        
        if positive_score > negative_score + 3:
            overall_sentiment = "positive"
        elif negative_score > positive_score + 3:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        # Score distribution
        score_distribution = [
            {
                "persona_id": r.persona_id,
                "persona_name": r.persona.name if r.persona else "Unknown",
                "trust_score": r.trust_score,
                "excitement_score": r.excitement_score,
                "backlash_score": r.backlash_risk_score
            }
            for r in simulation_results
        ]
        
        return {
            "average_scores": {
                "trust": round(avg_trust, 2),
                "excitement": round(avg_excitement, 2),
                "backlash": round(avg_backlash, 2)
            },
            "overall_sentiment": overall_sentiment,
            "score_distribution": score_distribution
        }
    
    async def extract_pain_points(
        self,
        draft_content: str,
        simulation_results: List[SimulationResult]
    ) -> List[Dict[str, Any]]:
        """
        Use LLM to extract pain points from persona feedback.
        
        Returns list of pain points with:
        - text: problematic phrase from draft
        - severity: high/medium/low
        - affected_personas: list of persona names
        - reasoning: why it's problematic
        """
        if not simulation_results:
            return []
        
        # Prepare context for LLM
        persona_feedback = []
        for result in simulation_results:
            persona_feedback.append({
                "persona_name": result.persona.name if result.persona else "Unknown",
                "loyalty_level": result.persona.loyalty_level if result.persona else 5,
                "internal_reaction": result.internal_monologue,
                "public_response": result.public_comment,
                "trust_score": result.trust_score,
                "excitement_score": result.excitement_score,
                "backlash_score": result.backlash_risk_score,
                "reasoning": result.reasoning
            })
        
        # Sort by backlash score (highest first)
        persona_feedback.sort(key=lambda x: x["backlash_score"], reverse=True)
        
        # Build prompt
        prompt = PAIN_POINT_EXTRACTION_PROMPT.format(
            draft_content=draft_content,
            persona_feedback=json.dumps(persona_feedback, indent=2)
        )
        
        try:
            # Call LLM
            response = await self.llm_service.generate(
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing social media reactions and identifying problematic content. You must respond ONLY with valid JSON array, no other text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response["content"]
            logger.info(f"Pain points LLM response length: {len(content)} chars")
            logger.debug(f"Pain points raw response: {content[:200]}...")
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse response (expecting JSON array)
            pain_points = json.loads(content)
            
            # Validate structure
            if not isinstance(pain_points, list):
                logger.error("Pain points response is not a list")
                return []
            
            return pain_points
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse pain points JSON: {e}")
            logger.error(f"Response content was: {content[:500] if 'content' in locals() else 'N/A'}")
            return []
        except Exception as e:
            logger.error(f"Pain point extraction failed: {e}")
            return []
    
    async def generate_improvement_tips(
        self,
        draft_content: str,
        simulation_results: List[SimulationResult],
        pain_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Use LLM to generate exactly 3 actionable improvement tips.
        
        Returns list of 3 tips with:
        - tip: actionable suggestion
        - rationale: why this would help
        - impact: estimated improvement (high/medium/low)
        - addresses: which pain points it addresses
        """
        if not simulation_results:
            return []
        
        # Prepare aggregate data
        aggregate_analytics = self.calculate_aggregate_analytics(simulation_results)
        
        # Prepare persona feedback summary
        persona_summaries = []
        for result in simulation_results:
            persona_summaries.append({
                "persona_name": result.persona.name if result.persona else "Unknown",
                "loyalty_level": result.persona.loyalty_level if result.persona else 5,
                "scores": {
                    "trust": result.trust_score,
                    "excitement": result.excitement_score,
                    "backlash": result.backlash_risk_score
                },
                "reasoning": result.reasoning
            })
        
        # Build prompt
        prompt = IMPROVEMENT_TIPS_PROMPT.format(
            draft_content=draft_content,
            aggregate_analytics=json.dumps(aggregate_analytics, indent=2),
            persona_summaries=json.dumps(persona_summaries, indent=2),
            pain_points=json.dumps(pain_points, indent=2)
        )
        
        try:
            # Call LLM
            response = await self.llm_service.generate(
                messages=[
                    {"role": "system", "content": "You are an expert social media strategist who provides actionable, specific advice. You must respond ONLY with valid JSON array containing exactly 3 tips, no other text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            content = response["content"]
            logger.info(f"Tips LLM response length: {len(content)} chars")
            logger.debug(f"Tips raw response: {content[:200]}...")
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse response (expecting JSON array with exactly 3 tips)
            tips = json.loads(content)
            
            # Validate structure
            if not isinstance(tips, list):
                logger.error("Tips response is not a list")
                return []
            
            # Ensure exactly 3 tips
            tips = tips[:3]
            
            return tips
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse tips JSON: {e}")
            logger.error(f"Response content was: {content[:500] if 'content' in locals() else 'N/A'}")
            return []
        except Exception as e:
            logger.error(f"Tip generation failed: {e}")
            return []
    
    async def generate_insights(
        self,
        draft_id: str,
        simulation_results: List[SimulationResult]
    ) -> Optional[Insight]:
        """
        Generate complete insights for a simulation.
        
        Steps:
        1. Calculate aggregate analytics
        2. Extract pain points via LLM
        3. Generate 3 improvement tips via LLM
        4. Save to database
        """
        if not simulation_results:
            logger.warning(f"No simulation results for draft {draft_id}")
            return None
        
        # Get draft
        draft = self.db.query(Draft).filter(Draft.id == draft_id).first()
        if not draft:
            logger.error(f"Draft {draft_id} not found")
            return None
        
        # Step 1: Calculate aggregate analytics
        logger.info(f"Calculating aggregate analytics for draft {draft_id}")
        aggregate_analytics = self.calculate_aggregate_analytics(simulation_results)
        
        # Step 2: Extract pain points
        logger.info(f"Extracting pain points for draft {draft_id}")
        pain_points = await self.extract_pain_points(
            draft_content=draft.content,
            simulation_results=simulation_results
        )
        
        # Step 3: Generate improvement tips
        logger.info(f"Generating improvement tips for draft {draft_id}")
        improvement_tips = await self.generate_improvement_tips(
            draft_content=draft.content,
            simulation_results=simulation_results,
            pain_points=pain_points
        )
        
        # Step 4: Save to database
        # Get simulation_id from results
        simulation_id = simulation_results[0].simulation_id if simulation_results else None
        if not simulation_id:
            logger.error("No simulation_id found in results")
            return None
        
        insight = Insight(
            simulation_id=simulation_id,
            pain_points=pain_points,
            improvement_tips=improvement_tips,
            overall_sentiment=aggregate_analytics["overall_sentiment"],
            avg_trust=aggregate_analytics["average_scores"]["trust"],
            avg_excitement=aggregate_analytics["average_scores"]["excitement"],
            avg_backlash_risk=aggregate_analytics["average_scores"]["backlash"]
        )
        
        self.db.add(insight)
        self.db.commit()
        self.db.refresh(insight)
        
        logger.info(f"Insights generated for draft {draft_id}: insight_id={insight.id}")
        
        return insight
    
    def get_persona_drill_down(
        self,
        persona_id: str,
        simulation_results: List[SimulationResult]
    ) -> Dict[str, Any]:
        """
        Get detailed view of a single persona compared to group average.
        
        Returns:
        - persona_details: name, loyalty, traits
        - persona_scores: trust, excitement, backlash
        - group_averages: same scores for comparison
        - delta: difference from group
        - is_outlier: True if significantly different
        """
        # Get persona result
        persona_result = next(
            (r for r in simulation_results if r.persona_id == persona_id),
            None
        )
        
        if not persona_result:
            return {}
        
        # Calculate group averages
        aggregate = self.calculate_aggregate_analytics(simulation_results)
        group_avg = aggregate["average_scores"]
        
        # Calculate deltas
        delta_trust = persona_result.trust_score - group_avg["trust"]
        delta_excitement = persona_result.excitement_score - group_avg["excitement"]
        delta_backlash = persona_result.backlash_risk_score - group_avg["backlash"]
        
        # Determine if outlier (>2 points difference in any score)
        is_outlier = (
            abs(delta_trust) > 2 or
            abs(delta_excitement) > 2 or
            abs(delta_backlash) > 2
        )
        
        return {
            "persona_details": {
                "id": persona_result.persona_id,
                "name": persona_result.persona.name,
                "loyalty_level": persona_result.persona.loyalty_level,
                "core_values": persona_result.persona.core_values,
                "traits": persona_result.persona.traits
            },
            "persona_scores": {
                "trust": persona_result.trust_score,
                "excitement": persona_result.excitement_score,
                "backlash": persona_result.backlash_risk_score
            },
            "group_averages": group_avg,
            "delta": {
                "trust": round(delta_trust, 2),
                "excitement": round(delta_excitement, 2),
                "backlash": round(delta_backlash, 2)
            },
            "is_outlier": is_outlier,
            "reactions": {
                "internal": persona_result.internal_monologue,
                "public": persona_result.public_comment,
                "reasoning": persona_result.reasoning
            }
        }
    
    def get_sentiment_trends(
        self,
        persona_set_id: str,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """
        Track sentiment trends across multiple simulations with the same persona set.
        
        Returns list of simulations with:
        - simulation_date
        - draft_content (first 100 chars)
        - average_scores
        - delta_from_previous (if applicable)
        """
        # Get all drafts for this user with this persona set
        drafts = (
            self.db.query(Draft)
            .filter(Draft.user_id == user_id, Draft.persona_set_id == persona_set_id)
            .order_by(Draft.created_at)
            .all()
        )
        
        if not drafts:
            return []
        
        trends = []
        previous_avg = None
        
        for draft in drafts:
            # Get simulation results for this draft
            simulation_results = (
                self.db.query(SimulationResult)
                .filter(SimulationResult.draft_id == draft.id)
                .all()
            )
            
            if not simulation_results:
                continue
            
            # Calculate aggregate
            aggregate = self.calculate_aggregate_analytics(simulation_results)
            avg_scores = aggregate["average_scores"]
            
            # Calculate delta from previous
            delta = None
            if previous_avg:
                delta = {
                    "trust": round(avg_scores["trust"] - previous_avg["trust"], 2),
                    "excitement": round(avg_scores["excitement"] - previous_avg["excitement"], 2),
                    "backlash": round(avg_scores["backlash"] - previous_avg["backlash"], 2)
                }
            
            trends.append({
                "draft_id": draft.id,
                "simulation_date": draft.created_at.isoformat(),
                "draft_preview": draft.content[:100] + "..." if len(draft.content) > 100 else draft.content,
                "average_scores": avg_scores,
                "overall_sentiment": aggregate["overall_sentiment"],
                "delta_from_previous": delta
            })
            
            previous_avg = avg_scores
        
        return trends
