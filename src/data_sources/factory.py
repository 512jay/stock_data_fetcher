# src/data_sources/factory.py
from src.data_sources.base import DataSource
from src.data_sources.alpha_vantage import AlphaVantageDataSource
from src.data_sources.iex_cloud import IEXCloudDataSource
from src.data_sources.investing_com import InvestingComDataSource
from src.data_sources.quandl import QuandlDataSource
from src.data_sources.yahoo_finance import YahooFinanceDataSource


class DataSourceFactory:
    @staticmethod
    def get_data_source(self, source_name: str) -> DataSource:
        if source_name == "alpha_vantage":
            return AlphaVantageDataSource()
        elif source_name == "yahoo_finance":
            return YahooFinanceDataSource()
        elif source_name == "quandl":
            return QuandlDataSource()
        elif source_name == "iex_cloud":
            return IEXCloudDataSource()
        elif source_name == "investing_com":
            return InvestingComDataSource()
        else:
            raise ValueError("Unsupported API")
