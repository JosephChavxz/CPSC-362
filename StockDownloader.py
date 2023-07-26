import yfinance as yf

class StockDownloader:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def download_stock_data(self):
        stock = yf.Ticker(self.symbol)
        self.data = stock.history(start=self.start_date, end=self.end_date)
        return self.data

    def print_stock_data(self):
        if self.data is None:
            print("No data available. Please download the data first using 'download_stock_data' method.")
            return

        for index, row in self.data.iterrows():
            date = index.strftime('%Y-%m-%d')
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            volume = row['Volume']
            print(
                f"{self.symbol} - On {date}: Open: {open_price:.2f}, High: {high_price:.2f}, Low: {low_price:.2f}, Close: {close_price:.2f}, Volume: {volume}")

    def save_data_as_json(self, filename):
        if self.data is None:
            print("No data available. Please download the data first using 'download_stock_data' method.")
            return

        data_json = self.data.to_json(orient='table')
        with open(filename, 'w') as json_file:
            json_file.write(data_json)


if __name__ == "__main__":
    # Prompt user to input a start date and end date
    fngu_symbol = 'FNGU'
    fngd_symbol = 'FNGD'
    print('**** Please enter a start and end date to begin the stock data download ****\n')
    start_date = input('Start date (yyyy-mm-dd): ')
    end_date = input('End date (yyyy-mm-dd): ')
    print()

    stock_downloader1 = StockDownloader(fngu_symbol, start_date, end_date)
    stock_data1 = stock_downloader1.download_stock_data()

    stock_downloader2 = StockDownloader(fngd_symbol, start_date, end_date)
    stock_data2 = stock_downloader2.download_stock_data()

    print('Data successfully downloaded!\n')
    print('Printing Downloaded Stock Data...')
    stock_downloader1.print_stock_data()
    print()
    stock_downloader2.print_stock_data()
    print()

    filename1 = 'fngu_data.json'
    filename2 = 'fngd_data.json'
    stock_downloader1.save_data_as_json(filename1)
    stock_downloader2.save_data_as_json(filename2)
    print(f"Stock data saved as {filename1} and {filename2}")

