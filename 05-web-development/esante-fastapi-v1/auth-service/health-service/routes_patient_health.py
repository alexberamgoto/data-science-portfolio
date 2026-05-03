# health-service/app/routes_patients.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import models, schemas
from .auth_dependency import get_current_doctor_id

router = APIRouter(prefix="/patients", tags=["patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.PatientRead)
def create_patient(
    patient_in: schemas.PatientCreate,
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patient = models.Patient(
        first_name=patient_in.first_name,
        last_name=patient_in.last_name,
        doctor_id=doctor_id,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("", response_model=list[schemas.PatientRead])
def list_patients(
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patients = db.query(models.Patient).filter(models.Patient.doctor_id == doctor_id).all()
    return patients

@router.get("/{id}", response_model=schemas.PatientRead)
def get_patient(
    id: int,
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor_id),
):
    patient = (
        db.query(models.Patient)
        .filter(models.Patient.id == id, models.Patient.doctor_id == doctor_id)
        .first()
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
