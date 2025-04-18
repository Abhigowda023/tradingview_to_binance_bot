
from flask import Flask, request, jsonify
from binance.client import Client
import json
import os

app = Flask(__name__)

# Binance API keys from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(API_KEY, API_SECRET)

@app.route('/')
def home():
    return "Binance TradingView Webhook Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)

    # Optional: Secret key check
    if data.get('secret') != os.getenv('WEBHOOK_SECRET'):
        return jsonify({'error': 'Unauthorized'}), 403

    action = data.get('action')
    symbol = data.get('symbol')
    quantity = float(data.get('qty', 0.001))

    try:
        if action == 'BUY':
            order = client.order_market_buy(symbol=symbol, quantity=quantity)
            print(f"BUY ORDER: {order}")
        elif action == 'SELL':
            order = client.order_market_sell(symbol=symbol, quantity=quantity)
            print(f"SELL ORDER: {order}")
        else:
            return jsonify({'error': 'Invalid action'}), 400

        return jsonify({'message': 'Order placed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
