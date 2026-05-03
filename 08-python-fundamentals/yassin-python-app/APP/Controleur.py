
import pandas as pd
import numpy as np
import joblib
from feature_builder import UserActivityFeatureBuilder


def _normalize_logs_df(df: pd.DataFrame):
    """Normalise les noms de colonnes et retourne (df_norm, renamed_map)."""
    rename_map = {
        'Date': 'date', 'DATE': 'date', 'timestamp': 'date', 'time': 'date', 'datetime': 'date',
        'User': 'pseudo', 'utilisateur': 'pseudo', 'user': 'pseudo', 'userid': 'pseudo', 'username': 'pseudo',
        'context': 'contexte', 'Context': 'contexte',
        'component': 'composant', 'Component': 'composant',
        'event': 'evenement', 'Event': 'evenement'
    }
    new_cols = {}
    for c in df.columns:
        new_c = rename_map.get(str(c), str(c))
        new_cols[c] = new_c
    df2 = df.rename(columns=new_cols)
    # ne retourner que les renommages effectifs
    renamed_only = {k: v for k, v in new_cols.items() if k != v}
    return df2, renamed_only


def _encode_datetime_to_days(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    dt_cols = X.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns
    if len(dt_cols) == 0:
        return X
    t0 = pd.to_datetime(X[dt_cols].stack().min())
    for c in dt_cols:
        X[c] = (pd.to_datetime(X[c]) - t0).dt.total_seconds() / 86400.0
    return X


class Controleur:
    @staticmethod
    def methodeA(fichier_logs, seuil: float = 10.0, model_path: str = "model_lr.pkl"):
        """
        Retourne (preds_df, counts, info) où info contient :
        - 'renamed_cols': dict des colonnes renommées
        - 'synthetic_date': bool indiquant si une date synthétique a été utilisée
        """
        df_logs = pd.read_csv(fichier_logs)
        df_logs, renamed = _normalize_logs_df(df_logs)

        fb = UserActivityFeatureBuilder(df_logs)
        feats = fb.build_features()  # contient 'pseudo'
        X = feats.drop(columns=["pseudo"], errors="ignore")

        X = _encode_datetime_to_days(X)
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        try:
            model = joblib.load(model_path)
        except Exception as e:
            raise RuntimeError(f"Impossible de charger le modèle '{model_path}': {e}")

        y_pred = model.predict(X)
        preds_df = pd.DataFrame({
            "pseudo": feats.get("pseudo", pd.Series(range(len(X)))),
            "prediction": y_pred
        })
        preds_df["resultat"] = np.where(preds_df["prediction"] >= seuil, "Réussite", "Échec")
        counts = preds_df["resultat"].value_counts().reindex(["Réussite", "Échec"], fill_value=0)

        info = {
            "renamed_cols": renamed,
            "synthetic_date": bool(getattr(fb, 'meta', {}).get('synthetic_date', False)),
        }
        return preds_df, counts, info
