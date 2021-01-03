from binance.client import Client
from binance.websockets import BinanceSocketManager
from realbotstrategy import RealBotStrategy
import queue
from binance.exceptions import BinanceAPIException
from binance.enums import *
import time
from builtins import int, str
class Experimenting(object):
    def __init__(self, pair, klineInterval):
        print("DON'T RUN THIS PROGRAM LESS THAN A MINUTE BEFORE A 30 MINUTE INTERVAL, MAY OR MAY NOT WORK I HAVE NO EARTHLY IDEA")
        print(klineInterval)
        print(type(klineInterval))
        
        
        #i'm not gonna deal with month interval for now
        self.intervalletters = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}
        #interval in seconds
        self.intersecs = self.klineinttosecs(klineInterval)
        print(self.intersecs)
        
        
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
        
        for n in range(1,51):
            try:
                balances = self.client.get_account()['balances']
                print("got balances")
                break
            except BinanceAPIException as e:
                print(e.message)
                if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                    print("Timestamp request failed",n,"times",str(self.client.get_server_time()),"Local time:",str(time.time() * 1000))
        btc = balances[0]
        btcamt = float(btc['free'])
        fun = balances[120]
        funamt = float(fun['free'])
        print("Success")
        
        #self.bm = BinanceSocketManager(self.client)
        self.result_q = queue.Queue()
        self.pair = pair
        #self.conn_key = self.bm.start_kline_socket(self.pair, self.read, interval="1m")
        self.botstrategylive = RealBotStrategy(100,self.pair,1,btcamt,funamt, self.client, klineInterval)
        self.prev = 0
        #self.bm.start()
        self.prevph = 0
        self.prevkline = {}
        first = True
        klinetime = 0
        
        #instead of "30 minutes ago UTC" etc. i'm gonna do time.time() - self.intersecs
        #can't handle low trading volume - if no trades in one interval, it gets skipped (?)
        while True:
            while True:
                kline = self.client.get_historical_klines(pair,klineInterval, int(time.time() - self.intersecs) * 1000)
                while len(kline) == 0:
                    kline = self.client.get_historical_klines(pair,klineInterval, int(time.time() - self.intersecs) * 1000)
                    print("we keep setting kline cause it's empty")
                    time.sleep(1)
                print(kline, "firstkline")
                kline = kline[0]
                if klinetime > kline[0] / 1000:
                    #this is not how this works
                    #p sure this will never trip
                    print("Oh shit we skipped a kline, must be cutting it too close / there's lag - maybe make klinetime + self.intersecs - 1 lower (the one bigger)")
                klinetime = kline[0] / 1000
                diff = time.time() - klinetime
                
                if diff < self.intersecs - 15: #1700 for 30 min int
                    time.sleep(self.intersecs - 15 - diff)
                else:
                    #i don't even have to do this shit man, but it was here so ig i'll keep using it
                    time.sleep(1)
                    #Change 60 to 1799
                    if time.time() >= klinetime + self.intersecs - 1:
                        print("success")
                        #Do the ticking
                        self.loop(kline)
                        #Keeps the program from looping the same kline twice
                        time.sleep(2)
            '''
            data = self.result_q.get()
            print(data)
            placeholder = data['k']
            if not int(placeholder['t']) == self.prevph and not first:
                #if you can detect when it's the last trade sooner that would be best
                self.loop(self.prevkline)
            self.prevph = int(placeholder['t'])
            self.prevkline = data
            first = False
            '''
    def klineinttosecs(self, klineint):
        number = ''
        for letter in klineint:
            if letter in self.intervalletters:
                
                number = int(number) * self.intervalletters[letter]
                return(number)
            else:
                number += letter
            
    
    def read(self, dict):
        self.result_q.put(dict)
        
    def loop(self, dict):
        #open = dict['k']
        '''
        if open['t'] == self.prev:
            #Change current tick
            self.botstrategylive.update(float(open['c']), "1", float(open['h']), float(open['l']), float(open['o']))
        else:
        '''
        #self.botstrategylive.tick(float(open['c']), "1", float(open['h']), float(open['l']), float(open['o']))
        #self.prev = open['t']
        #print("close:",float(open['c']))
        print("close:",float(dict[4]))
        self.botstrategylive.tick(float(dict[4]),"1",float(dict[2]),float(dict[3]),float(dict[1]))
    
experimenting = Experimenting("ZILBTC", KLINE_INTERVAL_30MINUTE)


