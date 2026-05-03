# health-service/app/main.py
from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routes_patients import router as patients_router
from .routes_predictions import router as predictions_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Health Service")

app.include_router(patients_router)
app.include_router(predictions_router)
