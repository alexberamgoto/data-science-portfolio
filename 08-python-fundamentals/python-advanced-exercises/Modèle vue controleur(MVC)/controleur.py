import pandas as pd


class controleur:

def select_data_deces(data,departement='01',de=None):
    """..."""
    if a is None:
        a = datetime(2020,12,1)
    if de is None:
        de = a - timedelta(days=7)
    a= pd.to_datetime(a)
    de= pd.to_datetime(de)
    departement= str(departement).zfill(2) #le departement est sur 2 chiffres
    logging.info(f'Selection des données du departement  {departement} de{de}à {a}')
    res= data[(data.dep==departement)]