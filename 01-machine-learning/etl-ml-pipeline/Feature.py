# Feature.py
import pandas as pd

class FeatureEngineering:
    def __init__(self, df, target_col=None):
        """
        df : DataFrame d'entrée (ex: le merged venant de l'ETL)
        target_col : nom de la colonne cible (si supervision) ex. 'label', 'target', etc.
        """
        if df is None or len(df) == 0:
            raise ValueError("FeatureEngineering: DataFrame d'entrée vide ou None.")
        self.df = df.copy()
        self.target_col = target_col

        # Ces attributs seront remplis par build_features()
        self.X = None
        self.y = None

    def build_features(self):
        """
        Construit X (features) et y (cible éventuelle) à partir de self.df.
        Retourne: X, y (y peut être None s'il n'y a pas de cible).
        """
        df = self.df.copy()

        # --- 1) Nettoyages/transformations simples (exemples à adapter) ---
        # a) Convertir bool -> int
        for col in df.select_dtypes(include=["bool"]).columns:
            df[col] = df[col].astype(int)

        # b) Gestion des catégorielles : one-hot encoding
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        if cat_cols:
            df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

        # --- 2) Séparation X / y ---
        target = self.target_col
        if target is None:
            # Essaie de déduire une cible courante si non fournie
            for candidate in ["label", "target", "y", "classe", "is_fraud"]:
                if candidate in df.columns:
                    target = candidate
                    break

        if target is not None and target in df.columns:
            y = df[target]
            X = df.drop(columns=[target])
        else:
            # Pas de cible → tâches non supervisées
            y = None
            X = df

        # --- 3) (Optionnel) Remplissage des NaN / scaling / etc. ---
        # Exemple simple : remplir NaN numériques par la médiane
        num_cols = X.select_dtypes(include=["number"]).columns
        for c in num_cols:
            if X[c].isna().any():
                X[c] = X[c].fillna(X[c].median())

        # Sauvegarder dans l'objet (utile pour debug/traçabilité)
        self.X, self.y = X, y
        return X, y

    # (Optionnel) Alias si ton main attend un autre nom de méthode
    def create_features(self):
        return self.build_features()