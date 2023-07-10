import pandas as pd
import numpy as np

class TrendFollowing():

    def __init__(self, stock_returns):
        self.stock_returns = stock_returns

    def get_moving_average(self, days=50):
        df = self.stock_returns.rolling(window=days).mean()
        df = df
        return df
    
    def trend_following_return(self):
        df_moving_average = self.get_moving_average()
        df = pd.concat(self.stock_returns, df_moving_average)
        print(df)