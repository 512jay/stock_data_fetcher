# /src/utils/exceptions.py


class StockDataFetcherError(Exception):
    """Base exception class for StockDataFetcher"""


class DataSourceError(StockDataFetcherError):
    """Exception raised for errors in the data source"""


class InvalidSymbolError(StockDataFetcherError):
    """Exception raised for invalid stock symbols"""


class DateRangeError(StockDataFetcherError):
    """Exception raised for invalid date ranges"""


class APIError(StockDataFetcherError):
    """Exception raised for API-related errors"""
