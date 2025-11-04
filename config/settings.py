"""
Application settings and configuration
"""
import os
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Server settings
    port: int = 8000
    host: str = "0.0.0.0"

    # Environment
    environment: str = "development"
    debug: bool = True

    # API Keys (to be set via .env file)
    openai_api_key: Optional[str] = None
    google_calendar_api_key: Optional[str] = None

    # Google Calendar settings
    google_calendar_id: Optional[str] = None

    # Application settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = ["pdf", "xlsx", "xls", "png", "jpg", "jpeg", "gif"]

    # MCP settings
    mcp_message_timeout: int = 30  # seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()

# Fixed application settings (not configurable via env)
ALLOWED_FILE_TYPES: List[str] = ["pdf", "xlsx", "xls", "png", "jpg", "jpeg", "gif"]

# Validate required settings for production
if settings.environment == "production":
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required in production")
    if not settings.google_calendar_api_key:
        raise ValueError("GOOGLE_CALENDAR_API_KEY is required in production")
    if not settings.google_calendar_id:
        raise ValueError("GOOGLE_CALENDAR_ID is required in production")
