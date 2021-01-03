from botindicators import BotIndicators
from graphlive import GraphLive
from graphics import Point
from graphics import Line
from twilio.rest import Client
from backtest import Backtest
from binance.exceptions import BinanceAPIException
import time
import math
class RealBotStrategy(object):
    def __init__(self, chartlen, pair, numofcharts,btcamt,funamt, client, interval):
        self.client = client
        
        f = open("twiliotoken.txt", "r")
        contents = f.read()
        newline = False
        account = ""
        token = ""
        for x in contents:
            if x == "\n":
                newline = True
                continue
            if not newline:
                account += x
            else:
                token += x
        self.tclient = Client(account, token)
        f.close() 
        
        self.sendsms("launched")
        
        self.altname = pair[0:int(math.ceil(len(pair) / 2.0))]

        self.masterDick = {}
        valuelist = [[False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],0,0,[],1,0,[],False,False,True,0,[],[],True,[],0,[],[],[],[],[],[],[],[],[]],[False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],0,0,[],1,0,[],False,False,True,0,[],[],True,[],0,[],[],[],[],[],[],[],[],[]], [False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],0,0,[],1,0,[],False,False,True,0,[],[],True,[],0,[],[],[],[],[],[],[],[],[]]]
        
        self.indicators = BotIndicators()
        
        self.symb = pair
        
        self.startingpos = 0
        #self.rsifirst = True
        self.rsiper = 12
        self.stochper = 14
        
        self.chartlen = chartlen
        
        self.last = False
        self.ma15 = 0
        self.ma5 = 0
        
        #coins available to spend
        self.startbtc = btcamt
        self.availablebtc = self.startbtc
        #self.firstbuy = self.availablebtc / 2.0
        #self.secondbuy = self.availablebtc - self.firstbuy
        
        self.amtofalt = 0
        
        #self.secondtradeentries = 0
        self.totalentries = 0
        
        #how many trades can there be
        self.entries = 1
        
        listofvars = ["crosstime","firstcross","crossPointA","crossPointB","percentlist","count",
                    "currentPrice","prices","ma5list","ma15list","ma15","ma5","pchange","ma5lower","ma5higher",
                    "lmaxes", "ema", "rsi", "rsilist", "botmax", "botmin","pricechg", "pag", "pal","rsifirst",
                    "k", "highs", "lows", "stochfirst", "k", "fast","crossPointAList","crossPointBList", "crossTimeList","firstCrossList",
                    "emalist","highlist","lowlist","klist","fastlist"]
        
        for i in range(numofcharts):
            for item in range(len(listofvars)):
                key = listofvars[item] + str(i + 1)
                listplaceholder = valuelist[i]
                self.masterDick[key] = listplaceholder[item]
        print(self.masterDick)
        
        self.graph = GraphLive(0,0,chartlen, pair, numofcharts, self.rsiper, self.stochper)
        
        #figure out orders with the dictionary
        #so keep these for now
        self.placedOrder = False
        self.orderPrice = 0
        self.orderGain = 0
        self.totalGainz = 0
        self.orderPercent = 0
        self.orders = {}
        
        #This only works for one chart at the moment
        self.entryprices = []
        #U still need to deal with self.orderPercent
        listoforder = ["totalGainz","orderPercent","avgentryprice","buys","sells"]
        #IF YOU ARE ADDING MULTIPLE GRAPHS AT ONCE CHANGE THIS, LISTS WILL BE LINKED
        ordervals = [0,0,0,[],[]]
        for num in range(numofcharts):
            for thing in range(len(listoforder)):
                key = listoforder[thing] + str(num + 1)
                self.orders[key] = ordervals[thing]
        print(self.orders)
        
        self.dentry = {}
        #setting number of allowed entries:
        #NEED TO DELETE THESE FROM ABOVE LOOP
        entryshit = ["placedOrder","orderPrice","orderGain","buy","tradeEntries","ordgains"]
        entvals = [False,0,0,0,0,[]]
        for n in range(numofcharts):
            for entr in range(1, self.entries + 1):
                for i in range(len(entryshit)):
                    key = entryshit[i] + str(entr) + str(n + 1)
                    self.dentry[key] = entvals[i]
        print(self.dentry)
        
        if funamt > 10:
            self.dentry["placedOrder11"] = True
        self.amtofalt = funamt
        self.prevEma = 0
        
        #get past data and continue
        #DOES THIS WORK??????????????????????!!!!!!!!!!!!?????????
        backtest = Backtest(self.symb, True, klineint=interval, graphics=False)
        self.masterDick["prices1"],self.masterDick["ma51"],self.masterDick["ma5list1"],self.masterDick["ma151"],self.masterDick["ma15list1"],self.prevEma,self.masterDick["ema1"],self.masterDick["k1"],self.masterDick["fast1"],self.masterDick["highs1"],self.masterDick["lows1"],self.masterDick["rsi1"],self.masterDick["pag1"],self.masterDick["pal1"], self.masterDick["pricechg1"] = backtest.getstuff()
        print(len(self.masterDick["highs1"]))
        #print last & current price and make sure they match up mane
    
    
    def sendsms(self, bodytext):
        message = self.tclient.messages.create(to="+14355130367", from_="+12565403212", body=bodytext)
    
        
    def tick(self, price, chartnumber, high, low, o, regraph=False):
        failed = True
        if self.dentry["placedOrder11"]:
            print("We tryna sell our",self.altname)
        else:
            print("We tryna buy some",self.altname)
        for n in range(1,16):
            try:
                balances = self.client.get_account()['balances']
                print("got balances")
                failed = False
                break
            except BinanceAPIException as e:
                if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                    print("Timestamp request failed",n,"times while getting balances.",str(self.client.get_server_time()),"Local time:",str(time.time() * 1000))
        if failed:
            self.sendsms("Failed to get balances - program crash - consider remote startup//server time: " + str(self.client.get_server_time()) + " local time: " + str(time.time() * 1000))
        bb = balances[0]
        self.availablebtc = float(bb['free'])
        ff = balances[120]
        self.amtofalt = float(ff['free'])
        #############################################
        if self.masterDick["ema" + chartnumber] == 0:
            self.masterDick["ema" + chartnumber] = float(price)
        self.prevEma = self.masterDick["ema" + chartnumber]
        
        #ema period is 20
        self.masterDick["ema" + chartnumber] = self.indicators.expMovingAverage(float(price), 20, self.prevEma)
        ema = self.masterDick["ema" + chartnumber]
        self.masterDick["emalist" + chartnumber].append(ema)
        emalist = self.masterDick["emalist" + chartnumber]
        if len(emalist) > self.chartlen:
            del emalist[0]
            
            self.startingpos += 1
        
        #this is the one screwing it up
        #lengpc = len(self.masterDick["pricechg" + chartnumber])
        if self.masterDick["count" + chartnumber] > 0:
            self.masterDick["pricechg" + chartnumber].append(float(price) - self.masterDick["currentPrice" + chartnumber])
        pricechg = self.masterDick["pricechg" + chartnumber]
        if len(pricechg) > self.rsiper:
            del pricechg[0]
            
        self.masterDick["currentPrice" + chartnumber] = float(price)
        
        self.masterDick["prices" + chartnumber].append(self.masterDick["currentPrice" + chartnumber])
        prices = self.masterDick["prices" + chartnumber]
        
        #stochastic
        self.masterDick["highs" + chartnumber].append(high)
        self.masterDick["lows" + chartnumber].append(low)
        highs = self.masterDick["highs" + chartnumber]
        lows = self.masterDick["lows" + chartnumber]
        if len(highs) > self.stochper:
            del highs[0]
            del lows[0]
        #adding these so refreshing screen will know the values
        self.masterDick["highlist" + chartnumber].append(high)
        self.masterDick["lowlist" + chartnumber].append(low)
        highlist = self.masterDick["highlist" + chartnumber]
        lowlist = self.masterDick["lowlist" + chartnumber]
        if len(highlist) > self.chartlen:
            del highlist[0]
            del lowlist[0]
        
        
        self.masterDick["ma15" + chartnumber] = self.indicators.movingAverage(self.masterDick["prices" + chartnumber], 15)
        self.ma15 = self.masterDick["ma15" + chartnumber]
        
        self.masterDick["ma15list" + chartnumber].append(self.masterDick["ma15" + chartnumber])
        ma15list = self.masterDick["ma15list" + chartnumber]
        
        self.masterDick["ma5" + chartnumber] = self.indicators.movingAverage(self.masterDick["prices" + chartnumber], 5)
        self.ma5 = self.masterDick["ma5" + chartnumber]
        
        self.masterDick["ma5list" + chartnumber].append(self.masterDick["ma5" + chartnumber])
        ma5list = self.masterDick["ma5list" + chartnumber]
        
        #Vertically scale the graph
        if(self.graph.chartmax == 0):
            self.graph.chartmax = price + (price / 1000)
            self.graph.chartmin = price - (price / 1000)
        else:
            if (price > self.graph.chartmax):
                self.graph.chartmax = price
                regraph = True
            if (price < self.graph.chartmin):
                self.graph.chartmin = price
                regraph = True
            if ema < self.graph.chartmin:
                self.graph.chartmin = ema
                regraph = True
            if ema > self.graph.chartmax:
                self.graph.chartmax = ema
                regraph = True
            if self.ma5 < self.graph.chartmin:
                self.graph.chartmin = self.ma5
                regraph = True
            if self.ma5 > self.graph.chartmax:
                self.graph.chartmax = self.ma5
                regraph = True
            if self.ma15 < self.graph.chartmin:
                self.graph.chartmin = self.ma15
                regraph = True
            if self.ma15 > self.graph.chartmax:
                self.graph.chartmax = self.ma15
                regraph = True
            if low < self.graph.chartmin:
                self.graph.chartmin = low
                regraph = True
            if high > self.graph.chartmax:
                self.graph.chartmax = high
                regraph = True
        
        #----rsi start----
        #If the data points hit the period of the rsi, start calculating it
        if self.masterDick["rsifirst" + chartnumber] and (len(pricechg) == self.rsiper):
            self.masterDick["rsi" + chartnumber] = self.indicators.rsi(pricechg)
            self.masterDick["pag" + chartnumber] = self.indicators.pag
            self.masterDick["pal" + chartnumber] = self.indicators.pal
            print("Ran on iteration",self.masterDick["count" + chartnumber])
            
            self.masterDick["rsilist" + chartnumber].append(self.masterDick["rsi" + chartnumber])
        elif not self.masterDick["rsifirst" + chartnumber]:
            self.masterDick["rsi" + chartnumber] = self.indicators.rsi(pricechg, self.masterDick["pag" + chartnumber], self.masterDick["pal" + chartnumber])
            self.masterDick["pag" + chartnumber] = self.indicators.pag
            self.masterDick["pal" + chartnumber] = self.indicators.pal

            self.masterDick["rsilist" + chartnumber].append(self.masterDick["rsi" + chartnumber])
        else:
            self.masterDick["rsilist" + chartnumber].append(0)
        rsi = self.masterDick["rsi" + chartnumber]
        
        if len(pricechg) == self.rsiper and self.masterDick["rsifirst" + chartnumber]:
            self.masterDick["rsifirst" + chartnumber] = False
            print("Falsified rsifirst",self.masterDick["count" + chartnumber],len(pricechg))
        #I didn't have this for some reason, hope it doesn't screw it up
        rsilist = self.masterDick["rsilist" + chartnumber]
        if len(rsilist) > self.chartlen:
            del rsilist[0]
        #----rsi end----
        
        #----stochastic start----
        if len(highs) == self.stochper:
            self.masterDick["k" + chartnumber].append(self.indicators.stochastic(float(price), min(lows), max(highs)))
            k = self.masterDick["k" + chartnumber]
            if len(k) > 3:
                del k[0]
            self.masterDick["fast" + chartnumber] = self.indicators.movingAverage(k, len(k))
        else:
            k = self.masterDick["k" + chartnumber]
        fast = self.masterDick["fast" + chartnumber]
        
        self.masterDick["klist" + chartnumber].append(k)
        klist = self.masterDick["klist" + chartnumber]
        self.masterDick["fastlist" + chartnumber].append(fast)
        fastlist = self.masterDick["fastlist" + chartnumber]
        if len(fastlist) > self.chartlen:
            del fastlist[0]
            del klist[0]
        #----stochastic end----
        
        '''
        if (self.orders["placedOrder" + chartnumber]):
            self.orderPercent = ((self.masterDick["currentPrice" + chartnumber] - self.orders["orderPrice" + chartnumber]) / self.orders["orderPrice" + chartnumber]) * 100
        '''
        if len(prices) > 1:
            lastwasmax = self.indicators.maxes(prices[-3:])
            if lastwasmax:
                lmaxes = self.masterDick["lmaxes" + chartnumber]
                if lmaxes[0] == -1:
                    lmaxes[0] = self.masterDick["count" + chartnumber] - 1
                else:
                    self.masterDick["lmaxes" + chartnumber].append(self.masterDick["count" + chartnumber] - 1)
            
        self.checkCross(prices[0], chartnumber)
                    
        
        self.masterDick["pchange" + chartnumber] = self.indicators.percentChange(prices, 5)
        self.masterDick["percentlist" + chartnumber].append(self.masterDick["pchange" + chartnumber])
        
        ##Added for live
        percentlist = self.masterDick["percentlist" + chartnumber]
        if len(percentlist) > self.chartlen:
            del percentlist[0]
            
        self.masterDick["crossPointAList" + chartnumber].append(self.masterDick["crossPointA" + chartnumber])
        crossPointAList = self.masterDick["crossPointAList" + chartnumber]
        if len(crossPointAList) > self.chartlen:
            del crossPointAList[0]
            
        self.masterDick["crossPointBList" + chartnumber].append(self.masterDick["crossPointB" + chartnumber])
        crossPointBList = self.masterDick["crossPointBList" + chartnumber]
        if len(crossPointBList) > self.chartlen:
            del crossPointBList[0]
        
        self.masterDick["firstCrossList" + chartnumber].append(self.masterDick["firstcross" + chartnumber])
        firstCrossList = self.masterDick["firstCrossList" + chartnumber]
        if len(firstCrossList) > self.chartlen:
            del firstCrossList[0]
        
        self.masterDick["crossTimeList" + chartnumber].append(self.masterDick["crosstime" + chartnumber])
        crossTimeList = self.masterDick["crossTimeList" + chartnumber]
        if len(crossTimeList) > self.chartlen:
            del crossTimeList[0]
        
        if chartnumber == "1":
            self.orders["buys" + chartnumber].append(0)
            self.orders["sells" + chartnumber].append(0)
            self.dentry["ordgains1" + chartnumber].append(0)
            buys = self.orders["buys" + chartnumber]
            sells = self.orders["sells" + chartnumber]
            ordgains = self.dentry["ordgains1" + chartnumber]
            if len(buys) > self.chartlen:
                del buys[0]
                del sells[0]
                del ordgains[0]
            
            #Buy/sell
            #I added +1 so we have the current and previous rsi/stochastic value available. could possibly need to change to +2
            #if self.masterDick["count" + chartnumber] >= self.stochper + 1 and self.masterDick["count" + chartnumber] >= self.rsiper + 1:
                
            self.evaluatePositions(price, lows, high, highs, k, o, rsi, chartnumber)
        
        full = self.masterDick["count" + chartnumber] > self.chartlen
        if regraph or full:
            self.graph.regraph(self.masterDick["prices" + chartnumber], ma5list, ma15list, percentlist, crossPointAList,crossPointBList,crossTimeList,firstCrossList,chartnumber,emalist, self.masterDick["rsilist" + chartnumber], highlist, lowlist, klist, fastlist, self.orders["buys" + chartnumber], self.orders["sells" + chartnumber], self.startingpos, self.dentry["ordgains1" + chartnumber])
        else:
            self.graph.add(price, self.ma5, self.ma15, self.masterDick["pchange" + chartnumber], self.masterDick["crossPointA" + chartnumber], self.masterDick["crossPointB" + chartnumber], self.masterDick["crosstime" + chartnumber], self.masterDick["firstcross" + chartnumber], chartnumber, ema, rsi, high, low, k, fast)
            regraph = False
        
        #Since the line between the last two MAcrosses was just graphed, we
        #change the first point for the next line to the last point of 
        #the current one
        if (self.masterDick["crosstime" + chartnumber]):
            self.masterDick["crossPointA" + chartnumber] = self.masterDick["crossPointB" + chartnumber]
            self.masterDick["crossPointB" + chartnumber] = 0
            self.masterDick["firstcross" + chartnumber] = self.masterDick["count" + chartnumber]
            self.masterDick["crosstime" + chartnumber] = False
        
        self.masterDick["count" + chartnumber] += 1
    
    ##########################################################
    ##########################################################
    ##########################################################
    
    
    def update(self, price, chartnumber):
        print(len(self.masterDick["prices" + chartnumber]))
        p = self.masterDick["prices" + chartnumber]
        del p[-1]
        print("len",len(self.masterDick["prices" + chartnumber]))
        m5l = self.masterDick["ma5list" + chartnumber]
        del m5l[-1]
        m15l = self.masterDick["ma15list" + chartnumber]
        del m15l[-1]
        pl = self.masterDick["percentlist" + chartnumber]
        del pl[-1]
        '''
        cpal = self.masterDick["crossPointAList" + chartnumber]
        del cpal[-1]
        cpbl = self.masterDick["crossPointBList" + chartnumber]
        del cpbl[-1]
        '''
        ctl = self.masterDick["crossTimeList" + chartnumber]
        del ctl[-1]
        fcl = self.masterDick["firstCrossList" + chartnumber]
        del fcl[-1]
        
        #
        self.masterDick["count" + chartnumber] -= 1
        #self.graph.regraph(price, self.ma5, self.ma15, self.masterDick["pchange" + chartnumber], self.masterDick["crossPointA" + chartnumber], self.masterDick["crossPointB" + chartnumber], self.masterDick["crosstime" + chartnumber], self.masterDick["firstcross" + chartnumber], chartnumber)
        #self.graph.removelastitem()
        self.tick(price, chartnumber, True)
        
        
    def checkCross(self, price, chartnumber):
        #if moving avgs cross
        if (self.masterDick["count" + chartnumber] > 0):
            
            ma5list = self.masterDick["ma5list" + chartnumber]
            ma15list = self.masterDick["ma15list" + chartnumber]
            self.masterDick["ma5lower" + chartnumber] = ma15list[-2] <= ma5list[-2] and ma15list[-1] > ma5list[-1]
            self.masterDick["ma5higher" + chartnumber] = ma15list[-2] >= ma5list[-2] and ma15list[-1] < ma5list[-1]
            
            #This buys or sells due to a cross in the MAs, you'll want to
            #move this out of this if statement eventually bcoz it will
            #evaluate other factors as well
            #self.evaluatePositions(chartnumber)
                    
            if(self.masterDick["ma5lower" + chartnumber] or self.masterDick["ma5higher" + chartnumber]):
                self.masterDick["crossPointA" + chartnumber], self.masterDick["crossPointB" + chartnumber] = self.indicators.MACross(ma5list[-2:], ma15list[-2:], self.masterDick["crossPointA" + chartnumber], price)
                
                self.masterDick["crosstime" + chartnumber] = True
                    
    #evaluate the position of a chart only when it's gained an item. use smaller chart changes
    #to influence current buys in the bigger charts
    def evaluatePositions(self, price, lows, high, highs, k, o, rsi, chartnumber):
        prices = self.masterDick["prices" + chartnumber]
        if((self.masterDick["currentPrice" + chartnumber] < self.ma5) and (self.masterDick["currentPrice" + chartnumber] < self.ma15)):
            if(self.masterDick["currentPrice" + chartnumber] > prices[-2] or self.masterDick["currentPrice" + chartnumber] == prices[-2]):
                #print("BUY")
                pass
        
        #you need to make sure the btc in your account matches up with availablebtc
        #could have rounding errors and say you have more than you actually do, shouldn't be significant tho-
        #especially if you check your bitcoin funds after every sell
        if not self.dentry["placedOrder1" + chartnumber]:
            '''
            #add these to a dict
            self.dentry["buy1" + chartnumber] = self.availablebtc / float(self.entries)
            countbro = self.entries - 1
            leftbtc = self.availablebtc - self.dentry["buy1" + chartnumber]
            #print(str(self.availablebtc - (self.dentry["buy1" + chartnumber] * countbro)))
            print(str(self.availablebtc / float(self.entries)))
            print("vbuy1",self.dentry["buy1" + chartnumber])
            '''
            for y in range(1, self.entries + 1):
                self.dentry["buy" + str(y) + chartnumber] = self.availablebtc / float(self.entries)
                #print("vbuy" + str(y),self.dentry["buy" + str(y) + chartnumber])
        
        
        self.firstone(price, prices, lows, high, highs, k, o, rsi, chartnumber)
        
        
        #MACrossing garbage
        '''
        if (self.masterDick["ma5higher" + chartnumber] and not self.orders["placedOrder" + chartnumber]):
            #evaluatePosition() - figure some shit out
            self.orders["placedOrder" + chartnumber] = True
            self.orders["orderPrice" + chartnumber] = self.masterDick["currentPrice" + chartnumber]
            self.graph.buy(self.masterDick["currentPrice" + chartnumber], self.masterDick["count" + chartnumber], chartnumber)
            
        elif(self.orders["placedOrder" + chartnumber]):
            if((self.masterDick["ma5lower" + chartnumber] or (self.masterDick["currentPrice" + chartnumber] - self.orders["orderPrice" + chartnumber])/self.orders["orderPrice" + chartnumber] > .01 )):
                self.orders["placedOrder" + chartnumber] = False
                self.orders["orderGain" + chartnumber] = ((self.masterDick["currentPrice" + chartnumber] - self.orders["orderPrice" + chartnumber]) / self.orders["orderPrice" + chartnumber]) * 100
                self.orders["totalGainz" + chartnumber] += self.orders["orderGain" + chartnumber]
                self.graph.sell(self.masterDick["currentPrice" + chartnumber], self.masterDick["count" + chartnumber], self.orders["orderGain" + chartnumber], chartnumber)
        '''
    
    ######Strategies######
    
    #THIS ONE IS FUCKING GREAT FOR FUNBTC
    def firstone(self, price, prices, lows, high, highs, k, o, rsi, chartnumber):
        for i in range(2, self.entries + 1):
            if len(self.entryprices) > 0:
                avgentryprice = sum(self.entryprices) / len(self.entryprices)
                #if previous entry has been placed and current hasn't and other args are met
                if self.dentry["placedOrder" + str(i - 1) + chartnumber] and float(price) < avgentryprice and float(price) < lows[-2] and float(price) < float(o) and not self.dentry["placedOrder" + str(i) + chartnumber]:
                    self.dentry["placedOrder" + str(i) + chartnumber] = True
                    #add these to dict
                    print("trade number",str(i))
                    self.dentry["tradeEntries" + str(i) + chartnumber] += 1
                    #self.totalentries += 1
                    self.dentry["orderPrice" + str(i) + chartnumber] = float(price)
                    altbuy = int(self.dentry["buy" + str(i) + chartnumber] / float(price))
                    #self.availablebtc -= altbuy * float(price)
                    
                    #There's gotta be a cleaner way to do this exception handling
                    bought = False
                    try:
                        order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                        bought = True
                    except BinanceAPIException as e:
                        if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                            for n in range(1,16):
                                try:
                                    order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                    bought = True
                                except BinanceAPIException as e:
                                    if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                        print("Failed buying",n,"times")
                                    else:
                                        break
                        else:
                            altbuy = int(altbuy * 0.95)
                            try:
                                order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                bought = True
                            except BinanceAPIException as e:
                                if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                    for n in range(1,16):
                                        try:
                                            order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                            bought = True
                                        except BinanceAPIException as e:
                                            if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                                print("Failed buying",n,"times")
                                            else:
                                                break
                                else:
                                    altbuy = int(altbuy * 0.95)
                                    try:
                                        order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                        bought = True
                                    except BinanceAPIException as e:
                                        if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                            for n in range(1,16):
                                                try:
                                                    order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                                    bought = True
                                                except BinanceAPIException as e:
                                                    if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                                        print("Failed buying",n,"times")
                                                    else:
                                                        break
                                        else:
                                            print("We tried to buy three times but the price skyrocketed ig")
                    if not bought:
                        print("Purchase failed")
                    altbuy -= altbuy * .001
                    #self.amtofalt += altbuy
                    self.entryprices.append(float(price))
                    self.graph.buy(self.masterDick["currentPrice" + chartnumber], self.masterDick["count" + chartnumber], chartnumber, i)
                    #print("Fun:",self.amtofalt)
                    #graph updating
                    buys = self.orders["buys" + chartnumber]
                    buys[-1] = self.masterDick["count" + chartnumber]
                    print("Buy" + str(i),self.dentry["buy" + str(i) + chartnumber])
                    break
            
        #buy/sell
        #need 2 change stochastic
        #just added rsi for testing
        if float(price) < prices[-2] and prices[-2] < prices[-3] and high < highs[-2] and k[-1] < self.masterDick["fast" + chartnumber] and not self.dentry["placedOrder1" + chartnumber]:# and rsi < 50:
            print("Make sure this is all right: price:",str(float(price)),"lastprice:",str(prices[-2]),"2 prices ago:",str(prices[-3]),"high:",str(high),"lasthigh:",str(highs[-2]),"d:",str(self.masterDick["fast" + chartnumber]),"k:",str(k[-1]))
            "do stuff, but add sfast and fast bro"
            print("buy")
            print('avbl BTC:',self.availablebtc)
            self.totalentries += 1
            #Wait put this statement in evaluatepositions and just call it
            #if not self.orders["placedOrder" + chartnumber]:
            self.dentry["placedOrder1" + chartnumber] = True
            #self.orders["orderPrice" + chartnumber] = self.masterDick["currentPrice" + chartnumber]
            self.dentry["orderPrice1" + chartnumber] = float(price)
            #altbuy = int(self.dentry["buy1" + chartnumber] / float(price))
            altbuy = int(self.availablebtc / float(price))
            #self.availablebtc -= altbuy * float(price)
            
            #This exception handling is butt
            bought = False
            messaged = False
            try:
                order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                self.sendsms("Bought " + str(altbuy) + " " + self.altname + " at " + str(float(price)) + " on first attempt")
                bought = True
                messaged = True
            except BinanceAPIException as e:
                if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                    for n in range(1,16):
                        try:
                            order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                            self.sendsms("Bought " + str(altbuy) + " " + self.altname + " at " + str(float(price)) + " on first attempt")
                            bought = True
                            messaged = True
                        except BinanceAPIException as e:
                            if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                print("Failed buying",n,"times",str(self.client.get_server_time()),"Local time:",str(time.time() * 1000))
                            else:
                                break
                else:
                    altbuy = int(altbuy * 0.99)
                    print("price went up")
                    try:
                        order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                        self.sendsms("Bought " + str(altbuy) + " " + self.altname + " at " + str(float(price)) + " on second attempt")
                        bought = True
                        messaged = True
                    except BinanceAPIException as e:
                        if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                            for n in range(1,16):
                                try:
                                    order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                    self.sendsms("Bought " + str(altbuy) + " " + self.altname + " at " + str(float(price)) + " on second attempt")
                                    bought = True
                                    messaged = True
                                except BinanceAPIException as e:
                                    if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                        print("Failed buying",n,"times",str(self.client.get_server_time()),"Local time:",str(time.time() * 1000))
                                    else:
                                        break
                        else:
                            altbuy = int(altbuy * 0.99)
                            print("price went up again")
                            try:
                                order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                self.sendsms("Bought " + str(altbuy) + " " + self.altname + " at " + str(float(price)) + " on third attempt")
                                bought = True
                                messaged = True
                            except BinanceAPIException as e:
                                if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                    for n in range(1,16):
                                        try:
                                            order = self.client.order_market_buy(symbol=self.symb,quantity=altbuy)
                                            self.sendsms("Bought " + str(altbuy) + " " + self.altname + " at " + str(float(price)) + " on third attempt")
                                            bought = True
                                            messaged = True
                                        except BinanceAPIException as e:
                                            if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                                                print("Failed buying",n,"times",str(self.client.get_server_time()),"Local time:",str(time.time() * 1000))
                                            else:
                                                break
                                else:
                                    print("We tried to buy three times but the price skyrocketed ig")
                                    self.sendsms("Buy failed due to price-" + e.message)
                                    messaged = True
            if not messaged:
                self.sendsms("Buy failed due to timestamp failure")
            altbuy -= altbuy * .001
            #self.amtofalt += altbuy
            self.entryprices.append(float(price))
            print(self.entryprices)
            self.graph.buy(self.masterDick["currentPrice" + chartnumber], self.masterDick["count" + chartnumber], chartnumber, 1)
            buys = self.orders["buys" + chartnumber]
            buys[-1] = self.masterDick["count" + chartnumber]
            print(self.altname + ":",self.amtofalt)
            print("Buy1",self.dentry["buy1" + chartnumber])
            
        
        elif float(price) > self.ma15 and float(price) > highs[-2] and self.dentry["placedOrder1" + chartnumber]:
            print("Prices list:",self.masterDick["prices" + chartnumber])
            self.dentry["placedOrder1" + chartnumber] = False
            if self.dentry["orderPrice1" + chartnumber] == 0:
                self.dentry["orderGain1" + chartnumber] = 0
            else:
                self.dentry["orderGain1" + chartnumber] = ((self.masterDick["currentPrice" + chartnumber] - self.dentry["orderPrice1" + chartnumber]) / self.dentry["orderPrice1" + chartnumber]) * 100
                self.dentry["orderGain1" + chartnumber] = self.dentry["orderGain1" + chartnumber] / float(self.entries)
            self.orders["totalGainz" + chartnumber] += self.dentry["orderGain1" + chartnumber]
            for x in range(2, self.entries + 1):
                if self.dentry["placedOrder" + str(x) + chartnumber]:
                    self.dentry["placedOrder" + str(x) + chartnumber] = False
                    self.dentry["orderGain" + str(x) + chartnumber] = ((self.masterDick["currentPrice" + chartnumber] - self.dentry["orderPrice" + str(x) + chartnumber]) / self.dentry["orderPrice" + str(x) + chartnumber]) * 100
                    self.dentry["orderGain" + str(x) + chartnumber] = self.dentry["orderGain" + str(x) + chartnumber] / float(self.entries)
                    self.orders["totalGainz" + chartnumber] += self.dentry["orderGain" + str(x) + chartnumber]
            ordgains = self.dentry["ordgains1" + chartnumber]
            ordgains[-1] = self.dentry["orderGain1" + chartnumber]
            #NO SELLING FEE WTF?????
            #Falese^^
            #self.availablebtc += (int(self.amtofalt) * float(price))
            #self.amtofalt -= int(self.amtofalt)
            for n in range(1,16):
                try:
                    order = self.client.order_market_sell(symbol=self.symb,quantity=int(self.amtofalt))
                    self.sendsms("Sold " + str(self.amtofalt) + " " + self.altname + " at " + str(float(price)) + ". (Price not accurate). MA15: " + str(self.ma15) + " last high: " + str(highs[-2]))
                    break
                except BinanceAPIException as e:
                    if e.message == "Timestamp for this request was 1000ms ahead of the server's time.":
                        print("Selling failed",n,"times")
                    else:
                        print("Unknown error occured during selling")
                        print(e.message)
                        self.sendsms("Error while selling-"+e.message)
                        if n > 10:
                            break
            self.graph.sell(self.masterDick["currentPrice" + chartnumber], self.masterDick["count" + chartnumber], self.dentry["orderGain1" + chartnumber], chartnumber)
            print("SELL")
            #this gon fuck it up
            self.entryprices = []
            #graph update sell
            sells = self.orders["sells" + chartnumber]
            sells[-1] = self.masterDick["count" + chartnumber]
        
        #error check
        '''
        if self.availablebtc < 0:
            print("FUCK BITCOIN IS IN THE NEGATIVES-ERROR")
            print(str(self.availablebtc))
        '''
    