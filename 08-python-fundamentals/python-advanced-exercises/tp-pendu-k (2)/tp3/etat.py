# -----------------------------------------------------------------------------
# Project      : tp3
# File         : etat.py
# Author       : Narek Eloyan
# Email        : pro.narekeloyan@gmail.com
# Copyright    : © 2025 Narek Eloyan. All rights reserved.
# License      : MIT
# Created      : 04/12/2025 10:21
# Description  : 
# -----------------------------------------------------------------------------

"""
    Classe qui représente l'affichage de l'état du jeu
"""

import tkinter as tk
class Etat(tk.Frame):
    def __init__(self, fenetre):
        super().__init__(fenetre, background="yellow")

        self.jeu = fenetre.jeu
        self.labels = list()
        self.initialiser = self.mettre_a_jour

    def mettre_a_jour (self):
        """
            Afficher le jeu
        """
        # on supprime les labels existants
        for lbl in self.labels:
            lbl. destroy()
        self.labels.clear()

        # créer les labels
        for c in self.jeu.mot:
            if c.upper() not in self.jeu._joue:
                lbl = tk. Label(self, text="_", borderwidth=1, relief="solid", padx=5, pady=5)
            else:
                lbl = tk. Label(self, text=c, borderwidth=1, relief="solid", padx=5, pady=5)

            lbl.pack(side="left", padx=2, pady=2)
            self.labels.append(lbl)