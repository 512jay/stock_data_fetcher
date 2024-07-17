# /src/stock_data_fetcher/main.py

import argparse
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from stock_data_fetcher.data_sources.factory import DataSourceFactory
from stock_data_fetcher.utils.logging_config import setup_logging
from stock_data_fetcher.utils.exceptions import StockDataFetcherError, InvalidSymbolError, DateRangeError
from stock_data_fetcher.utils.input_utils import get_date_input
from stock_data_fetcher.app import app

load_dotenv()

logger = setup_logging()

def main():
    """
    Main function to fetch stock data from various sources.
    Parses command-line arguments, gets the appropriate data source,
    and fetches historical data for a specified stock.
    """
    parser = argparse.ArgumentParser(description="Fetch stock data from various sources.")
    parser.add_argument("--api", type=str, help="The name of the API to use (e.g., alpha_vantage, yahoo_finance)")
    parser.add_argument("--symbol", type=str, help="The stock symbol to fetch data for")
    parser.add_argument("--web", action="store_true", help="Run the web interface")
    args = parser.parse_args()

    if args.web:
        logger.info("Starting web interface")
        app.run(debug=True)
        return

    try:
        api_name = args.api or os.getenv("API_NAME") or input("Enter the API name (e.g., alpha_vantage, yahoo_finance): ")
        symbol = args.symbol or input("Enter the stock symbol (e.g., AAPL): ")

        if not symbol:
            raise InvalidSymbolError("Stock symbol cannot be empty")

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        start_date = get_date_input(f"Enter start date (default: {start_date}): ") or start_date
        end_date = get_date_input(f"Enter end date (default: {end_date}): ") or end_date

        if start_date > end_date:
            raise DateRangeError("Start date cannot be after end date")

        logger.info(f"Fetching data for {symbol} from {api_name} between {start_date} and {end_date}")

        data_source = DataSourceFactory.get_data_source(api_name)
        historical_data = data_source.get_historical_data(symbol, start_date, end_date)
        
        print(f"Historical data for {symbol} from {start_date} to {end_date}:")
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
        print(f"An unexpected error occurred. Please check the logs for more information.")

if __name__ == "__main__":
    main()
