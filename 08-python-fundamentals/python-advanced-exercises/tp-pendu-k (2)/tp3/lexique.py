# -----------------------------------------------------------------------------
# Project      : tp3
# File         : lexique.py
# Author       : Narek Eloyan
# Email        : pro.narekeloyan@gmail.com
# Copyright    : © 2025 Narek Eloyan. All rights reserved.
# License      : MIT
# Created      : 04/12/2025 10:10
# Description  : 
# -----------------------------------------------------------------------------

"""
    Classe Lexique pour exploiter un fichier texte servant de lexique ou alors
    utiliser un dictionnaire en Python par défaut
"""

import logging
import random

class Lexique:
    def __init__(self, nom_fichier=None):
        '''
        Constructeur
        :param nom_fichier: nom du fichier contenant le lexique (optionnel)
        '''
        if nom_fichier is None:
            self._contenu= ['MAISON', 'TELEPHONE', 'TABLEAU', 'PYTHON', 'DICTIONNAIRE']
            return
        try:
            self._contenu = []
            with open(nom_fichier, 'r') as f:
                for ligne in f:
                    ligne = ligne.strip().upper()
                    self._contenu.append(ligne)
        except:
            logging.warning(f"Erreur lors de la lecture du fichier {nom_fichier}")
            self._contenu = ['MAISON', 'TELEPHONE', 'TABLEAU', 'PYTHON', 'DICTIONNAIRE']

    def choisir(self):
        '''
        Choisir au hasard un mot
        :return: str
        '''
        return random.choice(self._contenu)

    def _print(self):
        '''
        Afficher le contenu du lexique
        C'est une méthode privée !
        '''
        print(self._contenu)

if __name__ == '__main__':
    lex = Lexique()
