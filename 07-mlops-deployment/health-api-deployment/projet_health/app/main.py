from fastapi import FastAPI
from pydantic import BaseModel
import os
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import tensorflow as tf
import numpy as np
import pandas as pd
import joblib
import asyncio
# ... (Gardez vos autres imports : Pydantic, Patient

# 1. Création de l'application
app = FastAPI(
title="Service E-Santé Health",
description="API de prédiction de risques de cancer du sein",
version="1.0.0"
)
# 2. Définition d'une route de base (GET)
@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API Health"}


# Modèle de données attendu en entrée
# Basé sur les features du dataset du projet E-Santé
class PatientData(BaseModel):
    Id: int  # identifiant du Patient
    Age: int  # Age in years
    Gender: int  # (0 = Female, 1 = Male)
    Family_History: bool  # 0/1 -- positive family history
    BRCA_Mutation: bool  # 0/1 -- BRCA mutation flag
    Occupational_Hazards: int  # Ordinal exposure index (0-10)
    # Ajout à PatientData :
    Smoking: int
    Alcohol_Use: int
    Obesity: int
    Diet_Red_Meat: int
    Diet_Salted_Processed: int
    Fruit_Veg_Intake: int
    Physical_Activity: int
    Air_Pollution: int
    H_Pylori_Infection: bool
    Calcium_Intake: int
    BMI: float
    Physical_Activity_Level: int

    # Définition d'une classe pour le modèle
    class BreastCancerModel:
        def __init__(self):
            self.model_path = "models/model_reg.keras"
            self.model = None

            # utilisons un pipeline sklearn pour transformer les données
            self.pipeline_path = "models/pipeline.joblib"
            self.pipeline = None

            self.load_model()

        def load_model(self):
            """Charge le modèle TensorFlow en mémoire"""
            try:
                print(f"🔄 Chargement du modèle {self.model_path}...")
                # Chargement réel via Keras
                self.model = tf.keras.models.load_model(self.model_path)
                print("✅ Modèle chargé avec succès !")

                print(f"🔄 Chargement du pipeline {self.pipeline_path}...")
                # Chargement du pipeline via joblib
                self.pipeline = joblib.load(self.pipeline_path)
                print("✅ Modèle chargé avec succès !")

            except Exception as e:
                print(f"❌ Erreur critique au chargement du modèle : {e}")
                # En production, on pourrait vouloir arrêter l'app ici
                # raise e

        def preprocess(self, data: PatientData) -> pd.DataFrame:
            """Transforme les données pour utilisation."""
            # Le pipeline utilisé n'accepte qu'un DataFrame pandas en entrée.
            df_data = pd.DataFrame(data.model_dump(), index=[0])
            # Cela lui permet d'appliquer les bonnes transformations
            # et de dropper certaines colonnes
            return self.pipeline.transform(df_data)

        def predict(self, data: PatientData) -> float:
            if not self.model:
                # Fallback si le modèle n'est pas là (évite de planter le TP)
                print("⚠️ Utilisation du mode Mock (Modèle non chargé)")
                return 0.5

            # 1. Preprocessing
            input = self.preprocess(data)

            # 2. Inférence Réelle
            # predict retourne ici [[score]], on récupère le float
            prediction = self.model.predict(input)
            return float(prediction[0][0])

    def preprocess(self, data: PatientData) -> list:
        """Transforme les données brutes (Pydantic) en vecteur (Liste)"""

        # 1. Sélection des variables
        # Supposons que le modèle a été entraîné SANS certaines variables.

        # 2. Normalisation / Encodage
        # Exemple : On normalise l'âge entre 0 et 1 (si max age = 100)
        norm_age = data.Age / 100
        norm_hazards = data.Occupational_Hazards / 10

        # Exemple : Conversion Booléen -> Int (0 ou 1)
        has_history = 1 if data.Family_History else 0
        has_mutation = 1 if data.BRCA_Mutation else 0

        # Retourne le vecteur [Age, History, Mutation, Hazards]
        return [norm_age, has_history, has_mutation, norm_hazards]


def predict(self, data: PatientData) -> float:

    # 1. On nettoie les données d'abord
    features = self.preprocess(data)
    # 2. On fait l'inférence (Simulation)
    # Ici, ce serait : prediction = self.model.predict([features])
    # Logique factice pour l'exercice :
    risk_score = 0.1
    if features[0] > 0.5:  # Si age > 50 (0.5 * 100)
        risk_score += 0.3
    if features[1] == 1:  # Si antécédents
        risk_score += 0.4
    return min(risk_score + random.uniform(0, 0.1), 1.0)


# Instanciation Globale (Singleton)
ai_model = BreastCancerModel()

# Récupération de l'URL de la BDD depuis les variables d'environnement
# Si la variable n'existe pas (en local), on utilise localhost par défaut
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
db_client = None  # Variable globale pour le client BDD


# Gestion du cycle de vie (Démarrage / Extinction)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au démarrage
    global db_client
    print(f"Connexion à MongoDB sur : {MONGO_URL}")
    db_client = AsyncIOMotorClient(MONGO_URL)
    yield
    # À l'extinction
    db_client.close()
    print("Déconnexion de MongoDB")


# Mise à jour de l'app avec le lifespan
app = FastAPI(
    title="Service E-Santé Health",
    lifespan=lifespan  # On lie le cycle de vie ici
)


async def run_ai_prediction_task(id: str, patient_data: PatientData):
    """Simule le calcul long (Deep Learning) et sauvegarde en BDD."""
    print(f"🔄 [Background] Début du calcul pour le patient {id}...")

    # 1. Simulation du temps de calcul (ex: 10 secondes)
    # Dans la réalité, c'est ici que le modèle tourne



    # 2. Appel au modèle (Prédiction)
    # ai_model.predict est synchrone (CPU bound), on l'appelle directement.
    risk_score = ai_model.predict(patient_data)
    risk_level = "High" if risk_score > 0.5 else "Low"

    # 3. Sauvegarde dans MongoDB
    db = db_client.health_db
    collection = db.patients_data
    document = {
        "id": id,
        "patient_data": patient_data.model_dump(),
        "prediction": {
            "score": risk_score,
            "level": risk_level,
            "calculated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "status": "completed",
    }

    # On utilise update_one avec upsert=True :
    # Si le document existe pour ce patient -> MaJ. Sinon on le crée.
    await collection.update_one(
        {"id": id},
        {"$set": document},
        upsert=True,
    )
    print(f"✅ [Background] Calcul terminé et sauvegardé pour {id}")
