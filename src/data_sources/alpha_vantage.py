# src/data_sources/alpha_vantage.py
from src.data_sources.base import DataSource


class AlphaVantageDataSource(DataSource):
    def __init__(self):
        self.name = "Alpha Vantage"

    def get_historical_data(self, symbol, start_date, end_date):
        # Placeholder implementation
        return (
            f"AlphaVantage historical data for {symbol} from {start_date} to {end_date}"
        )

    def get_realtime_data(self, symbol):
        # Placeholder implementation
        return f"AlphaVantage real-time data for {symbol}"
