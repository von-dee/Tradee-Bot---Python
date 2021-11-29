from config import Connect
import math
import time

class Order:
    def __init__(self):
        self.client = Connect().make_connection()
        
        max_amount = 50

        # max_amount = self.client.get_max_margin_loan(asset="BTC",isolatedSymbol='BTCUSDT')['amount']
        #Change for how much money you allow for trade. Current one 35% from maximum allowed borrow limit
        # self.max_amount_sell = format(float(max_amount)*35/100,".6f")

        # max_amount = self.client.get_max_margin_loan(asset="USDT",isolatedSymbol='BTCUSDT')['amount']
        #Change for how much money you allow for trade. Current one 35% from maximum allowed borrow limit
        # self.max_amount_buy = format(float(max_amount)*35/100,".6f")
    

    def buy(self, last_price):

        try:

            if self.trade_type == 'spot':
                order = client.create_order(
                symbol='BTCUSDT',
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                timeInForce='GTC',
                quantity=format((float(self.max_amount_buy)/last_price)/100 * 70, ".5f"))

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
                type=self.client.ORDER_TYPE_MARKET,
                timeInForce='GTC',
                quantity=self.max_amount_sell)

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


    def close_order(self, qty, side):

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

    def close_order(self):
        self.client._delete('openOrders', True, data={'symbol': 'BTCUSDT'})