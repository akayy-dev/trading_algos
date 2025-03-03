from strategy import Strategy

class Instrument:
    def __init__(self, symbol: str, strategy: Strategy):
        self.symbol = symbol

        self.strategy = strategy

        self.forecast: float = 0.0
        """+20 indicates strong buy, -20 equals strong sell"""

class Group:
    """A group of assets to invest in"""
    def __init__(self, name: str):
        self.name = name

        self.weights: dict[str, list[Instrument, float]] = {}
        
    def add_symbol(self, symbol: str, weight: float, strategy: Strategy):
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