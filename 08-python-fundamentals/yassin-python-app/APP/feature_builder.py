
# =========================
# Imports
# =========================
import pandas as pd
import numpy as np
from typing import Optional

# =========================
# Helpers
# =========================

def _shannon_entropy(series: pd.Series) -> float:
    """
    Entropie de Shannon (base e) sur une série de catégories.
    Retourne 0.0 si la série est vide.
    """
    s = series.dropna()
    if s.empty:
        return 0.0
    counts = s.value_counts(normalize=True)
    return float(-(counts * np.log(counts + 1e-12)).sum())

# =========================
# Classe : Construction de features d'activité
# =========================
class UserActivityFeatureBuilder:
    """
    Construit des features par 'pseudo' à partir d'un DataFrame de logs.
    Résilient si certaines colonnes manquent (ex: 'date', 'contexte', 'composant', 'evenement').
    Expose des métadonnées dans self.meta (ex: synthetic_date: bool).
    """

    REQUIRED_PSEUDO = 'pseudo'
    OPTIONAL_COLS = ['date', 'contexte', 'composant', 'evenement']

    def __init__(self, df_logs: pd.DataFrame):
        self.meta = {"synthetic_date": False}
        # Normalisation minimale des noms de colonnes
        df = df_logs.copy()
        df.columns = [str(c).strip() for c in df.columns]
        # S'assurer de la présence de 'pseudo'
        if 'pseudo' not in df.columns:
            for cand in ['user', 'utilisateur', 'id', 'userid', 'username']:
                if cand in df.columns:
                    df = df.rename(columns={cand: 'pseudo'})
                    break
        if 'pseudo' not in df.columns:
            df['pseudo'] = [f"user_{i}" for i in range(len(df))]
        df['pseudo'] = df['pseudo'].astype(str)

        # Gestion de la date : si absente, créer une timeline synthétique (1s d'écart)
        if 'date' not in df.columns:
            self.meta["synthetic_date"] = True
            df['date'] = pd.Timestamp.utcnow() + pd.to_timedelta(np.arange(len(df)), unit='s')
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Colonnes optionnelles manquantes -> valeurs vides
        for col in ['contexte', 'composant', 'evenement']:
            if col not in df.columns:
                df[col] = ''

        self.df = df

    def _cumul_tps(self, x: pd.Series) -> int:
        x = pd.to_datetime(x, errors="coerce").dropna().sort_values()
        if x.empty:
            return 0
        t0 = x.iloc[0]
        res = 0.0
        for t in x.iloc[1:]:
            diff = (t - t0).total_seconds()
            if 0 < diff < 300:
                res += diff
            t0 = t
        return int(res)

    def _session_stats_by_day(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        df = df.dropna(subset=["pseudo"]).copy()
        if 'date' not in df.columns or df['date'].notna().sum() == 0:
            df['date'] = pd.Timestamp.utcnow()
        df["jour"] = pd.to_datetime(df["date"], errors='coerce').dt.date

        temps_par_jour = (
            df.groupby(["pseudo", "jour"]).apply(lambda g: self._cumul_tps(g['date']))
              .reset_index(name="temps")
        )
        session_stats = temps_par_jour.groupby("pseudo")["temps"].agg(
            temps_total="sum",
            avg_session_secs="mean",
            median_session_secs="median"
        ).reset_index()
        return temps_par_jour, session_stats

    def build_features(self) -> pd.DataFrame:
        df = self.df.dropna(subset=["pseudo"]).copy()
        df["jour"] = pd.to_datetime(df["date"], errors='coerce').dt.date
        df["dow"] = pd.to_datetime(df["date"], errors='coerce').dt.dayofweek
        df["hour"] = pd.to_datetime(df["date"], errors='coerce').dt.hour

        temps_par_jour, session_stats = self._session_stats_by_day(df)

        nb_logs = df.groupby("pseudo").size().reset_index(name="nb_logs")
        nb_jours = df.groupby("pseudo")["jour"].nunique().reset_index(name="nb_jours")
        nb_contextes = df.groupby("pseudo")["contexte"].nunique().reset_index(name="nb_contextes")
        nb_composants = df.groupby("pseudo")["composant"].nunique().reset_index(name="nb_composants")

        first_last = df.groupby("pseudo")["date"].agg(first_activity="min", last_activity="max").reset_index()
        first_last["days_active_span"] = (
            (pd.to_datetime(first_last["last_activity"]) - pd.to_datetime(first_last["first_activity"]))
            .dt.days
            .clip(lower=0)
        )

        logs_per_active_day = (
            df.groupby("pseudo").size() / df.groupby("pseudo")["jour"].nunique().replace(0, np.nan)
        ).reset_index(name="logs_per_active_day").fillna(0)

        nb_evenements = df.groupby("pseudo")["evenement"].nunique().reset_index(name="nb_evenements")
        context_entropy = (
            df.groupby("pseudo")["contexte"].apply(_shannon_entropy).reset_index(name="context_entropy")
        )
        component_entropy = (
            df.groupby("pseudo")["composant"].apply(_shannon_entropy).reset_index(name="component_entropy")
        )

        weekend_days = (
            df.assign(is_weekend=df["dow"] >= 5)
              .groupby(["pseudo", "jour"])["is_weekend"].max()
              .reset_index()
              .groupby("pseudo")["is_weekend"].sum()
              .reset_index(name="nb_weekend_days")
        )
        night_logs = (
            df.assign(is_night=(df["hour"] < 6))
              .groupby("pseudo")["is_night"].sum()
              .reset_index(name="nb_night_logs")
        )

        features = nb_logs
        for part in [nb_jours, nb_contextes, nb_composants]:
            features = pd.merge(features, part, on="pseudo", how="left")
        features = pd.merge(features, session_stats, on="pseudo", how="left")
        for part in [first_last, logs_per_active_day, nb_evenements, context_entropy, component_entropy, weekend_days, night_logs]:
            features = pd.merge(features, part, on="pseudo", how="left")

        features = features.fillna({
            "nb_logs": 0, "nb_jours": 0, "nb_contextes": 0, "nb_composants": 0,
            "temps_total": 0, "avg_session_secs": 0.0, "median_session_secs": 0.0,
            "logs_per_active_day": 0.0, "nb_evenements": 0,
            "context_entropy": 0.0, "component_entropy": 0.0,
            "nb_weekend_days": 0, "nb_night_logs": 0
        })
        return features
