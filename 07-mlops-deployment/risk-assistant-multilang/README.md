# Risk Assistant — API Python (FastAPI) + Client C# (.NET)

API multi-langage exposant 3 endpoints d'analyse client (scoring de risque, détection d'anomalies, recommandation produit) consommée par un client **.NET / C#**.

## Endpoints (FastAPI)

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET`   | `/`               | Health check |
| `POST`  | `/score_risque`   | Scoring de risque crédit (LOW/MEDIUM/HIGH) |
| `POST`  | `/detect_anomalie`| Détection d'anomalie de transaction |
| `POST`  | `/reco_financiere`| Recommandation de produits financiers |

## Architecture
```
┌─────────────────────────┐
│  Client .NET (C#)       │  ← RiskAssistantClients.cs
│  Models: Models-4.cs    │
│  Entrée:  Program-5.cs  │
└──────────┬──────────────┘
           │ HTTP/JSON
┌──────────▼──────────────┐
│  FastAPI (Python)       │  ← main.py
│  Models: # models.py    │
└─────────────────────────┘
```

## Lancer

**API Python**
```bash
pip install fastapi uvicorn numpy
uvicorn main:app --reload
```

**Client C#**
```bash
dotnet run
```

## Stack
Python 3.11 · FastAPI · Pydantic · numpy · .NET / C# · System.Net.Http
