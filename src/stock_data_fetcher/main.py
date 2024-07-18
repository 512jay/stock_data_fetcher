# /src/stock_data_fetcher/main.py

# /src/stock_data_fetcher/main.py

import argparse
import os
import webbrowser
from datetime import datetime, timedelta
from threading import Timer

from dotenv import load_dotenv

from .app import app
from .data_sources.factory import DataSourceFactory
from .utils.exceptions import DateRangeError, InvalidSymbolError, StockDataFetcherError
from .utils.input_utils import get_date_input
from .utils.logging_config import setup_logging

load_dotenv()

logger = setup_logging()


def open_browser():
    """Open the default web browser to the application URL."""
    webbrowser.open_new("http://127.0.0.1:5000/")


def start_browser_timer():
    """Start a timer to open the browser after a short delay."""
    Timer(1.25, open_browser).start()


def main():
    """
    Main function to fetch stock data from various sources.
    Parses command-line arguments, gets the appropriate data source,
    and fetches historical data for a specified stock.
    """
    parser = argparse.ArgumentParser(
        description="Fetch stock data from various sources."
    )
    parser.add_argument(
        "--api",
        type=str,
        help="The name of the API to use (e.g., alpha_vantage, yahoo_finance)",
    )
    parser.add_argument("--symbol", type=str, help="The stock symbol to fetch data for")
    parser.add_argument(
        "--granularity",
        type=str,
        default="1d",
        help="Data granularity (e.g., 1m, 5m, 1h, 1d)",
    )
    parser.add_argument("--web", action="store_true", help="Run the web interface")
    args = parser.parse_args()

    if args.web:
        logger.info("Starting web interface")
        start_browser_timer()
        app.run(debug=True, use_reloader=False)
        return

    try:
        api_name = (
            args.api
            or os.getenv("API_NAME")
            or input("Enter the API name (e.g., alpha_vantage, yahoo_finance): ")
        )
        symbol = args.symbol or input("Enter the stock symbol (e.g., AAPL): ")
        granularity = (
            args.granularity
            or input("Enter the data granularity (default: 1d): ")
            or "1d"
        )

        if not symbol:
            raise InvalidSymbolError("Stock symbol cannot be empty")

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        start_date = (
            get_date_input(f"Enter start date (default: {start_date}): ") or start_date
        )
        end_date = get_date_input(f"Enter end date (default: {end_date}): ") or end_date

        if start_date > end_date:
            raise DateRangeError("Start date cannot be after end date")

        logger.info(
            f"""Fetching data for {symbol} from {api_name} between {start_date}
              and {end_date} with granularity {granularity}"""
        )

        data_source = DataSourceFactory.get_data_source(api_name)
        historical_data = data_source.get_historical_data(
            symbol, start_date, end_date, granularity
        )

        print(
            f"""Historical data for {symbol} from {start_date} to {end_date}
              (granularity: {granularity}):"""
        )
        for data_point in historical_data:
            print(data_point)

        realtime_data = data_source.get_realtime_data(symbol)
        print(f"\nReal-time data for {symbol}:")
        print(realtime_data)

        logger.info(f"Successfully fetched data for {symbol}")

    except StockDataFetcherError as e:
        logger.error(f"Error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        print(
            "An unexpected error occurred. Please check the logs for more information."
        )


if __name__ == "__main__":
    main()
