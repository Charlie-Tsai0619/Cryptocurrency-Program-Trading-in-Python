import math
import config
from binance.client import Client
from binance.enums import *

## client
client = Client(config.API_KEY, config.API_SECRET)

##
Trading_symbol = 'BNBBUSD'

## constant 
#  purchase
purchase_asset = 'BUSD'
purchase_decimal = 4

# sell
sell_asset = 'BNB'
sell_decimal = 3 

## getting balance 
def get_balance(asset, decimals):
    free_asset = float(client.get_asset_balance(asset, recvWindow=10000)['free'])
    multiplier = 10 ** decimals
    return math.floor(free_asset * multiplier) / multiplier

def get_locked_balance(asset):
    free_asset = float(client.get_asset_balance(asset, recvWindow=10000)['locked'])


free_BUSD = get_balance(purchase_asset, purchase_decimal)
free_BNB = get_balance(sell_asset, sell_decimal)

# checking order price 
def check_order_price(last_price):
    open_orders = client.get_open_orders()
    if len(open_orders) > 0:
        open_order = str(open_orders[0])
        order_last_price = open_order[131:140]
        order_id = open_order[33:43]
        buy = 'BUY'

        if buy in open_order:
        
            order_last_price = str(order_last_price)
            last_price = last_price -2.3 
            last_price = str(last_price) 

            if last_price > order_last_price:
                cancel_order = client.cancel_order(symbol = Trading_symbol, orderId = order_id)
                print(cancel_order)
                print('order canceled')

# purchase power busd
def purchase_power(avilable_asset, price , decimals):
    free_asset = float(avilable_asset/price)
    multiplier = 10 ** decimals
    return math.floor(free_asset * multiplier) / multiplier


## OCO order -- one cnacel the other 
## OCO order -- suppose I have 5 BNB at $580 using side "Sell" OCO to place a profit taking order ("Price"),
#  ("stopPrice") should be lower than market price as it is set to be a trigger price to place a 
#  stop-loss order ("stopLimitPrice")

def oco_order(symbol, side, quantity, buying_price):
    try:
        oco_order = client.create_oco_order(symbol= symbol, side= side, 
                    quantity = quantity , 
                    price= buying_price +1.7 , stopPrice= buying_price -0.6, 
                    stopLimitPrice = buying_price-0.5, stopLimitTimeInForce = 'GTC')
        print('oco order send')
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def buy_limit_order(buying_price, Buy_quantity, what_rsi):
      
    def order(side, price, quantity, symbol,order_type = ORDER_TYPE_LIMIT_MAKER):
        try:
            buy_order = client.create_order(symbol = symbol, price = price, side = side, type = order_type, 
            quantity = quantity)

        except Exception as e:
            print("an exception occured - {}".format(e))
            return False

        return True

    if free_BUSD > 20 and what_rsi == 'last_closed_rsi_17':

        Buy_quantity = purchase_power(free_BUSD , buying_price, 3)
        order_succeeded = order('BUY', buying_price, Buy_quantity, "BNBBUSD")

        if order_succeeded:
            print('last_closed_rsi_17 limit  buy order send')


    if free_BUSD > 20 and what_rsi == 'last_closed_rsi_4':

        # only buy 20 BUSD
        Buy_quantity = purchase_power(20, buying_price, 3)
        first_order_succeeded = order('BUY', buying_price, Buy_quantity, "BNBBUSD")

        if first_order_succeeded:
            print('first limit buy order send')

        # only buy 20 BUSD
        Buy_quantity = purchase_power(20, buying_price -0.3, 3)
        sec_order_succeeded = order('BUY', buying_price-0.3, Buy_quantity, "BNBBUSD")

        if sec_order_succeeded:
            print('sec limit buy order send ')


    else:
        # only buy 10 BUSD
        Buy_quantity = purchase_power(20, buying_price, 3)
        order_succeeded = order('BUY', buying_price, Buy_quantity, "BNBBUSD")

        if order_succeeded:
            print('limit order send')


    # if hows_order == 'False' or free_BUSD > 20:
    #     buying_price = buying_price -0.2
    #     print('order_unsucessful')
    #     print('sending another lower price order')
    #     Buy_quantity = purchase_power(free_BUSD, buying_price, 3)
    #     print(Buy_quantity)
    #     order_succeeded = order('BUY', buying_price, Buy_quantity, "BNBBUSD")
    #     print(order_succeeded)
    
