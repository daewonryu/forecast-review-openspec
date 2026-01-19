"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


# Enums
class SentimentType(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class ResultStatus(str, Enum):
    success = "success"
    error = "error"


# User schemas
class UserBase(BaseModel):
    email: str = Field(..., max_length=255)
    username: str = Field(..., max_length=100)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Persona schemas
class PersonaBase(BaseModel):
    name: str = Field(..., max_length=50)
    archetype: str = Field(..., max_length=50)
    loyalty_level: int = Field(..., ge=1, le=10)
    core_values: List[str] = Field(..., min_items=2, max_items=4)
    
    @validator('core_values')
    def validate_core_values(cls, v):
        if not all(isinstance(val, str) for val in v):
            raise ValueError('All core values must be strings')
        return v


class PersonaCreate(PersonaBase):
    audience_description: str = Field(..., min_length=5, max_length=500)


class PersonaResponse(PersonaBase):
    id: int
    set_id: str
    audience_description: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class PersonaGenerateRequest(BaseModel):
    audience_description: str = Field(..., min_length=5, max_length=500)
    save_to_library: bool = True


class PersonaSetResponse(BaseModel):
    set_id: str
    personas: List[PersonaResponse]
    created_at: Optional[datetime] = None


# Draft schemas
class DraftCreate(BaseModel):
    content: str = Field(..., min_length=10, max_length=5000)


class DraftResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Simulation schemas
class ScoresResponse(BaseModel):
    trust: int = Field(..., ge=1, le=10)
    excitement: int = Field(..., ge=1, le=10)
    backlash_risk: int = Field(..., ge=1, le=10)


class PersonaResultResponse(BaseModel):
    persona_id: int
    persona_name: str
    internal_monologue: str
    public_comment: str
    scores: ScoresResponse
    reasoning: Optional[str] = None
    status: ResultStatus = ResultStatus.success
    error_message: Optional[str] = None


class AggregateScores(BaseModel):
    avg_trust: float
    avg_excitement: float
    avg_backlash_risk: float


class SimulationRunRequest(BaseModel):
    draft_content: str = Field(..., min_length=10, max_length=5000)
    persona_set_id: str


class SimulationResponse(BaseModel):
    draft_id: int
    simulation_id: str
    results: List[PersonaResultResponse]
    aggregate: AggregateScores
    completed_at: datetime
    duration_seconds: float


# Insights schemas
class PainPointResponse(BaseModel):
    text: str
    severity: str  # "high" | "medium" | "low"
    affected_personas: List[str]
    reasoning: str


class ImprovementTipResponse(BaseModel):
    tip: str
    rationale: str
    impact: str  # "high" | "medium" | "low"
    addresses: List[str]


class AggregateAnalytics(BaseModel):
    average_scores: dict
    overall_sentiment: str  # "positive" | "neutral" | "negative"
    score_distribution: List[dict]


class InsightResponse(BaseModel):
    id: int
    simulation_id: str
    pain_points: List[dict]
    improvement_tips: List[dict]
    overall_sentiment: str
    avg_trust: float
    avg_excitement: float
    avg_backlash_risk: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class PersonaDrillDownResponse(BaseModel):
    persona_details: dict
    persona_scores: dict
    group_averages: dict
    delta: dict
    is_outlier: bool
    reactions: dict


class SimulationTrend(BaseModel):
    draft_id: int
    simulation_date: str
    draft_preview: str
    average_scores: dict
    overall_sentiment: str
    delta_from_previous: Optional[dict] = None


class SentimentTrendsResponse(BaseModel):
    persona_set_id: str
    simulations: List[SimulationTrend]


# Health check
class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime

