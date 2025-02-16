from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from pandas import DataFrame
from datetime import datetime, timedelta
from os import getenv

class AlpacaIntegration:
	def __init__(self, API_KEY, SECRET_KEY):
		self.API_KEY = API_KEY
		self.SECRET_KEY = SECRET_KEY

		self._client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
	
	def _format_df(self, df: DataFrame) -> DataFrame:
		data = df.reset_index()
		data.columns = data.columns.str.title()
		data.set_index(["Timestamp"], inplace=True)
		return data
	
	def get_ticker_data(self, symbol: str,  start: datetime, end: datetime, timeframe: TimeFrame, pairs=[],) -> DataFrame:
		symbols_list = pairs + [symbol]

		request = StockBarsRequest(
			symbol_or_symbols=symbols_list,
			start=start,
			end=end,
			timeframe=timeframe
		)
		data = self._client.get_stock_bars(request).df

		# merge the pairs trading close price
		data_reset = data.reset_index()
		base_data = data_reset[data_reset["symbol"] == symbol]
		base_data = base_data.set_index("timestamp")

		for pair in pairs:
			pair_df = data_reset[data_reset["symbol"] == pair]
			pair_df = pair_df.rename(columns={"close": f"{pair}_close"})
			pair_df = pair_df[["timestamp", f"{pair}_close"]]
			base_data = base_data.merge(pair_df, on="timestamp", how="left")
			base_data = base_data.set_index("timestamp")

		base_data = base_data.rename(columns={
			"timestamp": "Timestamp",
			"open": "Open",
			"high": "High",
			"low": "Low",
			"close": "Close",
			"volume": "Volume"
		})
		base_data = base_data.drop("symbol", axis=1)
		return base_data

if __name__ == '__main__':
	alpaca = AlpacaIntegration(getenv('API_KEY'), getenv('SECRET_KEY'))
	print(alpaca.get_ticker_data("SPY", ["NVDA"], datetime(2024, 1, 1), datetime(2025, 1, 1), TimeFrame.Day))