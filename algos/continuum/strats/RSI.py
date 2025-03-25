from .strategy import Strategy
from datetime import timedelta, datetime
import talib
from loguru import logger


class RSI(Strategy):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
    
    async def on_bar(self, update):
        historical_data = self.get_historical_data(start=datetime.now() - timedelta(days=30))
        rsi = talib.RSI(historical_data["close"]).iloc[-1]

        logger.info(f"RSI for {self.symbol} is {rsi}")
        
