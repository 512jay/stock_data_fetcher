# src/data_sources/yahoo_finance.py
from src.data_sources.base import DataSource


class YahooFinanceDataSource(DataSource):
    def __init__(self):
        self.name = "Yahoo Finance"

    def get_historical_data(self, symbol, start_date, end_date):
        # Placeholder implementation
        return (
            f"YahooFinance historical data for {symbol} from {start_date} to {end_date}"
        )

    def get_realtime_data(self, symbol):
        # Placeholder implementation
        return f"YahooFinance real-time data for {symbol}"
