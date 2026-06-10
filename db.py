"""Database configuration and session management."""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Database URL from environment or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://vijo:vijolouis@localhost:5432/todo")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False").lower() == "true",
    pool_pre_ping=True,  # Validate connection before using
    pool_recycle=3600,  # Recycle connections every hour
)

# Session factory
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.

    Yields:
        Session: SQLAlchemy database session

    Example:
        Used as a FastAPI dependency:
        @router.get("/")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
