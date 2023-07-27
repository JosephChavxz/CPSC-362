import requests
import json

class StockData:

    API_KEY = '1JA77LS8UJHMNV19'

    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def download_stock_data(self):
        base_url = 'https://www.alphavantage.co/query'
        url_params = {
            'function': 'TIME_SERIES_DAILY',
            'outputsize': 'full',
            'symbol': self.symbol,
            'apikey': self.API_KEY
        }

        response = requests.get(base_url, params=url_params)
        if response.status_code == 200:
            data = response.json()
            daily_prices = data['Time Series (Daily)']

            filtered_data = {}
            for date, values in daily_prices.items():
                if self.start_date <= date <= self.end_date:
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

    def save_data_as_json(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def print_json_data(self, filename):
        try:
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

if __name__ == "__main__":
    symbol = input(f'Enter a ticker symbol (either FNGU or FNGD): ').upper()
    start_date = input(f'Enter a start date (YYYY-MM-DD): ')
    end_date = input(f'Enter an end date (YYYY-MM-DD): ')

    stock = StockData(symbol, start_date, end_date)

    stock_data = stock.download_stock_data()

    if stock_data:
        filename = f'{symbol}_stock_data.json'
        stock.save_data_as_json(stock_data, filename)
        print(f"Data saved as {filename}\n")
    else:
        print("Data download failed.")

    stock.print_json_data(f'{symbol}_stock_data.json')
