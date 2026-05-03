import pandas as pd
from datetime import datetime, timedelta


class Controller:

    def __init__(self):
        super().__init__()

    @staticmethod
    def select_data(data: pd.DataFrame, department:str = '01',
                    start:datetime|None = None, end:datetime|None = None) -> pd.DataFrame:
        max_date = data['jour'].max()
        if end is None:
            end = max_date
        else:
            end = pd.to_datetime(end)
        if start is None:
            start = end - timedelta(days=7)
        else:
            start = pd.to_datetime(start)
            #if start > end:
            #    raise ValueError(f"Start date must be smaller than {end}")

        print(f"Selecting data from {start} to {end} in department {department}")
        df = data.loc[(data['jour'] >= start) & (data['jour'] <= end) & \
                      (data['dep'] == department), :]
        df = df.sort_values(by=['jour'])
        return df


if __name__ == '__main__':
    from model import Model
    model =  Model('./data/big.csv')
    df = Controller.select_data(model.data, start=datetime(2020, 3, 19), end=datetime(2021, 3, 20))
    print(df.sample(10))
    df = Controller.select_data(model.data)
    print(df.sample(min(10, df.shape[0])))
