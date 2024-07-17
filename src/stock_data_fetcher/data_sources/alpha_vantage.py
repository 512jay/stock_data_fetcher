# /src/data_sources/alpha_vantage.py

import requests
from typing import Any, Dict, List
from datetime import datetime, timedelta
from .base import DataSource
from ..utils.logging_config import setup_logging
from ..utils.exceptions import DataSourceError, InvalidSymbolError, DateRangeError, APIError

logger = setup_logging()

class AlphaVantageDataSource(DataSource):
    """
    Alpha Vantage data source implementation.
    """

    def __init__(self):
        self.name = "Alpha Vantage"
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = "demo"  # Replace with actual API key in production

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from Alpha Vantage.

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
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "full"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "Time Series (Daily)" not in data:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            historical_data = []
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            for date, values in data["Time Series (Daily)"].items():
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                if start <= date_obj <= end:
                    historical_data.append({
                        "date": date,
                        "open": float(values["1. open"]),
                        "high": float(values["2. high"]),
                        "low": float(values["3. low"]),
                        "close": float(values["4. close"]),
                        "volume": int(values["5. volume"])
                    })

            logger.info(f"Successfully fetched {len(historical_data)} data points for {symbol}")
            return historical_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching data from Alpha Vantage: {str(e)}")
            raise APIError(f"API error when fetching data from Alpha Vantage: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing data from Alpha Vantage: {str(e)}")
            raise DataSourceError(f"Error processing data from Alpha Vantage: {str(e)}")

    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve real-time data for a given symbol from Alpha Vantage.

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
        
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "Global Quote" not in data:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            quote = data["Global Quote"]
            realtime_data = {
                "symbol": symbol,
                "price": float(quote["05. price"]),
                "change": float(quote["09. change"]),
                "change_percent": float(quote["10. change percent"].rstrip("%")),
                "volume": int(quote["06. volume"]),
                "last_updated": quote["07. latest trading day"]
            }

            logger.info(f"Successfully fetched real-time data for {symbol}")
            return realtime_data

        except requests.exceptions.RequestException as e:
            logger.error(f"API error when fetching real-time data from Alpha Vantage: {str(e)}")
            raise APIError(f"API error when fetching real-time data from Alpha Vantage: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing real-time data from Alpha Vantage: {str(e)}")
            raise DataSourceError(f"Error processing real-time data from Alpha Vantage: {str(e)}")
