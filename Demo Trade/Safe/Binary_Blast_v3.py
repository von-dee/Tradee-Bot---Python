from config import Connect
from order import Order
from datetime import datetime
import datetime as dt
import numpy
import talib
import time
import random, string

class Main:
    def __init__(self):

        self.client = Connect().make_connection()
        self.client.API_URL = 'http://testnet.binance.vision/api'

        print("logged in")


        # exchange_info = self.client.get_exchange_info()

        # symbols = exchange_info['symbols']


        # print(symbols)

        self.trade_type = 'spot' # spot | margin | futures

        self.trade_count = 0
        self.datadate = []
        self.dataclose = []
        self.dataopen = []
        self.datalow = []
        self.datahigh = []
        self.currentposition = None
        self.islong = None

        self.init_time = time.time()
        self.trade_timeframe = 1
        self.run = None
        self.orderfill_price = None

        self.trade_data = {}


        while True:
            print(self.isNewCandle())
            if self.isNewCandle() == 0:
                print('New Candle started')
                print(time.time())
                self.start_trade()
                break


    def isNewCandle(self):
        # if 1min : +1, 5min : -2, 15min : -2

        remainder = (time.time() - 2) % (60 * self.trade_timeframe)
        return round(remainder)


    def strategy_blast(self):
        def code_blast(self, id):
            x1 = ((self.dataclose[id] + self.datalow[id]) * (self.dataopen[id] + self.datahigh[id])) / 2
            y1 = ((self.dataclose[id] + self.datahigh[id]) * (self.dataopen[id] + self.datalow[id])) / 2
            spike = (x1/y1)

            return spike

        #Trade Logic Check
        spike_1 = code_blast(self,len(self.dataclose)-3)
        spike = code_blast(self,len(self.dataclose)-2)


        if spike_1 < 1 and spike >= 1:
            buy = True
        else:
            buy = False
        
        if spike_1 > 1 and spike <= 1:
            sell = True
        else:
            sell = False

        return {
            "buy" : buy,
            "sell" : sell,
        }     


    def gen_tradecode(self):
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return x  


    def get_date(self):
        now = datetime.now()
        date_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return date_string


    def start_trade(self):

        self.trading = Order()
        print("Starting new trade...")

        while True:
            try:
                #Change date and/or interval for different time frame
                klines = self.client.get_historical_klines("BTCUSDT", self.client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
            except: 
                print('Timeout! Waiting for time binance to respond...')
                time.sleep(120)
                print('Trying to connect agian...')
                klines = self.client.get_historical_klines("BTCUSDT", self.client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

            prices = []
            for i in klines:
                prices.append(float(i[4]))
                self.datadate.append(float(i[0]))
                self.dataopen.append(float(i[1]))
                self.datahigh.append(float(i[2]))
                self.datalow.append(float(i[3]))
                self.dataclose.append(float(i[4]))
        

            #Trade Logic Check
            response = self.strategy_blast()
            
            self.trade_count +=1
            

            if response.get('buy'):
                if self.islong == None:
                    self.log_activity(len(self.dataclose)-2, 'BUY')
                    self.currentposition = "BUY"
                    self.islong = True
                    print('BUY order placed at Last Price : ', prices[len(prices)-2], ' ', self.get_date())
                    # self.order_to_track = self.trading.sell(prices[len(prices)-1])

                    self.trade_data['Trade #'] = self.trade_count
                    self.trade_data['Entry Type'] = 'Entry Long'
                    self.trade_data['Entry Signal'] = 'Buy'
                    self.trade_data['Entry Date/Time'] = self.get_date()
                    self.trade_data['Entry Price'] = prices[len(prices)-1]

                    self.orderfill_price = float(prices[len(prices)-1])

                    self.track_trade_demo()

            elif response.get('sell'):
                if self.islong == None:
                    self.log_activity(len(self.dataclose)-2, 'SELL')
                    self.currentposition = "SELL"
                    self.islong = False
                    print('SELL order placed at Last Price : ', prices[len(prices)-2], ' ', self.get_date())
                    # self.order_to_track = self.trading.buy(prices[len(prices)-1])

                    self.trade_data['Trade #'] = self.trade_count
                    self.trade_data['Entry Type'] = 'Entry Short'
                    self.trade_data['Entry Signal'] = 'Sell'
                    self.trade_data['Entry Date/Time'] = self.get_date()
                    self.trade_data['Entry Price'] = prices[len(prices)-1]

                    self.orderfill_price = float(prices[len(prices)-1])

                    self.track_trade_demo()

            else:
                # self.currentposition = None
                self.islong = None
                time.sleep(1.5)
                print('Last Price : ', prices[len(prices)-1])
                print('No enter points, looking agian...')        


    def lastclose_value(self):

        try:
            #Change date and/or interval for different time frame
            klines = self.client.get_historical_klines("BTCUSDT", self.client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        except: 
            print('Timeout! Waiting for time binance to respond...')
            time.sleep(120)
            print('Trying to connect agian...')
            klines = self.client.get_historical_klines("BTCUSDT", self.client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

        prices = []
        for i in klines:
            prices.append(float(i[4]))
            self.datadate.append(float(i[0]))
            self.dataopen.append(float(i[1]))
            self.datahigh.append(float(i[2]))
            self.datalow.append(float(i[3]))
            self.dataclose.append(float(i[4]))

        klines = self.client.get_historical_klines("BTCUSDT", self.client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        
        return klines[len(klines)-1][4]
        

    def track_trade_demo(self):
        #How much price changed in % based on current price and order price

        def precent_change(current, previous):
            if current == previous:
                return 100.0
            try:
                return (abs(current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return 0

        while True:
            time.sleep(1.5)

            self.last_price = float(self.lastclose_value())

            print("Fill: ", self.orderfill_price," Close: ", self.last_price)

            # PERCENT TRAIL
            change = precent_change(self.orderfill_price, self.last_price)
            change_trail = precent_change(self.orderfill_price, self.orderfill_price-10)


            if (self.currentposition == 'BUY') and (self.orderfill_price > self.last_price):
                change_print = change*-1
            else:
                change_print = change


            if (self.currentposition == 'SELL') and (self.orderfill_price < self.last_price):
                change_print = change*-1
            else:
                change_print = change


            print("Target trail: ", change_trail," Current Change: ", change_print)

            EndTrade = False

            if(self.currentposition == 'BUY') and change_trail*-1 >= change*-1:
                self.trade_data['Exit Trigger'] = 'BUY Percent Trail'
                print("End Trade - BUY Percent Trail: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True
                
            if(self.currentposition == 'SELL') and change_trail <= change:
                self.trade_data['Exit Trigger'] = 'SELL Percent Trail'
                print("End Trade - SELL Percent Trail: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True


            # STOP LOSS
            if(self.currentposition == 'BUY') and (self.last_price >= self.orderfill_price-10) :
                self.trade_data['Exit Trigger'] = 'BUY Percent Stop Loss'
                print("End Trade - BUY Percent Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            if(self.currentposition == 'SELL') and (self.last_price >= self.orderfill_price+10) :
                self.trade_data['Exit Trigger'] = 'SELL Percent Stop Loss'
                print("End Trade - SELL Percent Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True



            # STRATEGY CLOSE
            response = self.strategy_blast()
            
            if (self.currentposition == 'BUY') and response.get('buy') == False:
                self.trade_data['Exit Trigger'] = 'BUY Strategy Close'
                print("End Trade - BUY Strategy Close: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            elif (self.currentposition  == 'SELL') and response.get('sell') == False:
                self.trade_data['Exit Trigger'] = 'SELL Strategy Close'
                print("End Trade - SELL Strategy Close: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = False


            # END TRADE CONDITION
            if EndTrade == True:
                self.end_trade()
                print('Current trade ended with profit  of:', change_print,'%')
                time.sleep(1.5)

                try:

                    self.start_trade()

                except:
                    print("Can't make new trade, trying agian in 120 sec...")
                    time.sleep(120)
                    self.start_trade()

            else:
                
                print("Current trade profit: ", format(change,'2f'),"% at close: ", self.last_price)


    def track_trade(self):
        #How much price changed in % based on current price and order price

        def precent_change(current, previous):
            if current == previous:
                return 100.0
            try:
                return (abs(current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return 0

        while True:
            time.sleep(1.5)

            try:
                self.last_price = self.client.get_recent_trades(symbol='BTCUSDT')[-1]['price']
            except: 
                print('Timeout! Waiting for  binance to respond...')
                time.sleep(120)
                print('Trying to connect agian...')
                self.last_price = self.client.get_recent_trades(symbol='BTCUSDT')[-1]['price']

            try:
                self.orderfill_price = self.order_to_track['fills'][0]['price']
            except: 
                print('Timeout! Waiting for  binance to respond...')
                time.sleep(120)
                print('Trying to connect agian...')
                self.orderfill_price = self.order_to_track['fills'][0]['price']


            change = precent_change(self.orderfill_price, self.last_price)
            change_trail = precent_change(self.orderfill_price, self.orderfill_price-100)
            

            if(self.order_to_track['side'] == 'BUY') and change_trail*-1 >= change*-1:
                EndTrade = True
                self.trade_data['Percentage Trail BUY']
                

            if(self.order_to_track['side'] == 'SELL') and change_trail <= change:
                EndTrade = True
                self.trade_data['Percentage Trail SELL']


            if (self.order_to_track['side']=='BUY') and (self.islong == None):
                EndTrade = True
                self.trade_data['BUY Close']
            elif (self.order_to_track['side']=='SELL') and (self.islong == None):
                EndTrade = True
                self.trade_data['SELL Close']


            if EndTrade == True:
                self.end_trade()
                print('Current trade ended with profit  of:', change,'%')
                time.sleep(1.5)

                try:

                    self.start_trade()

                except:
                    print("Can't make new trade, trying agian in 120 sec...")
                    time.sleep(120)
                    self.start_trade()

            else:
                
                print("Current trade profit: ", format(change,'2f'),"%")


    def end_trade(self):
        # self.trading.close_order(self.order_to_track['executedQty'], self.order_to_track['side'])

        if self.currentposition == 'BUY':
            self.trade_data['Exit Type'] = 'Exit Long'
            self.trade_data['Exit Signal'] = 'Buy'
            self.trade_data['Exit Date/Time'] = self.get_date()
            self.trade_data['Exit Price'] = self.lastclose_value()

        elif  self.currentposition == 'SELL':
            self.trade_data['Exit Type'] = 'Exit Short'
            self.trade_data['Exit Signal'] = 'Sell'
            self.trade_data['Exit Date/Time'] = self.get_date()
            self.trade_data['Exit Price'] = self.lastclose_value()

        self.log_trade()

        print('End. Order finished successfully')


    def log_activity(self,id, position):
        with open('Results/ActivityLog_Binary_Blast_v3.csv', 'a') as d:
            d.write(f'{self.datadate[id]}, {self.dataopen[id]}, {self.datahigh[id]}, {self.datalow[id]}, {self.dataclose[id]}, {position}\n')
    

    def log_trade(self):

        tradeno = self.trade_data['Trade #'] 
        entrytype = self.trade_data['Entry Type']
        entrysignal = self.trade_data['Entry Signal']
        entrydatetime = self.trade_data['Entry Date/Time']
        entryprice = self.trade_data['Entry Price']
        exittype = self.trade_data['Exit Type']
        exitsignal = self.trade_data['Exit Signal']
        exitdatetime = self.trade_data['Exit Date/Time']
        exitprice = self.trade_data['Exit Price']
        exittrigger = self.trade_data['Exit Trigger']


        with open('Results/TradeLog_Binary_Blast_v3.csv', 'a') as d:
            d.write(f'{tradeno}, {entrytype}, {entrysignal}, {entrydatetime}, {entryprice}, {exittype}, {exitsignal}, {exitdatetime}, {exitprice}, {exittrigger}\n')

Main()
