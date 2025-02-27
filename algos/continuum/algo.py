import abc
import asyncio
from os import getenv
from threading import Thread
from typing import List

from data.groups import Group
from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.live.stock import StockDataStream
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

		self.log_file = open('log.txt', 'w')

		self.weights: dict[Group, float]= {}

		self.cash = self.client.get_account().cash
	
	def add_group(self, g: Group, weight: float):
		"""Add a group"""
		self.weights[g] = weight

		for symbol in list(g.weights.keys()):
			# subscribe to symbols in list
			self.stream.subscribe_bars(self.on_bar, symbol)
			self.stream.subscribe_trades(self.on_bar, symbol)
		
		self.log(f"Added group {g.name}")


	
	def get_group(self, name: str):
		return self.groups.get(name)
	
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
	
	def add_equity(self, symbol):
		"""Adds equity to watchlist"""
		try:
			self.log(f"Adding {symbol} to watchlist")
			self.stream.subscribe_bars(self.on_bar, symbol)
			self.stream.subscribe_trades(self.on_traded, symbol)
			self.subscribed.append(symbol)
		except Exception as e:
			self.log(f"Failed to add {symbol} to watchlist")
			self.log(e)
	
	
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
	

	def log(self, message):
		"""Output logs to log.txt"""
		log_msg = f"{datetime.now()}: {message}"
		print(log_msg)
		self.log_file.write(f"{log_msg}\n")
		self.log_file.flush()

	def run(self):
		self.log("Connecting to to Alpaca Websocket")
		try:
			self.stream.run()
		except Exception as e:
			self.log(e)
		finally:
			self.log("Closing log file")
			self.log_file.close()
		
	

if __name__ == '__main__':
	algo = Algorithm(getenv("API_KEY"), getenv("SECRET_KEY"), paper=True)
	algo.run()
	
