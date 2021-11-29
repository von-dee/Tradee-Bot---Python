from config import Connect
from datetime import datetime
import pandas as pd
import numpy as np
import math
import time

class Brain:
    def __init__(self):
        #Init for Brain
        self.start = ''
    

    def strategy_blast(self, parent):
        
        def code_blast(parent, id):
            x1 = ((parent.dataclose[id] + parent.datalow[id]) * (parent.dataopen[id] + parent.datahigh[id])) / 2
            y1 = ((parent.dataclose[id] + parent.datahigh[id]) * (parent.dataopen[id] + parent.datalow[id])) / 2
            spike = (x1/y1)

            return spike

        #Trade Logic Check
        spike_1 = code_blast(parent,len(parent.dataclose)-3)
        spike = code_blast(parent,len(parent.dataclose)-2)


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

    def strategy_opbstrat(self, parent)

        #get the data from the market, create heikin ashi candles and then generate signals
        #return the signals to the bot
        def get_signal(client, _market="BTCUSDT", _period="15m", use_last=False):
            candles = client.get_candlestick_data(_market, interval=_period)
            o, h, l, c, v = convert_candles(candles)
            h_o, h_h, h_l, h_c = construct_heikin_ashi(o, h, l, c)
            ohlcv = to_dataframe(h_o, h_h, h_l, h_c, v)
            entry = trading_signal(h_o, h_h, h_l, h_c, use_last)
            return entry

        #get signal that is confirmed across multiple time scales
        def get_multi_scale_signal(client, _market="BTCUSDT", _periods=["1m"]):

            signals = np.zeros(499)
            use_last = True

            for i, v in enumerate(_periods):
        
                _signal = get_signal(client, _market, _period= v, use_last=use_last)
                signals = signals + np.array(_signal)

            signals = signals / len(_periods)

            trade_signal = []

            for i, v in enumerate(list(signals)):

                if v == -1:
                    trade_signal.append(-1)
                elif v == 1:
                    trade_signal.append(1)
                else:
                    trade_signal.append(0)

            return trade_signal

        def trading_signal(h_o, h_h, h_l, h_c, use_last=False):
            
            factor = 1
            pd = 1

            hl2 = (np.array(h_h) + np.array(h_l)) / 2
            hl2 = hl2[1:]

            atr = avarage_true_range(h_h, h_l, h_c)

            up = hl2 - (factor * atr)
            dn = hl2 + (factor * atr)

            trend_up = [0]
            trend_down = [0]

            for i, v in enumerate(h_c[1:]):
                if i != 0:

                    if h_c[i-1] > trend_up[i-1]:
                        trend_up.append(np.max([up[i], trend_up[i-1]]))
                    else:
                        trend_up.append(up[i])

                    if h_c[i-1] < trend_down[i-1]:
                        trend_down.append(np.min([dn[i], trend_down[i-1]]))
                    else:
                        trend_down.append(dn[i])

            trend = []
            last = 0
            for i, v in enumerate(h_c):
                if i != 0:
                    if h_c[i] > trend_down[i-1]:
                        tr = 1
                        last = tr
                    elif h_c[i] < trend_up[i-1]:
                        tr = -1
                        last = tr
                    else:
                        tr = last
                    trend.append(tr)

            entry = [0]
            last = 0
            for i, v in enumerate(trend):
                if i != 0:
                    if trend[i] == 1 and trend[i-1] == -1:
                        entry.append(1)
                        last = 1

                    elif trend[i] == -1 and trend[i-1] == 1:
                        entry.append(-1)
                        last = -1

                    else:
                        if use_last:
                            entry.append(last)
                        else:
                            entry.append(0)

            return entry
        

