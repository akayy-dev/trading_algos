from continuum.algo import Algorithm
from alpaca.data.models.bars import Bar
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from os import getenv


class Arbitrage(Algorithm):
	def __init__(self):
		super().__init__(getenv("API_KEY"), getenv("SECRET_KEY"), True)
	
	def on_bar(self, update: Bar):
		low = update.low
		high = update.high

		buy_at_low = LimitOrderRequest("SPY", 1, OrderSide.BUY, time_in_force = TimeInForce.GTC, limit_price=low)
		buy_order = self.client.submit_order(buy_at_low)
		print("Submitting buy order")

		if buy_order.status.FILLED:
			print(f"Bought at ${high}")
			sell_at_high = LimitOrderRequest("SPY", 1, OrderSide.SELL, time_in_force = TimeInForce.GTC, limit_price=high)
			sell_order = self.client.submit_order(sell_at_high)
			if sell_order.status.FILLED:
				print(f"Selling at {sell_order}")

		

if __name__ == '__main__':
	algo = Arbitrage()
	algo.run()