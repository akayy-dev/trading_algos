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

class RelativeStrengthIndex(Strategy):
	def init(self):
		self.sma = self.I(talib.SMA, self.data.Close, 20)
		self.rsi = self.I(talib.RSI, self.data.Close)

		# self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, talib.MA_Type.SMA)
	def next(self):
		if self.rsi > 70:
			print(f"{self.data.index[-1]}: Stock is possibly overbought, selling")
			self.position.close()
		elif self.rsi < 30:
			print(f"{self.data.index[-1]}: Stock is possibly underbought, buying")
			self.buy()


alpaca = AlpacaIntegration(getenv("API_KEY"), getenv("SECRET_KEY"))

bt = Backtest(alpaca.get_ticker_data("XOM", TimeFrame.Hour, 1825), RelativeStrengthIndex, cash=10000, commission=0.00)
stats = bt.run()

bt.plot()

print(stats)