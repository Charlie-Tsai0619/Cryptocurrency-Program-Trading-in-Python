import csv, asyncio, talib, numpy, config
import define as de
from binance.client import Client
from binance.enums import *
from datetime import datetime

# Making unverified HTTPS requests is strongly discouraged
import urllib3
urllib3.disable_warnings()

# csv file present in same directory
# Python program to delete a csv file 
import os
  
# first check whether file exists or not delete the csv file
file = 'data.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)
  print("file deleted")
else:
  print("file not found")
  open(file, 'w')

## create csv file
open(file, 'w')

# python terminal  to get the data 
# wscat -c "wss://stream.binance.com:9443/ws/bnbbusd@kline_1m" | tee data.csv

# mac time update
# sudo sntp -sS time.apple.com

# pip3 uninstall -r requirements.txt


## constant 
#  purchase
purchase_asset = 'BUSD'
purchase_decimal = 3

# sell
sell_asset = 'BNB'
sell_decimal = 3 

free_BUSD = de.get_balance(purchase_asset, purchase_decimal)
free_BNB = de.get_balance(sell_asset, sell_decimal)


## client
client = Client(config.API_KEY, config.API_SECRET, { "verify": False,"timeout": 20})
            
closes = [] 
candle_closes = []
csv_file = open('data.csv', 'r')
csv_reader = csv.reader(csv_file)


start_order =[]
start_order.append('bot start making orders')


###########################################################################################
async def data():
    global closes, csv_reader, start_order, free_BUSD, free_BUSD 
    while True:
        ## Time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # get close data
        for line in csv_reader:

            # c
            data =(line[10])
            close = data[3:9]
            closes.append(float(close))
            last_close = closes[-1]
            await asyncio.sleep(1)
            np_closes = numpy.array(closes)

            candle_closed = (line[15])

            ## RSI 
            rsi_13 = talib.RSI(np_closes, 7)
            last_rsi_13 =rsi_13[-1]

            last_close = last_close - 0.1
    
            free_BNB = de.get_balance(sell_asset, sell_decimal)
            free_BUSD = de.get_balance(purchase_asset, purchase_decimal)

            
            if len(start_order) ==1:
                print(start_order[0])
                start_order.clear()


                ## initial capital
                if free_BNB < 240:
                    initial_capital = 240
                    print('initial_capital', initial_capital)
                
                else:
                    initial_capital = free_BNB
                    print('initial_capital', initial_capital)

            
            # candle closed 
            if len(candle_closed) < 7:
                candle_closes.append(float(close))

                np_candle_closes = numpy.array(candle_closes)

                closed_rsi_17 = talib.RSI(np_candle_closes, 17) 

                last_closed_rsi_17 = closed_rsi_17[-1]

                # third signal 
                third_rsi = 5
                closed_rsi_5 = talib.RSI(np_candle_closes, third_rsi) 
                third_signal = closed_rsi_5
                third_signal_rsi = third_signal[-1]

                if free_BUSD > 20:

                    if len(closed_rsi_17) < 7:
                        print('candle closed', close, "Current Time", current_time)

                    elif last_rsi_13 < 13.13:
               
                        print('rsi 13 limit buy order send!!')
                        print(last_rsi_13)
                        success = de.buy_limit_order(last_close, 0.4, last_rsi_13)
                        if success:
                            print('order send',current_time)
                    
                    else:

                        if last_closed_rsi_17 < 17.17:  

                            print('candle closed rsi 17 limit buy order send!!')
                            print(last_closed_rsi_17)
                            success = de.buy_limit_order(last_close, 0.4, last_closed_rsi_17)
                            if success:
                                print("Current Time =", current_time)

                        
                        if third_signal_rsi < third_rsi * 1.01:
                        
                            print('third_signal_rsi', third_signal_rsi)    
                            success = de.buy_limit_order(last_close, 0.4, third_signal_rsi)
                            if success:
                                print("Current Time =", current_time)



            elif free_BNB > 0.07:
                oco_order_succeeded = de.oco_order('BNBBUSD', 'SELL', free_BNB, last_close)
                if oco_order_succeeded:
                    print('oco order send', current_time)

            ## check order price
            elif free_BUSD < initial_capital - 70:
                success = de.check_order_price(last_close)
                if success:
                    print("Current Time =", current_time)
            

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(data())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close() 


