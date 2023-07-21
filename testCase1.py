import unittest
import json
from StockDownloader import StockDownloader

class TestStockDownloader(unittest.TestCase):
    def setUp(self):
        self.fngu_symbol = 'FNGU'
        self.fngd_symbol = 'FNGD'
        self.start_date = '2023-01-23'
        self.end_date = '2023-01-27'

    def test_download_stock_data(self):
        stock_downloader = StockDownloader(self.fngu_symbol, self.start_date, self.end_date)
        data = stock_downloader.download_stock_data()
        self.assertIsNotNone(data)
        self.assertEqual(data.shape[0], 4)  # Assuming there are 4 trading days in the specified date range


    def test_save_data_as_json(self):
        stock_downloader = StockDownloader(self.fngu_symbol, self.start_date, self.end_date)
        stock_downloader.download_stock_data()
        filename = 'test_fngu_data.json'
        stock_downloader.save_data_as_json(filename)

        with open(filename, 'r') as json_file:
            data_json = json_file.read()

        data = json.loads(data_json)
        self.assertIsNotNone(data)
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 4)  # Assuming there are 4 trading days in the specified date range

        # Clean up - delete the test JSON file
        import os
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
