"""Configuration management for CSGirlies-AILAB"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # AI Provider - Can use OpenAI or Groq (free!)
    ai_provider: str = "groq"  # "openai" or "groq"
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Model selection based on provider
    openai_model: str = "gpt-4-turbo-preview"
    groq_model: str = "llama-3.3-70b-versatile"  # Free and fast! (Latest Groq model)

    # Wolfram
    wolfram_appid: str = "DEMO"  # Default demo mode

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

    @property
    def ai_api_key(self) -> str:
        """Get the appropriate API key based on provider"""
        if self.ai_provider == "groq":
            return self.groq_api_key or ""
        return self.openai_api_key or ""

    @property
    def ai_model(self) -> str:
        """Get the appropriate model based on provider"""
        if self.ai_provider == "groq":
            return self.groq_model
        return self.openai_model


settings = Settings()
