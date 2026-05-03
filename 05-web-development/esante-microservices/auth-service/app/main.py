from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routes.auth_routes import router as auth_router
from app.routes.proxy_routes import router as proxy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    print("✅ Auth Service: DB tables created — Ready on port 3000")
    yield
    print("🛑 Auth Service: Shutting down")


app = FastAPI(
    title="E-Santé Auth Service",
    description=(
        "Service d'authentification et Gateway pour la plateforme E-Santé. "
        "Gère l'inscription, le login, le refresh JWT, et proxifie les "
        "requêtes authentifiées vers le Health Service."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── Routes ────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(proxy_router)


@app.get("/", tags=["Root"])
def root():
    return {"service": "auth-gateway", "status": "running", "version": "1.0.0"}


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
