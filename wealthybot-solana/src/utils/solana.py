import pandas as pd
import aiohttp
from solders.pubkey import Pubkey

async def get_historical_data(mint: Pubkey) -> pd.DataFrame:
    async with aiohttp.ClientSession() as session:
        url = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={mint}&tsym=SOL&limit=100&api_key={os.getenv('CRYPTOCOMPARE_API')}"
        async with session.get(url) as response:
            data = await response.json()
            return pd.DataFrame(data['Data']['Data'])