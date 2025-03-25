from continuum.algo import Algorithm

import numpy as np
import sched
import talib
from continuum.strats.groups import Group
from alpaca.data.historical import StockHistoricalDataClient, NewsClient
from datetime import datetime, timedelta
from os import getenv

from continuum.strats.RSI import RSI


class RSIDemo(Algorithm):
	def __init__(self):
		super().__init__(getenv("API_KEY"), getenv("SECRET_KEY"), paper=True)
		self.history = StockHistoricalDataClient(getenv("API_KEY"), getenv("SECRET_KEY"))

		NVDA_RSI = RSI("NVDA_RSI", "NVDA")
		AAPL_RSI = RSI("AAPL_RSI", "AAPL")
		ASML_RSI = RSI("ASML_RSI", "ASML")

		self.tech = Group("tech stocks")
		self.tech.add_symbol("NVDA", .5, NVDA_RSI)
		self.tech.add_symbol("AAPL", .4, AAPL_RSI)
		self.tech.add_symbol("ASML", .1, ASML_RSI)

		self.add_group(self.tech, 0.5)

	

if __name__ == '__main__':
	algo = RSIDemo()
	algo.run()