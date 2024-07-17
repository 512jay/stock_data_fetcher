# src/data_sources/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DataSource(ABC):
    """
    Abstract base class for data sources.
    All concrete data source classes should inherit from this class and implement
    its methods.
    """

    @abstractmethod
    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.
        """
        pass

    @abstractmethod
    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Not currently implemented.
        Retrieve real-time data for a given symbol.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the real-time data.
        """
        pass
