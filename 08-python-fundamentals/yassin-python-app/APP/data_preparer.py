
# =========================
# Imports
# =========================
import pandas as pd
from typing import Tuple

# =========================
# Classe : Préparation des données logs/notes
# =========================
class LogNoteDataPreparer:
    """
    Prépare les jeux d'entraînement/test à partir des logs et des notes.

    - Lit deux CSV (logs, notes)
    - Merge sur 'pseudo'
    - Split par pseudos (stratification simple par fraction)
    - Exporte train/test pour X et Y aux mêmes noms de fichiers qu'avant.
    """

    def __init__(self, fichier_logs: str, fichier_notes: str):
        self.df_logs = pd.read_csv(fichier_logs)
        self.df_notes = pd.read_csv(fichier_notes)
        self.df_logs["pseudo"] = self.df_logs["pseudo"].astype(str)
        self.df_notes["pseudo"] = self.df_notes["pseudo"].astype(str)

    def split_train_test(self, train_size: float = 0.8, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Effectue le split par pseudos et sauvegarde aux fichiers CSV historiques.
        Retourne (train_x, test_x, train_y, test_y) pour une utilisation en mémoire si besoin.
        """
        df = pd.merge(self.df_logs, self.df_notes, on="pseudo")
        pseudos = pd.Series(df["pseudo"].unique())
        pseudos = pseudos.sample(frac=1, random_state=random_state).reset_index(drop=True)

        n = int(len(pseudos) * train_size)
        train_pseudos = pseudos.iloc[:n]
        test_pseudos = pseudos.iloc[n:]

        train = df[df["pseudo"].isin(train_pseudos)]
        test = df[df["pseudo"].isin(test_pseudos)]

        train_x = train[["date", "pseudo", "contexte", "composant", "evenement"]]
        test_x = test[["date", "pseudo", "contexte", "composant", "evenement"]]
        train_y = train[["pseudo", "note"]].drop_duplicates()
        test_y = test[["pseudo", "note"]].drop_duplicates()

        print("Nombre total de logs :", len(self.df_logs))
        print("Nombre initial de notes :", len(self.df_notes))
        print("Nombre d'étudiants après merge :", df["pseudo"].nunique())
        print("Nombre d'étudiants en train :", train["pseudo"].nunique())
        print("Nombre d'étudiants en test :", test["pseudo"].nunique())

        # Exports (noms conservés)
        train_x.to_csv("train_x.csv", index=False)
        test_x.to_csv("test_x.csv", index=False)
        train_y.to_csv("train_y.csv", index=False)
        test_y.to_csv("test_y.csv", index=False)

        return train_x, test_x, train_y, test_y
