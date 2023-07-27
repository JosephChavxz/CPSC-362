import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read the JSON file
with open('FNGD_stock_data.json') as f:
    data = json.load(f)

# turn the dictionary into a DataFrame with dates as index
df = pd.DataFrame.from_dict(data, orient='index')

# convert index to datetime
df.index = pd.to_datetime(df.index)

# convert closing prices to float
df['close'] = df['close'].astype(float)

# plot the data
plt.figure(figsize=(10,6))
plt.scatter(df.index, df['close'])
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.ylim([0, 100])
start, end = plt.ylim()  
stepsize = 5.0  
plt.yticks(np.arange(start, end, stepsize))  # sp
plt.xticks(rotation = 45)
plt.title('Closing Stock Prices Over Time')
plt.show()
