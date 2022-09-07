import numpy as np
import pandas as pd

x = np.NAN
abba = ['hi', 5, 5.3, x, 'I love life']
for i in abba:
    if pd.isnull(i) == False:
        print(i)
    else:
        print(f'Value of i not found')