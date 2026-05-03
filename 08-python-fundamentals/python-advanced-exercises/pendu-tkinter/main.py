from lexique import Lexique
from jeu import jeu
from fenetre import Fenetre
import sys



fichier= 'lexique.txt'


if len(sys.argv)>1:
    fichier=sys.argv[1]


    lex=Lexique(fichier)
    jeu=jeu.jeu(mot= lex.choisir())
    gagne=False
    while jeu.nb_erreurs()>6:
        char=input("Choissez un caractère:")
        jeu.jouer(char)
        jeu.afficher ()
        if jeu.est_complet():
            print('Bravo!')
            gagne=True
            break
    if not gagne:
        print('Perdu!')
        print(f"Le mot était:{jeu.mot}")

#test unitaire

if __name__ == "__main__":
    # tests unitaires ici
    # jeu = jeu('TOTO')
    # jeu.afficher()
    ...
    root = Fenetre("lexique.txt")
    root.mainloop()



