from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.middleware import get_current_doctor
from app.config import settings
import httpx

router = APIRouter(tags=["Health Proxy"])

HEALTH_URL = settings.HEALTH_SERVICE_URL


async def _proxy(request: Request, path: str, method: str = "GET"):
    """
    Proxy an authenticated request to the internal Health service.
    The Auth service acts as a Gateway:
    1. Validates the JWT token
    2. Extracts the doctor_id
    3. Forwards the request with X-Doctor-Id header
    """
    doctor = await get_current_doctor(request)

    url = f"{HEALTH_URL}{path}"
    body = None
    content_type = request.headers.get("content-type", "application/json")

    if method in ("POST", "PUT", "PATCH"):
        body = await request.body()

    headers = {
        "X-Doctor-Id": str(doctor["doctor_id"]),
        "Content-Type": content_type,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(
                method=method,
                url=url,
                content=body,
                headers=headers,
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=502, detail="Health service unavailable")

    return JSONResponse(content=resp.json(), status_code=resp.status_code)


# ── Endpoint 4 : Création d'un patient ───────────────────
@router.post("/patients", status_code=201)
async def create_patient(request: Request):
    """Crée un patient lié au médecin authentifié."""
    return await _proxy(request, "/patients", "POST")


# ── Endpoint 5 : Liste des patients ──────────────────────
@router.get("/patients")
async def get_patients(request: Request):
    """Retourne tous les patients du médecin authentifié."""
    return await _proxy(request, "/patients", "GET")


# ── Endpoint 6 : Détail d'un patient ─────────────────────
@router.get("/patients/{patient_id}")
async def get_patient(patient_id: str, request: Request):
    """Retourne un patient par son ID."""
    return await _proxy(request, f"/patients/{patient_id}", "GET")


# ── Endpoint 7 : Ajout de données de santé ───────────────
@router.post("/patients/{patient_id}/data")
async def add_health_data(patient_id: str, request: Request):
    """Ajoute des données de santé (facteurs de risque) pour un patient."""
    return await _proxy(request, f"/patients/{patient_id}/data", "POST")


# ── Endpoint 8 : Données de santé + prédiction ───────────
@router.get("/patients/{patient_id}/data")
async def get_health_data(patient_id: str, request: Request):
    """Retourne les données de santé et la prédiction du patient."""
    return await _proxy(request, f"/patients/{patient_id}/data", "GET")


# ── Endpoint 9 : Prédiction uniquement ───────────────────
@router.get("/patients/{patient_id}/prediction")
async def get_prediction(patient_id: str, request: Request):
    """Retourne uniquement la dernière prédiction du patient."""
    return await _proxy(request, f"/patients/{patient_id}/prediction", "GET")


# ── Endpoint 10 : Lancer une prédiction ──────────────────
@router.post("/patients/{patient_id}/prediction")
async def create_prediction(patient_id: str, request: Request):
    """Lance une prédiction ML en arrière-plan pour le patient."""
    return await _proxy(request, f"/patients/{patient_id}/prediction", "POST")
