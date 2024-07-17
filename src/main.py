# src/main.py
import argparse
import os

from dotenv import load_dotenv

from src.data_sources.factory import DataSourceFactory

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Fetch stock data from various sources."
    )
    parser.add_argument(
        "--api",
        type=str,
        help="The name of the API to use (e.g., alpha_vantage, yahoo_finance)",
    )
    args = parser.parse_args()

    api_name = args.api if args.api else os.getenv("API_NAME")
    if not api_name:
        api_name = input(
            """Enter the API name (e.g., alpha_vantage, yahoo_finance, quandl,
             iex_cloud, investing_com): """
        )

    data_source = DataSourceFactory.get_data_source(api_name)
    historical_data = data_source.get_historical_data(
        "AAPL", "2022-01-01", "2022-12-31"
    )
    print(historical_data)


if __name__ == "__main__":
    main()
