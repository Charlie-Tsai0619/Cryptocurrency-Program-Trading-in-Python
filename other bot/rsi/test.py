import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/bnbbusd@kline_30m"

RSI_PERIOD = 4
RSI_OVERBOUGHT = 83.13  #71.13
RSI_OVERSOLD = 10.13    #13.71 if the market going down use 7.13
TRADE_SYMBOL = 'BNBBUSD'
BUY_QUANTITY = 0.42     #0.42
SELL_QUANTITY = 0.42   #0.419

client = Client(config.API_KEY, config.API_SECRET)

### OCO order -- one cnacel the other 
## OCO order -- suppose I have 5 BNB at $580 using side "Sell" OCO to place a profit taking order $630 ("Price"),
#  ("stopPrice") ($560) should be lower than market price (e.g. $570) as it is set to be a trigger price to place a 
# stop-loss order ("stopLimitPrice") ('500')
order = client.create_oco_order(symbol="BNBBUSD", side= "SELL",
 quantity = 0.021, price= 590, stopPrice= 550, 
    stopLimitPrice = 500, stopLimitTimeInForce = 'GTC')

print(order)
