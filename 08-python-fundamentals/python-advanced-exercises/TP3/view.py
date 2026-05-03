import pandas as pd
import matplotlib.pyplot as plt


class View:
    def __init__(self, output_name:str):
        super().__init__()
        self.output_name = output_name

    def print_data(self, data:pd.DataFrame):
        plt.bar(data['jour'], data['incid_dc'])
        plt.xticks(rotation=45)n
        plt.savefig(self.output_name)
        plt.show()

    @staticmethod
    def get_figure(data:pd.DataFrame):
        fig = plt.figure(figsize=(20, 10))
        plt.bar(data['jour'], data['incid_dc'])
        plt.title("Evolution des décès COVID-19")
        plt.xlabel("jour")
        plt.ylabel("nombre de décès")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

