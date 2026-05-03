import locale
import random
import pandas as pd
import logging
from pathlib import Path

LOG_FILE = "logs.csv"
OUTPUT_DIR = "OUTPUT"


LOG_FILE = "logs.csv"
MAX_USERS = 1000000
class Anonym:


    def __init__(self):

        self._ens = set()

        self._tab = dict()

    def _anonymiser_id(self, id: str):
        # Normaliser  l'identifiant
        lid = id.lower()


        if lid in self._tab:
            return str(self._tab[lid])

        # Génére un nouveau pseudo unique
        i = random.randint(0, MAX_USERS)
        while i in self._ens:
            i = random.randint(0, MAX_USERS)

        # Enregistrer
        self._ens.add(i)
        self._tab[lid] = i

        logging.debug(f"Anonymisation de {lid} en {i}")

        return str(i)

    def anonymiser_logs(self, logs= LOG_FILE):
        # Charger le fichier export
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

        # Ajout d'une colonne de pseudo (anonymisé)
        df["pseudo"] = df["Nom complet de l’utilisateur"].apply(self._anonymiser_id)

        # Renomme les colonnes
        df = df.rename(
            columns={
                "Heure": "heure",
                "Nom complet de l'utilisateur": "id",
                "Contexte de l’événement": "contexte",
                "Composant": "composant",
                "Nom de l’événement": "evenement",
            }
        )
        print("Colonnes du CSV :", df.columns.tolist())
        # Conserver les colonnes à enregistrer
        df = df[["heure", "pseudo", "contexte", "composant", "evenement"]]

        df["heure"] = df['heure'].apply(self.remplacer_mois)
        df["date"] = df['heure'].apply(self.convertir_date)


        df = df[["date", "pseudo", "contexte", "composant", "evenement"]]

        df.sort_values(by="heure", inplace=True)

        return df

    def remplacer_mois(self, cellule):
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

    def convertir_date(self, d):
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

    from pathlib import Path
    import logging

    def anonymiser_logs_et_sauvegarder(self, logs=LOG_FILE, dossier="OUTPUT"):
        """
        Anonymise les logs, crée le dossier de sortie, sauvegarde le fichier
        et affiche des statistiques.
        """

        # Création du dossier de sortie
        Path(dossier).mkdir(parents=True, exist_ok=True)

        try:
            # Anonymisation
            df = self.anonymiser_logs(logs)

            # Nom du fichier de sortie
            filename = Path(dossier) / "logs_anonymises.csv"

            # Enregistrement
            df.to_csv(filename, index=False, encoding="utf-8")

            # Statistiques
            nb_usr = len(df["pseudo"].unique())
            nb_ctx = len(df["contexte"].unique())
            nb_evt = len(df["evenement"].unique())
            nb_ln = len(df)

            # Logs d'information
            logging.info("Anonymisation des logs terminée avec succès")
            logging.info(f"Nombre de lignes     = {nb_ln}")
            logging.info(f"Nombre d'utilisateurs= {nb_usr}")
            logging.info(f"Nombre de contextes  = {nb_ctx}")
            logging.info(f"Nombre d'événements  = {nb_evt}")

            print("Anonymisation terminée avec succès ✅")
            print(f"Fichier généré : {filename}")

            return df

        except Exception as e:
            logging.error(f"Erreur d'anonymisation : {e}")
            print("Erreur lors de l'anonymisation ❌")
            return None


if __name__ == "__main__":

    an = Anonym()
    date_x = "24 déc. 25, 16:48:46"

    x1 = an.remplacer_mois(date_x)
    print(x1)
    print(an.convertir_date(x1))

"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


    an = Anonym()

    df = an.anonymiser_logs_et_sauvegarder(
        logs=LOG_FILE,
        dossier=OUTPUT_DIR
    )

    if df is not None:
        print("\nAperçu des données anonymisées :")
        print(df.head())
    else:
        print("\nÉchec du traitement des logs.")
"""

