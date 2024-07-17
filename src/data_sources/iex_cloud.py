# src/data_sources/IEX_Cloud.py
from src.data_sources.base import DataSource


class IEXCloudDataSource(DataSource):
    def __init__(self):
        self.name = "IEX Cloud"

    def get_historical_data(self, symbol, start_date, end_date):
        # Placeholder implementation
        return f"IEX Cloud historical data for {symbol} from {start_date} to {end_date}"

    def get_realtime_data(self, symbol):
        # Placeholder implementation
        return f"IEX Cloud real-time data for {symbol}"
