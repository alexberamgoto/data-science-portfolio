import tkinter as tk

from charset_normalizer.cd import alphabet_languages

root = tk.Tk()
root.title("Certification IDMC")

label = tk.Label(root, text="Bonjour Yassin, c'est Alexis")
label.pack()
class Clavier(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.etat=root.etat
        self.boutons= dict()
        self.jeu =root.jeu
        self.initialiser()
    def initialiser(self):
        alphabet= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ln,col=0,0
        for char in alphabet:
            btn=tk.Button(self.root, text=char, command=lambda c=char:self.fonction(c))
            btn.grid(row=ln,column=col)
            self.boutons[char]=btn
            col+=1
            if col==9:
                col=0
                ln+=1

root.mainloop()
