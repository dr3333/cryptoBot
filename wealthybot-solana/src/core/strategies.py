# src/core/strategies.py
import pandas as pd

class TradingStrategies:
    @staticmethod
    def wealthy_strategy(data: pd.DataFrame) -> bool:
        data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        return data['EMA20'].iloc[-1] > data['EMA50'].iloc[-1]

    @staticmethod
    def bearish_strategy(data: pd.DataFrame) -> bool:
        data['RSI'] = TradingStrategies.calculate_rsi(data, 14)
        return data['RSI'].iloc[-1] > 70

    @staticmethod
    def calculate_rsi(data: pd.DataFrame, window: int) -> pd.Series:
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))