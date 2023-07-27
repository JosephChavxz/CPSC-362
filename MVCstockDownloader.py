import requests
import json

class StockDataModel:
    API_KEY = '1JA77LS8UJHMNV19'

    def __init__(self):
        self.symbol = None
        self.start_date = None
        self.end_date = None

    def set_data(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def download_stock_data(self):
        if not self.symbol or not self.start_date or not self.end_date:
            raise ValueError("Missing symbol, start date, or end date.")
        
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

    def load_data_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None


class StockDataView:
    def display_data(self, data):
        if data:
            print("Data:")
            for date, values in data.items():
                print(f"Date: {date}")
                print(f"Open: {values['open']}")
                print(f"High: {values['high']}")
                print(f"Low: {values['low']}")
                print(f"Close: {values['close']}")
                print(f"Volume: {values['volume']}")
                print("-" * 20)
        else:
            print("Data download failed.")

    def get_input(self, prompt):
        return input(prompt)

    def display_message(self, message):
        print(message)


class StockDataController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        symbol = self.view.get_input(f'Enter a ticker symbol (either FNGU or FNGD): ').upper()
        start_date = self.view.get_input(f'Enter a start date (YYYY-MM-DD): ')
        end_date = self.view.get_input(f'Enter an end date (YYYY-MM-DD): ')

        self.model.set_data(symbol, start_date, end_date)

        stock_data = self.model.download_stock_data()

        if stock_data:
            filename = f'{symbol}_stock_data.json'
            self.model.save_data_as_json(stock_data, filename)
            self.view.display_message(f"Data saved as {filename}\n")
        else:
            self.view.display_message("Data download failed.")

        loaded_data = self.model.load_data_from_json(f'{symbol}_stock_data.json')
        self.view.display_data(loaded_data)


if __name__ == "__main__":
    model = StockDataModel()
    view = StockDataView()
    controller = StockDataController(model, view)
    controller.run()
