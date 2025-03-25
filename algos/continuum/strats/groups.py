from typing import TYPE_CHECKING
from loguru import logger
from os import getenv
from datetime import datetime
import finnhub

if TYPE_CHECKING:
    from .strategy import Strategy


class Instrument:
    def __init__(self, symbol: str, strategy: 'Strategy'):
        self.symbol = symbol

        self.strategy = strategy

        self.forecast: float = 0.0
        """+20 indicates strong buy, -20 equals strong sell"""

        self.finn = finnhub.Client(getenv("FINNHUB_KEY"))
    
    def next_earnings_date(self):
        """Get the next earnings date"""
        now = datetime.now().strftime("%Y-%m-%d")
        year_from_now = datetime.now().replace(year=datetime.now().year + 1).strftime("%Y-%m-%d")
        req = self.finn.earnings_calendar(symbol=self.symbol, _from=now, to=year_from_now)

        print(now, year_from_now)
        print(req['earningsCalendar'][-1])


class Group:
    """A group of assets to invest in"""
    def __init__(self, name: str):
        self.name = name

        self.weights: dict[str, list[Instrument, float]] = {}
        
    def add_symbol(self, symbol: str, weight: float, strategy: 'Strategy'):
        """
        Adds a symbol with its corresponding weight to the group.

        Args:
            symbol (str): The symbol to be added.
            weight (float): The weight associated with the symbol.

        Returns:
            None
        """
        instrument = Instrument(symbol, strategy)
        self.weights[symbol] = [instrument, weight]
        logger.debug(f"Added {symbol} to {self.name} with weight of {weight}")

if __name__ == '__main__':
    i = Instrument("TSLA", 1)
    i.next_earnings_date()