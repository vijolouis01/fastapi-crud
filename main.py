"""FastAPI CRUD application entry point."""

from fastapi import FastAPI

from db import engine
from models import Base
from routers import router

# Create FastAPI application instance
app = FastAPI(
    title="FastAPI CRUD API",
    description="A simple CRUD application for managing users",
    version="0.1.0",
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
