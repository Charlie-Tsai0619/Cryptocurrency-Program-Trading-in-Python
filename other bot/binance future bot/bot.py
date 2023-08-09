import config
from binance.client import Client

binance_client = Client(config.API_KEY, config.API_SECRET)

tik = binance_client.futures_symbol_ticker(symbol='BNBBUSD')
print(tik)
binance_client.futures_change_leverage(symbol='BTCUSDT', leverage=1)
lamo = binance_client.create_order(
    symbol='BNBBUSD',
    type='MARKET',
    side='BUY',
    quantity=0.01
)

print(lamo)

print