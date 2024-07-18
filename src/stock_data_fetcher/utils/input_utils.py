# /src/utils/input_utils.py

import re
from datetime import datetime

from .logging_config import setup_logging

logger = setup_logging()


def get_date_input(prompt: str) -> str:
    """
    Get a date input from the user and validate it.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: A validated date string in the format YYYY-MM-DD.

    Raises:
        DateRangeError: If the input date is invalid.
    """
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            logger.warning(f"Invalid date format entered: {date_str}")
            print("Invalid date format. Please use YYYY-MM-DD.")


def validate_symbol(symbol: str) -> bool:
    """
    Validate the given stock symbol.

    Args:
        symbol (str): The stock symbol to validate.

    Returns:
        bool: True if the symbol is valid, False otherwise.
    """
    pattern = r"^[A-Z]{1,5}$"
    return bool(re.match(pattern, symbol))
