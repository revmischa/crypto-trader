import pandas_ta as ta
from pyjuque.Strategies import StrategyTemplate


class EMACross(StrategyTemplate):
    """Bollinger Bands x RSI"""

    minimum_period = 100

    def __init__(self, fast_ma_len=10, slow_ma_len=50):
        self.fast_ma_len = fast_ma_len
        self.slow_ma_len = slow_ma_len
        # the minimum number of candles needed to compute our indicators
        self.minimum_period = max(100, slow_ma_len)

    # the bot will call this function with the latest data from the exchange
    # passed through df; this function computes all the indicators needed
    # for the signal
    def setUp(self, df):
        df["slow_ma"] = ta.ema(df["close"], self.slow_ma_len)
        df["fast_ma"] = ta.ema(df["close"], self.fast_ma_len)
        self.dataframe = df

    # the bot will call this function with the latest data and if this
    # returns true, our bot will place an order
    def checkLongSignal(self, i=None):
        """ """
        df = self.dataframe
        if i == None:
            i = len(df) - 1
        if i < 1:
            return False
        if (
            df["low"][i - 1] < df["slow_ma"][i - 1]
            and df["low"][i] > df["slow_ma"][i]
            and df["low"][i] > df["fast_ma"][i]
            and df["fast_ma"][i] > df["slow_ma"][i]
        ):
            return True
        return False

    def checkShortSignal(self, i=None):
        df = self.dataframe
        if i == None:
            i = len(df) - 1
        if i < 1:
            return False
        if (
            (
                df["low"][i - 1] > df["slow_ma"][i - 1]
                or df["fast_ma"][i - 1] > df["slow_ma"][i - 1]
            )
            and df["close"][i] < df["slow_ma"][i]
            and df["close"][i] < df["fast_ma"][i]
            and df["fast_ma"][i] < df["slow_ma"][i]
        ):
            return True
        return False
