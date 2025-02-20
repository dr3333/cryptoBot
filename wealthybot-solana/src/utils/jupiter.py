# src/utils/jupiter.py
class JupiterClient:
    """Enhanced Jupiter API client"""
    async def get_best_route(self):
        """Add rate limiting and error handling"""
        