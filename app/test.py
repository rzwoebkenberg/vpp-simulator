import pandas as pd

df = pd.read_csv('../bin/history.csv')

ders_list = df.der_name.unique()
print(ders_list)