from datetime import datetime
import time
import mysql.connector
from mysql.connector import connect, Error
class SQLlink:
    def __init__(self):
        print('.....')  

    
    def generateCode(self, table, prefix, base_col):
        config = {
        # For online Server
        'user': 'root',
        'password': 'tiynkpassword',
        'host': '157.230.183.69',
        'database': 'tradee',

        'port': '3306',
        'raise_on_warnings': True}

        cnx = mysql.connector.connect(**config) 
        cursor = cnx.cursor()
    

        no_prec = 10

        try:

            query = """
            SELECT %s FROM  %s ORDER BY RIGHT (%s,%s) DESC LIMIT 1;
            """% (
                    base_col,
                    table,
                    base_col,
                    no_prec,
                )
            

            cursor.execute(query)

            results = cursor.fetchone()
            
            if results is not None:
                    
                for x in results:
                    result = x
            
                result_str = result.strip(prefix)
                
                rawcount = int(result_str)
                rawcount = rawcount + 1
                multiplier = no_prec - len(str(rawcount))
                multiplier = 0 if multiplier <=0 else multiplier 
                code = "0"*multiplier + str(rawcount)
                data = prefix+code
                cursor.close()
                cnx.close()
                return data

            else:
                cursor.close()
                cnx.close()
                return prefix+"0000000001"

            

        except Error as e:

            print (e)
            cursor.close()
            cnx.close()
            return "Error"


    def getCummulativeProfit(self, strategy_code):
        config = {
        # For online Server
        'user': 'root',
        'password': 'tiynkpassword',
        'host': '157.230.183.69',
        'database': 'tradee',

        'port': '3306',
        'raise_on_warnings': True}

        cnx = mysql.connector.connect(**config) 
        cursor = cnx.cursor()
    
        no_prec = 10

        try:

            query = """
            SELECT TRD_CUMPROFIT FROM  trade_trades where TRD_STRATEGY_CODE = "%s" ORDER BY TRD_ID DESC LIMIT 1;
            """% (
                    strategy_code
                )

            cursor.execute(query)

            results = cursor.fetchone()
            
            if results is not None:
                    
                for x in results:
                    result = x
                
                cum_profit = float(result) if result != "" else 0
                
                cursor.close()
                cnx.close()
                return cum_profit
            else:
                cursor.close()
                cnx.close()
                return 0

        except Error as e:

            print (e)
            cursor.close()
            cnx.close()
            return "Error"

    
    def getEquity(self, user_acc_code):
        config = {
        # For online Server
        'user': 'root',
        'password': 'tiynkpassword',
        'host': '157.230.183.69',
        'database': 'tradee',

        'port': '3306',
        'raise_on_warnings': True}

        cnx = mysql.connector.connect(**config) 
        cursor = cnx.cursor()
    
        no_prec = 10

        try:

            query = """
            SELECT ACT_EQUITY FROM trade_account where ACT_CODE = "%s" ORDER BY ACT_ID DESC LIMIT 1;
            """% (
                    user_acc_code
                )

            cursor.execute(query)

            results = cursor.fetchone()
            
            if results is not None:
                    
                for x in results:
                    result = x
                
                user_equity = float(result) if result != "" else 0
                
                cursor.close()
                cnx.close()
                return user_equity
            else:
                cursor.close()
                cnx.close()
                return 0

        except Error as e:

            print (e)
            cursor.close()
            cnx.close()
            return "Error"
         
            
    
    def LogTrade(self,params):
        config = {
        # For online Server
        'user': 'root',
        'password': 'tiynkpassword',
        'host': '157.230.183.69',
        'database': 'tradee',

        'port': '3306',
        'raise_on_warnings': True}

        cnx = mysql.connector.connect(**config) 
        cursor = cnx.cursor()

        trd_code = self.generateCode("trade_trades", "TRD", "TRD_CODE")
        equity = self.getEquity(params.get('trd_user_acc_code'))
        trd_equity = equity + ((params.get('trd_contracts')/100) * params.get('trd_profit'))

        try:

            update_query = """
            INSERT INTO trade_trades 
                (TRD_CODE, TRD_ENTRY_TYPE, TRD_ENTRY_SIGNAL, TRD_ENTRY_DATETIME, TRD_ENTRY_PRICE, TRD_EXIT_TYPE, TRD_EXIT_SIGNAL, TRD_EXIT_DATETIME, TRD_EXITTRIGGER, TRD_EXIT_PRICE, TRD_CONTRACTS, TRD_PROFIT, TRD_CUMPROFIT, TRD_RUNUP, TRD_DRAWDOWN, TRD_DATEADDED, TRD_STRATEGY_CODE, TRD_STRATEGY_NAME, TRD_EQUITY)
            VALUES 
                ( "%s",  "%s",  "%s",  "%s",  "%s", "%s", "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s");
            """ % (
                trd_code,
                params.get('trd_entry_type'),
                params.get('trd_entry_signal'),
                params.get('trd_entry_datetime'),
                params.get('trd_entryprice'),
                params.get('trd_exit_type'),
                params.get('trd_exit_signal'),
                params.get('trd_exit_datetime'),
                params.get('trd_exittrigger'),
                params.get('trd_exitprice'),
                params.get('trd_contracts'),
                params.get('trd_profit'),
                params.get('trd_cumprofit'),
                params.get('trd_runup'),
                params.get('trd_drawdown'),
                params.get('trd_dateadded'),
                params.get('trd_strategy_code'),
                params.get('trd_strategy_name'),
                trd_equity
            )



            update_account_query = """
                UPDATE trade_account SET ACT_EQUITY = "%s" WHERE ACT_USERCODE = "%s"
            """ % (
                trd_equity,
                params.get('trd_user_code')
            )

            cursor.execute(update_query)

            cursor.execute(update_account_query)
            
            cnx.commit()

            cursor.close()
            cnx.close()
            return {
                "data" : "Success",
                "msg" : "Successful Logged Trade",
            }     

        except Error as e:

            # print(e)
            cursor.close()
            cnx.close()
            return {
                "data" : "Error",
                "msg" : e
            }  

         

    def LogActivity(self, params):
        config = {
        # For online Server
        'user': 'root',
        'password': 'tiynkpassword',
        'host': '157.230.183.69',
        'database': 'tradee',

        'port': '3306',
        'raise_on_warnings': True}

        cnx = mysql.connector.connect(**config) 
        cursor = cnx.cursor()
        code = self.generateCode("trade_activities", "ACT", "ACT_CODE")

        try:

            update_query = """
            INSERT INTO trade_activities 
                (ACT_STATUS, ACT_DESCRIPTION, ACT_TITLE, ACT_TYPE, ACT_DATEADDED, ACT_CODE, ACT_STRAT_CODE)
            VALUES 
                ( "%s",  "%s",  "%s",  "%s",  "%s",  "%s",  "%s");
            """ % (
                params.get('act_status'),
                params.get('act_description'),
                params.get('act_title'),
                params.get('act_type'),
                params.get('act_dateadded'),
                code,
                params.get('act_strat_code'),
            )

            cursor.execute(update_query)
            cnx.commit()

            cursor.close()
            cnx.close()
            return {
                "data" : "Success",
                "msg" : "Successful Logged Activity",
            }     

        except Error as e:

            # print(e)
            cursor.close()
            cnx.close()
            return {
                "data" : "Error",
                "msg" : e
            }  


