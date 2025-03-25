import abc
import asyncio
from os import getenv
from threading import Thread
from typing import List

from .strats.groups import Group
from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.live.stock import StockDataStream
from alpaca.data.models import *
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Position
from alpaca.trading.requests import MarketOrderRequest
from alpaca.common.exceptions import APIError
from loguru import logger


class Algorithm:
	def __init__(self, API_KEY, API_SECRET, paper: bool):
		super().__init__()
		self.client = TradingClient(API_KEY, API_SECRET, paper=paper)

		self.stream = StockDataStream(API_KEY, API_SECRET)
		
		self.weights: dict[Group, float]= {}

		self.cash = float(self.client.get_account().cash)
	
	def add_group(self, g: Group, weight: float):
		"""Add a group"""
		self.weights[g] = weight

		for symbol, data in g.weights.items():

			instrument = data[0]
			iWeight = data[1] # instrument weight
			instrument.strategy.cash = (self.cash * weight) * iWeight

			# subscribe to symbols in list
			self.stream.subscribe_bars(instrument.strategy.on_bar, symbol)
			self.stream.subscribe_trades(instrument.strategy.on_trade, symbol)

			logger.debug(f"Added strategy {instrument.strategy.name} with dollar balance of ${instrument.strategy.cash}")
		
		logger.debug(f"Added group {g.name} with dollar balance of ${float(self.cash) * weight}")

	
	def run(self):
		logger.info("Connecting to to Alpaca Websocket")
		try:
			self.stream.run()
		except Exception as e:
			logger.exception(e)


if __name__ == '__main__':
	algo = Algorithm(getenv("API_KEY"), getenv("SECRET_KEY"), paper=True)
	algo.run()
	
