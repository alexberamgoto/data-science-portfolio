import pandas as pd
df=pd.read_csv('cleaned_dataset.csv')
df_trie=df.sort_values(by=['prix'],ascending=False)
print(df_trie)