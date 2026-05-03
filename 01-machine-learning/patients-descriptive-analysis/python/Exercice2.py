import pandas as pd


prix = {'marque':['Toyota','Honda','BMW','Audi'],
      'prix' :[23000,17000,135000,71400]}

prix_df=pd.DataFrame.from_dict(prix)
puissance={'marque':['Toyota','Honda','BMW','Audi'],
           'cv':[141,80,182,160]}
puissance_df=pd.DataFrame.from_dict(puissance)

df=pd.merge(prix_df,puissance_df,on='marque')
print(df)