from flask import Flask, render_template, request, flash, redirect, jsonify
import config, csv, datetime
import bot as myBot
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
app.debug = True  # Enable reloader and debugger
app.secret_key = b'Huat888'

import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('test.log')
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(message)s|%(pathname)s:%(lineno)d"))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

client = Client(config.API_KEY, config.API_SECRET)


#CCY = "ETHUSDT"
#TF = "M15"

@app.route('/')
def index():
    title = 'Binance Python Trader'
    subtitle = f'{config.CCY} {config.TF}'

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return render_template('index.html', title=title, subtitle=subtitle, symbols=symbols)


@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'], 
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=0 )#request.form['quantity']
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')


@app.route('/sell',  methods=['POST'])
def sell():
    #return 'sell'
    #print("sell")
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'], 
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=0 )#request.form['quantity']
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')    


@app.route('/bot', methods=['POST'])
def bot():
    if request.form['action'] != '':
        myBot.RUN(request.form['action'])
    # return ''
    return redirect('/')    

    


@app.route('/history')
def history():
    # https://api.binance.com/api/v3/ticker/price?symbol=ethusdt
    candlesticks = client.get_historical_klines( f'{config.CCY}', Client.KLINE_INTERVAL_15MINUTE, "14 day ago UTC")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)