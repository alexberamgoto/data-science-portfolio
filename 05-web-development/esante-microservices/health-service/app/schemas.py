from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Patient ───────────────────────────────────────────────
class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    gender: int = Field(..., ge=0, le=1, description="0=Femme, 1=Homme")


class PatientResponse(BaseModel):
    id: str
    doctor_id: int
    first_name: str
    last_name: str
    date_of_birth: str
    gender: int
    created_at: Optional[datetime] = None


# ── Health Data (17 facteurs de risque) ───────────────────
class HealthDataInput(BaseModel):
    age: int = Field(..., ge=0, le=120)
    gender: int = Field(..., ge=0, le=1)
    smoking: int = Field(..., ge=0, le=10)
    alcohol_use: int = Field(..., ge=0, le=10)
    obesity: int = Field(..., ge=0, le=10)
    family_history: bool
    diet_red_meat: int = Field(..., ge=0, le=10)
    diet_salted_processed: int = Field(..., ge=0, le=10)
    fruit_veg_intake: int = Field(..., ge=0, le=10)
    physical_activity: int = Field(..., ge=0, le=10)
    air_pollution: int = Field(..., ge=0, le=10)
    occupational_hazards: int = Field(..., ge=0, le=10)
    brca_mutation: bool
    h_pylori_infection: bool
    calcium_intake: int = Field(..., ge=0, le=10)
    bmi: float = Field(..., ge=10.0, le=60.0)
    physical_activity_level: int = Field(..., ge=0, le=10)


# ── Prediction ────────────────────────────────────────────
class PredictionResponse(BaseModel):
    id: str
    patient_id: str
    risk_level: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "pending"
    created_at: Optional[datetime] = None
