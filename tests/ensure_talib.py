"""Backtest just to make sure all the backages are installed and working."""
from backtesting.test import GOOG
from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import talib
import pandas

class EnsureTalibWorking(Strategy):
    def init(self):
        self.sma = self.I(talib.SMA, self.data.Close)
    
    def next(self):
        if crossover(self.data.Close, self.sma):
            print(f"{self.data.Close[-1]}: Selling")
            self.position.close()
        if crossover(self.sma, self.data.Close):
            print(f"{self.data.Close[-1]}: Buying")
            self.buy()


if __name__ == '__main__':
    bt = Backtest(GOOG, EnsureTalibWorking, cash=1000, commission=0.0)
    
    stats = bt.run()
    print(stats)