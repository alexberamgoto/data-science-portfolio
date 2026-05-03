##calculer la moyenne par constructeur

import pandas as pd
df=pd.read_csv('cleaned_dataset.csv')
kilometrage =df.groupby('marque')['kilometrage'].mean()
print(kilometrage)
print(type(kilometrage))