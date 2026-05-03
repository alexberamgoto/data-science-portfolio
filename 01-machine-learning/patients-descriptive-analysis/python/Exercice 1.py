import pandas as pd
df=pd.read_csv('dataset.csv', sep=';')
print('Les 5 prémieres lignes du dataset')
print(df.head(5))
print('Les 5 dernieres lignes du dataset')
print(df.tail(5))
print(df.info())


