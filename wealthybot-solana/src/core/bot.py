# src/core/bot.py
import os
import json
import asyncio
from typing import Dict
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from anchorpy import Provider, Wallet
from jupiter import Jupiter, SwapRequest
from .models import TokenConfig
from .strategies import TradingStrategies
from src.utils.solana import get_historical_data

class SolanaWealthyBot:
    def __init__(self):
        self.client = AsyncClient(os.getenv("SOLANA_RPC"))
        self.jupiter = Jupiter(self.client, Wallet(Keypair.from_bytes(
            bytes(json.loads(os.getenv("PRIVATE_KEY")))))
        self.token_configs: Dict[str, TokenConfig] = {}
        self.active_trades = {}

    async def load_config(self, config_file: str = "config/tokens.json"):
        with open(config_file) as f:
            configs = json.load(f)
            for cfg in configs['tokens']:
                token = TokenConfig(**cfg)
                self.token_configs[token.name] = token

    async def execute_swap(self, token: TokenConfig, is_buy: bool):
        try:
            routes = await self.jupiter.get_quote(
                input_mint=Pubkey.from_string("So11111111111111111111111111111111111111112") if is_buy else token.mint,
                output_mint=token.mint if is_buy else Pubkey.from_string("So11111111111111111111111111111111111111112"),
                amount=int(token.avg_amount * 1e9),
                slippage=50
            )
            swap_req = SwapRequest(route=routes[0])
            tx = await self.jupiter.swap(swap_req)
            print(f"Executed {'BUY' if is_buy else 'SELL'} for {token.name}: {tx}")
        except Exception as e:
            print(f"Trade failed: {str(e)}")

    async def run_strategy_cycle(self):
        for name, token in self.token_configs.items():
            data = await get_historical_data(token.mint)
            current_price = data['close'].iloc[-1]
            
            if token.strategy == "wealthy":
                signal = TradingStrategies.wealthy_strategy(data)
            elif token.strategy == "bearish":
                signal = TradingStrategies.bearish_strategy(data)

            if token.market_bias == "bearish" and not signal:
                continue

            if signal and len(self.active_trades.get(name, [])) < token.max_trades:
                await self.execute_swap(token, is_buy=True)
            elif not signal and name in self.active_trades:
                await self.execute_swap(token, is_buy=False)