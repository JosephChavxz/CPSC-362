import unittest
import datetime
import yfinance as yf
import pandas as pd
import json
from io import StringIO
from unittest.mock import patch
from DownloadToJSON import download_stock_data, print_stock_data, save_data_as_json

class StockDataTestCase(unittest.TestCase):
    def test_download_stock_data(self):
        # Set up test data
        symbol = 'FNGU'
        start_date = '2022-01-01'
        end_date = '2022-01-05'

        # Download stock data
        data = download_stock_data(symbol, start_date, end_date)

        # Verify data is of the correct type
        self.assertIsInstance(data, pd.DataFrame)

        # Verify data contains expected columns
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'Capital Gains']
        self.assertCountEqual(data.columns, expected_columns)

    def test_print_stock_data(self):
        # Set up test data
        data = pd.DataFrame({
            'Open': [100, 200, 300],
            'High': [110, 210, 310],
            'Low': [90, 190, 290],
            'Close': [105, 205, 305],
            'Volume': [1000, 2000, 3000]
        }, index=pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03']))
        stock_symbol = 'FNGU'

        # Redirect print output to a StringIO object
        output = StringIO()
        with patch('sys.stdout', new=output):
            # Print stock data
            print_stock_data(data, stock_symbol)

        # Get printed output
        printed_output = output.getvalue().strip()

        # Verify printed output contains expected information
        expected_output = """FNGU - On 2022-01-01: Open: 100.00, High: 110.00, Low: 90.00, Close: 105.00, Volume: 1000
FNGU - On 2022-01-02: Open: 200.00, High: 210.00, Low: 190.00, Close: 205.00, Volume: 2000
FNGU - On 2022-01-03: Open: 300.00, High: 310.00, Low: 290.00, Close: 305.00, Volume: 3000"""
        self.assertEqual(printed_output, expected_output)

    def test_save_data_as_json(self):
        # Set up test data
        data = pd.DataFrame({
            'Open': [100, 200, 300],
            'High': [110, 210, 310],
            'Low': [90, 190, 290],
            'Close': [105, 205, 305],
            'Volume': [1000, 2000, 3000]
        }, index=pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03']))
        filename = 'test_data.json'

        # Save data as JSON
        save_data_as_json(data, filename)

        # Read saved JSON file
        with open(filename, 'r') as json_file:
            saved_data_json = json.load(json_file)

        # Verify saved JSON contains expected data
        expected_data_json = {
            'schema': {
                'fields': [
                    {'name': 'index', 'type': 'datetime'},
                    {'name': 'Open', 'type': 'integer'},
                    {'name': 'High', 'type': 'integer'},
                    {'name': 'Low', 'type': 'integer'},
                    {'name': 'Close', 'type': 'integer'},
                    {'name': 'Volume', 'type': 'integer'}
                ],
                'primaryKey': ['index'],
                'pandas_version': '1.4.0'
            },
            'data': [
                {'index': '2022-01-01T00:00:00.000', 'Open': 100, 'High': 110, 'Low': 90, 'Close': 105, 'Volume': 1000},
                {'index': '2022-01-02T00:00:00.000', 'Open': 200, 'High': 210, 'Low': 190, 'Close': 205, 'Volume': 2000},
                {'index': '2022-01-03T00:00:00.000', 'Open': 300, 'High': 310, 'Low': 290, 'Close': 305, 'Volume': 3000}
            ]
        }
        self.assertEqual(saved_data_json, expected_data_json)

        # Clean up by deleting the test file
        import os
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
