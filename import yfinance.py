import yfinance
import yahoo_fin.stock_info as stockInfo


class StockData:
    def __init__(self, symbol: str = None):
        """
        :param symbol:
        """
        self.stockSymbol = None
        self.stockData = {"Opening Price": None, "Closing Price": None, "PE_ratio": None,
                          "PS_ratio": None, "Company_Cash_Reserve": None, "Company_Debt": None,
                          "bid": None, "volume": "", "ask": None}

        if symbol:
            self.set_symbol(symbol)
            self.retrieveData()

    def __str__(self):
        output = ""
        for key, value in self.stockData.items():
            output += f'{key}: {value}' + '\n'

        return output

    def retrieveData(self):
        """
        :return:
        """

        try:
            getInfo = yfinance.Ticker(self.stockSymbol)
            getInfo2 = stockInfo.get_quote_table(self.stockSymbol)

        except Exception:
            return None

        self.stockData["Company_Cash_Reserve"] = getInfo.info["totalCash"]
        self.stockData["Company_Debt"] = getInfo.info["totalDebt"]

        self.stockData["Opening Price"] = getInfo2["Open"]
        self.stockData["bid"] = getInfo2["Bid"]
        self.stockData["volume"] = getInfo2["Volume"]
        self.stockData["ask"] = getInfo2["Ask"]
        self.stockData["Closing Price"] = getInfo2["Previous Close"]
        self.stockData["PE_ratio"] = getInfo2["PE Ratio (TTM)"]

        val = stockInfo.get_stats_valuation(self.stockSymbol)
        val = val.iloc[:, : 2]
        val.columns = ["Attribute", "Recent"]

        PS = float(val[val.Attribute.str.contains("Price/Sales")].iloc[0,1])

        self.stockData["PS_ratio"] = PS

    def set_symbol(self, symbol: str):
        """
        :param symbol:
        :return:
        """
        self.stockSymbol = symbol

    def return_data(self) -> dict:
        """
        :return:
        """
        return {self.stockSymbol: self.stockData}

    def scrape_stock(self, symbol: str) -> dict:
        """
        :param symbol:
        :return:
        """

        self.set_symbol(symbol)
        self.retrieveData()
        return self.return_data()




def main():
    scraper = StockData()
    scraper.scrape_stock("amzn")
    print(scraper)




if __name__ == "__main__":
    main()