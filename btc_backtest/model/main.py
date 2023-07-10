import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from btc_backtest import Btc_backtest

backtest = Btc_backtest('BTC-USD BITO BITI', btc="BTC-USD", long_btc_proxy="BITO", short_btc_proxy="BITI", start_date='2022-06-21', days=50, tax_rate=0.3)
btc_spot_backtest = backtest.btc_spot_backtest()
print(btc_spot_backtest)