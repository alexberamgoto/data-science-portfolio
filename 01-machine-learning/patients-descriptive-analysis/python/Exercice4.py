import pandas as pd
df=pd.read_csv('cleaned_dataset.csv')
print(df['prix'].max())
print(df[['marque','prix']])
selection = df[['marque','prix']] [df['prix']==df['prix'].max()]
print(selection)
print(f'la voiture la plus chère est:{selection.iloc[0,0]}'
      f'avec un prix de {selection.iloc[0, 1]}')
