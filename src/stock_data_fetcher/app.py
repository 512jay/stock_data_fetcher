# /src/stock_data_fetcher/app.py

import base64
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
from flask import Flask, render_template, request

from .data_sources.factory import DataSourceFactory
from .utils.exceptions import StockDataFetcherError
from .utils.input_utils import validate_symbol
from .utils.logging_config import setup_logging

logger = setup_logging()

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api = request.form["api"]
        symbol = request.form["symbol"].upper()
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        granularity = request.form["granularity"]

        if not validate_symbol(symbol):
            return render_template(
                "index.html",
                error="Invalid stock symbol. Please enter 1-5 uppercase letters.",
            )

        try:
            data_source = DataSourceFactory.get_data_source(api)
            historical_data = data_source.get_historical_data(
                symbol, start_date, end_date, granularity
            )
            realtime_data = data_source.get_realtime_data(symbol)

            logger.debug(f"Historical data: {historical_data[:2]}")
            logger.debug(f"Realtime data: {realtime_data}")

            if not historical_data:
                raise StockDataFetcherError(
                    "No historical data available for the given parameters."
                )

            dates = []
            prices = []
            for data_point in historical_data:
                if isinstance(data_point, dict):
                    date = data_point.get("Date")
                    close = data_point.get("Close")
                    if date and close is not None:
                        try:
                            dates.append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
                        except ValueError:
                            dates.append(datetime.strptime(date, "%Y-%m-%d"))
                        prices.append(close)
                    else:
                        logger.warning(f"Incomplete data point: {data_point}")
                else:
                    logger.warning(f"Unexpected data point structure: {data_point}")

            if not dates or not prices:
                raise StockDataFetcherError(
                    "Unable to extract valid date and price data."
                )

            plt.figure(figsize=(10, 5))
            plt.plot(dates, prices)
            plt.title(f"{symbol} Stock Price")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.xticks(rotation=45)
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

            return render_template(
                "results.html",
                realtime_data=realtime_data,
                historical_data=historical_data,
                chart=plot_data,
            )

        except StockDataFetcherError as e:
            logger.error(f"StockDataFetcherError: {str(e)}")
            return render_template("index.html", error=str(e))
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return render_template(
                "index.html",
                error="An unexpected error occurred. Please try again later.",
            )

    # GET request
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
