from config import Connect
from datetime import datetime
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

