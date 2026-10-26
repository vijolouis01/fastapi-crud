"""FastAPI CRUD application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import get_settings
from core.db import engine
from models import Base
from routers import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup and close engine on shutdown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(router)


@app.get(
    "/",
    tags=["Root"],
    summary="API Health Check",
    description="Check if the API is running",
)
async def root() -> dict:
    """Health check endpoint."""
    return {"message": "FastAPI CRUD API is running"}
