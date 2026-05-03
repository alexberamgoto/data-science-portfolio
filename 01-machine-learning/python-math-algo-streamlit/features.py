# models/feature_builder.py
import pandas as pd

class FeatureBuilder:
    def __init__(self):
        pass

    @staticmethod
    def _cumul_temps(series_datetime: pd.Series) -> int:
        x = pd.to_datetime(series_datetime, errors='coerce').dropna().sort_values()
        if x.size < 2:
            return 0
        diffs = x.diff().dt.total_seconds().iloc[1:]
        return int(diffs[(diffs > 0) & (diffs < 300)].sum())

    def build_features(self, logs: pd.DataFrame) -> pd.DataFrame:
        logs['jour'] = logs['heure'].dt.date
        grp = logs.groupby('pseudo')

        feats = pd.DataFrame({'pseudo': grp.size().index})
        feats['events_total'] = grp.size().values
        feats['jours_actifs'] = grp['jour'].nunique().values
        feats['contexts_unique'] = grp['contexte'].nunique().values if 'contexte' in logs.columns else 0

        if 'composant' in logs.columns:
            comp_counts = logs.pivot_table(
                index='pseudo',
                columns='composant',
                values='evenement',
                aggfunc='count',
                fill_value=0
            )
            comp_counts.columns = [f"comp_{str(c).strip().lower()}" for c in comp_counts.columns]
            feats = feats.merge(comp_counts, left_on='pseudo', right_index=True, how='left')

        feats['temps_actif_s'] = feats['pseudo'].map(grp['heure'].apply(self._cumul_temps))

        last_activity = grp['heure'].max()
        max_date = logs['heure'].max()

        def _recence(p):
            la = last_activity.get(p)
            if pd.notnull(la) and pd.notnull(max_date):
                return (max_date - la).days
            return 0

        feats['recence_jours'] = feats['pseudo'].map(_recence)

        return feats.fillna(0)
