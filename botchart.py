from binance.client import Client
from dateparser import parse
import calendar
from datetime import datetime
import time

class BotChart(object):
    def __init__(self, currency, period, interval, start=0, stringy="", endstring=""):
        self.currency = currency
        self.period = period
        
        #set the start time for the charts
        if stringy != "":
            startstring = stringy
        elif (not start == 0):
            startstring = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
            print("startstring:",startstring)
        else:
            startstring = "10 days ago UTC"
        
        #idk maybe use this in the else statement^^ and make the startstring an input variable
        realperiod = parse("2 month ago UTC")
        realperiod = parse(stringy)
        #timestamp = calendar.timegm(realperiod.utctimetuple())
        print("OKAY TESTING MY SHIT")
        print(calendar.timegm(parse("30 minutes ago UTC").utctimetuple()))
        print(time.time() - 1800)
        d = datetime.utcnow()
        endtime = calendar.timegm(d.utctimetuple())
        self.data = []
        self.timestamps = []
        self.highs = []
        self.lows = []
        self.opens = []
        
        #read api token from text file, same code in botstrategy
        f = open("token.txt", "r")
        contents = f.read()
        newline = False
        secretkey = ""
        apikey = ""
        for x in contents:
            if x == "\n":
                newline = True
                continue
            if not newline:
                apikey += x
            else:
                secretkey += x
        self.client = Client(apikey, secretkey)
        f.close()
        ####
        
        
        print("should take a while...")
        if endstring == "":
            klines = self.client.get_historical_klines(symbol=currency, interval=interval, start_str=startstring)
        else:
            klines = self.client.get_historical_klines(symbol=currency, interval=interval, start_str=startstring, end_str=endstring)
 
        print("yep")

            
        #klines2 = self.client.get_historical_klines(currency, Client.KLINE_INTERVAL_5MINUTE, "3 days ago UTC")
        print(len(klines))
        #print(klines[0],klines2[0],klines[1],klines2[6])
        self.max = 0
        self.min = 0
        self.lmaxes = []
        self.valuesAre = "Closing Kline Trades"
        for val in klines:
            #IF YOU CHANGE VAL[1] MAKE SURE TO CHANGE THE MAX AND MIN VALUE SHIT
            
            self.data.append(val[4])
            self.timestamps.append(val[0])
            self.highs.append(val[2])
            self.lows.append(val[3])
            self.opens.append(val[1])
            
            #Ghetto way of calculating local max, use calculus formula in the future
            if(len(self.data) > 2 and (float(self.data[-2]) > float(self.data[-3])) and (float(self.data[-2]) > float(self.data[-1]))):
                self.lmaxes.append(len(self.data) - 2)
                    
            
            #!!!Changed val[4] to highs and lows
            #find max value to shift graph
            if(float(val[2]) > self.max):
                self.max = float(val[2])
                
            #find min value to shift graph
            if (float(val[3]) < self.min or self.min == 0):
                self.min = float(val[3])
        
    
    def getMax(self):
        return self.max
    
    def getMin(self):
        return self.min
        
        