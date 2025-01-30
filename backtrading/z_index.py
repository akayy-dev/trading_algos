from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
from backtesting.test import GOOG
import pandas as pd
import talib
from alpaca_data import AlpacaIntegration
from os import getenv
from alpaca.data.timeframe import TimeFrame

class ZIndex(Strategy):
	def init(self):
		self.sma = self.I(talib.SMA, self.data.Close, 5)
		self.z = self.I(lambda x: (x - self.sma[-1])/ talib.STDDEV(x, timeperiod=10), self.data.Close)
	def next(self):
		price = self.data.Close[-1]
		
		if self.z[-1] > 2:
			print(f"{self.data.index[-1]}: Selling at {price}, Z : {self.z[-1]}")
			self.position.close()
		if self.z[-1] < -2:
			print(f"{self.data.index[-1]}: Buying at {price}, Z :  {self.z[-1]}")
			self.buy()


alpaca = AlpacaIntegration(getenv("API_KEY"), getenv("SECRET_KEY"))

bt = Backtest(alpaca.get_ticker_data("SPY", TimeFrame.Minute, 365), ZIndex, cash=10000, commission=0)
stats = bt.run()

bt.plot()

print(stats)