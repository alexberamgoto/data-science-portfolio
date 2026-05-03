# -----------------------------------------------------------------------------
# Project      : tp3
# File         : fenetre.py
# Author       : Narek Eloyan
# Email        : pro.narekeloyan@gmail.com
# Copyright    : © 2025 Narek Eloyan. All rights reserved.
# License      : MIT
# Created      : 04/12/2025 10:20
# Description  : 
# -----------------------------------------------------------------------------

"""

"""
import tkinter as tk
import jeu
from lexique import Lexique
from etat import Etat
from clavier import Clavier


class Fenetre(tk.Tk):
    def __init__(self, nom_fichier = None):
        super().__init__()

        self.lex = Lexique(nom_fichier)
        self.jeu = jeu.Jeu(self.lex.choisir())

        self.etat = Etat(self)
        self.clavier = Clavier(self)

        self.geometry("500x300")
        self.etat.pack(expand = True, fill = tk.X)
        self.clavier.pack(expand = True, fill = tk.X)