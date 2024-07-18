# /src/stock_data_fetcher/data_sources/factory.py

import os
from typing import Dict, Type

from .alpha_vantage import AlphaVantageDataSource
from .base import DataSource
from .iex_cloud import IEXCloudDataSource
from .investing_com import InvestingComDataSource
from .quandl import QuandlDataSource
from .yahoo_finance import YahooFinanceDataSource


class DataSourceFactory:
    """Factory class for creating data source instances."""

    data_sources: Dict[str, Type[DataSource]] = {
        "alpha_vantage": AlphaVantageDataSource,
        "yahoo_finance": YahooFinanceDataSource,
        "iex_cloud": IEXCloudDataSource,
        "investing_com": InvestingComDataSource,
        "quandl": QuandlDataSource,
    }

    @classmethod
    def get_data_source(cls, source_name: str) -> DataSource:
        """
        Get a data source instance based on the source name.

        Args:
            source_name (str): The name of the data source.

        Returns:
            DataSource: An instance of the specified data source.

        Raises:
            ValueError: If an unsupported API is specified or if the API key is missing.
        """
        if source_name not in cls.data_sources:
            raise ValueError(f"Unsupported API: {source_name}")

        data_source_class = cls.data_sources[source_name]

        if source_name in ["alpha_vantage", "iex_cloud", "quandl"]:
            api_key = cls._get_api_key(source_name)
            return data_source_class(api_key)

        return data_source_class()

    @staticmethod
    def _get_api_key(source_name: str) -> str:
        """
        Get the API key for a given data source from environment variables.

        Args:
            source_name (str): The name of the data source.

        Returns:
            str: The API key.

        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        api_key = os.getenv(f"{source_name.upper()}_API_KEY")
        if not api_key:
            raise ValueError(
                f"API key for {source_name} not found in environment variables"
            )
        return api_key
