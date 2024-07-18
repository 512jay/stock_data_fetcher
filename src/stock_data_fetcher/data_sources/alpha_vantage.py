# /src/data_sources/alpha_vantage.py

from datetime import datetime
from typing import Any, Dict, List

import requests

from ..utils.exceptions import APIError, DataSourceError, InvalidSymbolError
from ..utils.logging_config import setup_logging
from .base import DataSource

logger = setup_logging()


class AlphaVantageDataSource(DataSource):
    """
    Alpha Vantage data source implementation.
    """

    def __init__(self, api_key: str):
        self.name = "Alpha Vantage"
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str, interval: str = "daily"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from Alpha Vantage.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).
            interval (str): The time interval between data points.
            Options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly',
            'monthly'. Default is 'daily'.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            DateRangeError: If the provided date range is invalid.
            APIError: If there's an error with the API request.
            DataSourceError: If there's an error processing the data.
        """
        logger.info(
            f"""Fetching historical data for {symbol} from {start_date} to {end_date}
             with interval {interval}"""
        )

        function = self._get_function_for_interval(interval)

        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "full",
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            time_series_key = self._get_time_series_key(function)
            if time_series_key not in data:
                logger.warning(f"No data found for symbol {symbol}")
                raise InvalidSymbolError(f"No data found for symbol {symbol}")

            historical_data = []
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            for date, values in data[time_series_key].items():
                date_obj = datetime.strptime(date[:10], "%Y-%m-%d")
                if start <= date_obj <= end:
                    historical_data.append(
                        {
                            "date": date,
                            "open": float(values["1. open"]),
                            "high": float(values["2. high"]),
                            "low": float(values["3. low"]),
                            "close": float(values["4. close"]),
                            "volume": int(values["5. volume"]),
                            "interval": interval,
                        }
                    )

            logger.info(
                f"Successfully fetched {len(historical_data)} data points for {symbol}"
            )
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

        params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": self.api_key}

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
                "last_updated": quote["07. latest trading day"],
                "open": float(quote["02. open"]),
                "high": float(quote["03. high"]),
                "low": float(quote["04. low"]),
                "previous_close": float(quote["08. previous close"]),
            }

            logger.info(f"Successfully fetched real-time data for {symbol}")
            return realtime_data

        except requests.exceptions.RequestException as e:
            logger.error(
                f"API error when fetching real-time data from Alpha Vantage: {str(e)}"
            )
            raise APIError(
                f"API error when fetching real-time data from Alpha Vantage: {str(e)}"
            )
        except (KeyError, ValueError) as e:
            logger.error(
                f"Error processing real-time data from Alpha Vantage: {str(e)}"
            )
            raise DataSourceError(
                f"Error processing real-time data from Alpha Vantage: {str(e)}"
            )

    def _get_function_for_interval(self, interval: str) -> str:
        """
        Get the appropriate Alpha Vantage API function for the given interval.

        Args:
            interval (str): The time interval between data points.

        Returns:
            str: The corresponding Alpha Vantage API function.

        Raises:
            ValueError: If an invalid interval is provided.
        """
        interval_functions = {
            "1min": "TIME_SERIES_INTRADAY",
            "5min": "TIME_SERIES_INTRADAY",
            "15min": "TIME_SERIES_INTRADAY",
            "30min": "TIME_SERIES_INTRADAY",
            "60min": "TIME_SERIES_INTRADAY",
            "daily": "TIME_SERIES_DAILY",
            "weekly": "TIME_SERIES_WEEKLY",
            "monthly": "TIME_SERIES_MONTHLY",
        }
        if interval not in interval_functions:
            raise ValueError(f"Invalid interval: {interval}")
        return interval_functions[interval]

    def _get_time_series_key(self, function: str) -> str:
        """
        Get the appropriate time series key for the given Alpha Vantage API function.

        Args:
            function (str): The Alpha Vantage API function.

        Returns:
            str: The corresponding time series key in the API response.

        Raises:
            ValueError: If an invalid function is provided.
        """
        time_series_keys = {
            "TIME_SERIES_INTRADAY": "Time Series (1min)",
            "TIME_SERIES_DAILY": "Time Series (Daily)",
            "TIME_SERIES_WEEKLY": "Weekly Time Series",
            "TIME_SERIES_MONTHLY": "Monthly Time Series",
        }
        if function not in time_series_keys:
            raise ValueError(f"Invalid function: {function}")
        return time_series_keys[function]
