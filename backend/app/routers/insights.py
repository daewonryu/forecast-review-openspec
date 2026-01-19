"""
Insights API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.db.database import get_db
from app.db.models import Draft, SimulationResult, Insight
from app.services.insights import InsightsService
from app.services.llm import LLMService
from app import schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/insights", tags=["insights"])


def get_insights_service(db: Session = Depends(get_db)) -> InsightsService:
    """Dependency to get insights service"""
    llm_service = LLMService()
    return InsightsService(db=db, llm_service=llm_service)


@router.post("/generate/{draft_id}", response_model=schemas.InsightResponse)
async def generate_insights(
    draft_id: str,
    service: InsightsService = Depends(get_insights_service)
):
    """
    Generate insights for a completed simulation.
    
    Steps:
    1. Calculate aggregate analytics
    2. Extract pain points via LLM
    3. Generate 3 improvement tips via LLM
    4. Save to database
    """
    # Get simulation results
    simulation_results = (
        service.db.query(SimulationResult)
        .filter(SimulationResult.draft_id == draft_id)
        .all()
    )
    
    if not simulation_results:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation results found for draft {draft_id}"
        )
    
    # Check if insights already exist for this simulation
    simulation_id = simulation_results[0].simulation_id
    existing_insight = (
        service.db.query(Insight)
        .filter(Insight.simulation_id == simulation_id)
        .first()
    )
    
    if existing_insight:
        logger.info(f"Returning existing insights for simulation {simulation_id}")
        return existing_insight
    
    try:
        # Generate insights
        insight = await service.generate_insights(
            draft_id=draft_id,
            simulation_results=simulation_results
        )
        
        if not insight:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate insights"
            )
        
        return insight
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating insights: {str(e)}"
        )


@router.get("/{insight_id}", response_model=schemas.InsightResponse)
def get_insights(
    insight_id: int,
    db: Session = Depends(get_db)
):
    """Get insights by ID"""
    insight = db.query(Insight).filter(Insight.id == insight_id).first()
    
    if not insight:
        raise HTTPException(
            status_code=404,
            detail=f"Insight {insight_id} not found"
        )
    
    return insight


@router.get("/draft/{draft_id}", response_model=schemas.InsightResponse)
def get_insights_by_draft(
    draft_id: int,
    db: Session = Depends(get_db)
):
    """Get insights for a specific draft"""
    # Get simulation_id from results
    simulation_result = (
        db.query(SimulationResult)
        .filter(SimulationResult.draft_id == draft_id)
        .first()
    )
    
    if not simulation_result:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation found for draft {draft_id}"
        )
    
    insight = db.query(Insight).filter(Insight.simulation_id == simulation_result.simulation_id).first()
    
    if not insight:
        raise HTTPException(
            status_code=404,
            detail=f"No insights found for draft {draft_id}. They may still be generating."
        )
    
    return insight


@router.get("/draft/{draft_id}/status")
def check_insights_status(
    draft_id: int,
    db: Session = Depends(get_db)
):
    """
    Check if insights are ready for a draft.
    Returns: {"ready": true/false, "insight_id": int or null}
    """
    # Get simulation_id from results
    simulation_result = (
        db.query(SimulationResult)
        .filter(SimulationResult.draft_id == draft_id)
        .first()
    )
    
    if not simulation_result:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation found for draft {draft_id}"
        )
    
    insight = db.query(Insight).filter(Insight.simulation_id == simulation_result.simulation_id).first()
    
    return {
        "ready": insight is not None,
        "insight_id": insight.id if insight else None,
        "draft_id": draft_id,
        "simulation_id": simulation_result.simulation_id
    }


@router.get("/persona/{persona_id}/drill-down", response_model=schemas.PersonaDrillDownResponse)
def get_persona_drill_down(
    persona_id: str,
    draft_id: str,
    service: InsightsService = Depends(get_insights_service)
):
    """
    Get detailed view of a single persona compared to group average.
    """
    # Get simulation results
    simulation_results = (
        service.db.query(SimulationResult)
        .filter(SimulationResult.draft_id == draft_id)
        .all()
    )
    
    if not simulation_results:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation results found for draft {draft_id}"
        )
    
    drill_down = service.get_persona_drill_down(
        persona_id=persona_id,
        simulation_results=simulation_results
    )
    
    if not drill_down:
        raise HTTPException(
            status_code=404,
            detail=f"Persona {persona_id} not found in simulation results"
        )
    
    return schemas.PersonaDrillDownResponse(**drill_down)


@router.get("/trends/{persona_set_id}", response_model=schemas.SentimentTrendsResponse)
def get_sentiment_trends(
    persona_set_id: str,
    user_id: str,
    service: InsightsService = Depends(get_insights_service)
):
    """
    Get sentiment trends across multiple simulations with the same persona set.
    """
    trends = service.get_sentiment_trends(
        persona_set_id=persona_set_id,
        user_id=user_id
    )
    
    if not trends:
        return schemas.SentimentTrendsResponse(
            persona_set_id=persona_set_id,
            simulations=[]
        )
    
    return schemas.SentimentTrendsResponse(
        persona_set_id=persona_set_id,
        simulations=trends
    )
