# auth-service/app/main.py
from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routes_auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth_router)
