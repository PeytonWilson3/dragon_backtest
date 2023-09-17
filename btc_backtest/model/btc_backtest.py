import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class Btc_backtest():

    def __init__(self, prices_df, btc:str, long_btc_proxy:str, short_btc_proxy:str, start_date, days, tax_rate):
        self.prices_df = prices_df
        self.btc = btc
        self.long_btc_proxy = long_btc_proxy
        self.short_btc_proxy = short_btc_proxy
        self.start_date = start_date
        self.days = days
        self.tax_rate = tax_rate

    def btc_spot_backtest(self):
        df = yf.download(self.prices_df, start=self.start_date)
        df = df['Adj Close']
        df = df.dropna()

        df["BTC-USD MA"] = df["BTC-USD"].rolling(window=self.days).mean()

        returns_df = []

        for i in range(len(df)):
            if df[self.btc].iloc[i] > df['BTC-USD MA'].iloc[i]:
                returns = np.log(df[self.btc].iloc[i] / df['BTC-USD'].iloc[i-1])
                returns_df.append(returns)
            if df[self.btc].iloc[i] < df['BTC-USD MA'].iloc[i]:
                returns = np.log(df[self.short_btc_proxy].iloc[i] / df[self.short_btc_proxy].iloc[i-1])
                returns_df.append(returns)

        returns_array = np.array(returns_df)

        growth = (1 + returns_array).cumprod()

        return growth[-1]

    def etf_backtest(self):
        df = yf.download(self.prices_df, start=self.start_date)
        df = df['Adj Close']
        df = df.dropna()

        df["BTC-USD MA"] = df["BTC-USD"].rolling(window=self.days).mean()

        returns_df = []

        for i in range(self.days+1, len(df)):
            if df[self.btc].iloc[i] > df['BTC-USD MA'].iloc[i]:
                returns = np.log(df[self.long_btc_proxy].iloc[i] / df[self.long_btc_proxy].iloc[i-1])
                returns_df.append(returns)
            if df[self.btc].iloc[i] < df['BTC-USD MA'].iloc[i]:
                returns = np.log(df[self.short_btc_proxy].iloc[i] / df[self.short_btc_proxy].iloc[i-1])
                returns_df.append(returns)

        returns_array = np.array(returns_df)

        growth = (1 + returns_array).cumprod()

        return growth[-1]

    def etf_backtest_tax_impact(self):
        df = yf.download(self.prices_df, start=self.start_date)
        df = df['Adj Close']
        df = df.dropna()

        df["BTC-USD MA"] = df["BTC-USD"].rolling(window=self.days).mean()

        returns_df = []
        holding_period_returns = []
        previous_position = None

        for i in range(self.days+1, len(df)):
            if df[self.btc].iloc[i] > df['BTC-USD MA'].iloc[i]:
                if previous_position == 'short':
                    tax_impact = sum(holding_period_returns) * self.tax_rate
                    holding_period_returns = [r - tax_impact for r in holding_period_returns]
                    returns_df += holding_period_returns
                    holding_period_returns = []
                returns = np.log(df[self.long_btc_proxy].iloc[i] / df[self.long_btc_proxy].iloc[i-1])
                holding_period_returns.append(returns)
                previous_position = 'long'
            if df[self.btc].iloc[i] < df['BTC-USD MA'].iloc[i]:
                if previous_position == 'long':
                    tax_impact = sum(holding_period_returns) * self.tax_rate
                    holding_period_returns = [r - tax_impact for r in holding_period_returns]
                    returns_df += holding_period_returns
                    holding_period_returns = []
                returns = np.log(df[self.short_btc_proxy].iloc[i] / df[self.short_btc_proxy].iloc[i-1])
                holding_period_returns.append(returns)
                previous_position = 'short'

        # add last holding period to returns if it hasn't been added yet
        if holding_period_returns:
            tax_impact = sum(holding_period_returns) * self.tax_rate
            holding_period_returns = [r - tax_impact for r in holding_period_returns]
            returns_df += holding_period_returns

        returns_array = np.array(returns_df)

        growth = (1 + returns_array).cumprod()

        return growth[-1]