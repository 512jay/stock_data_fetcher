# /setup.py

from setuptools import setup, find_packages

setup(
    name="stock_data_fetcher",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "yfinance",
        "pandas",
        "python-dotenv",
        "Flask",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "stock_data_fetcher=stock_data_fetcher.main:main",
        ],
    },
)
