# tests/test_factory.py
import unittest
from src.data_sources.factory import DataSourceFactory
from src.data_sources.base import DataSource

class TestDataSourceFactory(unittest.TestCase):
    def test_get_data_source_alpha_vantage(self):
        data_source = DataSourceFactory.get_data_source("alpha_vantage")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Alpha Vantage")
        self.assertTrue(callable(data_source.get_historical_data))
        self.assertTrue(callable(data_source.get_realtime_data))

    def test_get_data_source_yahoo_finance(self):
        data_source = DataSourceFactory.get_data_source("yahoo_finance")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Yahoo Finance")
        self.assertTrue(callable(data_source.get_historical_data))
        self.assertTrue(callable(data_source.get_realtime_data))

    def test_get_data_source_iex_cloud(self):
        data_source = DataSourceFactory.get_data_source("iex_cloud")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "IEX Cloud")
        self.assertTrue(callable(data_source.get_historical_data))
        self.assertTrue(callable(data_source.get_realtime_data))

    def test_get_data_source_investing_com(self):
        data_source = DataSourceFactory.get_data_source("investing_com")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Investing.com")
        self.assertTrue(callable(data_source.get_historical_data))
        self.assertTrue(callable(data_source.get_realtime_data))

    def test_get_data_source_quandl(self):
        data_source = DataSourceFactory.get_data_source("quandl")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Quandl")
        self.assertTrue(callable(data_source.get_historical_data))
        self.assertTrue(callable(data_source.get_realtime_data))

    def test_get_data_source_invalid(self):
        with self.assertRaises(ValueError) as context:
            DataSourceFactory.get_data_source("invalid_source")
        self.assertEqual(str(context.exception), "Unsupported API: invalid_source")

if __name__ == "__main__":
    unittest.main()
