import random
import os
import logging
import sys

class Lexique:

    def _init_(self, name_file=None):

        # Lexiquepardéfaut

        self._listes_mots = ['Sql', 'Algo', 'Heritage', 'python']

        # Si aucun fichier n'est donné → on utilise le lexique par défaut
        if name_file is None:
            print("Aucun fichier fourni → utilisation du lexique par défaut.")
            return

        # Si le fichier n'existe pas → lexique par défaut
        if not os.path.exists(name_file):
            print(f"Fichier introuvable : {name_file} → utilisation du lexique par défaut.")
            return

        # Sinon on charge le fichier
        try:
            with open(name_file, 'r', encoding='utf-8') as f:
                self._listes_mots = []  # on remplace complètement
                for line in f:
                    mot = line.strip().upper()
                    if mot:
                        self._listes_mots.append(mot)
            print(f"Lexique chargé depuis : {name_file}")

        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier {name_file} → utilisation du lexique par défaut.")
            logging.exception(e)

    def choisir(self):
        return random.choice(self._listes_mots)


class Jeux:
    def _init_(self, mot):
        self._mot = mot.upper()
        self._joue = set()

    def jouer(self,car):
        """
        mettre à jour le jeu

        """
        self._joue.add(car.upper())
        if car in self._mot:
            return True
        return False

    def nb_erreurs(self):
        nb = 0
        for car in self._joue:
            if not car in self._mot:
                nb += 1
        return nb

    def est_complet(self):
        for car in self._mot:
            if not car  in self._joue:
                return False
        return True



    def afficher(self):
        for car in self._mot:
            if car in self._joue:
                print(car,end="")
            else:
                print("_",end="")
        print()





if _name_ == '_main_':
    fichier = "Lexique"
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    lex = Lexique(fichier)
    mot_choisi = lex.choisir()
    print(mot_choisi)
    jeu = Jeux(mot=mot_choisi)
    print(jeu.nb_erreurs())
    gagne = False

    while jeu.nb_erreurs()<6:

        car = input("Choisissez un caractère: ")
        jeu.jouer(car)
        jeu.afficher()
        if jeu.est_complet():
            print("Bravo !")
            gagne = True
            break
        print("nb erreurs ",jeu.nb_erreurs())

    if not gagne:
        print("Perdu !")
        print("Le mot était",mot_choisi.upper())