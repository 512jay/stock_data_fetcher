# src/data_sources/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DataSource(ABC):
    """
    Abstract base class for data sources.
    All concrete data source classes should inherit from this class and implement
    its methods.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the DataSource.

        Args:
            api_key (Optional[str]): The API key for the data source, if required.
        """
        self.api_key = api_key

    @abstractmethod
    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str, granularity: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).
            granularity (str): The granularity of the data (e.g., "1d", "1h", "5m").

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.
        """
        pass

    @abstractmethod
    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve real-time data for a given symbol.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the real-time data.
        """
        pass
