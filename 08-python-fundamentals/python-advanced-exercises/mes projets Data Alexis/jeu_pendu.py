import random

mots = ['Algo', 'Heritage', 'data', 'Sql']
mot_choisi = random.choice(mots)
print(mot_choisi)

class Lexique:
    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

lex = Lexique("mot", mot_choisi)
print(lex.nom, ":", lex.valeur)
