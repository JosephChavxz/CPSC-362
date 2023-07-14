import unittest
#reset the path for this if not using on my laptop
from pythonProjects.stockProgram.getStockData import StockData

class testCase(unittest.TestCase):
    def test(self):
        obj = StockData("8")
        obj.retrieveData()
        print(obj)


        for key, value in obj.stockData.items():
            #if value == None:

            self.assertTrue(value, key + " expected float, but got None")
            print()

if __name__ == '__main__':
    unittest.main()