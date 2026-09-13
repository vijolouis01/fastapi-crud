"""FastAPI CRUD application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import engine, get_settings
from models import Base
from routers import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.

    Creates database tables on startup and closes engine on shutdown.
    """
    # Startup: Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Close engine
    await engine.dispose()


# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)


# Include routers
app.include_router(router)


@app.get(
    "/",
    tags=["Root"],
    summary="API Health Check",
    description="Check if the API is running",
)
async def root() -> dict:
    """
    Root endpoint for API health check.

    Returns:
        JSON message indicating API is running
    """
    return {"message": "FastAPI CRUD API is running"}
