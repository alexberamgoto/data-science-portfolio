import pandas as pd
df=pd.read_csv('cleaned_dataset.csv')
marques= df.groupby('marque')
print(type(marques))
toyota = marques.get_group('toyota')
print(toyota)