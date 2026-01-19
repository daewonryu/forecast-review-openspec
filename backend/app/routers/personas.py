"""
Persona API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.services.llm import get_llm_service, LLMService
from app.services.persona import PersonaService
from app.schemas import (
    PersonaGenerateRequest,
    PersonaSetResponse,
    PersonaResponse,
    SentimentTrendsResponse,
    SimulationTrend
)

router = APIRouter(prefix="/api/personas", tags=["Personas"])


def get_persona_service(llm_service: LLMService = Depends(get_llm_service)) -> PersonaService:
    """Dependency to get persona service"""
    return PersonaService(llm_service)


@router.post("/generate", response_model=PersonaSetResponse)
async def generate_personas(
    request: PersonaGenerateRequest,
    db: Session = Depends(get_db),
    persona_service: PersonaService = Depends(get_persona_service)
):
    """
    Generate 5 AI personas based on audience description.
    
    - **audience_description**: Description of target audience (5-500 chars)
    - **save_to_library**: Whether to save personas to user's library
    
    Returns a set_id and list of 5 personas with traits.
    """
    # For MVP, using a default user_id (in production, get from auth)
    user_id = 1
    
    try:
        result = await persona_service.generate_personas(
            audience_description=request.audience_description,
            user_id=user_id,
            db=db,
            save_to_library=request.save_to_library
        )
        
        # Convert to response format
        if request.save_to_library:
            # Get from database to ensure IDs are included
            personas = persona_service.get_persona_set(result["set_id"], user_id, db)
            persona_responses = [
                PersonaResponse(
                    id=p.id,
                    set_id=p.set_id,
                    name=p.name,
                    archetype=p.archetype,
                    loyalty_level=p.loyalty_level,
                    core_values=p.core_values,
                    audience_description=p.audience_description,
                    created_at=p.created_at
                )
                for p in personas
            ]
            created_at = personas[0].created_at if personas else None
        else:
            # Return generated data without IDs
            persona_responses = [
                PersonaResponse(
                    id=0,  # No ID if not saved
                    set_id=result["set_id"],
                    name=p["name"],
                    archetype=p["archetype"],
                    loyalty_level=p["loyalty_level"],
                    core_values=p["core_values"],
                    audience_description=result["audience_description"],
                    created_at=None
                )
                for p in result["personas"]
            ]
            created_at = None
        
        return PersonaSetResponse(
            set_id=result["set_id"],
            personas=persona_responses,
            created_at=created_at
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating personas: {str(e)}")


@router.get("/sets/{set_id}", response_model=PersonaSetResponse)
async def get_persona_set(
    set_id: str,
    db: Session = Depends(get_db),
    persona_service: PersonaService = Depends(get_persona_service)
):
    """
    Retrieve a previously generated persona set by ID.
    """
    user_id = 1  # MVP: default user
    
    personas = persona_service.get_persona_set(set_id, user_id, db)
    
    if not personas:
        raise HTTPException(status_code=404, detail="Persona set not found")
    
    persona_responses = [
        PersonaResponse(
            id=p.id,
            set_id=p.set_id,
            name=p.name,
            archetype=p.archetype,
            loyalty_level=p.loyalty_level,
            core_values=p.core_values,
            audience_description=p.audience_description,
            created_at=p.created_at
        )
        for p in personas
    ]
    
    return PersonaSetResponse(
        set_id=set_id,
        personas=persona_responses,
        created_at=personas[0].created_at
    )


@router.get("/sets")
async def list_persona_sets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    search: Optional[str] = Query(None, max_length=200),
    db: Session = Depends(get_db),
    persona_service: PersonaService = Depends(get_persona_service)
):
    """
    List all persona sets for the current user.
    
    - **skip**: Number of sets to skip (pagination)
    - **limit**: Maximum number of sets to return
    - **search**: Optional search term for audience description
    """
    user_id = 1  # MVP: default user
    
    sets = persona_service.list_persona_sets(
        user_id=user_id,
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )
    
    return {
        "total": len(sets),
        "sets": sets,
        "skip": skip,
        "limit": limit
    }


@router.delete("/sets/{set_id}")
async def delete_persona_set(
    set_id: str,
    db: Session = Depends(get_db),
    persona_service: PersonaService = Depends(get_persona_service)
):
    """
    Delete a persona set and all its personas.
    """
    user_id = 1  # MVP: default user
    
    deleted = persona_service.delete_persona_set(set_id, user_id, db)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Persona set not found")
    
    return {"message": "Persona set deleted successfully", "set_id": set_id}


@router.get("/sets/{set_id}/history", response_model=SentimentTrendsResponse)
async def get_sentiment_trends(
    set_id: str,
    limit: int = Query(10, ge=1, le=50, description="Maximum number of simulations to return"),
    db: Session = Depends(get_db)
):
    """
    Get sentiment trend tracking for a persona set across multiple simulations.
    
    Shows how scores change over multiple iterations with the same persona set.
    Useful for tracking improvement after applying feedback.
    """
    from app.db.models import Persona, SimulationResult, Draft
    from sqlalchemy import func, distinct
    
    user_id = 1  # MVP: default user
    
    # Verify persona set exists
    personas = db.query(Persona).filter(
        Persona.set_id == set_id,
        Persona.user_id == user_id
    ).all()
    
    if not personas:
        raise HTTPException(status_code=404, detail="Persona set not found")
    
    # Get all simulations that used this persona set
    # Group by simulation_id to get unique simulations
    persona_ids = [p.id for p in personas]
    
    simulations_query = (
        db.query(
            SimulationResult.simulation_id,
            SimulationResult.draft_id,
            func.min(SimulationResult.created_at).label('simulation_date')
        )
        .filter(SimulationResult.persona_id.in_(persona_ids))
        .group_by(SimulationResult.simulation_id, SimulationResult.draft_id)
        .order_by(func.min(SimulationResult.created_at).desc())
        .limit(limit)
        .all()
    )
    
    if not simulations_query:
        return SentimentTrendsResponse(
            persona_set_id=set_id,
            simulations=[]
        )
    
    trends = []
    prev_scores = None
    
    for sim_id, draft_id, sim_date in reversed(simulations_query):
        # Get all results for this simulation
        results = db.query(SimulationResult).filter(
            SimulationResult.simulation_id == sim_id
        ).all()
        
        # Get draft content
        draft = db.query(Draft).filter(Draft.id == draft_id).first()
        
        # Calculate averages
        avg_trust = sum(r.trust_score for r in results) / len(results)
        avg_excitement = sum(r.excitement_score for r in results) / len(results)
        avg_backlash = sum(r.backlash_risk_score for r in results) / len(results)
        
        # Determine sentiment
        if avg_trust >= 7 and avg_excitement >= 7 and avg_backlash <= 3:
            sentiment = "positive"
        elif avg_trust <= 4 or avg_backlash >= 7:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate delta from previous
        delta = None
        if prev_scores:
            delta = {
                "trust": round(avg_trust - prev_scores["trust"], 2),
                "excitement": round(avg_excitement - prev_scores["excitement"], 2),
                "backlash_risk": round(avg_backlash - prev_scores["backlash_risk"], 2)
            }
        
        trends.append(
            SimulationTrend(
                draft_id=draft_id,
                simulation_date=sim_date.isoformat(),
                draft_preview=draft.content[:100] + "..." if len(draft.content) > 100 else draft.content,
                average_scores={
                    "trust": round(avg_trust, 2),
                    "excitement": round(avg_excitement, 2),
                    "backlash_risk": round(avg_backlash, 2)
                },
                overall_sentiment=sentiment,
                delta_from_previous=delta
            )
        )
        
        prev_scores = {
            "trust": avg_trust,
            "excitement": avg_excitement,
            "backlash_risk": avg_backlash
        }
    
    return SentimentTrendsResponse(
        persona_set_id=set_id,
        simulations=list(reversed(trends))  # Return chronological order
    )
