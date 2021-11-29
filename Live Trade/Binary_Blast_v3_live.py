from config import Connect
from datetime import datetime
from helper import Helper
from strategy import Strategy
from brain import Brain
import datetime as dt
import numpy
# import talib
import time
import random, string

from sqllink import SQLlink


class Main:
    def __init__(self):


        self.client = Connect().make_connection()
        self.client.API_URL = 'http://testnet.binance.vision/api'
        self.helper = Helper()
        self.strategy = Strategy()
        self.brain = Brain()
        print("logged in")


        # exchange_info = self.client.get_exchange_info()
        # symbols = exchange_info['symbols']
        # print(symbols)

        # Parameters to Set
        self.strategy_name = 'Binary Blast V3'
        self.strategy_code = 'STG0000000002'
        self.user_name = 'solo@TLT'
        self.user_code = 'USR0000000002'
        self.user_acc_code = 'ACT0000000003'
        self.trade_type = 'spot' # spot | margin | futures

        self.trade_timeframe = 5
        self.KLINE_INTERVAL = self.client.KLINE_INTERVAL_5MINUTE # KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_1HOUR



        self.trade_count = 0
        self.datadate = []
        self.dataclose = []
        self.dataopen = []
        self.datalow = []
        self.datahigh = []
        self.currentposition = None
        self.islong = None

        self.init_time = time.time()
        
        self.run = None
        self.orderfill_price = None

        self.trade_data = {}

        self.sqllink = SQLlink()
        
        self.start_trade()
    
        


    def start_trade(self):

        #self.trading = Order()
        print("Starting new trade...")

        while True:

            while True:
                print(self.helper.isNewCandle(self.trade_timeframe)) #, end =""
                if self.helper.isNewCandle(self.trade_timeframe) == 0:
                    print('New Candle started', self.helper.get_date())
                    break

            time.sleep(2)
            
            while True:
                gotten_kline = self.helper.get_kline(self.KLINE_INTERVAL)

                prices = gotten_kline.get('prices')
                self.datadate = gotten_kline.get('datadate')
                self.dataopen = gotten_kline.get('dataopen')
                self.datahigh = gotten_kline.get('datahigh')
                self.datalow = gotten_kline.get('datalow')
                self.dataclose = gotten_kline.get('dataclose')

                

                #Trade Logic Check
                response = self.brain.strategy_blast(self)
                
                self.trade_count +=1
                self.orderfill_price = float(self.dataclose[len(self.dataclose)-1])

                print("dataclose lastprice")
                print(self.orderfill_price)

                if response.get('buy'):
                    if self.islong == None:
                        self.helper.log_activity(self, len(self.dataclose)-2, 'BUY')
                        self.currentposition = "BUY"
                        self.islong = True
                        print('BUY order placed at Last Price : ', prices[len(prices)-2], ' ', self.helper.get_date())
                        # self.order_to_track = self.trading.sell(prices[len(prices)-1])

                        self.trade_data['Trade #'] = self.trade_count
                        self.trade_data['Entry Type'] = 'Entry Long'
                        self.trade_data['Entry Signal'] = 'Buy'
                        self.trade_data['Entry Date/Time'] = self.helper.get_date()
                        self.trade_data['Entry Price'] = prices[len(prices)-1]
                        
                        self.strategy.exit(self)

                elif response.get('sell'):
                    if self.islong == None:
                        self.helper.log_activity(self, len(self.dataclose)-2, 'SELL')
                        self.currentposition = "SELL"
                        self.islong = False
                        print('SELL order placed at Last Price : ', prices[len(prices)-2], ' ', self.helper.get_date())
                        # self.order_to_track = self.trading.buy(prices[len(prices)-1])

                        self.trade_data['Trade #'] = self.trade_count
                        self.trade_data['Entry Type'] = 'Entry Short'
                        self.trade_data['Entry Signal'] = 'Sell'
                        self.trade_data['Entry Date/Time'] = self.helper.get_date()
                        self.trade_data['Entry Price'] = prices[len(prices)-1]
                        
                        self.strategy.exit(self)

                else:
                    # self.currentposition = None
                    self.islong = None
                    time.sleep(1.5)
                    print('Last Price : ', prices[len(prices)-1])
                    print('No enter points, looking agian...')        


Main()
