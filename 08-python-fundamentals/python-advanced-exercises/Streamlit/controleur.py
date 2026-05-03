# controleur.py
import logging
from datetime import date

import pandas as pd
from pandas import DataFrame

from modele import Modele, COL_DATE, COL_DEP, COL_DECES


class Controleur:
    """
    Logique métier : sélection et agrégation des données
    pour obtenir une série (date -> décès).
    """

    @staticmethod
    def select_data(
        modele: Modele,
        departement: int,
        date_de: date,
        date_a: date,
    ) -> DataFrame:
        """
        Filtre les données du modèle selon :
        - un département (si > 0)
        - un intervalle de dates [date_de, date_a]
        puis retourne une série agrégée par jour (somme de incid_dc).

        :param modele: instance de Modele contenant le DataFrame complet
        :param departement: code département (0 = tous les départements)
        :param date_de: date de début (type datetime.date)
        :param date_a: date de fin (type datetime.date)
        :return: DataFrame indexé par date avec une colonne 'incid_dc'
        """
        df = modele.df.copy()

        # Filtre sur le département si > 0 (0 = "toute la France")
        if departement > 0:
            df = df[df[COL_DEP] == departement]
            logging.info(f"Filtre sur département {departement}: {len(df)} lignes restantes.")
        else:
            logging.info("Aucun filtre de département (tous les départements).")

        # Conversion des bornes en Timestamp
        if date_de is not None:
            date_min = pd.to_datetime(date_de)
            df = df[df[COL_DATE] >= date_min]

        if date_a is not None:
            date_max = pd.to_datetime(date_a)
            df = df[df[COL_DATE] <= date_max]

        logging.info(f"Après filtrage dates [{date_de} -> {date_a}] : {len(df)} lignes restantes.")

        if df.empty:
            logging.warning("Aucune donnée après filtrage. Retour d'un DataFrame vide.")
            # DataFrame vide avec bonne structure
            return pd.DataFrame(columns=[COL_DECES]).set_index(
                pd.DatetimeIndex([], name=COL_DATE)
            )

        # Agrégation par jour : somme des décès
        df_grouped = (
            df.groupby(COL_DATE, as_index=True)[COL_DECES]
            .sum()
            .to_frame(name=COL_DECES)
            .sort_index()
        )

        logging.info(f"Série agrégée sur {len(df_grouped)} dates.")
        return df_grouped
