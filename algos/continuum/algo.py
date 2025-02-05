import abc
import asyncio
from os import getenv
from threading import Thread
from typing import List

from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.live.stock import StockDataStream
from alpaca.data.live.news import NewsDataStream
from alpaca.data.models import *
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Position
from alpaca.trading.requests import MarketOrderRequest
from alpaca.common.exceptions import APIError


class Algorithm:
	def __init__(self, API_KEY, API_SECRET, paper: bool):
		super().__init__()
		self.client = TradingClient(API_KEY, API_SECRET, paper=paper)

		self.paper = paper
		self.stream = StockDataStream(API_KEY, API_SECRET)
		

		# list of subscribed stocks
		self.subscribed = []

	
	@property
	def buying_power(self):
		return self.client.get_account().cash
	
	def place_order(self, symbol, qty, side):
		order = MarketOrderRequest(
			symbol=symbol,
			qty=qty,
			side=side,
			time_in_force = TimeInForce.GTC # good until cancelled
		)

		try:
			self.client.submit_order(order)
			print(f"✅ Order placed: {side} {qty} shares of {symbol}")
		except Exception as e:
			print(f"❌ Order failed: {e}")
	
	
	def add_equity(self, symbol):
		"""Adds equity to watchlist"""
		try:
			print(f"Adding {symbol} to watchlist")
			self.stream.subscribe_bars(self.on_bar, symbol)
			self.stream.subscribe_trades(self.on_traded, symbol)
			self.subscribed.append(symbol)
		except Exception as e:
			print(f"Failed to add {symbol} to watchlist")
			print(e)
	
	
	@property
	def positions(self) -> List[Position]:
		return self.client.get_all_positions()
	
	def get_position(self, symbol):
		"""Returns a position object for the given symbol"""
		try:
			return self.client.get_open_position(symbol)
		except APIError as e:
			return None
	
	@abc.abstractmethod
	async def on_bar(self, update: Bar):
		pass
	
	@abc.abstractmethod
	async def on_traded(self, trade: Trade):
		pass
	

	def run(self):
		print("Connecting to to Alpaca Websocket")
		try:
			self.stream.run()
		except Exception as e:
			print(e)
		
	

if __name__ == '__main__':
	algo = Algorithm(getenv("API_KEY"), getenv("SECRET_KEY"), paper=True)
	algo.run()
	
