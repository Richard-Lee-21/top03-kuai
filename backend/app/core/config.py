import os
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Top03-Kuai"
    PROJECT_VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Redis Cache
    REDIS_URL: str = Field(..., env="REDIS_URL")
    
    # Admin
    ADMIN_PASSWORD: str = Field(..., env="ADMIN_PASSWORD")
    
    # External APIs
    SERPER_API_KEY: Optional[str] = Field(None, env="SERPER_API_KEY")
    LLM_API_KEY: Optional[str] = Field(None, env="LLM_API_KEY")
    LLM_PROVIDER: str = Field("anthropic", env="LLM_PROVIDER")  # anthropic or openai
    LLM_MODEL_NAME: str = Field("claude-3-opus-20240229", env="LLM_MODEL_NAME")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()