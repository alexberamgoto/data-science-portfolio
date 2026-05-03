from e1 import Personne
class_Etudiant(Personne):
def __init__(self, nom, prenom, diplome="Licence MIASHS"):
super ().__init__(nom, prenom)
self. diplome = diplome
def afficher (self):
super (). afficher()
print(f"Diplôme : {self. diplome}")
if __name__=='-main':
e = Etudiant ("Alexis", "Djekounmian"
,"Data Science")
e.afficher ()
e2 = Etudiant ("Alexis", "Djekounmian")
e2.afficher()