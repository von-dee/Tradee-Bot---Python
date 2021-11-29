from config import Connect
from datetime import datetime
import math
import time
from sqllink import SQLlink

class Helper:
    def __init__(self):
        # print('.....')
        self.sqllink = SQLlink()
        self.client = Connect().make_connection()

        

    def isNewCandle(self,trade_timeframe):
        # if 1min : +1, 5min : -2, 15min : -2
        remainder = (time.time()) % (60 * trade_timeframe)
        return round(remainder)


    def gen_tradecode(self):
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return x  


    def get_date(self):
        now = datetime.now()
        date_string = now.strftime("%m/%d/%Y %H:%M:%S")
        return date_string

        # return time.time()


    def get_change(current, previous):
        if current == previous:
            return 100.0
        try:
            return (abs(current - previous) / previous) * 100.0
        except ZeroDivisionError:
            return 0


    def log_activity(self, parent, id, position):
        with open('Results/ActivityLog_Binary_Blast_v3.csv', 'a') as d:
            d.write(f'{parent.datadate[id]}, {parent.dataopen[id]}, {parent.datahigh[id]}, {parent.datalow[id]}, {parent.dataclose[id]}, {position}\n')
        
        params = {
            "act_code" : "ACT0000000001",
            "act_title" : position + " Trade Placed",
            "act_description" : "Successfully placed" + position + "at this close" + str(parent.dataclose[id]),
            "act_type" : "Successful Placed Trade",
            "act_dateadded" : self.get_date(),
            "act_status" : "1"
        }     

        response = self.sqllink.LogActivity(params)
        print(response.get('msg'))


    def log_trade(self, parent):

        tradeno = parent.trade_data['Trade #'] 
        entrytype = parent.trade_data['Entry Type']
        entrysignal = parent.trade_data['Entry Signal']
        entrydatetime = parent.trade_data['Entry Date/Time']
        entryprice = parent.trade_data['Entry Price']
        exittype = parent.trade_data['Exit Type']
        exitsignal = parent.trade_data['Exit Signal']
        exitdatetime = parent.trade_data['Exit Date/Time']
        exitprice = parent.trade_data['Exit Price']
        exittrigger = parent.trade_data['Exit Trigger']

        contracts = parent.trade_data['Contract']
        profit = parent.trade_data['Profit']
        
        cumprofit = profit + self.sqllink.getCummulativeProfit(parent.trade_data['Strategy Code'])
        drawdown = parent.trade_data['Drawdown']
        roundup   = parent.trade_data['Roundup']
        dateadded = self.get_date()
        strategy_code = parent.trade_data['Strategy Code']
        strategy_name = parent.trade_data['Strategy Name']
        user_code = parent.trade_data['User Code']
        user_name = parent.trade_data['User Name']
        user_acc_code = parent.trade_data['User Acocount Code']


        with open('Results/TradeLog_Binary_Blast_v3.csv', 'a') as d:
            d.write(f'{tradeno}, {entrytype}, {entrysignal}, {entrydatetime}, {entryprice}, {exittype}, {exitsignal}, {exitdatetime}, {exitprice}, {exittrigger}\n')

        params = {
                "trd_code" : "TRD0000000001",
                "trd_entry_type" : entrytype,
                "trd_entry_signal" : entrysignal,
                "trd_entry_datetime" : entrydatetime,
                "trd_exit_type" : exittype,
                "trd_exit_signal" : exitsignal,
                "trd_exit_datetime" : exitdatetime,
                "trd_price" : exitprice,
                "trd_exittrigger" : exittrigger,
                "trd_contracts" : contracts,
                "trd_profit" : profit,
                "trd_cumprofit" : cumprofit,
                "trd_runup" : roundup,
                "trd_drawdown" : drawdown,
                "trd_dateadded" : dateadded,
                "trd_strategy_code" : strategy_code,
                "trd_strategy_name" : strategy_name,
                "trd_user_code" : user_code,
                "trd_user_name" : user_name,
                "trd_user_acc_code" : user_acc_code
            }     
        

        response = self.sqllink.LogTrade(params)
        print(response.get('msg'))


    def get_kline(self, KLINE_INTERVAL):

        try:
            #Change date and/or interval for different time frame
            klines = self.client.get_historical_klines("BTCUSDT", KLINE_INTERVAL, "1 day ago UTC")
        except: 
            print('Timeout! Waiting for time binance to respond...')
            time.sleep(120)
            print('Trying to connect agian...')
            klines = self.client.get_historical_klines("BTCUSDT", KLINE_INTERVAL, "1 day ago UTC")

        prices = []
        datadate = []
        dataclose = []
        dataopen = []
        datalow = []
        datahigh = []

        for i in klines:
            prices.append(float(i[4]))
            datadate.append(float(i[0]))
            dataopen.append(float(i[1]))
            datahigh.append(float(i[2]))
            datalow.append(float(i[3]))
            dataclose.append(float(i[4]))


        params = {
                "lastprice" : klines[len(klines)-1][4],
                "prices" : prices,
                "datadate" : datadate,
                "dataopen" : dataopen,
                "datahigh" : datahigh,
                "datalow" : datalow,
                "dataclose" : dataclose
            }     

        
        return params
        
        


      


