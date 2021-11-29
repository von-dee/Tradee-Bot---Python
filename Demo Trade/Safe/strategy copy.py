from config import Connect
import math
import time

class Strategy:
    def __init__(self):
        self.client = Connect().make_connection()
        
        

        inpLeverage = 1
        inpTakeProfit = 0
        inpStopLoss = 0
        inpTrailStop = 0
        inpTrailOffset = 0

        self.datadate = []
        self.dataclose = []
        self.dataopen = []
        self.datalow = []
        self.datahigh = []

        useLeverage = inpLeverage if inpLeverage >= 1 else 1
        useTakeProfit = inpTakeProfit if inpTakeProfit >= 1 else 0
        useStopLoss = inpStopLoss if inpStopLoss >= 1 else 0
        useTrailStop = inpTrailStop if inpTrailStop >= 1 else 0
        useTrailOffset = inpTrailOffset if inpTrailOffset >= 1 else 0

        self.trade_amount = 50
        commission_value = 0.075

        self.contract_size = self.trade_amount + (self.trade_amount * commission_value)

        self.trailing_points = 100
        self.trailing_price = None
        self.current_price = None

        self.trade_data = {}
        self.change_print = None
        self.profit_percent = 0
        self.drawdown_percent = 0
        self.roundup = 0

    
    def entry(self, id = "Buy", long = True):
    
        def buy(self, last_price):

            try:

                if self.trade_type == 'spot':
                    order = client.create_order(
                    symbol='BTCUSDT',
                    side=self.client.SIDE_BUY,
                    type=self.client.STOP_LOSS,
                    timeInForce='GTC',
                    quantity=format((float(self.max_amount_buy)/last_price)/100 * 70, ".5f"),
                    stopPrice=parent.orderfill_price-self.trailing_points)

                elif self.trade_type == 'margin':
                    order = self.client.create_margin_order(
                    sideEffectType='MARGIN_BUY',
                    symbol='BTCUSDT',
                    side=self.client.SIDE_BUY,
                    type=self.client.ORDER_TYPE_MARKET,
                    #Converting USDT to BTC based on last price and trading 70% of that amount for the precision
                    quantity=format((float(self.max_amount_buy)/last_price)/100 * 70, ".5f"),
                    isIsolated='TRUE'
                    )

                elif self.trade_type == 'futures':
                    
                    self.client.futures_change_leverage(symbol='BTCUSDT', leverage=1)

                    order = self.client.futures_create_order(
                    symbol='BTCUSDT',
                    type=self.client.ORDER_TYPE_MARKET,
                    timeInForce='GTC',
                    side=self.client.SIDE_BUY,
                    quantity=format((float(self.max_amount_buy)/last_price)/100 * 70, ".5f"),
                    )

                else:
                    print('Please Set Trading Type')
                
                
                return(order)

            except BinanceAPIException as e:
                # error handling goes here
                print(e)
            except BinanceOrderException as e:
                # error handling goes here
                print(e)
            

        def sell(self, last_price):
            try:

                if self.trade_type == 'spot':
                    order = client.create_order(
                    symbol='BTCUSDT',
                    side=self.client.SIDE_SELL,
                    type=self.client.STOP_LOSS,
                    timeInForce='GTC',
                    quantity=self.max_amount_sell,
                    stopPrice=parent.orderfill_price+self.trailing_points)

                elif self.trade_type == 'margin':
                    order = self.client.create_margin_order(
                    sideEffectType='MARGIN_BUY',
                    symbol='BTCUSDT',
                    side=self.client.SIDE_SELL,
                    type=self.client.ORDER_TYPE_MARKET,
                    #Converting USDT to BTC based on last price and trading 70% of that amount for the precision
                    quantity=self.max_amount_sell,
                    isIsolated='TRUE'
                    )

                elif self.trade_type == 'futures':
                    
                    self.client.futures_change_leverage(symbol='BTCUSDT', leverage=1)

                    order = self.client.futures_create_order(
                    symbol='BTCUSDT',
                    type=self.client.ORDER_TYPE_MARKET,
                    timeInForce='GTC',
                    side=self.client.SIDE_SELL,
                    quantity=self.max_amount_sell,
                    )
                else:
                    print('Please Set Trading Type')
                
                return(order)

            except BinanceAPIException as e:
                # error handling goes here
                print(e)
            except BinanceOrderException as e:
                # error handling goes here
                print(e)

        
    def close(self, position = None, islong = None):
        
        try:
            

            # Spot Trades
            if side == "BUY" and self.trade_type == 'spot':
                order = client.create_order(
                symbol='BTCUSDT',
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_MARKET,
                timeInForce='GTC',
                quantity=qty)
                
            elif side == "SELL" and self.trade_type == 'margin':
                order = client.create_order(
                symbol='BTCUSDT',
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                timeInForce='GTC',
                quantity=qty)


            # Margin Trades
            if side == "BUY" and self.trade_type == 'margin':
                order = self.client.create_margin_order(
                symbol='BTCUSDT',
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_MARKET,
                quantity=qty,
                isIsolated='TRUE',
                sideEffectType='AUTO_REPAY'
                )

            elif side == "SELL" and self.trade_type == 'margin':
                order = self.client.create_margin_order(
                symbol='BTCUSDT',
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                quantity=qty,
                isIsolated='TRUE',
                sideEffectType='AUTO_REPAY'
                )


            # Futures Trades
            if side == "BUY" and self.trade_type == 'margin':
                order = self.client.futures_create_order(
                symbol='BTCUSDT',
                type=self.client.ORDER_TYPE_MARKET,
                timeInForce='GTC',
                side=self.client.SIDE_SELL,
                quantity=qty)

            elif side == "SELL" and self.trade_type == 'margin':
                order = self.client.futures_create_order(
                symbol='BTCUSDT',
                type=self.client.ORDER_TYPE_MARKET,
                timeInForce='GTC',
                side=self.client.SIDE_BUY,
                quantity=qty)


        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

        self.clean(self)


    def exit(self, parent, info = None, from_entry = None, profit = None, loss = None, trail_points = None, trail_offset = None):
        def precent_change(previous, current):
            if current == previous:
                return 0
            try:
                return (abs(previous - current) / previous) * 100.0
            except ZeroDivisionError:
                return 0

        def get_change_print(change):

            if (parent.currentposition == 'BUY') and (parent.orderfill_price > self.last_price):
                change_print = change*-1
            else:
                change_print = change

            if (parent.currentposition == 'SELL') and (parent.orderfill_price < self.last_price):
                change_print = change*-1
            else:
                change_print = change

            return change_print
              
        def trail_points(position = None, change_print = None, islong = parent.islong):
            EndTrade = False
            if islong == True:
                if self.last_price - self.trailing_price > self.trailing_points:
                    self.trailing_price = self.last_price - self.trailing_points

                if self.last_price - self.trailing_price <= 0:
                    # self.close(position = None, islong = self.islong)
                    self.trade_data['Exit Trigger'] = 'BUY Trail Stop Loss'
                    print("End Trade - BUY Trail Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                    EndTrade = True


            if islong == False:
                if self.last_price - self.trailing_price > self.trailing_points:
                    self.trailing_price = self.last_price - self.trailing_points

                if self.trailing_price - self.last_price <= 0:
                    # self.close(position = None, islong = self.islong)
                    self.trade_data['Exit Trigger'] = 'SELL Trail Stop Loss'
                    print("End Trade - SELL Trail Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                    EndTrade = True

            return EndTrade

        def percent_stop(change, change_trail, change_print):
            # PERCENT TRAIL
            EndTrade = False
            if(parent.currentposition == 'BUY') and change_trail <= change:
                self.trade_data['Exit Trigger'] = 'BUY Percent Trail'
                print("End Trade - BUY Percent Trail: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True
                
            if(parent.currentposition == 'SELL') and change_trail*-1 >= change*-1:
                self.trade_data['Exit Trigger'] = 'SELL Percent Trail'
                print("End Trade - SELL Percent Trail: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            return EndTrade
        
        def stop_loss(change_print):
            EndTrade = False
            
            if(parent.currentposition == 'BUY') and (self.last_price >= parent.orderfill_price-self.trailing_points) :
                self.trade_data['Exit Trigger'] = 'BUY Stop Loss'
                print("End Trade - BUY Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            if(parent.currentposition == 'SELL') and (self.last_price >= parent.orderfill_price+self.trailing_points) :
                self.trade_data['Exit Trigger'] = 'SELL Stop Loss'
                print("End Trade - SELL Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            return EndTrade

        def strategy_close(change_print):
            response = parent.brain.strategy_blast(self)
            EndTrade = False

            if (parent.currentposition == 'BUY') and response.get('buy') == False:
                self.trade_data['Exit Trigger'] = 'BUY Strategy Close'
                print("End Trade - BUY Strategy Close: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            elif (parent.currentposition  == 'SELL') and response.get('sell') == False:
                self.trade_data['Exit Trigger'] = 'SELL Strategy Close'
                print("End Trade - SELL Strategy Close: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True
            
            return EndTrade

        def stoptrade(EndTrade):
            if EndTrade == True:
                self.end_trade(parent)
                print('Current trade ended with profit  of:', change_print,'%',' 0rderfill:',parent.orderfill_price,' Last_price:', self.last_price)
                time.sleep(1.5)

                try:

                    parent.start_trade()

                except:
                    print("Can't make new trade, trying agian in 120 sec...")
                    time.sleep(120)
                    parent.start_trade()

            else:
                print("Current trade profit: ", format(change_print,'2f'),"% at close: ", self.last_price)


        if parent.islong == True:
            self.trailing_price = parent.orderfill_price - self.trailing_points

        if parent.islong == False:
            self.trailing_price = parent.orderfill_price + self.trailing_points


        

        while True:
            time.sleep(1.5)
            EndTrade = False
            self.last_price = float(self.lastclose_value(parent.KLINE_INTERVAL))
            print("Fill: ", parent.orderfill_price," Close: ", self.last_price)


            # PERCENT ENGINE
            change = precent_change(parent.orderfill_price, self.last_price)
            change_trail = precent_change(parent.orderfill_price, parent.orderfill_price-self.trailing_points)
            
            
            # CHANGE PRINT
            change_print = get_change_print(change)
            self.change_print = change_print

            print("Target trail: ", change_trail," Current Change: ", self.change_print)
            

            self.profit_percent = self.change_print
            self.drawdown_percent = change_print if ((change_print < 0) and (change_print <= self.drawdown_percent)) else self.drawdown_percent
            self.roundup  = change_print if ((change_print > 0) and (change_print >= self.roundup)) else self.roundup

            # STOP TRAIL 
            EndTrade = trail_points(change_print = change_print) if EndTrade == False else True


            # # PERCENT STOP
            # EndTrade = percent_stop(change, change_trail, change_print) if EndTrade == False else True


            # # STOP LOSS
            # EndTrade = stop_loss(change_print) if EndTrade == False else True


            # # STRATEGY CLOSE
            # EndTrade = strategy_close(change_print) if EndTrade == False else True


            # END TRADE CONDITION
            stoptrade(EndTrade)
            

            # # Call functions that correspond to parameters
            # if trail_points != None:
            #     self.trail_points(self, position = None)

    def end_trade(self, parent):
        # self.trading.close_order(self.order_to_track['executedQty'], self.order_to_track['side'])

        self.trade_data['Trade #']  = parent.trade_data['Trade #'] 
        self.trade_data['Entry Type'] = parent.trade_data['Entry Type']
        self.trade_data['Entry Signal'] = parent.trade_data['Entry Signal']
        self.trade_data['Entry Date/Time'] = parent.trade_data['Entry Date/Time']
        self.trade_data['Entry Price'] = parent.trade_data['Entry Price']

        self.trade_data['Contract'] = self.trade_amount
        self.trade_data['Profit'] = self.profit_percent
        self.trade_data['Strategy Name'] = parent.strategy_name
        self.trade_data['Strategy Code'] = parent.strategy_code
        self.trade_data['User Name'] = parent.user_name
        self.trade_data['User Code'] = parent.user_code
        self.trade_data['User Acocount Code'] = parent.user_acc_code
        self.trade_data['Drawdown'] = self.drawdown_percent
        self.trade_data['Drawdown'] = self.drawdown_percent
        self.trade_data['Roundup'] = self.roundup
        

        if parent.currentposition == 'BUY':
            self.trade_data['Exit Type'] = 'Exit Long'
            self.trade_data['Exit Signal'] = 'Buy'
            self.trade_data['Exit Date/Time'] = parent.helper.get_date()
            self.trade_data['Exit Price'] = self.lastclose_value(parent.KLINE_INTERVAL)

        elif  parent.currentposition == 'SELL':
            self.trade_data['Exit Type'] = 'Exit Short'
            self.trade_data['Exit Signal'] = 'Sell'
            self.trade_data['Exit Date/Time'] = parent.helper.get_date()
            self.trade_data['Exit Price'] = self.lastclose_value(parent.KLINE_INTERVAL)

        parent.helper.log_trade(self)

        print('End. Order finished successfully')

        self.clean()

    def clean(self):

        self.trailing_price = None
        self.current_price = None
        self.trade_data = {}
        self.change_print = None
        self.change_print = 0
        self.drawdown_percent = 0
        self.roundup = 0


    def track_trade_demo(self, parent):
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

            EndTrade = False

            self.last_price = float(self.lastclose_value(parent.KLINE_INTERVAL))

            print("Fill: ", parent.orderfill_price," Close: ", self.last_price)

            # PERCENT ENGINE
            change = precent_change(parent.orderfill_price, self.last_price)
            change_trail = precent_change(parent.orderfill_price, parent.orderfill_price-self.trailing_points)

            
            if (parent.currentposition == 'BUY') and (parent.orderfill_price > self.last_price):
                change_print = change*-1
            else:
                change_print = change

            if (parent.currentposition == 'SELL') and (parent.orderfill_price < self.last_price):
                change_print = change*-1
            else:
                change_print = change
            print("Target trail: ", change_trail," Current Change: ", change_print)

            # PERCENT TRAIL
            if(parent.currentposition == 'BUY') and change_trail*-1 >= change*-1:
                self.trade_data['Exit Trigger'] = 'BUY Percent Trail'
                print("End Trade - BUY Percent Trail: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True
                
            if(parent.currentposition == 'SELL') and change_trail <= change:
                self.trade_data['Exit Trigger'] = 'SELL Percent Trail'
                print("End Trade - SELL Percent Trail: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True


            # STOP LOSS
            if(parent.currentposition == 'BUY') and (self.last_price >= parent.orderfill_price-self.trailing_points) :
                self.trade_data['Exit Trigger'] = 'BUY Percent Stop Loss'
                print("End Trade - BUY Percent Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            if(parent.currentposition == 'SELL') and (self.last_price >= parent.orderfill_price+self.trailing_points) :
                self.trade_data['Exit Trigger'] = 'SELL Percent Stop Loss'
                print("End Trade - SELL Percent Stop Loss: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True



            # STRATEGY CLOSE
            response = parent.brain.strategy_blast(self)
                        
            if (parent.currentposition == 'BUY') and response.get('buy') == False:
                self.trade_data['Exit Trigger'] = 'BUY Strategy Close'
                print("End Trade - BUY Strategy Close: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = True

            elif (parent.currentposition  == 'SELL') and response.get('sell') == False:
                self.trade_data['Exit Trigger'] = 'SELL Strategy Close'
                print("End Trade - SELL Strategy Close: ", format(change_print,'2f'),"% at close: ", self.last_price)
                EndTrade = False


            # END TRADE CONDITION
            if EndTrade == True:
                self.end_trade(parent)
                print('Current trade ended with profit  of:', change_print,'%')
                time.sleep(1.5)

                try:

                    parent.start_trade()

                except:
                    print("Can't make new trade, trying agian in 120 sec...")
                    time.sleep(120)
                    parent.start_trade()

            else:
                
                print("Current trade profit: ", format(change_print,'2f'),"% at close: ", self.last_price)


    def track_trade(self):
        #How much price changed in % based on current price and order price

        def precent_change(current, previous):
            if current == previous:
                return 0 #100.0
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
            change_trail = precent_change(self.orderfill_price, self.orderfill_price-self.trailing_points)
            

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
                
                print("Current trade profit: ", format(self.change_print,'2f'),"%")
   
    
    def lastclose_value(self, KLINE_INTERVAL):

        try:
            #Change date and/or interval for different time frame
            klines = self.client.get_historical_klines("BTCUSDT", KLINE_INTERVAL, "1 day ago UTC")
        except: 
            print('Timeout! Waiting for time binance to respond...')
            time.sleep(120)
            print('Trying to connect agian...')
            klines = self.client.get_historical_klines("BTCUSDT", KLINE_INTERVAL, "1 day ago UTC")

        prices = []
        for i in klines:
            prices.append(float(i[4]))
            self.datadate.append(float(i[0]))
            self.dataopen.append(float(i[1]))
            self.datahigh.append(float(i[2]))
            self.datalow.append(float(i[3]))
            self.dataclose.append(float(i[4]))

        klines = self.client.get_historical_klines("BTCUSDT", KLINE_INTERVAL, "1 day ago UTC")
        
        return klines[len(klines)-1][4]


