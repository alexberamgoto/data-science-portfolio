import logging
import random
import pandas as pd
import locale

MAX_USERS = 100_000
LOG_FILE = "logs.csv"
OUT_FILE = "logs_anonymises.csv"


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

        # Conversion en datetime en laissant pandas deviner le format
        #df["Heure"] = pd.to_datetime(df["Heure"], errors="coerce")


        # Anonymisation
        df["pseudo"] = df["Nom complet de l’utilisateur"].apply(self._anonymiser_id)

        # Renommage des colonnes
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
        df["heure"] = df['heure'].apply(self._remplacer_mois)
        df["date"] = df['heure'].apply(self._convertir_date)
        # Colonnes finales
        df = df[["date", "pseudo", "contexte", "composant", "evenement"]]

        return df


    def _remplacer_mois(self, cellule):
        c = str(cellule)
        c = c.replace('nov.', 'november') \
            .replace('déc.', 'december') \
            .replace('dec.', 'december') \
            .replace('oct.', 'october') \
            .replace('sept.', 'september') \
            .replace('juil.', 'july') \
            .replace('avr.', 'april') \
            .replace('févr.', 'february') \
            .replace('fevr.', 'february') \
            .replace('janv.', 'january') \
            .replace('août.', 'august') \
            .replace('aout.', 'august')
        return c

    def _convertir_date(self, d):
        try:
            locale.setlocale(locale.LC_TIME, "C")

            s = str(d).strip()
            #print("Valeur testée :", s)

            res = pd.to_datetime(s, format="%d %B %y, %H:%M:%S")

            #print("Conversion OK :", res)
            return res

        except Exception as e:
            print("ERREUR de conversion pour :", d)
            print("Message d'erreur :", e)
            return pd.NaT


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    anonymiser = Anonymiser()
    df_logs = anonymiser.anonymiser_logs()

    print(df_logs.head())

    # Enregistrement dans un nouveau fichier CSV
    df_logs.to_csv(OUT_FILE, index=False)
    print(f"Fichier sauvegardé sous : {OUT_FILE}")
