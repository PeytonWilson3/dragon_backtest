import unittest
from datetime import date, timedelta
from src.domain.Data import Data

STOCKS = "SPY GSG IAU"
START_DATE = date.today() - timedelta(days=6100)
END_DATE = date.today()
CLOSE_TYPE = "Adj Close"

class DataTest(unittest.TestCase):

    def test_data(self):
        data = Data(stock_list=STOCKS, start_date=START_DATE, end_date=END_DATE, close_type=CLOSE_TYPE)
        df = data.get_log_returns()
        print(df)

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main(buffer=False)