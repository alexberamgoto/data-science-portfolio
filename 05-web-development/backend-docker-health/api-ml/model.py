# Modèle simple embarqué (pseudo-ML) : pondération + sigmoïde
from math import exp
from typing import Dict

# Coefficients "prétrainiés" (exemple)
COEFFS = {
    'bias': -3.0,
    'weight': 0.01,
    'systolic': 0.02,
    'diastolic': 0.015,
    'glucose': 4.0,  # g/L a fort poids
}

LEVELS = [
    (0.2, 'LOW'),
    (0.5, 'MEDIUM'),
    (0.8, 'HIGH'),
]

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + exp(-x))

def score_sample(sample: Dict) -> Dict:
    x = COEFFS['bias']
    for k, w in COEFFS.items():
        if k == 'bias':
            continue
        val = float(sample.get(k, 0) or 0)
        x += w * val
    s = sigmoid(x)
    risk = 'VERY_HIGH'
    for thr, lvl in LEVELS:
        if s <= thr:
            risk = lvl
            break
    explanation = (
        'Score construit via combinaison linéaire (poids médicaux simplifiés) '
        'puis passage par sigmoïde. Valeurs élevées de glucose et de tension '
        'augmentent fortement le risque.'
    )
    return { 'score': round(s, 4), 'riskLevel': risk, 'explanation': explanation }
