import backtrader as bt
import datetime

class RSIStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

        # To keep track of pending orders
        self.order = None

        # To keep track of placed positions
        self.currentposition = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # # Write down: no pending order
        # self.order = None

    def strategy_blast(self, id):
        x1 = ((self.dataclose[id] + self.datalow[id]) * (self.dataopen[id] + self.datahigh[id])) / 2
        y1 = ((self.dataclose[id] + self.datahigh[id]) * (self.dataopen[id] + self.datalow[id])) / 2
        spike = (x1/y1)

        return spike

    def next(self):

        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # # Check if an order is pending ... if yes, we cannot send a 2nd one
        # if self.order:
        #     return
        
        # self.close()

        spike_1 = self.strategy_blast(-1)
        spike = self.strategy_blast(0)


        if spike_1 > 1 and spike <= 1:
            buy = True
        else:
            buy = False
        
        if spike_1 < 1 and spike >= 1:
            sell = True
        else:
            sell = False


        # Check if we are in the market
        if not self.position:
            self.close()

            # Open all Opened Positions
            if buy == True:

                # print('Buy Position Opened, %.2f'% self.dataopen[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(size=1)
                self.currentposition = "Buy"
            
            if sell == True:
                
                # print('Sell Position Opened, %.2f'% self.dataopen[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=1)
                self.currentposition = "Sell"


        else:
            # Close all Opened Positions


            if self.order is not None:

                if self.currentposition == "Buy" and buy == False:
                    self.close()
                    self.currentposition = None
                    # print('Buy Position Closed, %.2f'% self.dataclose[0])

                if self.currentposition == "Sell" and sell == False:
                    self.close()
                    self.currentSellposition = None
                    # print(' Position Closed, %.2f'% self.dataclose[0])
           




cerebro = bt.Cerebro()

fromdate = datetime.datetime.strptime('2021-09-01', '%Y-%m-%d')
todate = datetime.datetime.strptime('2021-09-30', '%Y-%m-%d')

data = bt.feeds.GenericCSVData(dataname='data/2021_Sep_15minutes.csv', dtformat=2, compression=15, timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)

cerebro.adddata(data)

cerebro.addstrategy(RSIStrategy)

cerebro.broker.setcash(100000.0)



print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()