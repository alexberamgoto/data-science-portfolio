"""
databuilder.py
Classe pour le chargement et le nettoyage des données ARCHE
Projet : Prédiction de Réussite Étudiante
Auteur : Étudiant FC Data Science 2025-2026
"""

import pandas as pd
import numpy as np


class DataBuilder:
    """
    Classe pour construire et nettoyer les données
    
    Cette classe permet de :
    - Charger les fichiers CSV (logs et notes)
    - Nettoyer les données (valeurs manquantes, doublons)
    - Valider la structure des données
    """
    
    def __init__(self):
        """Initialise le DataBuilder"""
        self.logs = None
        self.notes = None
        self.logs_propres = None
        self.notes_propres = None
        
    def charger_donnees(self, chemin_logs, chemin_notes):
        """
        Charge les fichiers CSV
        
        Args:
            chemin_logs (str): Chemin vers logs.csv
            chemin_notes (str): Chemin vers notes.csv
            
        Returns:
            tuple: (logs, notes) DataFrames chargés
        """
        print("📁 Chargement des données...")
        
        try:
            # Charger les logs
            self.logs = pd.read_csv(chemin_logs)
            print(f"✅ Logs chargés : {len(self.logs)} lignes")
            
            # Charger les notes
            self.notes = pd.read_csv(chemin_notes)
            print(f"✅ Notes chargées : {len(self.notes)} étudiants")
            
            return self.logs, self.notes
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {e}")
            return None, None
    
    def nettoyer_logs(self):
        """
        Nettoie les données de logs
        
        Returns:
            DataFrame: Logs nettoyés
        """
        print("\n🧹 Nettoyage des logs...")
        
        if self.logs is None:
            print("❌ Aucune donnée à nettoyer")
            return None
        
        # Copie pour ne pas modifier l'original
        logs_propres = self.logs.copy()
        
        # 1. Détecter et convertir la colonne de date
        colonnes_date = ['heure', 'date', 'time', 'timestamp']
        colonne_trouvee = None
        
        for col in colonnes_date:
            if col in logs_propres.columns:
                colonne_trouvee = col
                break
        
        if colonne_trouvee:
            logs_propres[colonne_trouvee] = pd.to_datetime(
                logs_propres[colonne_trouvee], 
                errors='coerce'
            )
            print(f"✅ Colonne date convertie : {colonne_trouvee}")
        
        # 2. Supprimer les valeurs manquantes
        lignes_avant = len(logs_propres)
        logs_propres = logs_propres.dropna()
        lignes_apres = len(logs_propres)
        print(f"✅ Valeurs manquantes supprimées : {lignes_avant - lignes_apres} lignes")
        
        # 3. Supprimer les doublons
        doublons_avant = len(logs_propres)
        logs_propres = logs_propres.drop_duplicates()
        doublons_apres = len(logs_propres)
        print(f"✅ Doublons supprimés : {doublons_avant - doublons_apres} lignes")
        
        # 4. Convertir les types
        if 'pseudo' in logs_propres.columns:
            logs_propres['pseudo'] = logs_propres['pseudo'].astype(str)
        
        self.logs_propres = logs_propres
        print(f"✅ Logs nettoyés : {len(logs_propres)} lignes finales\n")
        
        return logs_propres
    
    def nettoyer_notes(self):
        """
        Nettoie les données de notes
        
        Returns:
            DataFrame: Notes nettoyées
        """
        print("🧹 Nettoyage des notes...")
        
        if self.notes is None:
            print("❌ Aucune donnée à nettoyer")
            return None
        
        # Copie pour ne pas modifier l'original
        notes_propres = self.notes.copy()
        
        # 1. Supprimer les valeurs manquantes
        lignes_avant = len(notes_propres)
        notes_propres = notes_propres.dropna()
        lignes_apres = len(notes_propres)
        print(f"✅ Valeurs manquantes supprimées : {lignes_avant - lignes_apres} lignes")
        
        # 2. Supprimer les doublons sur pseudo
        doublons_avant = len(notes_propres)
        notes_propres = notes_propres.drop_duplicates(subset=['pseudo'])
        doublons_apres = len(notes_propres)
        print(f"✅ Doublons supprimés : {doublons_avant - doublons_apres} lignes")
        
        # 3. Convertir les types
        notes_propres['pseudo'] = notes_propres['pseudo'].astype(str)
        notes_propres['note'] = pd.to_numeric(notes_propres['note'], errors='coerce')
        
        # 4. Valider les notes (entre 0 et 20)
        notes_invalides = notes_propres[
            (notes_propres['note'] < 0) | (notes_propres['note'] > 20)
        ]
        if len(notes_invalides) > 0:
            print(f"⚠️  {len(notes_invalides)} notes invalides détectées")
            notes_propres = notes_propres[
                (notes_propres['note'] >= 0) & (notes_propres['note'] <= 20)
            ]
        
        self.notes_propres = notes_propres
        print(f"✅ Notes nettoyées : {len(notes_propres)} étudiants finaux\n")
        
        return notes_propres
    
    def valider_colonnes(self):
        """
        Valide que toutes les colonnes nécessaires sont présentes
        
        Returns:
            bool: True si valide, False sinon
        """
        print("✔️  Validation de la structure...")
        
        # Colonnes requises pour les logs
        colonnes_logs_requises = ['pseudo', 'evenement', 'composant', 'contexte']
        
        # Colonnes requises pour les notes
        colonnes_notes_requises = ['pseudo', 'note']
        
        # Vérifier les logs
        if self.logs_propres is not None:
            manquantes_logs = [
                col for col in colonnes_logs_requises 
                if col not in self.logs_propres.columns
            ]
            
            if manquantes_logs:
                print(f"❌ Colonnes manquantes dans logs : {manquantes_logs}")
                return False
            else:
                print("✅ Structure logs valide")
        
        # Vérifier les notes
        if self.notes_propres is not None:
            manquantes_notes = [
                col for col in colonnes_notes_requises 
                if col not in self.notes_propres.columns
            ]
            
            if manquantes_notes:
                print(f"❌ Colonnes manquantes dans notes : {manquantes_notes}")
                return False
            else:
                print("✅ Structure notes valide")
        
        print("✅ Validation réussie !\n")
        return True
    
    def obtenir_statistiques(self):
        """
        Affiche des statistiques sur les données nettoyées
        
        Returns:
            dict: Dictionnaire avec les statistiques
        """
        stats = {}
        
        if self.logs_propres is not None:
            stats['nb_logs'] = len(self.logs_propres)
            stats['nb_etudiants_logs'] = self.logs_propres['pseudo'].nunique()
            stats['nb_actions_total'] = len(self.logs_propres)
        
        if self.notes_propres is not None:
            stats['nb_etudiants_notes'] = len(self.notes_propres)
            stats['note_moyenne'] = self.notes_propres['note'].mean()
            stats['note_min'] = self.notes_propres['note'].min()
            stats['note_max'] = self.notes_propres['note'].max()
        
        print("📊 STATISTIQUES DES DONNÉES")
        print("=" * 50)
        for cle, valeur in stats.items():
            if isinstance(valeur, float):
                print(f"{cle:30} : {valeur:.2f}")
            else:
                print(f"{cle:30} : {valeur}")
        print("=" * 50 + "\n")
        
        return stats
    
    def pipeline_complet(self, chemin_logs, chemin_notes):
        """
        Exécute le pipeline complet de nettoyage
        
        Args:
            chemin_logs (str): Chemin vers logs.csv
            chemin_notes (str): Chemin vers notes.csv
            
        Returns:
            tuple: (logs_propres, notes_propres)
        """
        print("\n" + "="*60)
        print("🚀 DÉMARRAGE DU PIPELINE DE NETTOYAGE")
        print("="*60 + "\n")
        
        # 1. Charger
        self.charger_donnees(chemin_logs, chemin_notes)
        
        # 2. Nettoyer
        if self.logs is not None:
            self.nettoyer_logs()
        
        if self.notes is not None:
            self.nettoyer_notes()
        
        # 3. Valider
        if self.valider_colonnes():
            # 4. Statistiques
            self.obtenir_statistiques()
            
            print("="*60)
            print("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
            print("="*60 + "\n")
            
            return self.logs_propres, self.notes_propres
        else:
            print("="*60)
            print("❌ PIPELINE ÉCHOUÉ - Données invalides")
            print("="*60 + "\n")
            return None, None


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer un DataBuilder
    builder = DataBuilder()
    
    # Exécuter le pipeline complet
    logs_propres, notes_propres = builder.pipeline_complet(
        "logs.csv",
        "notes.csv"
    )
    
    if logs_propres is not None and notes_propres is not None:
        print("✅ Données prêtes pour l'extraction de features !")
    else:
        print("❌ Erreur dans le nettoyage des données")
