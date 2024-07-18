# /src/stock_data_fetcher/data_sources/quandl.py

from typing import Any, Dict, List, Union

import requests

from ..utils.exceptions import APIError, DataSourceError, InvalidSymbolError
from ..utils.logging_config import setup_logging
from .base import DataSource

logger = setup_logging()


class QuandlDataSource(DataSource):
    """
    Quandl data source implementation.
    """

    def __init__(self, api_key: str):
        self.name = "Quandl"
        self.base_url = "https://www.quandl.com/api/v3/datasets"
        self.api_key = api_key

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str, interval: str = "daily"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from Quandl.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).
            interval (str): The time interval between data points.
            Options: 'daily', 'weekly', 'monthly', 'quarterly', 'annual'.
            Default is 'daily'.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            DateRangeError: If the provided date range is invalid.
            APIError: If there's an error with the API request.
            DataSourceError: If there's an error processing the data.
        """
        logger.info(
            f"""Fetching historical data for {symbol} from {start_date} to
              {end_date} with interval {interval}"""
        )

        endpoint = f"{self.base_url}/WIKI/{symbol}.json"
        params: Dict[str, Union[str, int]] = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "collapse": interval,
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "dataset" not in data or "data" not in data["dataset"]:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            column_names = data["dataset"]["column_names"]
            historical_data = [
                {
                    "date": item[column_names.index("Date")],
                    "open": item[column_names.index("Open")],
                    "high": item[column_names.index("High")],
                    "low": item[column_names.index("Low")],
                    "close": item[column_names.index("Close")],
                    "volume": item[column_names.index("Volume")],
                    "interval": interval,
                    "ex_dividend": item[column_names.index("Ex-Dividend")],
                    "split_ratio": item[column_names.index("Split Ratio")],
                    "adj_open": item[column_names.index("Adj. Open")],
                    "adj_high": item[column_names.index("Adj. High")],
                    "adj_low": item[column_names.index("Adj. Low")],
                    "adj_close": item[column_names.index("Adj. Close")],
                    "adj_volume": item[column_names.index("Adj. Volume")],
                }
                for item in data["dataset"]["data"]
            ]

            logger.info(
                f"Successfully fetched {len(historical_data)} data points for {symbol}"
            )
            return historical_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching data from Quandl: {str(e)}")
            raise APIError(f"API error when fetching data from Quandl: {str(e)}")
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error processing data from Quandl: {str(e)}")
            raise DataSourceError(f"Error processing data from Quandl: {str(e)}")

    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve the latest available data for a given symbol from Quandl.
        Note: Quandl doesn't provide real-time data, so we'll fetch the most
        recent data point.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the latest available data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            APIError: If there's an error with the API request.
            DataSourceError: If there's an error processing the data.
        """
        logger.info(f"Fetching latest data for {symbol}")

        endpoint = f"{self.base_url}/WIKI/{symbol}.json"
        params: Dict[str, Union[str, int]] = {"api_key": self.api_key, "limit": 1}

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if (
                "dataset" not in data
                or "data" not in data["dataset"]
                or not data["dataset"]["data"]
            ):
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            column_names = data["dataset"]["column_names"]
            latest_data = data["dataset"]["data"][0]
            realtime_data = {
                "symbol": symbol,
                "date": latest_data[column_names.index("Date")],
                "price": latest_data[column_names.index("Close")],
                "change": latest_data[column_names.index("Close")]
                - latest_data[column_names.index("Open")],
                "change_percent": (
                    (
                        latest_data[column_names.index("Close")]
                        - latest_data[column_names.index("Open")]
                    )
                    / latest_data[column_names.index("Open")]
                )
                * 100,
                "volume": latest_data[column_names.index("Volume")],
                "open": latest_data[column_names.index("Open")],
                "high": latest_data[column_names.index("High")],
                "low": latest_data[column_names.index("Low")],
                "close": latest_data[column_names.index("Close")],
                "ex_dividend": latest_data[column_names.index("Ex-Dividend")],
                "split_ratio": latest_data[column_names.index("Split Ratio")],
                "adj_open": latest_data[column_names.index("Adj. Open")],
                "adj_high": latest_data[column_names.index("Adj. High")],
                "adj_low": latest_data[column_names.index("Adj. Low")],
                "adj_close": latest_data[column_names.index("Adj. Close")],
                "adj_volume": latest_data[column_names.index("Adj. Volume")],
            }

            logger.info(f"Successfully fetched latest data for {symbol}")
            return realtime_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching latest data from Quandl: {str(e)}")
            raise APIError(f"API error when fetching latest data from Quandl: {str(e)}")
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error processing latest data from Quandl: {str(e)}")
            raise DataSourceError(f"Error processing latest data from Quandl: {str(e)}")
