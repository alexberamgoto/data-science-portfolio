#####Voici tous les extraits de code de votre document, classés par page.J'ai corrigé les petites erreurs de formatage (lignes coupées, listes d'emojis) du PDF pour que le code soit directement utilisable.

### Page 6

python

class Personne:
    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom

    def afficher(self):
        print(f"Nom: {self.nom}")
        print(f"Prénom : {self.prenom}")


if __name__ == '__main__':
    p = Personne("Roussanaly", "Azim")
    p.afficher()

-----

### Page 9

python
from e1 import Personne


class Etudiant(Personne):
    def __init__(self, nom, prenom, diplome="Licence MIASHS"):
        super().__init__(nom, prenom)
        self.diplome = diplome

    def afficher(self):
        super().afficher()
        print(f"Diplôme : {self.diplome}")


if __name__ == '__main__':
    # Note : j'ai ajouté la virgule manquante entre "Azim" et "Master Informatique"
    e = Etudiant("Roussanaly", "Azim", "Master Informatique")
    e.afficher()

    e2 = Etudiant("Tabbone", "Antoine")
    e2.afficher()

-----

### Page 12

python
import random


class Personne:
    # Liste d'emojis (reconstituée à partir du document)
    emoticones = ["🐍", "💻", "🎓", "🚀", "🤖", "📚", "✨"]

    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom

    def _choisir(self):
        return random.choice(Personne.emoticones)

    def afficher(self):
        emoticone = self._choisir()
        print(f"{emoticone} {self.prenom} {self.nom}")


-----

### Page 15

###python
from abc import ABC, abstractmethod


class Personne(ABC):
    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom

    @abstractmethod
    def afficher(self):
        pass


-----

### Page 16

(Note : j'ai corrigé les sauts de ligne au milieu des print)

python


class Etudiant(Personne):
    def __init__(self, nom, prenom, diplome):
        super().__init__(nom, prenom)
        self.diplome = diplome

    def afficher(self):
        print(f"Étudiant - Nom: {self.nom}, Prénom: {self.prenom}, Diplôme: {self.diplome}")


class Enseignant(Personne):
    def __init__(self, nom, prenom, titre):
        super().__init__(nom, prenom)
        self.titre = titre

    def afficher(self):
        print(f"Enseignant - Nom: {self.nom}, Prénom: {self.prenom}, Titre: {self.titre}")


-----

### Page 17

python
if __name__ == '__main__':
    e = Etudiant("Roussanaly", "Azim", "Master Informatique")
    e.afficher()

    ens = Enseignant("Tabbone", "Antoine", "Professeur")
    ens.afficher()

    # erreur car Personne est abstraite
    # p = Personne("Bou Saleh", "Mira")
    # p.afficher()

-----

### Page 20

##(Note : j'ai corrigé le saut de ligne à self.__prenom)

###python


class Personne:
    def __init__(self, nom, prenom):
        self.__nom = nom  # attribut privé
        self.__prenom = prenom  # attribut privé

    def afficher(self):
        print(f"Nom: {self.__nom}, Prénom: {self.__prenom}")


-----

### Page 21

##python
if __name__ == '__main__':
    p = Personne("Roussanaly", "Azim")
    p.afficher()
    print(p)

    p.nom = "Tabbone"
    p.prenom = "Antoine"
    p.afficher()
    print(p)

    try:
        p.nom = 123  # Devrait lever une exception
    except TypeError as e:
        print(e)

    try:
        p.prenom = None  # Devrait lever une exception
    except TypeError as e:
        print(e)

-----

### Page 22

(Ce code est la suite de la classe Personne des pages précédentes, il définit les "properties")

python


@property
def nom(self):
    return self.__nom


@property
def prenom(self):
    return self.__prenom


@nom.setter
def nom(self, valeur):
    if isinstance(valeur, str):
        self.__nom = valeur
    else:
        raise TypeError("Le nom doit être une str")


@prenom.setter
def prenom(self, valeur):
    if isinstance(valeur, str):
        self.__prenom = valeur
    else:
        raise TypeError("Le prénom doit être une str")


-----

### Page 23

(Ceci est aussi une méthode à ajouter à la classe Personne)

python


def __str__(self):
    return f"Personne: {self.__prenom} {self.__nom}"
