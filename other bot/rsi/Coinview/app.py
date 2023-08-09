
from flask import Flask, render_template, request, flash, redirect, jsonify
import config, csv, datetime
from binance.client import Client
from binance.enums import *

# run this file in temrinal 
# first - set FLASK_ENV=development
# then - flask run

app = Flask(__name__)
app.secret_key = b'somelongrandomstring'

client = Client(config.API_KEY, config.API_SECRET)

app = Flask(__name__)

@app.route("/")
def index():
    title = 'CoinView'

    account = client.get_account()

    balances = account['balances']

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return render_template('index.html', title=title, my_balances=balances, symbols=symbols)

@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'], 
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    return 'sell'

@app.route('/settings')
def settings():
    return 'settings'

@app.route('/history')
def history():
    candlesticks = client.get_historical_klines('BNBBUSD', Client.KLINE_INTERVAL_3MINUTE,'1 Jan, 2020', '22 Jul, 2021')

    processed_candlesticks = []

    for data in candlesticks:
        candlesticks = {
            'time': data[0],
            'open': data[1],
            'high': data[2],
            'low' : data[3],
            'close': data[4]

        }
    return jsonify(candlesticks)
app.run(debug=True)