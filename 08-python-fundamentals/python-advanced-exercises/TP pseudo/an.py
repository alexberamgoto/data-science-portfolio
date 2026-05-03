from dataclasses import replace

import pandas as pd
import random
import logging


class Anonymiser:
    def _anonymiser_id(self, id) :

    lid = id. Lower ()
    if lid in self._table.keys():
        return str (self._table [lid])
    i = random. randint(0, MAX_USERS)
    while i in self._ensemble:
        i = random.randint(0, MAX_USERS)
    self._ensemble.add(i)
    self._table [lid] = i
    logging. debug (f" Anonymisation de {lid} en {i}")
    return str(i)
def anonymiser_logs(self, logs=L0G_FILE) :
    """..."""
#charger le fichier export
    try:
        df = pd. read_csv(Logs, sep=",", usecols=[ 'Heure',
                                                   "Nom complet de l'utilisateur",
                                                    "Contexte de l'événement" ,
                                                    'Composant' ,
                                                    "Nom de l'événement"])
    except:
        Logging.warning(f'Erreur de lecture du fichier de logs : {logs}')
        return pd. DataFrame ()
#ajouter une colonne de pseudo (anonymisé)
    df['pseudo'] = df["Nom complet de l'utilisateur"]. apply(self._anonymiser_id)
#renommer les colonnes
df = df. rename ({'Heure' : 'heure',
                    "Nom complet de l'utilisateur": 'id',
                    "Contexte de l'événement" : 'contexte'
                    'Composant' : 'composant',
                    "Nom de l'événement" : 'evenement'}, axis=' columns')
# conserver les colonnes à enregistrer
    df = df[['heure', 'pseudo', 'contexte', 'composant', 'evenement']]

    #remplacer les mois
def_remplacer_mois(self,cellule):
""""..."""
def _remplacer_mois(self, cellule):
    c = cellule.replace('nov.', 'novembre') \
        .replace('dec.', 'decembre') \
        .replace('oct.', 'octobre') \
        .replace('sept.', 'septembre') \
        .replace('juil.', 'juillet') \
        .replace('avr.', 'avril') \
        .replace('févr', 'février') \
        .replace('janv.', 'janvier')
    return c
def _convertir_date(self,d) :
    """..."""
    Locale. setlocale(Locale.LC_ALL, 'fr_FR.UTF-8')
    try:
    res = pd.to_datetime(d, format="%d %B %y, %H:%M:%S"')
except:
    logging warning(f"Erreur de format de date : {d}")
    return pd.Timestamp.now()
return res



def
    anonymiser_et_enregistrer_logs(self, logs=LOG_FILE, dossier=OUTUT_DIR) :
#créer le dossier de sortie s'il n'existe pas
    Path (dossier). mkdir(parents=True, exist_ok=True) #anonymiser
df = self.anonymiser_logs (logs)
#enregistrer
filename = dossier + '/' + Path (Logs). stem + '_pseudo'+ '.csv'
try:
df.to_csv (filename, index=False)
logging. info(msg= "Anonymisation des logs réussie: " + filename)
nb_In = len(df)
nb_usr = len(df[' pseudo' l.unique ())
nb_ctx = len(df['contexte']. unique())
nb_comp = len(df['composant'l. unique())
nb_evt = len(df['evenement'l.unique())
logging. info(msg=f"total={nb_In}\n"+
f"pseudo={nb_usr-\n"+
f"contexte={nb_ctx}\n" +
f"composant={nb_comp\n" +
f evenement=(nb_evt} \n")
return
except:
logging. warning (msg= "Erreur d'anonymisation des logs : " + filename)