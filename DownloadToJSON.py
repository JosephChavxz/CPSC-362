import yfinance as yf
import json

def download_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    return data

def print_stock_data(data, stock_symbol):
    for index, row in data.iterrows():
        date = index.strftime('%Y-%m-%d')
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        volume = row['Volume']
        print(stock_symbol + ' - ' + f"On {date}: " + f"Open: {open_price:.2f}, "
              + f"High: {high_price:.2f}, " + f"Low: {low_price:.2f}, "
              + f"Close: {close_price:.2f}, " + f"Volume: {volume}")

def save_data_as_json(data, filename):
    data_json = data.to_json(orient='table')
    with open(filename, 'w') as json_file:
        json_file.write(data_json)

# Prompt user to input a start date and end date
fngu_symbol = 'FNGU'
fngd_symbol = 'FNGD'
print('**** Please enter a start and end date to begin the stock data download ****\n')
start_date = input('Start date (yyyy-mm-dd): ')
end_date = input('End date (yyyy-mm-dd): ')
print()
stock_data1 = download_stock_data(fngu_symbol, start_date, end_date)
stock_data2 = download_stock_data(fngd_symbol, start_date, end_date)
print('Data successfully downloaded!\n')
print('Printing Downloaded Stock Data...')
print_stock_data(stock_data1, fngu_symbol)
print()
print_stock_data(stock_data2, fngd_symbol)
print()

filename1 = 'fngu_data.json'
filename2 = 'fngd_data.json'
save_data_as_json(stock_data1, filename1)
save_data_as_json(stock_data2, filename2)
print(f"Stock data saved as {filename1} and {filename2}")