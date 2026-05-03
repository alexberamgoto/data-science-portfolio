import random

class Personne:
    emoticone  = ["😘", "😖", "😲", "😴","😃"]
    def __init__(self, nom, prenom):
        self.name = nom
        self.prenom = prenom

    def _choisir(self): # _ pour dire que c'est une fonction privée
        return random.choice(Personne.emoticone)

    def affiche(self):
        print(f'{self.name} et {self.prenom}  {self._choisir()}')


class Etudiant(Personne):
    def __init__(self, nom, prenom, diplome = 'Licence MIASHS'):
        super().__init__(nom, prenom)
        self.diplome = diplome
    def affiche(self):
        super().affiche()
        print(f'{self.diplome}')


if __name__ == '__main__':
    p = Personne('Alexis', 'Beramgoto')
    p.affiche()

    e = Etudiant('Alexis', 'Beramgoto')
    e.affiche()