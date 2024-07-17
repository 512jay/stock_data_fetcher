# /src/data_sources/quandl.py

import requests
from typing import Any, Dict, List
from datetime import datetime
from .base import DataSource
from ..utils.logging_config import setup_logging
from ..utils.exceptions import DataSourceError, InvalidSymbolError, DateRangeError, APIError

logger = setup_logging()

class QuandlDataSource(DataSource):
    """
    Quandl data source implementation.
    """

    def __init__(self):
        self.name = "Quandl"
        self.base_url = "https://www.quandl.com/api/v3/datasets"
        self.api_key = "your_api_key_here"  # Replace with actual API key in production

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from Quandl.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            DateRangeError: If the provided date range is invalid.
            APIError: If there's an error with the API request.
            DataSourceError: If there's an error processing the data.
        """
        logger.info(f"Fetching historical data for {symbol} from {start_date} to {end_date}")
        
        endpoint = f"{self.base_url}/WIKI/{symbol}.json"
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "dataset" not in data or "data" not in data["dataset"]:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            historical_data = [
                {
                    "date": item[0],
                    "open": item[1],
                    "high": item[2],
                    "low": item[3],
                    "close": item[4],
                    "volume": item[5]
                }
                for item in data["dataset"]["data"]
            ]

            logger.info(f"Successfully fetched {len(historical_data)} data points for {symbol}")
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
        Note: Quandl doesn't provide real-time data, so we'll fetch the most recent data point.

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
        params = {
            "api_key": self.api_key,
            "limit": 1
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if "dataset" not in data or "data" not in data["dataset"] or not data["dataset"]["data"]:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            latest_data = data["dataset"]["data"][0]
            realtime_data = {
                "symbol": symbol,
                "price": latest_data[4],  # Closing price
                "change": latest_data[4] - latest_data[1],  # Close - Open
                "change_percent": ((latest_data[4] - latest_data[1]) / latest_data[1]) * 100,
                "volume": latest_data[5],
                "last_updated": latest_data[0]
            }

            logger.info(f"Successfully fetched latest data for {symbol}")
            return realtime_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching latest data from Quandl: {str(e)}")
            raise APIError(f"API error when fetching latest data from Quandl: {str(e)}")
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error processing latest data from Quandl: {str(e)}")
            raise DataSourceError(f"Error processing latest data from Quandl: {str(e)}")
