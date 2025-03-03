import abc
from alpaca.data.models import *
from groups import Group

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Position
from alpaca.trading.requests import MarketOrderRequest
from alpaca.common.exceptions import APIError
from os import getenv

class Strategy:
	"""Abstract class that represents a trading strategy."""

	def __init__(self, name: str, API_KEY = getenv("API_KEY"), API_SECRET = getenv("API_KEY"), paper = True):
		self.name = name
		
		self.client = TradingClient(API_KEY, API_SECRET, paper=paper)

	@abc.abstractmethod
	async def on_bar(self, update: Bar):
		pass
	
	@abc.abstractmethod
	async def on_trade(self, trade: Trade):
		pass

	def buy(self, group: Group, symbol: str):
		iWeight = group._weights[symbol]
		gWeight = self.weights[group]

		orderAmount = (self.cash * gWeight) * iWeight

		order = MarketOrderRequest(
			symbol=symbol,
			notional= orderAmount,
			side=OrderSide.BUY,
			time_in_force = TimeInForce.GTC
		)
		try:
			self.log(f"Submitted order for {symbol} in {group.name} group for ${orderAmount:.2f}")
			self.client.submit_order(order)
		except Exception as e:
			self.log(f"Order failed {e}")
	
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