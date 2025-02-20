# main.py
import asyncio
from src.core.bot import SolanaWealthyBot

async def main():
    bot = SolanaWealthyBot()
    await bot.load_config()
    await bot.run_strategy_cycle()

if __name__ == "__main__":
    asyncio.run(main())