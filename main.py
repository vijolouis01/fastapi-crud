from fastapi import FastAPI
from routers.user import router
from models.user import Base
from db import engine

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(router)
