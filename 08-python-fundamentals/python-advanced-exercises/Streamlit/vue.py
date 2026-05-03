# vue.py
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pandas import DataFrame

class Vue:

    @staticmethod
    def get_fig_deces(data: DataFrame) -> Figure:
        fig, ax = plt.subplots(figsize=(16, 9))

        ax.bar(data.index, data["incid_dc"], color="steelblue")
        ax.set_xlabel("Date")
        ax.set_ylabel("Nombre de décès")
        ax.set_title("Évolution des décès COVID-19")

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    