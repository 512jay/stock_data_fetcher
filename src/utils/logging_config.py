# /src/utils/logging_config.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='stock_data_fetcher.log'):
    """
    Set up logging configuration for the application.

    Args:
        log_file (str): Name of the log file.

    Returns:
        logging.Logger: Configured logger object.
    """
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a logger
    logger = logging.getLogger('StockDataFetcher')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(os.path.join(log_dir, log_file), maxBytes=1024*1024, backupCount=5)

    # Create formatters
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set formatters for handlers
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
