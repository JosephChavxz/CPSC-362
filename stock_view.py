class StockView:
    def print_stock_data(self, symbol, data):
        if data is None:
            print(f"No data available for {symbol}. Please download the data first using 'download_stock_data' method.")
            return

        for index, row in data.iterrows():
            date = index.strftime('%Y-%m-%d')
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            volume = row['Volume']
            print(
                f"{symbol} - On {date}: Open: {open_price:.2f}, High: {high_price:.2f}, Low: {low_price:.2f}, Close: {close_price:.2f}, Volume: {volume}")
