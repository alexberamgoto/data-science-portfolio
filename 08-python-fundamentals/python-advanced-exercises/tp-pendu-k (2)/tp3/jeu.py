# -----------------------------------------------------------------------------
# Project      : tp3
# File         : jeu.py
# Author       : Narek Eloyan
# Email        : pro.narekeloyan@gmail.com
# Copyright    : © 2025 Narek Eloyan. All rights reserved.
# License      : MIT
# Created      : 04/12/2025 10:12
# Description  : 
# -----------------------------------------------------------------------------

# CLASSE JEU DU "PENDU"

class Jeu:
    def __init__(self, mot):
        self._mot = mot
        self._joue = set()

    def jouer(self, char):
        """
            Méthode qui met à jour le jeu lorsque le caractère Char a été joué
            :param char: caractère joué
            :return: vrai i char est dans le mot à deviner
        """

        # Correction : on compare en majuscules
        if char.upper() in self._mot.upper():
            trouve = True
        else:
            trouve = False

        self._joue.add(char.upper())
        return trouve

    def nb_erreurs(self):
        """
            Nombre d'erreurs
            :return: int
        """
        nb = 0
        for c in self._joue:
            # Correction : on vérifie si le caractère joué (majuscule)
            # est dans le mot (converti en majuscules)
            if not c in self._mot.upper():
                nb += 1
        return nb

    def est_complet(self):
        """
            Verifier si tous les caractères ont été joués
            :return: booléen
        """
        for c in self._mot:
            # Correction : on compare le caractère du mot (converti en majuscule)
            # avec les caractères joués
            if c.upper() not in self._joue:
                return False
        return True

    def afficher(self):
        """
            Afficher le jeu
        """
        for c in self._mot:
            # Correction : affichage si la version majuscule est dans les joués
            if c.upper() in self._joue:
                print(c, end = ' ')
            else:
                print('_', end = ' ')

        print()
        print(f'erreurs= {self.nb_erreurs()}')

    @property
    def mot(self):
        return self._mot


# Test unitaire
if __name__ == '__main__':
    jeu = Jeu('TOTO')
    jeu.afficher()
    jeu.jouer('t')