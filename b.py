import pandas as pd

a = pd.DataFrame([["x", 'y']],
                       columns=['x', 'y'])
a.to_csv('data.csv', mode='a', index=False, header=False)