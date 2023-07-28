import json
import pandas as pd
import numpy as np

def calculate_moving_average_signals(filename):
    # Load data from json file
    with open(filename, 'r') as f:
        data = json.load(f)

    # Convert the data to pandas DataFrame
    df = pd.DataFrame(data).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)

    # Convert the 'close' column to numeric type
    df['close'] = pd.to_numeric(df['close'])

    # Calculate the 5-day moving average
    df['5_day_ma'] = df['close'].rolling(window=5).mean()

    # Calculate the 10-day moving average
    df['10_day_ma'] = df['close'].rolling(window=10).mean()

    # Create an 'order' column to record the "buy" and "sell" signals
    df['order'] = 'N/A'
    # If the 5-day moving average is larger than the 10-day moving average, set order as 'buy'
    df.loc[df['5_day_ma'] > df['10_day_ma'], 'order'] = 'buy'
    # If the 5-day moving average is less than the 10-day moving average, set order as 'sell'
    df.loc[df['5_day_ma'] < df['10_day_ma'], 'order'] = 'sell'

    # print the DataFrame
    print(df.to_string())

