from alpaca.trading.client import TradingClient
from alpaca.data.live.stock import StockDataStream
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from os import getenv
import asyncio
from threading import Thread

class Algorithm(Thread):
	def __init__(self, API_KEY, API_SECRET, paper: bool):
		super().__init__()
		self.client = TradingClient(API_KEY, API_SECRET, paper=paper)
		self.paper = paper
		self.stream = StockDataStream(API_KEY, API_SECRET)
		
		print("Connecting to to Alpaca Websocket")

		# list of subscribed stocks
		self.subscribed = []

		self.start()
		print("Connected to Alpaca Websocket")
	
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
	
	def subscribe_to(self, symbol):
		try:
			self.stream.subscribe_bars(self.on_bar, symbol)
			print(f"Subscribed to {symbol}")
			self.subscribed.append(symbol)
		except Exception as e:
			print(f"Failed to subscribe to {symbol}")
			print(e)
	
	def add_equity(self, symbol):
		"""Adds equity to watchlist"""
		print('equity added')
		try:
			print(f"Adding {symbol} to watchlist")
			self.stream.subscribe_bars(self.on_bar(), symbol)
			print(f"Added {symbol} to watchlist")
		except:
			print(f"Failed to add {symbol} to watchlist")

	
	async def on_bar(self, update):
		print(update)
	
	def run(self):
		self.stream.run()
	

if __name__ == '__main__':
	algo = Algorithm(getenv("API_KEY"), getenv("SECRET_KEY"), paper=True)
	
	print("Subscribing to SPY")
