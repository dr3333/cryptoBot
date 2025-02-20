# src/core/models.py
from solders.pubkey import Pubkey

class TokenConfig:
    def __init__(self, 
                 name: str,
                 mint: str,
                 profit_pct: float = 2.0,
                 stop_above: float = None,
                 avg_amount: float = 0.1,
                 max_trades: int = 3,
                 strategy: str = "wealthy",
                 market_bias: str = "bullish"):
        self.name = name
        self.mint = Pubkey.from_string(mint)
        self.profit_pct = profit_pct
        self.stop_above = stop_above
        self.avg_amount = avg_amount
        self.max_trades = max_trades
        self.strategy = strategy
        self.market_bias = market_bias