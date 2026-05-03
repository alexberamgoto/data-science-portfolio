"""
modele.py
Classe Modèle - Gestion des modèles de Machine Learning
Architecture MVC pour l'application Streamlit
Projet : Prédiction de Réussite Étudiante
"""

import joblib
import pandas as pd
import numpy as np


class Modele:
    """
    Classe pour charger et utiliser les modèles ML
    
    Cette classe gère :
    - Le chargement des modèles sauvegardés
    - Les prédictions
    - Les probabilités
    """
    
    def __init__(self):
        """Initialise le Modèle"""
        self.modele_lr = None
        self.modele_rf = None
        self.modele_charge = False
        
    def charger_modele_lr(self, chemin="model_lr.pkl"):
        """
        Charge le modèle de régression linéaire
        
        Args:
            chemin (str): Chemin vers le fichier .pkl
            
        Returns:
            bool: True si chargé, False sinon
        """
        try:
            self.modele_lr = joblib.load(chemin)
            self.modele_charge = True
            return True
        except Exception as e:
            return False
    
    def predire_note(self, nb_actions, nb_connexions, nb_ressources):
        """
        Prédit la note d'un étudiant avec le modèle de régression
        
        Args:
            nb_actions (int): Nombre d'actions
            nb_connexions (int): Nombre de connexions
            nb_ressources (int): Nombre de ressources
            
        Returns:
            float: Note prédite (0-20)
        """
        if self.modele_lr is None:
            return None
        
        # Créer le DataFrame avec les features
        X = pd.DataFrame({
            'nb_actions': [nb_actions],
            'nb_connexions': [nb_connexions],
            'nb_ressources': [nb_ressources]
        })
        
        # Prédire
        note = self.modele_lr.predict(X)[0]
        
        # S'assurer que la note est entre 0 et 20
        note = max(0, min(20, note))
        
        return note
    
    def obtenir_coefficients(self):
        """
        Retourne les coefficients du modèle de régression
        
        Returns:
            dict: Dictionnaire avec les coefficients
        """
        if self.modele_lr is None:
            return None
        
        return {
            'nb_actions': self.modele_lr.coef_[0],
            'nb_connexions': self.modele_lr.coef_[1],
            'nb_ressources': self.modele_lr.coef_[2],
            'intercept': self.modele_lr.intercept_
        }
    
    def valider_inputs(self, nb_actions, nb_connexions, nb_ressources):
        """
        Valide les inputs de l'utilisateur
        
        Args:
            nb_actions (int): Nombre d'actions
            nb_connexions (int): Nombre de connexions
            nb_ressources (int): Nombre de ressources
            
        Returns:
            tuple: (is_valid, message_erreur)
        """
        # Vérifier que ce sont des nombres positifs
        if nb_actions < 0:
            return False, "Le nombre d'actions doit être positif"
        
        if nb_connexions < 0:
            return False, "Le nombre de connexions doit être positif"
        
        if nb_ressources < 0:
            return False, "Le nombre de ressources doit être positif"
        
        # Vérifier la cohérence
        if nb_connexions > nb_actions:
            return False, "Le nombre de connexions ne peut pas dépasser le nombre d'actions"
        
        if nb_ressources > nb_actions:
            return False, "Le nombre de ressources ne peut pas dépasser le nombre d'actions"
        
        return True, "OK"
