from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load data (no model re‑sampling)
df = pd.read_csv('data/BrentOilPrices.csv', parse_dates=['Date'])
df.sort_values('Date', inplace=True)
df.set_index('Date', inplace=True)
df['log_return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
df.dropna(inplace=True)

# Hardcoded results from your notebook
CHANGE_DATE = '2013-04-11'
MU1 = 0.00017
MU2 = 0.0005
IMPACT = 0.033  # percent

# Load events
events = pd.read_csv('data/events.csv', parse_dates=['event_date'])

@app.route('/')
def index():
    return render_template('dashboard.html',
                           change_date=CHANGE_DATE,
                           mu1=f"{MU1:.4f}",
                           mu2=f"{MU2:.4f}",
                           impact=f"{IMPACT:.2f}")

@app.route('/api/prices')
def prices():
    start = request.args.get('start')
    end = request.args.get('end')
    if start and end:
        mask = (df.index >= start) & (df.index <= end)
        filtered = df.loc[mask]
    else:
        filtered = df
    data = filtered[['Price']].reset_index()
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/events')
def events_api():
    data = events.copy()
    data['event_date'] = data['event_date'].dt.strftime('%Y-%m-%d')
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/change_point')
def change_point_api():
    return jsonify({
        'date': CHANGE_DATE,
        'mu1': MU1,
        'mu2': MU2,
        'impact': IMPACT
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)