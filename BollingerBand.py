import json
import pandas as pd
import numpy as np

# Load data from json file
with open('FNGD_stock_data.json', 'r') as f:
    data = json.load(f)

# Convert the data to pandas DataFrame
df = pd.DataFrame(data).T
df.index = pd.to_datetime(df.index)
df = df.sort_index(ascending=True)

# Convert the 'close' column to numeric type
df['close'] = pd.to_numeric(df['close'])

# Calculate the 5-day moving average
df['5_day_ma'] = df['close'].rolling(window=5).mean()

# Calculate the standard deviation for Bollinger Bands
df['std'] = df['close'].rolling(window=5).std()

# Calculate upper and lower Bollinger Bands
df['upper_band'] = df['5_day_ma'] + 2 * df['std']
df['lower_band'] = df['5_day_ma'] - 2 * df['std']

# Create an 'order' column to record the "buy" and "sell" signals based on Bollinger Band Bounce strategy
df['order'] = 'N/A'
# If the closing price crosses above the upper Bollinger Band, set order as 'sell'
df.loc[df['close'] > df['upper_band'], 'order'] = 'sell'
# If the closing price crosses below the lower Bollinger Band, set order as 'buy'
df.loc[df['close'] < df['lower_band'], 'order'] = 'buy'

# print the DataFrame
print(df.to_string())
