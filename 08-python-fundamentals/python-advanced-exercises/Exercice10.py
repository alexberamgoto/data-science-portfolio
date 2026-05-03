import pandas as pd
allemandes={'marque':['Ford','Mercedes','BMW', 'Audi'],
            'prix':[23845,171995,135925,71400]}
adf= pd.DataFrame(allemandes)
japonaises ={'marque':['Toyota','Honda','Nissan','Mitsubishi'],
             'prix':[29995,23600,61500,58900]}
jdf= pd.DataFrame(japonaises)
df = pd.concat([adf, jdf]).reset_index(drop=True)
print(df)