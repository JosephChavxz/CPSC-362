from flask import Flask, jsonify, request
import time
import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/api/finance', methods=['GET'])
def get_finance_data():
    symbol = request.args.get('symbol')
    if symbol not in ['FNGU', 'FNGD']:
        return jsonify({"error": "Invalid symbol. Must be either FNGU or FNGD."}), 400

    # We use the same date range for this example
    period1 = int(time.mktime(datetime.datetime(2020, 12, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
    interval = '1d' # 1d, 1m

    API_endpoint = (
        f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?'
        f'period1={period1}&period2={period2}&interval={interval}'
        '&events=history&includeAdjustedClose=true'
    )

    df = pd.read_csv(API_endpoint)
    # Convert DataFrame to JSON
    data_json = df.to_json(orient="records")

    return jsonify(data_json)

if __name__ == "__main__":
    app.run(debug=True)
