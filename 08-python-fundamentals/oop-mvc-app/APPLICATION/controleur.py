"""
controleur.py
Classe Contrôleur - Logique de l'application
Architecture MVC pour l'application Streamlit
Projet : Prédiction de Réussite Étudiante
"""

from modele import Modele
from vue import Vue


class Controleur:
    """
    Classe Contrôleur - Coordonne le Modèle et la Vue
    
    Cette classe gère :
    - La logique métier de l'application
    - La coordination entre Modèle et Vue
    - Le flux d'exécution de l'application
    """
    
    def __init__(self):
        """Initialise le Contrôleur"""
        self.modele = Modele()
        self.vue = Vue()
        self.modele_charge = False
    
    def initialiser_application(self):
        """
        Initialise l'application
        
        Returns:
            bool: True si l'initialisation réussit
        """
        # Charger le modèle
        if self.modele.charger_modele_lr("model_lr.pkl"):
            self.modele_charge = True
            return True
        else:
            return False
    
    def executer(self):
        """
        Exécute l'application principale
        
        Cette méthode orchestre tout le flux de l'application :
        1. Afficher l'interface
        2. Récupérer les inputs
        3. Valider les données
        4. Faire la prédiction
        5. Afficher les résultats
        """
        # Afficher la sidebar
        self.vue.afficher_sidebar()
        
        # Afficher l'en-tête
        self.vue.afficher_entete()
        
        # Vérifier si le modèle est chargé
        if not self.modele_charge:
            if not self.initialiser_application():
                self.vue.afficher_erreur("""
                **Modèle non trouvé !**
                
                Veuillez d'abord exécuter le notebook `main.ipynb` pour entraîner 
                et sauvegarder le modèle.
                
                Fichier requis : `model_lr.pkl`
                """)
                return
            else:
                self.vue.afficher_succes("Modèle chargé avec succès !")
        
        # Afficher la description
        self.vue.afficher_description()
        
        # Afficher le formulaire et récupérer les inputs
        nb_actions, nb_connexions, nb_ressources = self.vue.afficher_formulaire()
        
        # Valider les inputs
        valide, message = self.modele.valider_inputs(
            nb_actions, nb_connexions, nb_ressources
        )
        
        if not valide:
            self.vue.afficher_avertissement(message)
        
        # Afficher le bouton de prédiction
        if self.vue.afficher_bouton_prediction() and valide:
            # Faire la prédiction
            self.faire_prediction(nb_actions, nb_connexions, nb_ressources)
        
        # Afficher le footer
        self.vue.afficher_footer()
    
    def faire_prediction(self, nb_actions, nb_connexions, nb_ressources):
        """
        Effectue la prédiction et affiche les résultats
        
        Args:
            nb_actions (int): Nombre d'actions
            nb_connexions (int): Nombre de connexions
            nb_ressources (int): Nombre de ressources
        """
        # Prédire la note
        note_predite = self.modele.predire_note(
            nb_actions, nb_connexions, nb_ressources
        )
        
        if note_predite is None:
            self.vue.afficher_erreur("Erreur lors de la prédiction")
            return
        
        # Afficher les résultats
        self.vue.afficher_resultats(note_predite)
        
        # Afficher les coefficients
        coefficients = self.modele.obtenir_coefficients()
        if coefficients is not None:
            self.vue.afficher_coefficients(coefficients)
    
    def analyser_profil(self, nb_actions, nb_connexions, nb_ressources):
        """
        Analyse le profil d'un étudiant
        
        Args:
            nb_actions (int): Nombre d'actions
            nb_connexions (int): Nombre de connexions
            nb_ressources (int): Nombre de ressources
            
        Returns:
            dict: Analyse du profil
        """
        analyse = {
            'nb_actions': nb_actions,
            'nb_connexions': nb_connexions,
            'nb_ressources': nb_ressources
        }
        
        # Calculer des ratios
        if nb_actions > 0:
            analyse['ratio_connexions'] = nb_connexions / nb_actions
            analyse['ratio_ressources'] = nb_ressources / nb_actions
        else:
            analyse['ratio_connexions'] = 0
            analyse['ratio_ressources'] = 0
        
        # Évaluer le niveau d'activité
        if nb_actions >= 200:
            analyse['niveau_activite'] = "Très élevé"
        elif nb_actions >= 100:
            analyse['niveau_activite'] = "Élevé"
        elif nb_actions >= 50:
            analyse['niveau_activite'] = "Moyen"
        else:
            analyse['niveau_activite'] = "Faible"
        
        # Évaluer la régularité (connexions)
        if nb_connexions >= 20:
            analyse['regularite'] = "Excellente"
        elif nb_connexions >= 10:
            analyse['regularite'] = "Bonne"
        elif nb_connexions >= 5:
            analyse['regularite'] = "Moyenne"
        else:
            analyse['regularite'] = "Faible"
        
        # Évaluer la diversité (ressources)
        if nb_ressources >= 10:
            analyse['diversite'] = "Très bonne"
        elif nb_ressources >= 5:
            analyse['diversite'] = "Bonne"
        elif nb_ressources >= 3:
            analyse['diversite'] = "Moyenne"
        else:
            analyse['diversite'] = "Faible"
        
        return analyse
    
    def generer_recommandations(self, note_predite, analyse):
        """
        Génère des recommandations personnalisées
        
        Args:
            note_predite (float): Note prédite
            analyse (dict): Analyse du profil
            
        Returns:
            list: Liste de recommandations
        """
        recommandations = []
        
        # Recommandations basées sur la note
        if note_predite < 10:
            recommandations.append("⚠️ Risque d'échec : Augmenter significativement l'activité")
        
        # Recommandations basées sur les actions
        if analyse['niveau_activite'] == "Faible":
            recommandations.append("📊 Augmenter le nombre d'actions sur la plateforme")
        
        # Recommandations basées sur les connexions
        if analyse['regularite'] == "Faible":
            recommandations.append("🔑 Se connecter plus régulièrement (objectif : 2-3 fois par semaine)")
        
        # Recommandations basées sur les ressources
        if analyse['diversite'] == "Faible":
            recommandations.append("📚 Explorer plus de ressources pédagogiques variées")
        
        # Recommandations positives
        if note_predite >= 16:
            recommandations.append("🌟 Excellent travail ! Continuer sur cette lancée")
        
        if not recommandations:
            recommandations.append("✅ Bon profil, continuer ainsi")
        
        return recommandations


# Point d'entrée de l'application
if __name__ == "__main__":
    # Créer le contrôleur
    controleur = Controleur()
    
    # Exécuter l'application
    controleur.executer()
