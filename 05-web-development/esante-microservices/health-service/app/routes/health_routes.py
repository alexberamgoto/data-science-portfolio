from fastapi import APIRouter, HTTPException, Request, status, BackgroundTasks
from app.database import get_database
from app.schemas import PatientCreate, HealthDataInput
from app.ml_model import predict_risk
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(tags=["Health"])


# ── Helpers ───────────────────────────────────────────────

def _doctor_id(request: Request) -> int:
    """Extract doctor_id from the X-Doctor-Id header (set by Auth gateway)."""
    did = request.headers.get("X-Doctor-Id")
    if not did:
        raise HTTPException(status_code=401, detail="Missing doctor identification")
    return int(did)


def _oid(patient_id: str) -> ObjectId:
    """Convert string to MongoDB ObjectId, or raise 400."""
    try:
        return ObjectId(patient_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID format")


def _serialize(doc: dict) -> dict:
    """Convert MongoDB _id (ObjectId) to string 'id' for JSON."""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# ══════════════════════════════════════════════════════════
# PATIENTS
# ══════════════════════════════════════════════════════════

@router.post(
    "/patients",
    status_code=status.HTTP_201_CREATED,
    summary="Endpoint 4 — Création d'un patient",
)
async def create_patient(body: PatientCreate, request: Request):
    """
    Crée un nouveau patient lié au médecin authentifié.
    Le doctor_id est extrait du header X-Doctor-Id (posé par le gateway).
    """
    doctor_id = _doctor_id(request)
    db = get_database()

    doc = {
        "doctor_id": doctor_id,
        "first_name": body.first_name,
        "last_name": body.last_name,
        "date_of_birth": body.date_of_birth,
        "gender": body.gender,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = await db.patients.insert_one(doc)
    doc["_id"] = result.inserted_id

    return _serialize(doc)


@router.get(
    "/patients",
    summary="Endpoint 5 — Liste des patients du médecin",
)
async def get_patients(request: Request):
    """Retourne tous les patients associés au médecin authentifié."""
    doctor_id = _doctor_id(request)
    db = get_database()

    patients = []
    async for doc in db.patients.find({"doctor_id": doctor_id}):
        patients.append(_serialize(doc))

    return patients


@router.get(
    "/patients/{patient_id}",
    summary="Endpoint 6 — Détail d'un patient",
)
async def get_patient(patient_id: str, request: Request):
    """Retourne un patient par son ID, vérifie qu'il appartient au médecin."""
    doctor_id = _doctor_id(request)
    db = get_database()

    patient = await db.patients.find_one({
        "_id": _oid(patient_id),
        "doctor_id": doctor_id,
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return _serialize(patient)


# ══════════════════════════════════════════════════════════
# HEALTH DATA
# ══════════════════════════════════════════════════════════

@router.post(
    "/patients/{patient_id}/data",
    summary="Endpoint 7 — Ajout de données de santé",
)
async def add_health_data(patient_id: str, body: HealthDataInput, request: Request):
    """
    Ajoute un jeu de données de santé (17 facteurs de risque)
    pour un patient donné. Plusieurs jeux peuvent être ajoutés
    (historique). La prédiction utilise le plus récent.
    """
    doctor_id = _doctor_id(request)
    db = get_database()

    # Vérifier que le patient existe et appartient au médecin
    patient = await db.patients.find_one({
        "_id": _oid(patient_id),
        "doctor_id": doctor_id,
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    doc = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "data": body.model_dump(),
        "created_at": datetime.now(timezone.utc),
    }

    result = await db.health_data.insert_one(doc)
    doc["_id"] = result.inserted_id

    return _serialize(doc)


@router.get(
    "/patients/{patient_id}/data",
    summary="Endpoint 8 — Données de santé + prédiction",
)
async def get_health_data(patient_id: str, request: Request):
    """
    Retourne le patient, ses dernières données de santé,
    et sa dernière prédiction (si disponible).
    """
    doctor_id = _doctor_id(request)
    db = get_database()

    patient = await db.patients.find_one({
        "_id": _oid(patient_id),
        "doctor_id": doctor_id,
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Dernières données de santé
    health = await db.health_data.find_one(
        {"patient_id": patient_id, "doctor_id": doctor_id},
        sort=[("created_at", -1)],
    )

    # Dernière prédiction
    prediction = await db.predictions.find_one(
        {"patient_id": patient_id, "doctor_id": doctor_id},
        sort=[("created_at", -1)],
    )

    return {
        "patient": _serialize(patient),
        "health_data": _serialize(health) if health else None,
        "prediction": _serialize(prediction) if prediction else None,
    }


# ══════════════════════════════════════════════════════════
# PREDICTIONS
# ══════════════════════════════════════════════════════════

@router.get(
    "/patients/{patient_id}/prediction",
    summary="Endpoint 9 — Dernière prédiction",
)
async def get_prediction(patient_id: str, request: Request):
    """Retourne la dernière prédiction pour un patient."""
    doctor_id = _doctor_id(request)
    db = get_database()

    patient = await db.patients.find_one({
        "_id": _oid(patient_id),
        "doctor_id": doctor_id,
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    prediction = await db.predictions.find_one(
        {"patient_id": patient_id, "doctor_id": doctor_id},
        sort=[("created_at", -1)],
    )

    if not prediction:
        return {
            "patient_id": patient_id,
            "prediction": None,
            "status": "no_prediction",
        }

    return _serialize(prediction)


async def _run_prediction_background(
    patient_id: str, doctor_id: int, health_data: dict
):
    """
    Background task: compute ML prediction and store it in MongoDB.
    Cette tâche s'exécute de manière asynchrone après la réponse HTTP.
    """
    db = get_database()
    try:
        result = await predict_risk(health_data)
        await db.predictions.insert_one({
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "risk_level": result["risk_level"],
            "confidence": result["confidence"],
            "probabilities": result.get("probabilities"),
            "status": "completed",
            "created_at": datetime.now(timezone.utc),
        })
        print(f"✅ Prediction for {patient_id}: {result['risk_level']} "
              f"(confidence: {result['confidence']})")
    except Exception as e:
        print(f"❌ Prediction failed for {patient_id}: {e}")
        await db.predictions.insert_one({
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "risk_level": None,
            "confidence": None,
            "status": "error",
            "error": str(e),
            "created_at": datetime.now(timezone.utc),
        })


@router.post(
    "/patients/{patient_id}/prediction",
    summary="Endpoint 10 — Lancer une prédiction (async)",
)
async def create_prediction(
    patient_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Lance une prédiction ML en arrière-plan (BackgroundTasks).
    Le médecin reçoit immédiatement un statut 'pending' et devra
    consulter le résultat ultérieurement via GET /patients/{id}/prediction.
    """
    doctor_id = _doctor_id(request)
    db = get_database()

    # Vérifier patient
    patient = await db.patients.find_one({
        "_id": _oid(patient_id),
        "doctor_id": doctor_id,
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Vérifier qu'il y a des données de santé
    health = await db.health_data.find_one(
        {"patient_id": patient_id, "doctor_id": doctor_id},
        sort=[("created_at", -1)],
    )
    if not health:
        raise HTTPException(
            status_code=400,
            detail="No health data available. Submit health data first (POST /patients/{id}/data).",
        )

    # Lancer la prédiction en arrière-plan
    background_tasks.add_task(
        _run_prediction_background,
        patient_id,
        doctor_id,
        health["data"],
    )

    return {
        "patient_id": patient_id,
        "status": "pending",
        "message": "Prediction is being computed. Use GET /patients/{id}/prediction to check results.",
    }
