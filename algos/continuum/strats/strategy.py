import abc
from alpaca.data.models import *

import pandas
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Position
from alpaca.trading.requests import MarketOrderRequest
from alpaca.common.exceptions import APIError
from alpaca.data.timeframe import TimeFrame
from os import getenv

from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
	from .groups import Group

class Strategy(abc.ABC):
	"""Abstract class that represents a trading strategy."""

	def __init__(self, name: str, symbol: str, API_KEY = getenv("API_KEY"), API_SECRET = getenv("SECRET_KEY"), paper = True):


		self.name = name
		self.symbol = symbol

		self.client = TradingClient(API_KEY, API_SECRET, paper=paper)

		self.cash: float 
		"""Cash availible to execute strategy with"""

		logger.info(f"Created strategy {self.name}")

		self.historical = StockHistoricalDataClient(API_KEY, API_SECRET)
	
	async def on_bar(self, update: Bar):
		pass
	
	async def on_trade(self, trade: Trade):
		pass

	def buy(self, group: 'Group', symbol: str):

		order = MarketOrderRequest(
			symbol=symbol,
			notional= self.cash,
			side=OrderSide.BUY,
			time_in_force = TimeInForce.GTC
		)
		try:
			logger.info(f"Submitted order for {symbol} in {group.name} group for ${self.cash:.2f}")
			self.client.submit_order(order)
		except Exception as e:
			logger.exception(f"Order failed {e}")
			print(f"Order failed {e}")
	
	def close_position(self, symbol: str):
		self.close_position(symbol=symbol)


	@property
	def positions(self) -> List[Position]:
		return self.client.get_all_positions()

	def get_position(self, symbol):
		"""Returns a position object for the given symbol"""
		try:
			return self.client.get_open_position(symbol)
		except APIError as e:
			return None

	def close_position(self, symbol: str):
		self.close_position(symbol=symbol)
	
	def get_historical_data(self, start, timeframe = TimeFrame.Day, end = datetime.now()) -> pandas.DataFrame:
		request = StockBarsRequest(
			symbol_or_symbols=self.symbol,
			start=start,
			end=end,
			timeframe=timeframe
		)
		return self.historical.get_stock_bars(request).df