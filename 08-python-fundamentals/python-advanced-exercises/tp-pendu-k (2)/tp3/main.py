# MAIN.PY
from lexique import Lexique
from jeu import Jeu
from fenetre import Fenetre
import sys

fichier = 'lexique.txt'

if len(sys.argv) > 1:
    fichier = sys.argv[1]

lex = Lexique(fichier)
jeu = Jeu(mot = lex.choisir())

gagne = False

while jeu.nb_erreurs() < 6:
    char = input("Choisissez un caractère: ")

    jeu.jouer(char)
    jeu.afficher()

    if jeu.est_complet():
        print('Bravo !')
        gagne = True
        break

if not gagne:
    print("Perdu !")
    print(f"Le mot était: {jeu.mot}")

# Test unitaire
if __name__ == '__main__':
    """
        Test unitaire du jeu du pendu basique
    """
    # jeu = Jeu('T0T0')
    # jeu.afficher()
    # jeu.jouer('t')
    # jeu.afficher()
    # print(jeu.nb_erreurs())
    # jeu.jouer('a')
    # print(jeu.nb_erreurs())
    # jeu.afficher()
    # print(jeu.nb_erreurs())
    # jeu.jouer('t')
    # jeu.afficher()
    # print(jeu.nb_erreurs())
    # jeu.jouer('i')
    # print(jeu.nb_erreurs())
    # jeu.jouer('0')
    # print(jeu.nb_erreurs())
    # jeu. afficher()

    """
        Test unitaire du jeu avec Tkinter
    """
    root = Fenetre("lexique.txt")
    root.mainloop()