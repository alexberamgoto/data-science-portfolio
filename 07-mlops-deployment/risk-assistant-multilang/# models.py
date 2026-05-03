# models.py
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
import numpy as np

# === Scoring de risque (dummy) ===
risk_model = LogisticRegression()
risk_model.classes_ = np.array([0, 1])

def risk_predict_proba(features: np.ndarray) -> float:
    # POC : scoring "fake" (à remplacer par un vrai modèle)
    # Exemple simple : plus le montant est grand, plus le risque est élevé
    amount = features[0]
    score = 1 / (1 + np.exp(- (amount / 1000)))
    return float(score)

# === Détection d’anomalies (dummy IsolationForest-like) ===
anomaly_model = IsolationForest()

def anomaly_score(features: np.ndarray) -> float:
    # POC : score simple basé sur un z-score
    x = features
    mean = np.mean(x)
    std = np.std(x) if np.std(x) > 0 else 1
    z = abs((x[0] - mean) / std)
    return float(z)

# === Recommandations financières (dummy) ===
def recommend_products(risk_score: float, income: float):
    recos = []
    if risk_score < 0.3:
        recos.append("Carte de crédit premium")
        recos.append("Portefeuille d’investissement dynamique")
    elif risk_score < 0.7:
        recos.append("Crédit à la consommation standard")
        recos.append("Fonds équilibré")
    else:
        recos.append("Compte épargne sécurisé")
        recos.append("Micro-crédit à faible montant")
    if income > 4000:
        recos.append("Conseiller financier dédié")
    return recos
