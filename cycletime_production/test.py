# data = [False, True, True]
# print(sum(data))
# # True

import pandas as pd

df = pd.DataFrame()
x = [1,2,2,2,3,4,5,5,5,6,6,7,7,2]
df['x'] = x

print(df['x'].quantile([0.00, 1]))

# print(x.quantile