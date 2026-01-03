from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
from datetime import datetime

app = Flask(__name__)

# YOUR KEYS (replace with your real ones)
ALPACA_API_KEY = "PKVP5SEAT4T63LGA6625GVU4JU"
ALPACA_SECRET_KEY = "4mpL37jy8WYQkqcQ7ssTX1zeTQPKRv2P6e9TuJ8Sccqv"
PAPER = True

SYMBOL = "AAPL"
SHARES_TO_BUY = 10

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url='https://paper-api.alpaca.markets')

@app.route('/webhook', methods=['POST'])
def webhook():
    print(f"{datetime.now()} | Alert received")
    if request.is_json:
        data = request.get_json()
    else:
        data = request.data.decode("utf-8")

    print("Message:", data)

    if "buy" in str(data).lower():
        api.submit_order(symbol=SYMBOL, qty=SHARES_TO_BUY, side='buy', type='market', time_in_force='gtc')
        return jsonify({"status": "bought"}), 200

    if "sell" in str(data).lower():
        api.submit_order(symbol=SYMBOL, qty=SHARES_TO_BUY, side='sell', type='market', time_in_force='gtc')
        return jsonify({"status": "sold"}), 200

    return jsonify({"status": "ignored"}), 200

@app.route('/')
def home():
    return "Bot running"

if __name__ == '__main__':
    print("Bot started – ready for alerts")
    app.run(host='0.0.0.0', port=5000)
