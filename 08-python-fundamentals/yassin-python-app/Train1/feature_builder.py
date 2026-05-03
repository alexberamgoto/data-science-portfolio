
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
# (ex-ClasseB)
# =========================
class UserActivityFeatureBuilder:
    """
    Construit des features par 'pseudo' à partir d'un DataFrame de logs.
    Conserve les colonnes historiques et ajoute des caractéristiques avancées.
    """

    def __init__(self, df_logs: pd.DataFrame):
        self.df = df_logs.copy()
        self.df["pseudo"] = self.df["pseudo"].astype(str)
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")

    def _cumul_tps(self, x: pd.Series) -> int:
        x = pd.to_datetime(x, errors="coerce").dropna().sort_values()
        if x.empty:
            return 0
        t0 = x.iloc[0]
        res = 0.0
        # cumul des sessions < 5 minutes entre logs consécutifs
        for t in x.iloc[1:]:
            diff = (t - t0).total_seconds()
            if 0 < diff < 300:
                res += diff
            t0 = t
        return int(res)

    def _session_stats_by_day(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calcule par (pseudo, jour) la durée cumulée des sessions
        puis agrège au niveau pseudo en somme / moyenne / médiane.
        """
        df = df.dropna(subset=["pseudo", "date"]).copy()
        df["jour"] = df["date"].dt.date

        # Durée cumulée par jour (logique existante)
        temps_par_jour = (
            df.groupby(["pseudo", "jour"])["date"]
            .apply(self._cumul_tps)
            .reset_index(name="temps")
        )

        # Agrégations supplémentaires
        session_stats = temps_par_jour.groupby("pseudo")["temps"].agg(
            temps_total="sum",
            avg_session_secs="mean",
            median_session_secs="median"
        ).reset_index()

        return temps_par_jour, session_stats

    def build_features(self) -> pd.DataFrame:
        """
        Construit et retourne le DataFrame de features par 'pseudo'.
        Conserve : nb_logs, nb_jours, nb_contextes, nb_composants, temps_total
        Ajoute : avg_session_secs, median_session_secs, first/last_activity, days_active_span,
                 logs_per_active_day, nb_evenements, entropies, nb_weekend_days, nb_night_logs
        """
        df = self.df.dropna(subset=["pseudo", "date"]).copy()
        df["jour"] = df["date"].dt.date
        df["dow"] = df["date"].dt.dayofweek  # 0=lundi .. 6=dimanche
        df["hour"] = df["date"].dt.hour

        # ---- Stats de sessions (inclut l'existant temps_total)
        temps_par_jour, session_stats = self._session_stats_by_day(df)

        # ---- Métriques historiques (préservées)
        nb_logs = df.groupby("pseudo").size().reset_index(name="nb_logs")
        nb_jours = df.groupby("pseudo")["jour"].nunique().reset_index(name="nb_jours")
        nb_contextes = df.groupby("pseudo")["contexte"].nunique().reset_index(name="nb_contextes")
        nb_composants = df.groupby("pseudo")["composant"].nunique().reset_index(name="nb_composants")

        # ---- Nouvelles features
        # 1) Bornes temporelles et étendue
        first_last = df.groupby("pseudo")["date"].agg(first_activity="min", last_activity="max").reset_index()
        first_last["days_active_span"] = (first_last["last_activity"] - first_last["first_activity"]).dt.days.clip(lower=0)

        # 2) Densité d'activité
        logs_per_active_day = (
            df.groupby("pseudo").size() / df.groupby("pseudo")["jour"].nunique()
        ).reset_index(name="logs_per_active_day")

        # 3) Événements distincts
        nb_evenements = df.groupby("pseudo")["evenement"].nunique().reset_index(name="nb_evenements")

        # 4) Entropies de diversité
        context_entropy = (
            df.groupby("pseudo")["contexte"].apply(_shannon_entropy).reset_index(name="context_entropy")
        )
        component_entropy = (
            df.groupby("pseudo")["composant"].apply(_shannon_entropy).reset_index(name="component_entropy")
        )

        # 5) Week-end et activité nocturne
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

        # ---- Assemblage des features
        features = nb_logs
        for part in [nb_jours, nb_contextes, nb_composants]:
            features = pd.merge(features, part, on="pseudo", how="left")

        # join session stats (inclut temps_total, avg, median)
        features = pd.merge(features, session_stats, on="pseudo", how="left")

        # joindre extras
        for part in [first_last, logs_per_active_day, nb_evenements, context_entropy, component_entropy, weekend_days, night_logs]:
            features = pd.merge(features, part, on="pseudo", how="left")

        # Nettoyage final
        features = features.fillna({
            "nb_logs": 0, "nb_jours": 0, "nb_contextes": 0, "nb_composants": 0,
            "temps_total": 0, "avg_session_secs": 0.0, "median_session_secs": 0.0,
            "logs_per_active_day": 0.0, "nb_evenements": 0,
            "context_entropy": 0.0, "component_entropy": 0.0,
            "nb_weekend_days": 0, "nb_night_logs": 0
        })

        return features
