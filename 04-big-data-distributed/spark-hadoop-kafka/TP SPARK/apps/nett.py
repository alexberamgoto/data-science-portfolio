from  sklearn.impute import simple_imputer
import nympy as np
import pandas as pd
data = pd.read_csv('logs_info_25_pseudo.csv')
cp = data.copy()
