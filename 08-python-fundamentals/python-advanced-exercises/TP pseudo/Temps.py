import pandas as pd
import matplotlib.pyplot as plt
import logging
import seaborn as sns
from zope.interface import named


class Temps:

    def _init_(self, log_file: str):
        """
        Charge le fichier CSV et prépare le DataFrame.
        """
        self.data = pd.read_csv(log_file)

        # Convertir la date si elle existe
        if "date" in self.data.columns:
            self.data["date"] = pd.to_datetime(self.data["date"], errors="coerce")

    def _cumul_tps(self, x: pd.Series) -> int:
        """
        x : Series de timestamps (ou strings de dates)
        Retour : cumul des deltas successifs < 300s, en secondes (int).
        """
        # convertir en datetime, supprimer les NaN et trier
        x = pd.to_datetime(x, errors="coerce").dropna().sort_values()

        if x.empty:
            return 0

        t0 = x.iloc[0]
        res = 0.0

        # parcourir à partir du second élément
        for t in x.iloc[1:]:
            diff = (t - t0).total_seconds()
            if 0 < diff < 300:
                res += diff
            t0 = t  # on avance le point de référence

        return int(res)

    def tmps_activites_par_jour(self):
        # copier les données utiles et filtrer les lignes incomplètes
        df = self.data[['pseudo', 'date']].dropna(subset=['pseudo', 'date']).copy()

        # s'assurer que les timestamps sont bien de type datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])

        # trier par pseudo et heure pour garantir l'ordre chronologique
        df = df.sort_values(['pseudo', 'date'])

        # ajouter le jour (date sans l'heure)
        df['jour'] = df['date'].dt.date

        # calculer le temps d'activité par utilisateur et par jour
        # self._cumul_tps doit prendre une Series de timestamps et retourner un int (secondes)
        res = (
            df.groupby(['pseudo', 'jour'])['date']
            .apply(self._cumul_tps)
            .reset_index(name='temps')
        )

        return res

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import logging

    def ficher_diagramme_thermique(self, date_debut=None, date_fin=None):
        """
        Génère une heatmap des temps d'activité par utilisateur et par jour.
        date_debut / date_fin sont optionnels (string, datetime ou None).
        """
        try:
            # Récupérer les temps d'activité agrégés
            df = self.tmps_activites_par_jour()  # colonnes : pseudo, jour, temps

            # Filtre par date de début
            if date_debut is not None:
                date_debut = pd.to_datetime(date_debut).date()
                df = df[df["jour"] >= date_debut]

            # Filtre par date de fin
            if date_fin is not None:
                date_fin = pd.to_datetime(date_fin).date()
                df = df[df["jour"] <= date_fin]

            if df.empty:
                logging.warning("Aucune donnée à afficher pour l'intervalle donné.")
                return

            # Tableau croisé : lignes = pseudo, colonnes = jour, valeurs = temps
            pivot = (
                df.pivot_table(
                    index="pseudo",
                    columns="jour",
                    values="temps",
                    fill_value=0
                )
                .astype(int)
            )

            # Trier les utilisateurs et les jours
            pivot = pivot.sort_index()
            pivot = pivot.reindex(sorted(pivot.columns), axis=1)

            # Plot de la heatmap
            sns.set_theme(style="white", font_scale=0.9)
            plt.figure(figsize=(12, 6))
            ax = sns.heatmap(
                pivot,
                linewidths=0.5,
                annot=True,
                fmt=".0f",
                cmap="YlGnBu"
            )

            # Titres et labels
            titre = "Heatmap des temps d'activité par utilisateur et par jour"
            ax.set_title(titre)
            ax.set_xlabel("Jour")
            ax.set_ylabel("Utilisateur")

            # Lisibilité des ticks
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

        except Exception as e:
            logging.exception("Erreur lors de la génération de la heatmap: %s", e)


if __name__== "_main_":

    obj = Temps(log_file="OUTPUT/logs_anonymises.csv")
    obj.ficher_diagramme_thermique()