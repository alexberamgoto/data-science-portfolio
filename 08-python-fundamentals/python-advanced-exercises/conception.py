class jeu:

    def __init__(self,mot):
        self._mot=mot
        self._joue=set()
    def jouer(self,car):...
        if car in self._mot:
            trouve = True
        else:
            trouve = False
    def nb_erreurs(self):...
        nb=0
        for c in self._joue:
            if car in self._mot:
                nb+=1
        return
    def est_complet(self):...
    def afficher(self):...
        for c in self._mot:
            print(c,end)
if __name__=="__main__":...