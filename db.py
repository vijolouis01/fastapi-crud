from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://vijo:vijolouis@localhost:5432/todo"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)


def get_db():
    with SessionLocal() as db:
        yield db
