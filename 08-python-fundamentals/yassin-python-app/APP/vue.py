import matplotlib.pyplot as plt

class Vue:

    @staticmethod
    def methodeA(counts):
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values)
        ax.set_xlabel("Résultat")
        ax.set_ylabel("Nombre d'étudiants")
        ax.set_title("Réussite / Échec")
        return fig
