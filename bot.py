from ctypes import wstring_at
import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
# SOCKET = f'wss://stream.binance.com:9443/ws/{config.CCY}@kline_1m'

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.001

closes = []
has_short_position = False #singleton
has_long_position = False #singleton

client = Client(config.API_KEY, config.API_SECRET)

def RUN(action):
    if action == 'START':
        print("bot started...")
        ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
        ws.run_forever()
    if action == 'STOP':
        print("bot stopping...")
        ws.close() # UnboundLocalError: local variable 'ws' referenced before assignment

def orderSend(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('connection opened')

def on_close(ws):
    print('connection closed')

def on_message(ws, message):
    global closes, has_long_position, has_short_position
    
    # print('received message')
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                print("Overbought! Sell!")
                if has_long_position:                        # Close Long
                    order_succeeded = orderSend(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        has_long_position = False
                if has_short_position == False:              # Open Short
                    #order_succeeded = orderSend(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    print("Overbought! Sold!")
                    order_succeeded = True
                    if order_succeeded:
                        has_short_position = True                    
            
            if last_rsi < RSI_OVERSOLD:
                print("OverSold! Buy!")
                if has_short_position:                        # Close Short 
                    order_succeeded = orderSend(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        has_short_position = False
                if has_long_position == False:               # Open Long
                    # order_succeeded = orderSend(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    print("OverSold! Bought!")
                    order_succeeded = True
                    if order_succeeded:
                        has_long_position = True     


