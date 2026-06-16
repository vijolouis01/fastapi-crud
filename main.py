"""FastAPI CRUD application entry point."""

from fastapi import FastAPI

from core import engine, get_settings
from models import Base
from routers import router

settings = get_settings()

# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# Create database tables
Base.metadata.create_all(engine)

# Include routers
app.include_router(router)


@app.get(
    "/",
    tags=["Root"],
    summary="API Health Check",
    description="Check if the API is running",
)
def root() -> dict:
    """
    Root endpoint for API health check.

    Returns:
        JSON message indicating API is running
    """
    return {"message": "FastAPI CRUD API is running"}
