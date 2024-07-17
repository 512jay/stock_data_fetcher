# /src/app.py

from flask import Flask, render_template, request, jsonify
from data_sources.factory import DataSourceFactory
from utils.exceptions import StockDataFetcherError
from utils.logging_config import setup_logging
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
logger = setup_logging()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle both GET and POST requests for the main page.
    GET: Display the form.
    POST: Process the form data and display results.
    """
    if request.method == 'POST':
        api_name = request.form['api']
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            data_source = DataSourceFactory.get_data_source(api_name)
            historical_data = data_source.get_historical_data(symbol, start_date, end_date)
            realtime_data = data_source.get_realtime_data(symbol)

            # Generate chart
            chart = generate_chart(historical_data, symbol)

            return render_template('results.html', 
                                   historical_data=historical_data, 
                                   realtime_data=realtime_data, 
                                   chart=chart)
        except StockDataFetcherError as e:
            logger.error(f"Error occurred: {str(e)}")
            return render_template('index.html', error=str(e))

    return render_template('index.html')

def generate_chart(data, symbol):
    """
    Generate a line chart of closing prices using matplotlib.
    
    Args:
        data (list): List of dictionaries containing historical data.
        symbol (str): Stock symbol for the chart title.
    
    Returns:
        str: Base64 encoded string of the chart image.
    """
    dates = [item['date'] for item in data]
    closing_prices = [item['close'] for item in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closing_prices)
    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True)
