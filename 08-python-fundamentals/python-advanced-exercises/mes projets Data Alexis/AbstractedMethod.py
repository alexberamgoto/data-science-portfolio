import random
from abc import ABC, abstractmethod


class Personne(ABC):
    """Classe de base pour représenter une personne."""

    def _init_(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom

    @abstractmethod
    def afficher(self):
        pass


# --- CLASSE 1 : Etudiant ---
class Etudiant(Personne):
    """Représente un étudiant. Hérite de Personne."""

    def _init_(self, nom, prenom, diplome):
        # Initialise nom et prenom via la classe Personne
        super()._init_(nom, prenom)
        # Ajoute l'attribut spécifique 'diplome'
        self.diplome = diplome

    def afficher(self):
        """Affiche les informations spécifiques à l'étudiant."""
        print(f"Étudiant - Nom: {self.nom}, Prénom: {self.prenom}, Diplôme: {self.diplome}")


# --- CLASSE 2 : Enseignant ---
class Enseignant(Personne):
    """Représente un enseignant. Hérite de Personne."""

    def _init_(self, nom, prenom, titre):
        # Initialise nom et prenom via la classe Personne
        super()._init_(nom, prenom)
        # Ajoute l'attribut spécifique 'titre'
        self.titre = titre

    def afficher(self):
        """Affiche les informations spécifiques à l'enseignant."""
        print(f"Enseignant - Nom: {self.nom}, Prénom: {self.prenom}, Titre: {self.titre}")


# --- BLOC DE TEST ET D'EXÉCUTION ---
if __name__== '_main_':
    print("--- Test de la classe Etudiant ---")
    etudiant1 = Etudiant("Dubois", "Léa", "Licence Informatique")
    etudiant1.afficher()

    print("--- Test de la classe Enseignant ---")
    enseignant1 = Enseignant("Dupont", "Marc", "Professeur Agrégé")
    enseignant1.afficher()