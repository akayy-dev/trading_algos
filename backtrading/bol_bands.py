from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
from backtesting.test import GOOG
import pandas as pd
import talib
from alpaca_data import AlpacaIntegration
from os import getenv
from alpaca.data.timeframe import TimeFrame
import numpy
numpy.std

class BolBands(Strategy):
	def init(self):
		self.sma = self.I(talib.SMA, self.data.Close, 20)
		self.z = self.I(lambda x: (x - self.sma[-1])/ talib.STDDEV(x, timeperiod=20), self.data.Close)


		self.std_dev = self.I(talib.STDDEV, self.data.Close, 20)
		


		bol_up = lambda x: self.sma + (self.std_dev[-1] * 2)
		bol_down = lambda x: self.sma - (self.std_dev[-1] * 2)

		self.upper = self.I(bol_up, self.data.Close)
		self.lower = self.I(bol_down, self.data.Close)

		# self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, talib.MA_Type.SMA)
	def next(self):
		price = self.data.Close[-1]
		
		if price < self.lower:
			# if underbought
			self.buy()
			print(f"{self.data.index[-1]}: Buying at {price}, Z : {self.z[-1]}")
		if price >= self.upper:
			self.position.close()
			print(f"{self.data.index[-1]}: Selling at {price}, Z : {self.z[-1]}")


alpaca = AlpacaIntegration(getenv("API_KEY"), getenv("SECRET_KEY"))

bt = Backtest(alpaca.get_ticker_data("TSLA", TimeFrame.Minute, 365), BolBands, cash=10000, commission=0.00)
stats = bt.run()

bt.plot()

print(stats)