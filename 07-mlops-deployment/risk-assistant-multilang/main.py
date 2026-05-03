# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from models import risk_predict_proba, anomaly_score, recommend_products

app = FastAPI(title="Risk & Personalization API")

class RiskRequest(BaseModel):
    client_id: str
    amount: float
    income: float
    tenure_months: int

class RiskResponse(BaseModel):
    client_id: str
    risk_score: float
    risk_level: str

class AnomalyRequest(BaseModel):
    client_id: str
    amount: float
    balance: float
    tx_per_day: float

class AnomalyResponse(BaseModel):
    client_id: str
    anomaly_score: float
    is_anomaly: bool

class RecoRequest(BaseModel):
    client_id: str
    income: float
    risk_score: float

class RecoResponse(BaseModel):
    client_id: str
    recommended_products: list[str]

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/score_risque", response_model=RiskResponse)
def score_risque(req: RiskRequest):
    features = np.array([req.amount, req.income, req.tenure_months], dtype=float)
    score = risk_predict_proba(features)
    level = "LOW" if score < 0.3 else ("MEDIUM" if score < 0.7 else "HIGH")
    return RiskResponse(client_id=req.client_id, risk_score=score, risk_level=level)

@app.post("/detect_anomalie", response_model=AnomalyResponse)
def detect_anomalie(req: AnomalyRequest):
    features = np.array([req.amount, req.balance, req.tx_per_day], dtype=float)
    score = anomaly_score(features)
    is_anomaly = score > 2.0
    return AnomalyResponse(
        client_id=req.client_id,
        anomaly_score=score,
        is_anomaly=is_anomaly
    )

@app.post("/reco_financiere", response_model=RecoResponse)
def reco_financiere(req: RecoRequest):
    recos = recommend_products(req.risk_score, req.income)
    return RecoResponse(client_id=req.client_id, recommended_products=recos)
