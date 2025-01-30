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
	
	def get_ticker_data(self, symbol: str, timeframe: TimeFrame, days_ago) -> DataFrame:
		start_date = datetime.now() - timedelta(days = days_ago)
		end_date = datetime.now() # end date today.

		request = StockBarsRequest(
			symbol_or_symbols = symbol,
			timeframe=timeframe,
			start=start_date,
			end=end_date,
		)

		bars = self._client.get_stock_bars(request)

		return self._format_df(bars.df)

if __name__ == '__main__':
	alpaca = AlpacaIntegration(getenv('API_KEY'), getenv('SECRET_KEY'))
	print(alpaca.get_ticker_data("SPY", TimeFrame.Day, 3650))