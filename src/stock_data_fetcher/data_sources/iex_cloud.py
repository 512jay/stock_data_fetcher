# /src/data_sources/iex_cloud.py

import requests
from typing import Any, Dict, List
from datetime import datetime
from .base import DataSource
from ..utils.logging_config import setup_logging
from ..utils.exceptions import DataSourceError, InvalidSymbolError, DateRangeError, APIError

logger = setup_logging()

class IEXCloudDataSource(DataSource):
    """
    IEX Cloud data source implementation.
    """

    def __init__(self):
        self.name = "IEX Cloud"
        self.base_url = "https://cloud.iexapis.com/stable"
        self.api_key = "Tpk_your_test_api_key_here"  # Replace with actual API key in production

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from IEX Cloud.

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
        
        endpoint = f"{self.base_url}/stock/{symbol}/chart/range"
        params = {
            "token": self.api_key,
            "from": start_date,
            "to": end_date
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            historical_data = [
                {
                    "date": item["date"],
                    "open": item["open"],
                    "high": item["high"],
                    "low": item["low"],
                    "close": item["close"],
                    "volume": item["volume"]
                }
                for item in data
            ]

            logger.info(f"Successfully fetched {len(historical_data)} data points for {symbol}")
            return historical_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching data from IEX Cloud: {str(e)}")
            raise APIError(f"API error when fetching data from IEX Cloud: {str(e)}")
        except (KeyError, TypeError) as e:
            logger.error(f"Error processing data from IEX Cloud: {str(e)}")
            raise DataSourceError(f"Error processing data from IEX Cloud: {str(e)}")

    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve real-time data for a given symbol from IEX Cloud.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the real-time data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            APIError: If there's an error with the API request.
            DataSourceError: If there's an error processing the data.
        """
        logger.info(f"Fetching real-time data for {symbol}")
        
        endpoint = f"{self.base_url}/stock/{symbol}/quote"
        params = {
            "token": self.api_key
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            realtime_data = {
                "symbol": data["symbol"],
                "price": data["latestPrice"],
                "change": data["change"],
                "change_percent": data["changePercent"],
                "volume": data["volume"],
                "last_updated": data["latestUpdate"]
            }

            logger.info(f"Successfully fetched real-time data for {symbol}")
            return realtime_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching real-time data from IEX Cloud: {str(e)}")
            raise APIError(f"API error when fetching real-time data from IEX Cloud: {str(e)}")
        except (KeyError, TypeError) as e:
            logger.error(f"Error processing real-time data from IEX Cloud: {str(e)}")
            raise DataSourceError(f"Error processing real-time data from IEX Cloud: {str(e)}")
