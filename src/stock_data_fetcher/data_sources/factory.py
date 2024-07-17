# src/data_sources/factory.py
from typing import Dict, Type

from .alpha_vantage import AlphaVantageDataSource
from .base import DataSource
from .iex_cloud import IEXCloudDataSource
from .investing_com import InvestingComDataSource
from .quandl import QuandlDataSource
from .yahoo_finance import YahooFinanceDataSource


class DataSourceFactory:
    """
    Factory class for creating data source objects.
    """

    @staticmethod
    def get_data_source(source_name: str) -> DataSource:
        """
        Create and return a data source object based on the given source name.

        Args:
            source_name (str): The name of the data source to create.

        Returns:
            DataSource: An instance of the specified data source.

        Raises:
            ValueError: If an unsupported data source is specified.
        """
        data_sources: Dict[str, Type[DataSource]] = {
            "alpha_vantage": AlphaVantageDataSource,
            "yahoo_finance": YahooFinanceDataSource,
            "quandl": QuandlDataSource,
            "iex_cloud": IEXCloudDataSource,
            "investing_com": InvestingComDataSource,
        }

        if source_name in data_sources:
            return data_sources[source_name]()
        else:
            raise ValueError(f"Unsupported API: {source_name}")
