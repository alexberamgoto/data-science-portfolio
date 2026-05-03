import locale
import logging
import random

import pandas as pd

MAX_USERS = 10_000
LOG_FILE = "logs_anonymises.csv"


class Anonymiser:
    def __init__(self):
        self._table = {}
        self._ensemble = set()

    def _anonymiser_id(self, id_):
        lid = str(id_).lower()
        if lid in self._table:
            return str(self._table[lid])

        i = random.randint(0, MAX_USERS)
        while i in self._ensemble:
            i = random.randint(0, MAX_USERS)

        self._ensemble.add(i)
        self._table[lid] = i
        logging.debug(f"Anonymisation de {lid} en {i}")
        return str(i)

    def anonymiser_logs(self, logs=LOG_FILE):
        """Charge le CSV, anonymise le nom complet et retourne un DataFrame nettoyé."""
        try:
            df = pd.read_csv(
                logs,
                sep=";",
                usecols=[
                    "Heure",
                    "Nom complet de l’utilisateur",
                    "Contexte de l’événement",
                    "Composant",
                    "Nom de l’événement",
                ],
            )
        except Exception as e:
            logging.warning(f"Erreur de lecture du fichier de logs : {logs} ({e})")
            return pd.DataFrame()

        # nettoyage/normalisation de la date
        df["Heure"] = df["Heure"].apply(self._remplacer_mois)
        df["Heure"] = df["Heure"].apply(self._convertir_date)

        # anonymisation
        df["pseudo"] = df["Nom complet de l’utilisateur"].apply(self._anonymiser_id)

        # renommage des colonnes
        df = df.rename(
            {
                "Heure": "heure",
                "Nom complet de l’utilisateur": "id",
                "Contexte de l’événement": "contexte",
                "Composant": "composant",
                "Nom de l’événement": "evenement",
            },
            axis="columns",
        )

        # colonnes finales
        df = df[["heure", "pseudo", "contexte", "composant", "evenement"]]

        return df

    def _remplacer_mois(self, cellule):
        """Remplace les abréviations françaises des mois par leur nom complet."""
        c = (
            str(cellule)
            .replace("nov.", "novembre")
            .replace("déc.", "décembre")
            .replace("oct.", "octobre")
            .replace("sept.", "septembre")
            .replace("juil.", "juillet")
            .replace("avr.", "avril")
            .replace("févr.", "février")
            .replace("janv.", "janvier")
        )
        return c

    def _convertir_date(self, d):
        """Convertit une date texte française en Timestamp."""
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        try:
            return pd.to_datetime(d, dayfirst=True, errors="coerce")
        except Exception:
            logging.warning(f"Erreur de format de date : {d}")
            return pd.NaT


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    anonymiser = Anonymiser()
    df_logs = anonymiser.anonymiser_logs()
    print(df_logs.head())
