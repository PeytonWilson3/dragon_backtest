import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

STOCKS = 'BTC-USD BITO BITI'
START_DATE = '2022-06-21'
DAYS = 50

df = yf.download(STOCKS, start=START_DATE)
df = df['Adj Close']

df["BTC-USD MA"] = df["BTC-USD"].rolling(window=DAYS).mean()

returns_df = []

for i in range(len(df)):
    if df['BTC-USD'].iloc[i] > df['BTC-USD MA'].iloc[i]:
        returns = np.log(df['BTC-USD'].iloc[i] / df['BTC-USD'].iloc[i-1])
        returns_df.append(returns)
    if df['BTC-USD'].iloc[i] < df['BTC-USD MA'].iloc[i]:
        returns = -np.log(df['BTC-USD'].iloc[i] / df['BTC-USD'].iloc[i-1])
        returns_df.append(returns)

returns_array = np.array(returns_df)

growth = (1 + returns_array).cumprod()

def btc_backtest(prices_df, btc:str, long_btc_proxy:str, short_btc_proxy:str, start_date, days):
    df = yf.download(prices_df, start=start_date)
    df = df['Adj Close']
    df = df.dropna()

    df["BTC-USD MA"] = df["BTC-USD"].rolling(window=DAYS).mean()

    returns_df = []

    for i in range(days+1, len(df)):
        if df[btc].iloc[i] > df['BTC-USD MA'].iloc[i]:
            returns = np.log(df[long_btc_proxy].iloc[i] / df[long_btc_proxy].iloc[i-1])
            returns_df.append(returns)
        if df[btc].iloc[i] < df['BTC-USD MA'].iloc[i]:
            returns = np.log(df[short_btc_proxy].iloc[i] / df[short_btc_proxy].iloc[i-1])
            returns_df.append(returns)

    returns_array = np.array(returns_df)

    growth = (1 + returns_array).cumprod()

    return growth[-1]

a = btc_backtest(STOCKS, btc="BTC-USD", long_btc_proxy="BITO", short_btc_proxy="BITI", start_date=START_DATE, days=DAYS)

class btc_backtest():

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
        print(df)
        df["BTC-USD MA"] = df[self.btc].rolling(window=DAYS).mean()

        returns_df = []

        for i in range(len(df)):
            if df[self.btc].iloc[i] > df['BTC-USD MA'].iloc[i]:
                returns = np.log(df[self.long_btc_proxy].iloc[i] / df[self.long_btc_proxy].iloc[i-1])
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
        df["BTC-USD MA"] = df[self.btc].rolling(window=self.days).mean()

        returns_list = []  # Create a list to store returns
        positions = []  # Create a list to track positions

        for i in range(self.days+1, len(df)):
            if df[self.btc].iloc[i] > df['BTC-USD MA'].iloc[i]:
                if not positions or positions[-1] != 'long':
                    # Assume a long position for the first return after a change
                    positions.append('long')
                    returns = np.log(df[self.short_btc_proxy].iloc[i] / df[self.short_btc_proxy].iloc[i-1])
                    returns_list.append(returns)
                else:
                    positions.append('long')
                    returns = np.log(df[self.long_btc_proxy].iloc[i] / df[self.long_btc_proxy].iloc[i-1])
                    returns_list.append(returns)
            elif df[self.btc].iloc[i] < df['BTC-USD MA'].iloc[i]:
                if not positions or positions[-1] != 'short':
                    # Assume a short position for the first return after a change
                    positions.append('short')
                    returns = np.log(df[self.long_btc_proxy].iloc[i] / df[self.long_btc_proxy].iloc[i-1])
                    returns_list.append(returns)
                else:
                    positions.append('short')
                    returns = np.log(df[self.short_btc_proxy].iloc[i] / df[self.short_btc_proxy].iloc[i-1])
                    returns_list.append(returns)
            else:
                # No position change, use a return of 0
                positions.append(positions[-1] if positions else None)  # Maintain the previous position
                returns_list.append(0)

        positions = pd.Series(positions, index=df.index[self.days+1:])  # Create a Series for positions

        # Create a DataFrame with returns and positions
        returns_df = pd.DataFrame({'Returns': returns_list, 'Position': positions})

        # Corrected line: Set the index for returns_df
        returns_df.index = df.index[self.days+1:]

        returns_array = returns_df.to_numpy()

        growth = (1 + returns_array[:, 0]).cumprod()  # Calculate growth based on returns

        returns_df.to_excel("gsg_gsg_sco_returns.xlsx")

        return growth[-1]

    def etf_backtest_tax_impact(self):
        df = yf.download(self.prices_df, start=self.start_date)
        df = df['Adj Close']
        df = df.dropna()

        df["BTC-USD MA"] = df[self.btc].rolling(window=self.days).mean()

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

b = btc_backtest(STOCKS, btc="BTC-USD", long_btc_proxy="BITO", short_btc_proxy="BITI", start_date=START_DATE, days=DAYS, tax_rate=0.3).etf_backtest()
c = btc_backtest(STOCKS, btc="BTC-USD", long_btc_proxy="BITO", short_btc_proxy="BITI", start_date=START_DATE, days=DAYS, tax_rate=0.3).btc_spot_backtest()
d = btc_backtest(STOCKS, btc="BTC-USD", long_btc_proxy="BITO", short_btc_proxy="BITI", start_date=START_DATE, days=DAYS, tax_rate=0.3).etf_backtest_tax_impact()
print(b, c, d)

# Commodity Trend-Following Backtest
GSG = 'GSG USO SCO SPY'
GSG_START_DATE = '2006-12-12'
MOVING_AVERAGE = 50
gsg = btc_backtest(GSG, btc="GSG", long_btc_proxy="GSG", short_btc_proxy="SCO", start_date=GSG_START_DATE, days=MOVING_AVERAGE, tax_rate=0.3).etf_backtest()
# gsg_ = btc_backtest(GSG, btc="BTC-USD", long_btc_proxy="BTC-USD", short_btc_proxy="BTC-USD", start_date=GSG_START_DATE, days=MOVING_AVERAGE, tax_rate=0.3).etf_backtest()
# _gsg_ = btc_backtest(GSG, btc="GSG", long_btc_proxy="USO", short_btc_proxy="SCO", start_date=GSG_START_DATE, days=MOVING_AVERAGE, tax_rate=0.3).etf_backtest_tax_impact()

print(gsg)