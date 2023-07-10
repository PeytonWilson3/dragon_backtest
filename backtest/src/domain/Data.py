import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta

class Data():

    def __init__(self, stock_list, start_date, end_date, close_type:str):
        self.stock_list = stock_list
        self.start_date = start_date
        self.end_date = end_date
        self.close_type = close_type

    def get_historical_prices(self):
        df = yf.download(self.stock_list, self.start_date, self.end_date)
        df = df[self.close_type]
        return df
    
    def get_log_returns(self):
        df = self.get_historical_prices()
        df = np.log(df) - np.log(df).shift(1)
        df = df[1:]
        return df