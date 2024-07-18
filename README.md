# Stock Data Fetcher

A Python application for fetching historical and real-time stock data from various financial data sources.

## Features

- Fetch historical stock data for a specified date range and granularity
- Retrieve real-time stock data
- Support for multiple data sources (Yahoo Finance, Alpha Vantage, etc.)
- Command-line interface for easy data retrieval
- Web interface for interactive use

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/512jay/stock_data_fetcher.git
   cd stock_data_fetcher
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   IEX_CLOUD_API_KEY=your_iex_cloud_api_key
   ```

## Usage

There are several ways to run the Stock Data Fetcher:

### 1. As a Python module (recommended)

This method works best for both the command-line interface and the web interface:

```sh
# For the command-line interface
python -m src.stock_data_fetcher.main --api yahoo_finance --symbol AAPL --granularity 1d

# For the web interface
python -m src.stock_data_fetcher.main --web
```

### 2. Directly running the main script

You can also run the main script directly, but you might need to adjust your `PYTHONPATH`:

```sh
# Set PYTHONPATH (you might want to add this to your .bashrc or .bash_profile)
export PYTHONPATH=$PYTHONPATH:/path/to/stock_data_fetcher

# Then run the script
python src/stock_data_fetcher/main.py --api yahoo_finance --symbol AAPL --granularity 1d
```

### 3. Using the installed package

If you've installed the package (e.g., with `pip install -e .`), you can use the entry point:

```sh
stock_data_fetcher --api yahoo_finance --symbol AAPL --granularity 1d
```

## Command-line Arguments

- `--api`: The name of the API to use (e.g., yahoo_finance, alpha_vantage)
- `--symbol`: The stock symbol to fetch data for (e.g., AAPL)
- `--granularity`: Data granularity (e.g., 1m, 5m, 1h, 1d)
- `--web`: Run the web interface

If you don't provide command-line arguments, the script will prompt you for the necessary information.

## Web Interface

To start the web interface, run:

```sh
python -m src.stock_data_fetcher.main --web
```

Then open a web browser and navigate to `http://localhost:5000`.

## Running Tests

To run the test suite:

```sh
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Jay - [@512jay](https://x.com/512jay) - 512jay@gmail.com

Project Link: [https://github.com/512jay/stock_data_fetcher](https://github.com/512jay/stock_data_fetcher)
