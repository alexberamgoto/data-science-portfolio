from model import Model
from controller import Controller
from view import View
from datetime import datetime

if __name__ == "__main__":
    model = Model('./data/big.csv')
    df = Controller.select_data(model.data,
                           department = '75',
                           start=datetime(2020, 3, 19),
                           end=datetime(2023, 1, 26),)
    view = View(output_name='./output/barchart.png')
    view.print_data(df)

    var = 2022 / 03 / 23

    2022 / 12 / 31