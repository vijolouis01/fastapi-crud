"""Application configuration settings."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "FastAPI CRUD"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://vijo:vijolouis@localhost:5432/todo"
    )

    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).

    Returns:
        Settings instance
    """
    return Settings()
