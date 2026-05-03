# modele.py
import logging
from dataclasses import dataclass

import pandas as pd
from pandas import DataFrame

# Noms des colonnes dans le CSV (après nettoyage)
COL_DATE = "jour"
COL_DEP = "dep"
COL_DECES = "incid_dc"


@dataclass
class Modele:
    """
    Modèle chargé de lire et préparer les données à partir du fichier CSV.
    """
    fichier: object  # UploadedFile de Streamlit
    df: DataFrame = None

    def __post_init__(self):
        self.df = self._load_data(self.fichier)

    @staticmethod
    def _load_data(fichier) -> DataFrame:
        """
        Charge le CSV et prépare le DataFrame.
        - utilise le séparateur ';'
        - nettoie les noms de colonnes (enlève les guillemets)
        - parse les dates
        """
        try:
            # ⚠️ Ton fichier est séparé par des ';'
            df = pd.read_csv(fichier, sep=";")
        except Exception as e:
            logging.error(f"Erreur lors du chargement du fichier CSV : {e}")
            raise

        # Nettoyage des noms de colonnes : enlever les guillemets et espaces
        df.columns = [c.strip().strip('"').strip("'") for c in df.columns]


        # Conversion robuste "01" -> 1
        df["dep"] = pd.to_numeric(df["dep"], errors="coerce").astype("Int64")

        logging.info(f"Colonnes présentes dans le CSV : {set(df.columns)}")

        # Vérification des colonnes obligatoires
        colonnes_obligatoires = {COL_DATE, COL_DEP, COL_DECES}
        if not colonnes_obligatoires.issubset(df.columns):
            raise ValueError(
                f"Le fichier CSV doit contenir les colonnes : {colonnes_obligatoires}, "
                f"mais contient : {set(df.columns)}"
            )

        # Conversion de la colonne de date en datetime
        df[COL_DATE] = pd.to_datetime(df[COL_DATE], errors="coerce")

        # Suppression des lignes avec date invalide
        df = df.dropna(subset=[COL_DATE])

        logging.info(f"CSV chargé avec {len(df)} lignes après nettoyage.")
        return df
