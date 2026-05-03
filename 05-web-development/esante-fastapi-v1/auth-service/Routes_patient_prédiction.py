# health-service/app/routes_predictions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import models, schemas
from .auth_dependency import get_current_doctor_id

router = APIRouter(prefix="/patients", tags=["health"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_patient_for_doctor(db: Session, patient_id: int, doctor_id: int) -> models.Patient:
    patient = (
        db.query(models.Patient)
        .filter(models.Patient.id == patient_id, models.Patient.doctor_id == doctor_id)
        .first()
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/{id}/data")
def add_health_data(
    id: int,
    data_in: schemas.HealthDataCreate,
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patient = get_patient_for_doctor(db, id, doctor_id)

    existing = db.query(models.HealthData).filter(models.HealthData.patient_id == patient.id).first()
    if existing:
        for field, value in data_in.dict().items():
            setattr(existing, field, value)
        db.commit()
        return {"status": "updated"}
    else:
        health_data = models.HealthData(patient_id=patient.id, **data_in.dict())
        db.add(health_data)
        db.commit()
        return {"status": "created"}

@router.get("/{id}/data", response_model=schemas.HealthDataRead | None)
def get_health_data(
    id: int,
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patient = get_patient_for_doctor(db, id, doctor_id)
    data = db.query(models.HealthData).filter(models.HealthData.patient_id == patient.id).first()
    if not data:
        return None
    return data

def simple_risk_rule(h: models.HealthData) -> str:
    """
    Règle heuristique simple pour approximer un niveau de risque (Low/Medium/High)
    en attendant l'intégration du vrai modèle de Machine Learning.
    """
    score = 0.0

    # Habitudes de vie
    score += 0.8 * h.Smoking
    score += 0.5 * h.Alcohol_Use
    score += 0.7 * h.Obesity
    score += 0.4 * h.Diet_Red_Meat
    score += 0.4 * h.Diet_Salted_Processed
    score -= 0.5 * h.Fruit_Veg_Intake  # fruits/légumes protecteurs
    score -= 0.3 * h.Physical_Activity
    score -= 0.3 * h.Physical_Activity_Level

    # Facteurs environnementaux
    score += 0.3 * h.Air_Pollution
    score += 0.3 * h.Occupational_Hazards

    # Facteurs familiaux / génétiques / médicaux
    if h.Family_History:
        score += 4.0
    if h.BRCA_Mutation:
        score += 6.0
    if h.H_Pylori_Infection:
        score += 1.5

    # BMI : surpoids / obésité augmente le risque
    if h.BMI >= 30:
        score += 3.0
    elif h.BMI >= 25:
        score += 1.5

    # Normalisation très grossière
    if score < 15:
        return "Low"
    elif score < 30:
        return "Medium"
    return "High"


@router.post("/{id}/prediction")
def create_prediction(
    id: int,
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patient = get_patient_for_doctor(db, id, doctor_id)
    health_data = db.query(models.HealthData).filter(models.HealthData.patient_id == patient.id).first()
    if not health_data:
        raise HTTPException(status_code=400, detail="Health data required before prediction")

    risk = simple_risk_rule(health_data)
    existing = db.query(models.Prediction).filter(models.Prediction.patient_id == patient.id).first()
    if existing:
        existing.risk_level = risk
    else:
        pred = models.Prediction(patient_id=patient.id, risk_level=risk)
        db.add(pred)
    db.commit()
    return {"risk_level": risk}

@router.get("/{id}/prediction", response_model=schemas.PredictionRead | None)
def get_prediction(
    id: int,
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patient = get_patient_for_doctor(db, id, doctor_id)
    pred = db.query(models.Prediction).filter(models.Prediction.patient_id == patient.id).first()
    if not pred:
        return None
    return pred
