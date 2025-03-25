import abc
from alpaca.data.models import *

import time
import sched
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
from datetime import datetime, timedelta

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

		# Schedule on-close
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self._schedule_close()
		self.scheduler.run()
	
	async def on_bar(self, update: Bar):
		pass
	
	async def on_trade(self, trade: Trade):
		pass

	async def on_close(self):
		"""Run 1 minute before close every weekday (3:59 PM)"""
		pass
	
	def _schedule_close(self):
		"""Schedules the on_close method to run 1m before market close (3:59 PM)"""
		now = datetime.now()
		
		# one minute before close time (4PM)
		today_close = now.replace(hour=15, minute=59, second=0, microsecond=0)

		# if past closing time
		if now > today_close:
			today_close += timedelta(days=1)
			logger.trace(f"Past closing time, scheduling for tommorow.")
		
		while today_close.weekday() > 4:
			today_close += timedelta(days=1)
			logger.trace(f"Moving scheduled on_close event to {today_close.weekday()}")
		
		self.scheduler.enterabs(time.mktime(today_close.timetuple()), 1, self._on_close_callback)
		
	def _on_close_callback(self):
		"""Callback that runs the on_close method and schedules the next one."""
		self.on_close()
		logger.trace("Ran on close method")
		self._schedule_close()	
		logger.trace("Scheduled next on_close")

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