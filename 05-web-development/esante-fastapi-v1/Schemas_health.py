# health-service/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    first_name: str
    last_name: str

class PatientRead(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class HealthDataCreate(BaseModel):
    Age: int
    Gender: int
    Smoking: int
    Alcohol_Use: int
    Obesity: int
    Family_History: bool
    Diet_Red_Meat: int
    Diet_Salted_Processed: int
    Fruit_Veg_Intake: int
    Physical_Activity: int
    Air_Pollution: int
    Occupational_Hazards: int
    BRCA_Mutation: bool
    H_Pylori_Infection: bool
    Calcium_Intake: int
    BMI: float
    Physical_Activity_Level: int

class HealthDataRead(HealthDataCreate):
    pass

class PredictionRead(BaseModel):
    risk_level: Optional[str]
