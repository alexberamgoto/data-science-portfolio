from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from model import score_sample

app = FastAPI(title="API ML Santé", version="1.0.0")

class Input(BaseModel):
    patientId: int
    weight: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    glucose: Optional[float] = None

@app.get('/health')
def health():
    return { 'status': 'ok' }

@app.post('/analyze')
def analyze(inp: Input):
    payload = {k: v for k, v in inp.model_dump().items() if v is not None}
    result = score_sample(payload)
    return result
