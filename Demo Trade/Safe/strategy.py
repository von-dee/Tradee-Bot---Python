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

        useLeverage = inpLeverage if inpLeverage >= 1 else 1
        useTakeProfit = inpTakeProfit if inpTakeProfit >= 1 else 0
        useStopLoss = inpStopLoss if inpStopLoss >= 1 else 0
        useTrailStop = inpTrailStop if inpTrailStop >= 1 else 0
        useTrailOffset = inpTrailOffset if inpTrailOffset >= 1 else 0

        self.trade_amount = 50
        commission_value = 0.075

        self.trailing_price = None
        self.current_price = None

    
    def entry(self, id = "Buy", long = true):
    
        def sell(self, last_price = None):

            order = self.client.create_order(
            symbol='BTCUSDT',
            side=self.client.SIDE_SELL,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=self.trade_amount,
            isIsolated='TRUE'
            )

            return(order)


        def buy(self, last_price = None):

            order = self.client.create_order(
            symbol='BTCUSDT',
            side=self.client.SIDE_BUY,
            type=self.client.ORDER_TYPE_MARKET,
            #Converting USDT to BTC based on last price and trading 70% of that amount for the precision
            quantity=format((float(self.trade_amount)/last_price), ".5f"),
            isIsolated='TRUE'
            )
            
            return(order)
        

    def close(self, position = None, islong = None):

        if islong == True:
            order = self.client.create_margin_order(
            symbol='BTCUSDT',
            side=self.client.SIDE_SELL,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )

        elif islong == False:
            order = self.client.create_margin_order(
            symbol='BTCUSDT',
            side=self.client.SIDE_BUY,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )

        self.clean(self)


    def exit(self, info = None, from_entry = None, profit = None, loss = None, trail_points = None, trail_offset = None):

        def trail_points(self, position = None, islong = self.islong):

            if islong == True:
                if self.current_price - self.trailing_price > 100:
                    self.trailing_price = self.current_price - 100

                if self.current_price - self.trailing_price <= 0:
                    self.close(position = None, islong = self.islong)

            if islong == False:
                if self.current_price - self.trailing_price > 100:
                    self.trailing_price = self.current_price - 100

                if self.current_price - self.trailing_price <= 0:
                    self.close(position = None, islong = self.islong)

        # Call functions that correspond to parameters

        if trail_points != None:
            self.trail_points(self, position = None)


    def clean(self):
        self.trailing_price = None
        self.current_price = None


    # Helper functions

    def get_change(current, previous):
        if current == previous:
            return 100.0
        try:
            return (abs(current - previous) / previous) * 100.0
        except ZeroDivisionError:
            return 0
