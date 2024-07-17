# Stock Data Fetcher

A Python application for fetching historical and real-time stock data from various financial data sources.

## Features

- Fetch historical stock data for a specified date range
- Retrieve real-time stock data
- Support for multiple data sources (Yahoo Finance, Alpha Vantage, etc.)
- Command-line interface for easy data retrieval

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

Run the main script with optional arguments:

```sh
python -m src.main --api yahoo_finance --symbol AAPL
```

If you don't provide command-line arguments, the script will prompt you for the necessary information.

## Running Tests

To run the test suite:

```sh
python -m unittest discover tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/512jay/stock_data_fetcher](https://github.com/512jay/stock_data_fetcher)
