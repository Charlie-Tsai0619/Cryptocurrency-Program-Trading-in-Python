import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/bnbbusd@kline_5m"

RSI_PERIOD = 4
RSI_OVERBOUGHT = 75.13  #71.13
RSI_OVERSOLD = 10.13    #13.71 if the market going down use 7.13
TRADE_SYMBOL = 'BNBBUSD'
BUY_QUANTITY = 0.42     #0.42
SELL_QUANTITY = 0.419   #0.419
Leverage = 5

closes = [] 
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

client.futures_change_leverage(symbol= TRADE_SYMBOL, leverage = Leverage )


def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position
    
    json_message = json.loads(message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        #print("closes")
        #print(closes)

        more_data = len(closes) - RSI_PERIOD * 7
        if more_data < RSI_PERIOD:
            print('bot not start!')

        if more_data > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)

            #print("all rsis calculated so far")
            #print(rsi)
            
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    order_succeeded = order(SIDE_SELL, SELL_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, BUY_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True

                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()