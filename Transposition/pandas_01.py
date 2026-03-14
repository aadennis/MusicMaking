import pandas as pd

chord_file = 'transpose.csv'
x = pd.read_csv(chord_file)

sets = x.groupby('transposition')  

filtered = x[x['transposition'] == 'C-D']
print(filtered)

