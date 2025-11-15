"""Configuration management for CSGirlies-AILAB"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    
    # Wolfram
    wolfram_appid: str
    
    # GitBook
    gitbook_api_key: Optional[str] = None
    gitbook_space_id: Optional[str] = None
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
