"""
Configuration management
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "FanEcho MVP"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/fanecho"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # LLM Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    PRIMARY_LLM_PROVIDER: str = "openai"  # "openai" or "anthropic"
    LLM_TIMEOUT: int = 60
    LLM_MAX_RETRIES: int = 1
    LLM_TEMPERATURE: float = 0.7  # Balanced: 0.5-0.6 for consistency, 0.7-0.8 for creativity
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
