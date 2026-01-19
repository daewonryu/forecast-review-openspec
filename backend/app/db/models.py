"""
Database models for FanEcho MVP
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    BigInteger, Column, String, Integer, Text, JSON, 
    TIMESTAMP, ForeignKey, Enum as SQLEnum, DECIMAL, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    updated_at = Column(
        TIMESTAMP, 
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
    
    # Relationships
    personas = relationship("Persona", back_populates="user", cascade="all, delete-orphan")
    drafts = relationship("Draft", back_populates="user", cascade="all, delete-orphan")


class Persona(Base):
    """Persona model"""
    __tablename__ = "personas"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    set_id = Column(String(36), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    archetype = Column(String(50), nullable=False)
    loyalty_level = Column(Integer, nullable=False)
    core_values = Column(JSON, nullable=False)
    audience_description = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    
    __table_args__ = (
        CheckConstraint('loyalty_level BETWEEN 1 AND 10', name='check_loyalty_level'),
    )
    
    # Relationships
    user = relationship("User", back_populates="personas")
    simulation_results = relationship("SimulationResult", back_populates="persona", cascade="all, delete-orphan")


class Draft(Base):
    """Draft model"""
    __tablename__ = "drafts"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
    
    # Relationships
    user = relationship("User", back_populates="drafts")
    simulation_results = relationship("SimulationResult", back_populates="draft", cascade="all, delete-orphan")


class SimulationResult(Base):
    """Simulation result model"""
    __tablename__ = "simulation_results"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    simulation_id = Column(String(36), nullable=False, index=True)
    draft_id = Column(BigInteger, ForeignKey("drafts.id", ondelete="CASCADE"), nullable=False)
    persona_id = Column(BigInteger, ForeignKey("personas.id", ondelete="CASCADE"), nullable=False)
    trust_score = Column(Integer, nullable=False)
    excitement_score = Column(Integer, nullable=False)
    backlash_risk_score = Column(Integer, nullable=False)
    internal_monologue = Column(Text, nullable=False)
    public_comment = Column(Text, nullable=False)
    reasoning = Column(Text)
    status = Column(SQLEnum('success', 'error', name='result_status'), default='success')
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    
    __table_args__ = (
        CheckConstraint('trust_score BETWEEN 1 AND 10', name='check_trust_score'),
        CheckConstraint('excitement_score BETWEEN 1 AND 10', name='check_excitement_score'),
        CheckConstraint('backlash_risk_score BETWEEN 1 AND 10', name='check_backlash_risk_score'),
    )
    
    # Relationships
    draft = relationship("Draft", back_populates="simulation_results")
    persona = relationship("Persona", back_populates="simulation_results")


class Insight(Base):
    """Insight model (optional - can be computed on-demand)"""
    __tablename__ = "insights"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    simulation_id = Column(String(36), nullable=False, unique=True, index=True)
    pain_points = Column(JSON, nullable=False)
    improvement_tips = Column(JSON, nullable=False)
    overall_sentiment = Column(SQLEnum('positive', 'neutral', 'negative', name='sentiment'), nullable=False)
    avg_trust = Column(DECIMAL(3, 1), nullable=False)
    avg_excitement = Column(DECIMAL(3, 1), nullable=False)
    avg_backlash_risk = Column(DECIMAL(3, 1), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
