# /src/stock_data_fetcher/data_sources/yahoo_finance.py

from datetime import datetime, timedelta
from typing import Any, Dict, List

import yfinance as yf

from ..utils.exceptions import InvalidSymbolError, StockDataFetcherError
from ..utils.logging_config import setup_logging
from .base import DataSource

logger = setup_logging()


class YahooFinanceDataSource(DataSource):
    """
    Yahoo Finance data source implementation.
    """

    def __init__(self):
        self.name = "Yahoo Finance"

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str, granularity: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from Yahoo Finance.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).
            granularity (str): The time interval between data points.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.

        Raises:
            InvalidSymbolError: If no data is found for the given symbol.
            StockDataFetcherError: If there's an error fetching or processing the data.
        """
        try:
            logger.info(
                f"Fetching historical data for {symbol} from {start_date} to {end_date}"
            )
            ticker = yf.Ticker(symbol)

            interval = self._get_interval(granularity)

            # Convert start_date and end_date to datetime objects
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            # For intraday data, Yahoo Finance only provides last 7 days
            if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]:
                if (end - start).days > 7:
                    start = end - timedelta(days=7)
                    logger.warning(
                        f"Adjusted start date to {start.strftime('%Y-%m-%d')} "
                        "due to Yahoo Finance limitations"
                    )

            df = ticker.history(start=start, end=end, interval=interval)

            if df.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                raise InvalidSymbolError(f"No data found for symbol: {symbol}")

            # Reset index to make Date a column
            df = df.reset_index()

            # Check if 'Date' or 'Datetime' column exists
            date_column = next(
                (col for col in df.columns if col.lower() in ["date", "datetime"]), None
            )
            if not date_column:
                logger.error("Date/Datetime column not found in the data")
                raise StockDataFetcherError(
                    "Date/Datetime column not found in the data"
                )

            # Convert Date column to string
            df[date_column] = df[date_column].dt.strftime("%Y-%m-%d %H:%M:%S")

            # Rename columns to ensure consistency
            df = df.rename(
                columns={
                    date_column: "Date",
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Volume": "volume",
                }
            )

            # Convert DataFrame to list of dictionaries
            historical_data = df.to_dict("records")

            logger.info(f"Successfully fetched historical data for {symbol}")
            logger.debug(f"Sample data: {historical_data[:2]}")
            return historical_data

        except InvalidSymbolError:
            raise
        except Exception as e:
            logger.error(f"Error fetching data from Yahoo Finance: {str(e)}")
            raise StockDataFetcherError(
                f"Error fetching data from Yahoo Finance: {str(e)}"
            )

    def _get_interval(self, granularity: str) -> str:
        """
        Convert granularity to yfinance interval format.

        Args:
            granularity (str): The input granularity.

        Returns:
            str: The corresponding yfinance interval.
        """
        granularity_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "60m": "60m",
            "1h": "60m",
            "1d": "1d",
            "5d": "5d",
            "1wk": "1wk",
            "1mo": "1mo",
            "3mo": "3mo",
        }
        return granularity_map.get(granularity, "1d")

    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve real-time data for a given symbol from Yahoo Finance.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the real-time data.

        Raises:
            InvalidSymbolError: If no data is found for the given symbol.
            StockDataFetcherError: If there's an error fetching or processing the data.
        """
        try:
            logger.info(f"Fetching real-time data for {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info

            if not info:
                logger.warning(f"No data found for symbol: {symbol}")
                raise InvalidSymbolError(f"No data found for symbol: {symbol}")

            realtime_data = {
                "symbol": symbol,
                "price": info.get("currentPrice"),
                "change": info.get("change"),
                "change_percent": info.get("changePercent"),
                "volume": info.get("volume"),
                "last_updated": info.get("regularMarketTime"),
            }

            # Check if any required field is missing
            if any(value is None for value in realtime_data.values()):
                logger.error(f"Incomplete real-time data for {symbol}")
                raise StockDataFetcherError(f"Incomplete real-time data for {symbol}")

            logger.info(f"Successfully fetched real-time data for {symbol}")
            return realtime_data

        except InvalidSymbolError:
            raise
        except Exception as e:
            logger.error(f"Error fetching real-time data from Yahoo Finance: {str(e)}")
            raise StockDataFetcherError(
                f"Error fetching real-time data from Yahoo Finance: {str(e)}"
            )
