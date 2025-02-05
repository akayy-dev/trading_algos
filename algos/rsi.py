from continuum.algo import Algorithm

import numpy as np
import talib
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
		self.add_equity("XLK")

	
	async def on_bar(self, bar: Bar):
		# get the current time
		timestamp = bar.timestamp
		
		request = StockBarsRequest(
			symbol_or_symbols = bar.symbol,
			timeframe = TimeFrame.Day,
			start=bar.timestamp - timedelta(days=20),
			end_date = bar.timestamp,
		)

		data = self.history.get_stock_bars(request).df
		data.reset_index(inplace=True)
		
		close_prices = data["close"].values.astype(np.float64)

		rsi = talib.RSI(close_prices, timeperiod=len(close_prices) - 1)[-1]

		self.log(f"RSI for {bar.symbol} @ {bar.timestamp}: {rsi}")

		if rsi > 70:
			self.log(f"{bar.symbol} is overbought, selling")
			self.place_order(bar.symbol, 1, OrderSide.SELL)
		if rsi < 30:
			self.log(f"{bar.symbol} is oversold, buying")
			self.place_order(bar.symbol, 1, OrderSide.BUY)



if __name__ == '__main__':
	algo = RSI()
	algo.run()