# tests/test_factory.py
import unittest

from src.data_sources.factory import DataSourceFactory
from src.data_sources.base import DataSource


class TestDataSourceFactory(unittest.TestCase):
    def setUp(self):
        self.factory = DataSourceFactory()

    def test_get_data_source_alpha_vantage(self):
        data_source = DataSourceFactory.get_data_source(self, "alpha_vantage")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Alpha Vantage")
        self.assertTrue(hasattr(data_source, "get_historical_data"))
        self.assertTrue(hasattr(data_source, "get_realtime_data"))

    def test_get_data_source_yahoo_finance(self):
        data_source = DataSourceFactory.get_data_source(self, "yahoo_finance")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Yahoo Finance")
        self.assertTrue(hasattr(data_source, "get_historical_data"))
        self.assertTrue(hasattr(data_source, "get_realtime_data"))

    def test_get_data_source_IEXCloudDataSource(self):
        data_source = DataSourceFactory.get_data_source(self, "iex_cloud")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "IEX Cloud")
        self.assertTrue(hasattr(data_source, "get_historical_data"))
        self.assertTrue(hasattr(data_source, "get_realtime_data"))

    def test_get_data_source_InvestingCom(self):
        data_source = DataSourceFactory.get_data_source(self, "investing_com")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Investing Com")
        self.assertTrue(hasattr(data_source, "get_historical_data"))
        self.assertTrue(hasattr(data_source, "get_realtime_data"))

    def test_get_data_source_Quandl(self):
        data_source = DataSourceFactory.get_data_source(self, "quandl")
        self.assertIsInstance(data_source, DataSource)
        self.assertEqual(data_source.name, "Quandl")
        self.assertTrue(hasattr(data_source, "get_historical_data"))
        self.assertTrue(hasattr(data_source, "get_realtime_data"))

    def test_get_data_source_invalid(self):
        with self.assertRaises(ValueError) as context:
            DataSourceFactory.get_data_source(self, "invalid_source")
        self.assertEqual(str(context.exception), "Unsupported API")


if __name__ == "__main__":
    unittest.main()
