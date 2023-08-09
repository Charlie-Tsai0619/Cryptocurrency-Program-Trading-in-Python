import config, csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

csvfile = open('BNBBUSD_3minutes.csv', 'w', newline='') 
candlestick_writer = csv.writer(csvfile, delimiter=',')

candlesticks = client.get_historical_klines("BNBBUSD", Client.KLINE_INTERVAL_3MINUTE, "1 Jan, 2020", "1 NOV, 2021")

for candlestick in  candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)

csvfile.close()