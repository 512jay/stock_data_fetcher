# /src/data_sources/yahoo_finance.py

import yfinance as yf  # type: ignore
from typing import Any, Dict, List
from .base import DataSource
from ..utils.exceptions import StockDataFetcherError, InvalidSymbolError
from ..utils.logging_config import setup_logging

logger = setup_logging()

class YahooFinanceDataSource(DataSource):
    """
    Yahoo Finance data source implementation using the yfinance library.
    """

    def __init__(self):
        self.name = "Yahoo Finance"

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical data for a given symbol and date range from Yahoo Finance.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the historical data.

        Raises:
            InvalidSymbolError: If no data is found for the given symbol.
            StockDataFetcherError: If there's an error fetching or processing data.
        """
        try:
            logger.info(f"Fetching historical data for {symbol} from {start_date} to {end_date}")
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            if df.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                raise InvalidSymbolError(f"No data found for symbol: {symbol}")

            historical_data = df.reset_index().to_dict('records')
            logger.info(f"Successfully fetched historical data for {symbol}")
            return historical_data

        except InvalidSymbolError:
            raise
        except Exception as e:
            logger.error(f"Error fetching data from Yahoo Finance: {str(e)}")
            raise StockDataFetcherError(f"Error fetching data from Yahoo Finance: {str(e)}")

    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve real-time data for a given symbol from Yahoo Finance.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the real-time data.

        Raises:
            InvalidSymbolError: If no data is found for the given symbol.
            StockDataFetcherError: If there's an error fetching or processing data.
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
                "price": info['currentPrice'],
                "change": info['change'],
                "change_percent": info['changePercent'],
                "volume": info['volume'],
                "last_updated": info['regularMarketTime'],
            }

            logger.info(f"Successfully fetched real-time data for {symbol}")
            return realtime_data

        except KeyError as e:
            logger.error(f"Missing key in Yahoo Finance data: {str(e)}")
            raise StockDataFetcherError(f"Error processing data from Yahoo Finance: {str(e)}")
        except InvalidSymbolError:
            raise
        except Exception as e:
            logger.error(f"Error fetching real-time data from Yahoo Finance: {str(e)}")
            raise StockDataFetcherError(f"Error fetching real-time data from Yahoo Finance: {str(e)}")
