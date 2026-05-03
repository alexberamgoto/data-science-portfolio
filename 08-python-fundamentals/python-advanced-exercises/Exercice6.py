import pandas as pd
df = pd.read_csv('cleaned_dataset.csv')
print(df['marque'].value_counts())
