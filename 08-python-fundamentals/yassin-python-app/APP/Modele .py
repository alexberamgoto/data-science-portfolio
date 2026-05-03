
import pandas as pd
import numpy as np
import joblib
from feature_builder import UserActivityFeatureBuilder


def _encode_datetime_to_days(X: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes datetime en jours depuis t0 (min observé)."""
    X = X.copy()
    dt_cols = X.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns
    if len(dt_cols) == 0:
        return X
    t0 = pd.to_datetime(X[dt_cols].stack().min())
    for c in dt_cols:
        X[c] = (pd.to_datetime(X[c]) - t0).dt.total_seconds() / 86400.0
    return X


class Modele:
    def __init__(self, fichier_logs, model_path: str = "model_lr.pkl"):
        """
        Initialise le modèle en chargeant le CSV de logs et le modèle sklearn.
        - fichier_logs: chemin ou buffer (ex: Streamlit UploadedFile)
        - model_path: chemin du modèle sauvegardé (joblib)
        """
        # Lecture souple du CSV (chemin ou fichier-like)
        df = pd.read_csv(fichier_logs)
        # Normalisations minimales (types)
        if "pseudo" in df.columns:
            df["pseudo"] = df["pseudo"].astype(str)
        # Tenter de caster la/les colonnes date si présente(s)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        self.df_logs = df

        # Charger le modèle
        self.model = joblib.load(model_path)

    def predict(self):
        """Construit les features et renvoie les prédictions du modèle chargé."""
        # Construire les features
        feats = UserActivityFeatureBuilder(self.df_logs).build_features()  # avec 'pseudo'
        X = feats.drop(columns=["pseudo"], errors="ignore")
        # Encoder datetime -> jours
        X = _encode_datetime_to_days(X)
        # Numériser & NaN -> 0
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)
        # Prédire
        return self.model.predict(X)
