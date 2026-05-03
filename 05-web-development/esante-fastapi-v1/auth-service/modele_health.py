# health-service/app/models.py
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, index=True)  # id du user (Auth)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    health_data = relationship("HealthData", back_populates="patient", uselist=False)
    prediction = relationship("Prediction", back_populates="patient", uselist=False)

class HealthData(Base):
    __tablename__ = "health_data"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True)

    Age = Column(Integer)
    Gender = Column(Integer)  # 0 = Female, 1 = Male
    Smoking = Column(Integer)
    Alcohol_Use = Column(Integer)
    Obesity = Column(Integer)
    Family_History = Column(Boolean)
    Diet_Red_Meat = Column(Integer)
    Diet_Salted_Processed = Column(Integer)
    Fruit_Veg_Intake = Column(Integer)
    Physical_Activity = Column(Integer)
    Air_Pollution = Column(Integer)
    Occupational_Hazards = Column(Integer)
    BRCA_Mutation = Column(Boolean)
    H_Pylori_Infection = Column(Boolean)
    Calcium_Intake = Column(Integer)
    BMI = Column(Float)
    Physical_Activity_Level = Column(Integer)

    patient = relationship("Patient", back_populates="health_data")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True)
    risk_level = Column(String(10), nullable=True)  # Low / Medium / High

    patient = relationship("Patient", back_populates="prediction")
