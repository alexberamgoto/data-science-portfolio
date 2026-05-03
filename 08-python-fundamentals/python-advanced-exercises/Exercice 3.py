##Nettoyer
import pandas as pd
df = pd.read_csv('dataset.csv',delimiter=';', na_values={'prix':'?'})
print(df)
df.to_csv('cleaned_dataset.csv',index=False)
