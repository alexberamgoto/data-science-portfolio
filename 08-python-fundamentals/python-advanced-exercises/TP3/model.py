import pandas as pd
import traceback


class Model:
    def __init__(self, filename: str = None)->None:
        self._data = Model.load(filename)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @staticmethod
    def load(filename: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(filename, sep=';', usecols=['dep', 'jour', 'incid_dc'])
            df['jour'] = pd.to_datetime(df['jour'], errors='coerce')
            df = df.dropna()
            return df
        except Exception:
            traceback.print_exc()
            return pd.DataFrame()


if __name__ == '__main__':
    model = Model()
    print()
    model = Model('./data/big.csv')
    data = model.data
    print(data.head())
    print(data.info())
    print(data.describe())




