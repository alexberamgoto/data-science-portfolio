from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_to_mongodb, close_mongodb_connection
from app.routes.health_routes import router as health_router
from app.ml_model import load_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to MongoDB and load ML model on startup."""
    await connect_to_mongodb()
    load_model()
    print("✅ Health Service: Ready on port 8000")
    yield
    await close_mongodb_connection()
    print("🛑 Health Service: Shutting down")


app = FastAPI(
    title="E-Santé Health Service",
    description=(
        "Service de gestion des données de santé et prédictions ML. "
        "Ce service est interne et accessible uniquement via le gateway Auth."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── Routes ────────────────────────────────────────────────
app.include_router(health_router)


@app.get("/", tags=["Root"])
def root():
    return {"service": "health", "status": "running", "version": "1.0.0"}


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
