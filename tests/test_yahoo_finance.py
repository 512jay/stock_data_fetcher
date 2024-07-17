# /tests/test_yahoo_finance.py

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.data_sources.yahoo_finance import YahooFinanceDataSource
from src.utils.exceptions import StockDataFetcherError, InvalidSymbolError
from src.utils.logging_config import setup_logging

logger = setup_logging()

class TestYahooFinanceDataSource(unittest.TestCase):
    """
    Test cases for the YahooFinanceDataSource class.
    """

    def setUp(self):
        """
        Set up the test environment before each test method.
        """
        self.data_source = YahooFinanceDataSource()
        logger.info(f"Starting test: {self._testMethodName}")

    def tearDown(self):
        """
        Clean up after each test method.
        """
        logger.info(f"Finished test: {self._testMethodName}")
        logger.info("-" * 40)

    @patch('yfinance.Ticker')
    def test_get_historical_data_success(self, mock_ticker):
        """
        Test successful retrieval of historical data.
        """
        mock_history = MagicMock()
        mock_history.empty = False
        mock_history.reset_index.return_value.to_dict.return_value = [
            {'Date': '2023-01-01', 'Open': 100, 'High': 110, 'Low': 95, 'Close': 105, 'Volume': 1000000},
            {'Date': '2023-01-02', 'Open': 105, 'High': 115, 'Low': 100, 'Close': 110, 'Volume': 1200000}
        ]
        mock_ticker.return_value.history.return_value = mock_history

        result = self.data_source.get_historical_data('AAPL', '2023-01-01', '2023-01-02')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Date'], '2023-01-01')
        self.assertEqual(result[1]['Close'], 110)

    @patch('yfinance.Ticker')
    def test_get_historical_data_empty(self, mock_ticker):
        """
        Test handling of empty historical data.
        """
        mock_history = MagicMock()
        mock_history.empty = True
        mock_ticker.return_value.history.return_value = mock_history

        with self.assertRaises(InvalidSymbolError):
            self.data_source.get_historical_data('INVALID', '2023-01-01', '2023-01-02')

    @patch('yfinance.Ticker')
    def test_get_historical_data_error(self, mock_ticker):
        """
        Test handling of yfinance errors.
        """
        mock_ticker.return_value.history.side_effect = Exception("API Error")

        with self.assertRaises(StockDataFetcherError):
            self.data_source.get_historical_data('AAPL', '2023-01-01', '2023-01-02')

    @patch('yfinance.Ticker')
    def test_get_realtime_data_success(self, mock_ticker):
        """
        Test successful retrieval of real-time data.
        """
        mock_info = {
            'currentPrice': 150.0,
            'change': 2.5,
            'changePercent': 1.67,
            'volume': 1000000,
            'regularMarketTime': int(datetime.now().timestamp())
        }
        mock_ticker.return_value.info = mock_info

        result = self.data_source.get_realtime_data('AAPL')

        self.assertEqual(result['symbol'], 'AAPL')
        self.assertEqual(result['price'], 150.0)
        self.assertEqual(result['change'], 2.5)
        self.assertEqual(result['change_percent'], 1.67)
        self.assertEqual(result['volume'], 1000000)

    @patch('yfinance.Ticker')
    def test_get_realtime_data_empty(self, mock_ticker):
        """
        Test handling of empty real-time data.
        """
        mock_ticker.return_value.info = {}

        with self.assertRaises(InvalidSymbolError):
            self.data_source.get_realtime_data('INVALID')

    @patch('yfinance.Ticker')
    def test_get_realtime_data_error(self, mock_ticker):
        """
        Test handling of yfinance errors in real-time data retrieval.
        """
        mock_ticker.return_value.info = {'currentPrice': 100}  # Missing required keys

        with self.assertRaises(StockDataFetcherError):
            self.data_source.get_realtime_data('AAPL')

if __name__ == '__main__':
    unittest.main()
