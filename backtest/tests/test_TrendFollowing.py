import unittest
from datetime import date, timedelta
from src.domain.Data import Data
from src.domain.TrendFollowing import TrendFollowing

STOCKS = "GSG"
START_DATE = date.today() - timedelta(days=6100)
END_DATE = date.today()
CLOSE_TYPE = 'Close'

TREND_FOLLOWING_DAYS = 50

class TrendFollowingTest(unittest.TestCase):

    def setUp(self):
        self.data = Data(stock_list=STOCKS, start_date=START_DATE, end_date=END_DATE, close_type=CLOSE_TYPE)
        self.df_historical_prices = self.data.get_historical_prices()
        self.trend_following = TrendFollowing(self.df_historical_prices)
        self.df_trend_following = self.trend_following.get_moving_average(TREND_FOLLOWING_DAYS)

    def test_moving_average(self):
        df = self.df_trend_following
        print(df)  #TODO: START HERE

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main(buffer=False)