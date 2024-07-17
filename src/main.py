# src/main.py
import argparse
import os

from dotenv import load_dotenv

from .data_sources.factory import DataSourceFactory

load_dotenv()


def main():
    """
    Main function to fetch stock data from various sources.
    Parses command-line arguments, gets the appropriate data source,
    and fetches historical data for AAPL stock.
    """
    parser = argparse.ArgumentParser(
        description="Fetch stock data from various sources."
    )
    parser.add_argument(
        "--api",
        type=str,
        help="The name of the API to use (e.g., alpha_vantage, yahoo_finance)",
    )
    args = parser.parse_args()

    api_name = (
        args.api
        or os.getenv("API_NAME")
        or input(
            """Enter the API name (e.g., alpha_vantage, yahoo_finance, quandl,
             iex_cloud, investing_com): """
        )
    )

    try:
        data_source = DataSourceFactory.get_data_source(api_name)
        historical_data = data_source.get_historical_data(
            "AAPL", "2022-01-01", "2022-12-31"
        )
        print(historical_data)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
