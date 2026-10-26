"""Application configuration settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # App settings
    app_name: str = Field(default="FastAPI CRUD")
    app_version: str = Field(default="0.1.0")
    app_description: str = Field(default="A simple CRUD application for managing users")
    debug: bool = Field(default=False)

    # Database settings
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/fastapi_crud"
    )

    # Server settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).

    Returns:
        Settings instance
    """
    return Settings()
