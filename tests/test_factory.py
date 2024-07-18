# /tests/test_factory.py

import os
import unittest
from unittest.mock import patch

from stock_data_fetcher.data_sources.base import DataSource
from stock_data_fetcher.data_sources.factory import DataSourceFactory


class TestDataSourceFactory(unittest.TestCase):
    """Test cases for the DataSourceFactory class."""

    @patch.dict(os.environ, {"ALPHA_VANTAGE_API_KEY": "dummy_key"})
    def test_get_data_source_alpha_vantage(self):
        """Test getting Alpha Vantage data source."""
        data_source = DataSourceFactory.get_data_source("alpha_vantage")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Alpha Vantage")

    def test_get_data_source_yahoo_finance(self):
        """Test getting Yahoo Finance data source."""
        data_source = DataSourceFactory.get_data_source("yahoo_finance")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Yahoo Finance")

    @patch.dict(os.environ, {"IEX_CLOUD_API_KEY": "dummy_key"})
    def test_get_data_source_iex_cloud(self):
        """Test getting IEX Cloud data source."""
        data_source = DataSourceFactory.get_data_source("iex_cloud")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "IEX Cloud")

    def test_get_data_source_investing_com(self):
        """Test getting Investing.com data source."""
        data_source = DataSourceFactory.get_data_source("investing_com")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Investing.com")

    @patch.dict(os.environ, {"QUANDL_API_KEY": "dummy_key"})
    def test_get_data_source_quandl(self):
        """Test getting Quandl data source."""
        data_source = DataSourceFactory.get_data_source("quandl")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Quandl")

    def test_get_data_source_invalid(self):
        """Test getting an invalid data source."""
        with self.assertRaises(ValueError) as context:
            DataSourceFactory.get_data_source("invalid_source")
        self.assertEqual(str(context.exception), "Unsupported API: invalid_source")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_data_source_missing_api_key(self):
        """Test getting a data source with a missing API key."""
        with self.assertRaises(ValueError) as context:
            DataSourceFactory.get_data_source("alpha_vantage")
        self.assertEqual(
            str(context.exception),
            "API key for alpha_vantage not found in environment variables"
        )


if __name__ == "__main__":
    unittest.main()
