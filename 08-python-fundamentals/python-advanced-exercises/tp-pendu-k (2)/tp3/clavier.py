# -----------------------------------------------------------------------------
# Project      : tp3
# File         : clavier.py
# Author       : Narek Eloyan
# Email        : pro.narekeloyan@gmail.com
# Copyright    : © 2025 Narek Eloyan. All rights reserved.
# License      : MIT
# Created      : 04/12/2025 10:40
# Description  : 
# -----------------------------------------------------------------------------

"""
    Classe qui représente le clavier
"""

import tkinter as tk
from tkinter import messagebox as msg

class Clavier(tk.Frame):
    def __init__(self, fenetre):
        super().__init__(fenetre)
        self.fenetre = fenetre
        self.etat = fenetre.etat
        self.boutons = dict()
        self.jeu = fenetre.jeu
        self.initialiser()

    def initialiser(self):
        """réinitialiser le clavier"""

        # on supprime les boutons existants
        for btn in self.boutons:
            btn.destroy()
        self.boutons.clear()

        # créer les boutons
        alphabet = "AZERTYUIOPQSDFGHJKLMWXCVBN"
        ln, col = 0, 0

        for c in alphabet:
            btn = tk.Button(self, text=c, command=lambda car=c: self.selectionner(car))
            btn.grid(row=ln, column=col)
            self.boutons[c] = btn
            col += 1
            if col == 9:
                col = 0
                ln += 1

    def selectionner(self, char):
        """call-back des boutons"""
        self.jeu.jouer(char)
        #print(car)

        self.boutons[char]['state'] = tk.DISABLED
        self.boutons[char]['relief'] = 'sunken'
        self.boutons[char]['command'] = None

        self.etat.initialiser()

        if self.jeu.est_complet():
            msg.showinfo("Bravo", "C'est gagné !")
            self.fenetre.quit()
        elif self.jeu.nb_erreurs() >= 6:
            msg.showerror("Oups", f"Vous avez perdu ! le mot est : {self.jeu.mot}")
            self.fenetre.quit()
        else:
            pass
