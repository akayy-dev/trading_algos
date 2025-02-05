from datetime import datetime, timedelta
from os import getenv

from continuum.algo import Algorithm

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models.bars import Bar
from alpaca.data.models.trades import Trade
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.enums import OrderSide
from alpaca.common.enums import Sort

import talib


class MeanReversion(Algorithm):
	def __init__(self):
		super().__init__(getenv("API_KEY"), getenv("SECRET_KEY"), True)
		self.history = StockHistoricalDataClient(getenv("API_KEY"), getenv("SECRET_KEY"))

		self.add_equity("SPY")

	
	async def on_bar(self, bar: Bar):
		
		price = bar.close

		# get average price of stock over 10 minutes
		# BUG: Seems to only get the past 8 minutes, interesting.
		WINDOW = 10
		start_date = datetime.now() - timedelta(days=1)
		end_date = datetime.now() # end date today.


		request = StockBarsRequest(
			symbol_or_symbols = bar.symbol, 
			timeframe = TimeFrame.Minute,
			start = start_date, 
			end = end_date,
			sort=Sort.DESC
		)

		df = self.history.get_stock_bars(request).df
		df.reset_index(inplace=True)
		rolling_avg = df["close"].rolling(window=WINDOW).mean().iloc[-1]
		price_deviation = price - rolling_avg
		std_deviation = df["close"].rolling(window=WINDOW).std().iloc[-1]
		z_score = price_deviation / std_deviation

		print(f'Price for {bar.symbol}:{price} - Rolling Avg: {rolling_avg} - Z Score: {z_score}')

		if z_score > 2:
			print("Stock is possibly overbought, triggering a sell.")
			self.place_order(bar.symbol, 1, OrderSide.SELL)
		if z_score < -2:
			print("Stock is possibly oversold, triggering a buy.")
			self.place_order(bar.symbol, 1, OrderSide.BUY)

	

if __name__ == '__main__':
	algo = MeanReversion()
	algo.run()
