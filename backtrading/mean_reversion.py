from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
from backtesting.test import GOOG
import pandas as pd
import talib
from alpaca_data import AlpacaIntegration
from os import getenv
from alpaca.data.timeframe import TimeFrame

class MeanReversion(Strategy):
	def init(self):
		self.sma = self.I(talib.SMA, self.data.Close, 5)
	def next(self):
		price = self.data.Close[-1]
		
		if price > self.sma[-1]:
			print(f"{self.data.index[-1]}: Selling at {price}")
			self.position.close()
		if price < self.sma[-1]:
			print(f"{self.data.index[-1]}: Buying at {price}")
			self.buy()


alpaca = AlpacaIntegration(getenv("API_KEY"), getenv("SECRET_KEY"))

bt = Backtest(alpaca.get_ticker_data("SPY", TimeFrame.Day, 50), MeanReversion, cash=10000, commission=0)
stats = bt.run()

bt.plot()

print(stats)