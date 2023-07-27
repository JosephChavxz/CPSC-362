import requests
import json

API_KEY = '1JA77LS8UJHMNV19'

# fnction to download stock data from Alpha Vantage API
def download_stock_data(symbol, start_date, end_date):
    base_url = 'https://www.alphavantage.co/query'
    url_params = {
        'function': 'TIME_SERIES_DAILY',
        'outputsize': 'full',
        'symbol': symbol,
        'apikey': API_KEY
    }

    response = requests.get(base_url, params=url_params)
    if response.status_code == 200:
        data = response.json()
        daily_prices = data['Time Series (Daily)']

        filtered_data = {}
        for date, values in daily_prices.items():
            if start_date <= date <= end_date:
                filtered_data[date] = {
                    'open': values['1. open'],
                    'high': values['2. high'],
                    'low': values['3. low'],
                    'close': values['4. close'],
                    'volume': values['5. volume']
                }

        return filtered_data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# function to save data as JSON
def save_data_as_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

# function to print data from JSON file
def print_json_data(filename):
    try:
        # open JSON file
        with open(filename, 'r') as file:
            data = json.load(file)

        print("Data from JSON file:")
        for date, values in data.items():
            print(f"Date: {date}")
            print(f"Open: {values['open']}")
            print(f"High: {values['high']}")
            print(f"Low: {values['low']}")
            print(f"Close: {values['close']}")
            print(f"Volume: {values['volume']}")
            print("-" * 20)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON data in '{filename}'.")

# main function to run the program from the command line 
if __name__ == "__main__":
    symbol = input(f'Enter a ticker symbol (either FNGU or FNGD): ').upper()
    start_date = input(f'Enter a start date (YYYY-MM-DD): ')
    end_date = input(f'Enter an end date (YYYY-MM-DD): ')

    # download stock data
    stock_data = download_stock_data(symbol, start_date, end_date)

    if stock_data:
        filename = f'{symbol}_stock_data.json'
        save_data_as_json(stock_data, filename)
        print(f"Data saved as {filename}\n")
    else:
        print("Data download failed.")

    print_json_data(f'{symbol}_stock_data.json')