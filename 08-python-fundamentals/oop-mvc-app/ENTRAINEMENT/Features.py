"""
Features.py
Classe pour extraire les features (caractéristiques) des données
Projet : Prédiction de Réussite Étudiante
Auteur : Étudiant FC Data Science 2025-2026
"""

import pandas as pd
import numpy as np


class Features:
    """
    Classe pour créer les features à partir des logs
    
    Cette classe calcule des indicateurs d'activité pour chaque étudiant :
    - Nombre d'actions
    - Nombre de connexions
    - Nombre de ressources consultées
    """
    
    def __init__(self, logs, notes):
        """
        Initialise la classe Features
        
        Args:
            logs (DataFrame): Données des logs nettoyées
            notes (DataFrame): Données des notes nettoyées
        """
        self.logs = logs.copy()
        self.notes = notes.copy()
        self.features = None
        self.donnees_completes = None
        
    def calculer_features_base(self):
        """
        Calcule les features de base pour chaque étudiant
        
        Returns:
            DataFrame: Features calculées
        """
        print("🔧 Calcul des features de base...")
        
        # Grouper par étudiant et calculer les indicateurs
        features = self.logs.groupby("pseudo").agg(
            nb_actions=("evenement", "count"),              # Nombre total d'actions
            nb_connexions=("composant", lambda x: (x == "login").sum()),  # Nombre de login
            nb_ressources=("contexte", "nunique")           # Nombre de ressources uniques
        ).reset_index()
        
        print(f"✅ Features calculées pour {len(features)} étudiants")
        print(f"   - nb_actions : Nombre total d'événements")
        print(f"   - nb_connexions : Nombre de connexions (login)")
        print(f"   - nb_ressources : Nombre de contextes différents\n")
        
        self.features = features
        return features
    
    def fusionner_avec_notes(self):
        """
        Fusionne les features avec les notes des étudiants
        
        Returns:
            DataFrame: Données complètes (features + notes)
        """
        print("🔗 Fusion des features avec les notes...")
        
        if self.features is None:
            print("❌ Aucune feature calculée. Appelez d'abord calculer_features_base()")
            return None
        
        # Fusionner features et notes sur 'pseudo'
        donnees_completes = pd.merge(
            self.features,
            self.notes,
            on="pseudo",
            how="inner"  # Garder seulement les étudiants présents dans les deux
        )
        
        # Créer la variable cible binaire (Réussite/Échec)
        donnees_completes['reussite'] = (donnees_completes['note'] >= 10).astype(int)
        
        print(f"✅ Fusion réussie : {len(donnees_completes)} étudiants")
        print(f"   - Réussite (note ≥ 10) : {(donnees_completes['reussite'] == 1).sum()}")
        print(f"   - Échec (note < 10) : {(donnees_completes['reussite'] == 0).sum()}\n")
        
        self.donnees_completes = donnees_completes
        return donnees_completes
    
    def afficher_statistiques(self):
        """
        Affiche les statistiques des features
        
        Returns:
            DataFrame: Statistiques descriptives
        """
        if self.donnees_completes is None:
            print("❌ Aucune donnée complète. Appelez fusionner_avec_notes()")
            return None
        
        print("📊 STATISTIQUES DES FEATURES")
        print("=" * 70)
        
        # Sélectionner les colonnes numériques (features + note)
        colonnes_features = [col for col in self.donnees_completes.columns 
                            if col not in ['pseudo', 'reussite']]
        
        stats = self.donnees_completes[colonnes_features].describe()
        print(stats.to_string())
        print("=" * 70 + "\n")
        
        return stats
    
    def afficher_correlations(self):
        """
        Affiche les corrélations entre les features et la note
        
        Returns:
            Series: Corrélations avec la note
        """
        if self.donnees_completes is None:
            print("❌ Aucune donnée complète")
            return None
        
        print("🔗 CORRÉLATIONS AVEC LA NOTE")
        print("=" * 50)
        
        # Calculer les corrélations
        colonnes_numeriques = self.donnees_completes.select_dtypes(
            include=[np.number]
        ).columns
        
        correlations = self.donnees_completes[colonnes_numeriques].corr()['note'].sort_values(
            ascending=False
        )
        
        for feature, corr in correlations.items():
            if feature != 'note':
                emoji = "📈" if corr > 0 else "📉"
                print(f"{emoji} {feature:25} : {corr:+.4f}")
        
        print("=" * 50 + "\n")
        
        return correlations
    
    def obtenir_X_y(self):
        """
        Prépare les données pour le machine learning
        
        Returns:
            tuple: (X, y) où X sont les features et y la note
        """
        if self.donnees_completes is None:
            print("❌ Aucune donnée complète")
            return None, None
        
        # Colonnes features de base
        colonnes = ['nb_actions', 'nb_connexions', 'nb_ressources']
        
        # Extraire X et y
        X = self.donnees_completes[colonnes]
        y = self.donnees_completes['note']
        
        print(f"📦 Données préparées pour le ML")
        print(f"   - X (features) : {X.shape}")
        print(f"   - y (notes) : {y.shape}")
        print(f"   - Features utilisées : {', '.join(colonnes)}\n")
        
        return X, y
    
    def pipeline_complet(self):
        """
        Exécute le pipeline complet d'extraction de features
        
        Returns:
            DataFrame: Données complètes prêtes pour le ML
        """
        print("\n" + "="*60)
        print("🚀 DÉMARRAGE DU PIPELINE D'EXTRACTION DE FEATURES")
        print("="*60 + "\n")
        
        # 1. Calculer features de base
        self.calculer_features_base()
        
        # 2. Fusionner avec les notes
        self.fusionner_avec_notes()
        
        # 3. Afficher statistiques
        if self.donnees_completes is not None:
            self.afficher_statistiques()
            self.afficher_correlations()
            
            print("="*60)
            print("✅ PIPELINE FEATURES TERMINÉ AVEC SUCCÈS")
            print("="*60 + "\n")
            
            return self.donnees_completes
        else:
            print("="*60)
            print("❌ PIPELINE FEATURES ÉCHOUÉ")
            print("="*60 + "\n")
            return None
    
    def sauvegarder_donnees(self, nom_fichier="data_features.csv"):
        """
        Sauvegarde les données complètes dans un fichier CSV
        
        Args:
            nom_fichier (str): Nom du fichier de sortie
        """
        if self.donnees_completes is None:
            print("❌ Aucune donnée à sauvegarder")
            return
        
        try:
            self.donnees_completes.to_csv(nom_fichier, index=False)
            print(f"💾 Données sauvegardées dans : {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")


# Exemple d'utilisation
if __name__ == "__main__":
    # Simuler des données pour tester
    print("📚 Test de la classe Features\n")
    
    # Données de test
    logs_test = pd.DataFrame({
        'pseudo': ['etud1', 'etud1', 'etud1', 'etud2', 'etud2'],
        'evenement': ['view', 'submit', 'download', 'view', 'submit'],
        'composant': ['login', 'quiz', 'resource', 'login', 'quiz'],
        'contexte': ['cours1', 'cours1', 'cours2', 'cours1', 'cours1']
    })
    
    notes_test = pd.DataFrame({
        'pseudo': ['etud1', 'etud2'],
        'note': [15.0, 8.0]
    })
    
    # Créer et exécuter le pipeline
    features = Features(logs_test, notes_test)
    donnees = features.pipeline_complet()
    
    if donnees is not None:
        print("✅ Test réussi !")
        print("\nAperçu des données :")
        print(donnees)
