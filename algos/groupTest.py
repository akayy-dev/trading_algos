from continuum.algo import Algorithm

import numpy as np
import talib
from algos.strats.groups import Group
from alpaca.data.historical import StockHistoricalDataClient, NewsClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.live.stock import StockDataStream
from alpaca.data.live.news import NewsDataStream
from alpaca.data.models.bars import Bar
from alpaca.data.models.news import News
from alpaca.data.models.trades import Trade
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Position
from alpaca.trading.requests import MarketOrderRequest
from alpaca.common.exceptions import APIError
from datetime import datetime, timedelta
from os import getenv


class RSI(Algorithm):
	def __init__(self):
		super().__init__(getenv("API_KEY"), getenv("SECRET_KEY"), paper=True)
		self.history = StockHistoricalDataClient(getenv("API_KEY"), getenv("SECRET_KEY"))

		self.tech = Group("tech stocks")
		self.tech.add_symbol("NVDA", 0.5)
		self.tech.add_symbol("AAPL", 0.25)
		self.tech.add_symbol("MSFT", 0.5)

		self.add_group(self.tech, .20)
		
		self.etfs = Group("ETF Indices")
		self.etfs.add_symbol("SPY", .5)
		self.etfs.add_symbol("FEZ", .25)
		self.etfs.add_symbol("NANC", .25)

		self.add_group(self.etfs, .70)

		self.finance = Group("Financial Stocks")
		self.finance.add_symbol("BRK.B", 1/3)
		self.finance.add_symbol("BAC", 1/3)
		self.finance.add_symbol("C", 1/3)

		self.add_group(self.finance, .10)

	
	async def on_bar(self, bar: Bar):
		# get the current time
		print(bar)


if __name__ == '__main__':
	algo = RSI()
	algo.run()