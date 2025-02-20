class RiskManager:
    @staticmethod
    def check_exposure(active_trades, max_trades):
        return len(active_trades) >= max_trades

    @staticmethod
    def calculate_position_size(balance, risk_pct=0.02):
        return balance * risk_pct