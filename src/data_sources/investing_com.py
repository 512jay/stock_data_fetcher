# /src/data_sources/investing_com.py

from typing import Any, Dict, List
from datetime import datetime, timedelta
import random
from .base import DataSource
from ..utils.logging_config import setup_logging
from ..utils.exceptions import DataSourceError, InvalidSymbolError, DateRangeError

logger = setup_logging()

class InvestingComDataSource(DataSource):
    """
    Investing.com data source implementation (mock version).
    """

    def __init__(self):
        self.name = "Investing.com"

    def get_historical_data(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve mock historical data for a given symbol and date range.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            start_date (str): The start date for the data range (format: YYYY-MM-DD).
            end_date (str): The end date for the data range (format: YYYY-MM-DD).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the mock historical data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            DateRangeError: If the provided date range is invalid.
            DataSourceError: If there's an error generating mock data.
        """
        logger.info(f"Generating mock historical data for {symbol} from {start_date} to {end_date}")
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start > end:
                raise DateRangeError("Start date must be before end date")
            
            current_date = start
            base_price = random.uniform(50, 200)
            historical_data = []

            while current_date <= end:
                price = base_price + random.uniform(-5, 5)
                historical_data.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "open": round(price, 2),
                    "high": round(price * (1 + random.uniform(0, 0.02)), 2),
                    "low": round(price * (1 - random.uniform(0, 0.02)), 2),
                    "close": round(price * (1 + random.uniform(-0.01, 0.01)), 2),
                    "volume": random.randint(100000, 1000000)
                })
                current_date += timedelta(days=1)
                base_price = historical_data[-1]["close"]

            logger.info(f"Successfully generated {len(historical_data)} data points for {symbol}")
            return historical_data

        except ValueError as e:
            logger.error(f"Invalid date format: {str(e)}")
            raise DateRangeError(f"Invalid date format: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating mock data: {str(e)}")
            raise DataSourceError(f"Error generating mock data: {str(e)}")

    def get_realtime_data(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve mock real-time data for a given symbol.

        Args:
            symbol (str): The stock symbol to retrieve data for.

        Returns:
            Dict[str, Any]: A dictionary containing the mock real-time data.

        Raises:
            InvalidSymbolError: If the provided symbol is invalid.
            DataSourceError: If there's an error generating mock data.
        """
        logger.info(f"Generating mock real-time data for {symbol}")
        
        try:
            if not symbol or not isinstance(symbol, str):
                raise InvalidSymbolError("Invalid symbol provided")

            price = random.uniform(50, 200)
            change = random.uniform(-5, 5)
            realtime_data = {
                "symbol": symbol,
                "price": round(price, 2),
                "change": round(change, 2),
                "change_percent": round((change / price) * 100, 2),
                "volume": random.randint(100000, 1000000),
                "last_updated": datetime.now().isoformat()
            }

            logger.info(f"Successfully generated mock real-time data for {symbol}")
            return realtime_data

        except Exception as e:
            logger.error(f"Error generating mock real-time data: {str(e)}")
            raise DataSourceError(f"Error generating mock real-time data: {str(e)}")
