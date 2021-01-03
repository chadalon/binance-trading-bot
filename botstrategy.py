from botindicators import BotIndicators
from graph import Graph
from graphics import Point
from graphics import Line
from binance.client import Client
#from astropy.io.fits.util import first ???
#NOW MOVING HIGH TO GLOBAL
class BotStrategy(object):
    def __init__(self, strat, chartmax, chartmin, chartlengths, pair, numofcharts, valuesAre, timestamps, extra, valuelist, intervals, beginag, endag, tlen, live=False, aggTrades=True, aggisNext=True, graphics=True, ma5on=True, handlon=True):
        self.masterDick = {}
        self.graphics = graphics
        
        #If we want these indicators graphed:
        self.ma5on = ma5on
        
        
        #***************************#
        
        #read api token from text file, hopefully I don't accidentally upload the text file to github lol
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
        
        self.strat = strat
        self.stratlist = ["",
                          "self.firstone(lows, highs, k, o)#, nextTradeSeller)",
                          "self.secondone(lows, highs, k, o)",
                          "self.thirdone()"
                          ]
        
        #this checks if ur trading larger(not fractional) currencies (BTCUSD, etc)
        
        self.largerpair = False
        
        largepairlist = ["BTCUSDT"]
        for fuck in largepairlist:
            if pair == fuck:
                self.largerpair = True
        
        
        self.aggisNext = aggisNext
        self.aggTrades = aggTrades
        
        #price change during market buying
        self.amtofups = 0
        self.amtofdowns = 0
        self.pair = pair
        self.indicators = BotIndicators()
        self.live = live
        #self.rsifirst = True
        self.rsiper = 12
        self.stochper = 14
        self.bollingerper = 20
        
        self.chartlen = chartlengths
        
        self.last = False
        self.bigma = 0
        self.ma15 = 0
        self.ma5 = 0
        
        self.bolup = 0
        self.bollow = 0
        self.bolmid = 0
        self.bandwidth = 0
        
        #BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        #BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
        #slutty variables turned global
        #if u wanna call functions that used to take params like chartnumber, nextTrade, etc. but with a different chartnumber
        #or price or whatever, just update global chartnumber or whatevs, call the function, then set the var back to what it was
        self.price = 0
        self.nextTrade = 0
        self.chartnumber = 0
        #doin these now
        self.high = 0
        self.low = 0
        
        #coins available to spend
        #A little fucked for larger pair, startbtc is going to actually be usdt
        if self.largerpair:
            #base is in USDT
            self.startbase = 100
        else:
            #base is in BTC
            self.startbase = 10
        self.availablebase = self.startbase
        #self.firstbuy = self.availablebase / 2.0
        #self.secondbuy = self.availablebase - self.firstbuy
        
        self.amtofalt = 0
        
        #self.secondtradeentries = 0
        self.totalentries = 0
        
        #how many trades can there be
        self.entries = 1
        #stop loss percent
        self.stopPercent = 10
        
        listofvars = ["crosstime","firstcross","crossPointA","crossPointB","percentlist","count",
                    "currentPrice","prices","ma5list","ma15list","ma15","ma5","pchange","ma5lower","ma5higher",
                    "lmaxes", "lmins", "ema", "rsi", "rsilist", "botmax", "botmin","pricechg", "pag", "pal","rsifirst",
                    "highs", "lows", "stochfirst", "k", "fast","bigma","bigmalist", "bolup", "bolmid", "bollow", "bandwidth"]
        
        '''
        Vars Explained:
        crosstime
            idk
        firstcross
            idk
        crossPointA
            idk
        crossPointB
            idk
        percentlist
            list for how much price has gone up/down percentage-wise for each
            ticker. Usually compared to last price, is changeable though
        count
            i think -tick number
        currentPrice
        prices
        ma5list
        ma15list
        ma15
        ma5
        pchange
        ma5lower
        ma5higher
        lmaxes
        lmins
        ema
        rsi
        rsilist
            
        '''
        
        for i in range(numofcharts):
            for item in range(len(listofvars)):
                key = listofvars[item] + str(i + 1)
                self.masterDick[key] = valuelist[item]
        print(self.masterDick)
        
        if self.graphics:
            self.graph = Graph(chartmax, chartmin, self.chartlen, pair, numofcharts, valuesAre, timestamps, extra, intervals, self.rsiper, self.stochper, self.bollingerper, ma5on=ma5on, handlon=handlon)
        
        
        
        #This only works for one chart at the moment
        self.entryprices = []
        #U still need to deal with self.orderPercent
        listoforder = ["orderPercent","avgentryprice"]
        ordervals = [0,0]
        self.orders = {}
        for num in range(numofcharts):
            for thing in range(len(listoforder)):
                key = listoforder[thing] + str(num + 1)
                self.orders[key] = ordervals[thing]
        print(self.orders)
        
        self.dentry = {}
        #setting number of allowed entries:
        #NEED TO DELETE THESE FROM ABOVE LOOP
        entryshit = ["placedOrder","orderPrice","orderGain","buy","tradeEntries"]
        entvals = [False,0,0,0,0]
        for n in range(numofcharts):
            for entr in range(1, self.entries + 1):
                for i in range(len(entryshit)):
                    key = entryshit[i] + str(entr) + str(n + 1)
                    self.dentry[key] = entvals[i]
        
        self.prevEma = 0
        #I'm lazy, we definitely can't run more than one chart now
        self.prevbigma = 0
        self.prevma15 = 0
        self.prevma5 = 0
        self.prevma15list = []
        self.prevma5list = []
        self.prevbigmalist = []
        self.prevPrices = []
        self.prevPrevEma = 0
        self.prevk = []
        self.prevfast = 0
        self.prevhighs = []
        self.prevlows = []
        self.prevrsi = 0
        self.prevpag = 0
        self.prevpal = 0
        self.prevPriceChg = []
        #Bollinger
        self.prevBolUp = 0
        self.prevBolMid = 0
        self.prevBolLow = 0
        
        #analytical
        self.upcount = 0
        self.downcount = 0
        self.downsnups = {}
        
        '''
        self.allAggs = []
        #Get ALL aggregate trades
        
        time = 0
        for time in range(time, tlen):
            self.allAggs.extend(self.client.get_aggregate_trades(symbol=self.pair, startTime=beginag + time * 3600000, endTime=beginag + (time + 1) * 3600000))
        self.lastAggIter = 0
        #print(self.allAggs)
        '''
    def tick(self, price, chartnumber, high, low, o, t):
        #############################################
        self.price = price
        self.chartnumber = chartnumber
        self.high = high
        self.low = low
        
        #nextTrade work
        nextTrades = []
        nextTradeTimes = []
        if self.last:
            #once we get to the latest kline we store current price into next trade vars 
            self.nextTrade = float(price)
            #nextTradeSeller = float(price)
            nextTradeTime = 0
        else:
            #testing to see if aggtrades enable/disable works
            #I'm setting nextTrades to current price so when we buy & sell it should be the same as if there was no nextTrades
            self.nextTrade = float(price)
            #nextTradeSeller = float(price)
            if self.aggTrades:
                #agtrades = self.client.get_aggregate_trades(symbol=self.pair, startTime=int(t),endTime=int(t) + 14400000)
                agtrades = self.client.get_aggregate_trades(symbol=self.pair, startTime=int(t),endTime=int(t) + 900000)
                print("agtrade len",len(agtrades))
                print("timestamp for agtrade is ", t)


                nextTradeSeller = agtrades[0]
                print(price)
                print (self.nextTrade)
                firstNextTrade = float(self.nextTrade['p'])
                print("FirstNextTrade:",firstNextTrade)
                print("Kline price:",price)
                if float(self.nextTrade['p']) == float(price):
                    print("Trade is equal :(")
                else:
                    print("Woohoo this means the next trade and not the current price is being used !! :)")
                    
                if not self.aggisNext:
                    counterbro = 1
                    while self.nextTrade['m']:
                        if counterbro >= len(agtrades):
                            self.nextTrade = agtrades[counterbro - 1]
                            print("There was no buyer that was maker ! ! ! !")
                            break
                        else:
                            self.nextTrade = agtrades[counterbro]
                            counterbro += 1
                    
                    counterbro = 1
                    while not nextTradeSeller['m']:
                        if counterbro >= len(agtrades):
                            nextTradeSeller = agtrades[counterbro - 1]
                            print("There was no seller that was maker ! ! !")
                            break
                        else:
                            nextTradeSeller = agtrades[counterbro]
                            counterbro += 1
                
                #get the fraction of nexttrade so we can plot it on x axis
                print("nextTrade time offset",str(float(self.nextTrade['T']) - t))
                #These numbers are hardcoded fuck
                nextTradeTime = (float(self.nextTrade['T']) - t) / 14400000
                
                nextTradeSeller = float(nextTradeSeller['p'])
                #print(nextTrade)
                self.nextTrade = float(self.nextTrade['p'])
                
            else:
                #ADDED THIS WHEN I RETURNED, TRYING TO ABANDON AGGTRADES
                #GOOD LUCK BRO
                pass
        
        #'''
        
        
        if self.masterDick["ema" + chartnumber] == 0:
            self.masterDick["ema" + chartnumber] = float(price)
        self.prevPrevEma = self.prevEma
        self.prevEma = self.masterDick["ema" + chartnumber]
        
        #ema period is 20
        self.masterDick["ema" + chartnumber] = self.indicators.expMovingAverage(float(price), 20, self.prevEma)
        ema = self.masterDick["ema" + chartnumber]
        
        #this is the one screwing it up
        #lengpc = len(self.masterDick["pricechg" + chartnumber])
        self.prevPriceChg = self.masterDick["pricechg" + chartnumber]
        if self.masterDick["count" + chartnumber] > 0:
            self.masterDick["pricechg" + chartnumber].append(float(price) - self.masterDick["currentPrice" + chartnumber])
        pricechg = self.masterDick["pricechg" + chartnumber]
        if len(pricechg) > self.rsiper:
            del pricechg[0]
            
        self.masterDick["currentPrice" + chartnumber] = float(price)
        
        self.prevPrices = self.masterDick["prices" + chartnumber]
        self.masterDick["prices" + chartnumber].append(self.masterDick["currentPrice" + chartnumber])
        prices = self.masterDick["prices" + chartnumber]
        
        #stochastic
        self.prevhighs = self.masterDick["highs" + chartnumber]
        self.prevlows = self.masterDick["lows" + chartnumber]
        self.masterDick["highs" + chartnumber].append(high)
        self.masterDick["lows" + chartnumber].append(low)
        highs = self.masterDick["highs" + chartnumber]
        lows = self.masterDick["lows" + chartnumber]
        if len(highs) > self.stochper:
            del highs[0]
            del lows[0]
        
        self.prevbigma = self.masterDick["bigma" + chartnumber]
        self.masterDick["bigma" + chartnumber] = self.indicators.movingAverage(self.masterDick["prices" + chartnumber], 250)
        self.bigma = self.masterDick["bigma" + chartnumber]
        
        self.prevbigmalist = self.masterDick["bigmalist" + chartnumber]
        self.masterDick["bigmalist" + chartnumber].append(self.masterDick["bigma" + chartnumber])
        bigmalist = self.masterDick["bigmalist" + chartnumber]
        
        self.prevma15 = self.masterDick["ma15" + chartnumber]
        self.masterDick["ma15" + chartnumber] = self.indicators.movingAverage(self.masterDick["prices" + chartnumber], 15)
        self.ma15 = self.masterDick["ma15" + chartnumber]
        
        self.prevma15list = self.masterDick["ma15list" + chartnumber]
        self.masterDick["ma15list" + chartnumber].append(self.masterDick["ma15" + chartnumber])
        ma15list = self.masterDick["ma15list" + chartnumber]
        
        self.prevma5 = self.masterDick["ma5" + chartnumber]
        self.masterDick["ma5" + chartnumber] = self.indicators.movingAverage(self.masterDick["prices" + chartnumber], 5)
        self.ma5 = self.masterDick["ma5" + chartnumber]
        
        self.prevma5list = self.masterDick["ma5list" + chartnumber]
        self.masterDick["ma5list" + chartnumber].append(self.masterDick["ma5" + chartnumber])
        ma5list = self.masterDick["ma5list" + chartnumber]
        
        ####Bollinger####
        #I think using greater than fixed something
        if (len(self.masterDick["prices" + chartnumber]) > self.bollingerper):
            self.bolmid = self.indicators.movingAverage(self.masterDick["prices" + chartnumber], self.bollingerper)
            self.masterDick["bolmid" + chartnumber].append(self.bolmid)
            self.bolup = self.bolmid + self.indicators.stddev(self.masterDick["prices" + chartnumber][(self.bollingerper * -1):]) * 2
            self.masterDick["bolup" + chartnumber].append(self.bolup)
            self.bollow = self.bolmid - self.indicators.stddev(self.masterDick["prices" + chartnumber][(self.bollingerper * -1):]) * 2
            self.masterDick["bollow" + chartnumber].append(self.bollow)
            self.bandwidth = (self.bolup - self.bollow) / float(price) * 100
            self.masterDick["bandwidth" + chartnumber].append(self.bandwidth)
        #just untabbed these for reference in graph.listadd
        boluplist = self.masterDick["bolup" + chartnumber]
        bollowlist = self.masterDick["bollow" + chartnumber]
        bolmidlist = self.masterDick["bolmid" + chartnumber]
        bandwidth = self.masterDick["bandwidth" + chartnumber]
        #print("Bandwidth:",self.bandwidth)
            
        
        #----rsi start----
        #If the data points hit the period of the rsi, start calculating it
        if self.masterDick["rsifirst" + chartnumber] and (len(pricechg) == self.rsiper):
            self.masterDick["rsi" + chartnumber] = self.indicators.rsi(pricechg)
            self.masterDick["pag" + chartnumber] = self.indicators.pag
            self.masterDick["pal" + chartnumber] = self.indicators.pal
            print("Ran on iteration",self.masterDick["count" + chartnumber])
            
            self.masterDick["rsilist" + chartnumber].append(self.masterDick["rsi" + chartnumber])
        elif not self.masterDick["rsifirst" + chartnumber]:
            #prev values
            self.prevrsi = self.masterDick["rsi" + chartnumber]
            self.prevpag = self.masterDick["pag" + chartnumber]
            self.prevpal = self.masterDick["pal" + chartnumber]
            
            self.masterDick["rsi" + chartnumber] = self.indicators.rsi(pricechg, self.masterDick["pag" + chartnumber], self.masterDick["pal" + chartnumber])
            self.masterDick["pag" + chartnumber] = self.indicators.pag
            self.masterDick["pal" + chartnumber] = self.indicators.pal

            self.masterDick["rsilist" + chartnumber].append(self.masterDick["rsi" + chartnumber])
        
        rsilist = self.masterDick["rsilist" + chartnumber]
        rsi = self.masterDick["rsi" + chartnumber]
        
        if len(pricechg) == self.rsiper and self.masterDick["rsifirst" + chartnumber]:
            self.masterDick["rsifirst" + chartnumber] = False
            print("Falsified rsifirst",self.masterDick["count" + chartnumber],len(pricechg))
        #----rsi end----
        
        #----stochastic start----
        if len(highs) == self.stochper:
            #previous values
            if len(self.masterDick["k" + chartnumber]) > 0:
                self.prevk = self.masterDick["k" + chartnumber]
                self.prevfast = self.masterDick["fast" + chartnumber]
                
            self.masterDick["k" + chartnumber].append(self.indicators.stochastic(float(price), min(lows), max(highs)))
            k = self.masterDick["k" + chartnumber]
            if len(k) > 3:
                del k[0]
            self.masterDick["fast" + chartnumber] = self.indicators.movingAverage(k, len(k))
        else:
            k = self.masterDick["k" + chartnumber]
        fast = self.masterDick["fast" + chartnumber]
        #----stochastic end----
        
        
        #Local Maximums and Minimums
        if len(prices) > 1:
            lastwasmax = self.indicators.maxes(prices[-3:])
            lastwasmin = self.indicators.mins(prices[-3:])
            
            if lastwasmax:
                lmaxes = self.masterDick["lmaxes" + chartnumber]
                if lmaxes[0] == -1:
                    lmaxes[0] = self.masterDick["count" + chartnumber] - 1
                else:
                    lmaxes.append(self.masterDick["count" + chartnumber] - 1)
                    
            
            elif lastwasmin:
                lmins = self.masterDick["lmins" + chartnumber]
                if lmins[0] == -1:
                    lmins[0] = self.masterDick["count" + chartnumber] - 1
                else:
                    lmins.append(self.masterDick["count" + chartnumber] - 1)
            
        self.checkCross(prices[0])
                    
        
        self.masterDick["pchange" + chartnumber] = self.indicators.percentChange(prices, 5)
        self.masterDick["percentlist" + chartnumber].append(self.masterDick["pchange" + chartnumber])
        
        #setting these to clean up graph.add below
        lmax = self.masterDick["lmaxes" + chartnumber]
        lmins = self.masterDick["lmins" + chartnumber]
        
        if chartnumber == "1":
            #Buy/sell
            #I added +1 so we have the current and previous rsi/stochastic value available. could possibly need to change to +2
            if self.masterDick["count" + chartnumber] >= self.stochper + 1 and self.masterDick["count" + chartnumber] >= self.rsiper + 1:
                
                #JUST TOOK OUT EVALUATEPOSITIONS() BECAUSE IT FUCKIN SUCKS PASSING EVERYTHING THROUGH
                #self.evaluatePositions(price, lows, high, highs, k, o, rsi, chartnumber, t)
                #self.evaluatePositions(price, nextTrade, lows, high, highs, k, o, rsi, chartnumber, t)#, nextTradeSeller)
                prices = self.masterDick["prices" + chartnumber]
        
                if((self.masterDick["currentPrice" + chartnumber] < self.ma5) and (self.masterDick["currentPrice" + chartnumber] < self.ma15)):
                    if(self.masterDick["currentPrice" + chartnumber] > prices[-2] or self.masterDick["currentPrice" + chartnumber] == prices[-2]):
                        #print("BUY")
                        pass
                
                #you need to make sure the btc in your account matches up with availablebtc
                #This sets available trading funds (entries)
                if not self.dentry["placedOrder1" + chartnumber]:
                    for y in range(1, self.entries + 1):
                        self.dentry["buy" + str(y) + chartnumber] = self.availablebase / float(self.entries)
                        #print("vbuy" + str(y),self.dentry["buy" + str(y) + chartnumber])
                
                #trying moving entrycalc outside strats, check history to see if entrycalc is same in each
                #Most recent - it passed self through as an argument - deleting that
                self.entrycalc(lows, o)
                if self.strat > 0:
                    eval(self.stratlist[self.strat])
                    #putting stoploss check after strat(so it doesn't buy again instantly, REVIEW THIS IN THE FUTURE
                    if self.dentry["placedOrder1" + chartnumber]:
                        self.stoploss()
                    
                    #error check
                    if self.availablebase < 0:
                        print("FUCK BITCOIN IS IN THE NEGATIVES-ERROR")
                        print(str(self.availablebase))
                        
        
        if self.graphics:
            self.graph.add(price, self.ma5, self.ma15, self.bigma, self.masterDick["pchange" + chartnumber], self.masterDick["crossPointA" + chartnumber], self.masterDick["crossPointB" + chartnumber], self.masterDick["crosstime" + chartnumber], self.masterDick["firstcross" + chartnumber], chartnumber, lmax[-1], lmins[-1], ema, rsi, high, low, k, fast, self.nextTrade, self.bolmid, self.bolup, self.bollow, self.bandwidth)#, nextTradeTime)
        
        
        #Since the line between the last two MAcrosses was just graphed, we
        #change the first point for the next line to the last point of 
        #the current one
        if (self.masterDick["crosstime" + chartnumber]):
            self.masterDick["crossPointA" + chartnumber] = self.masterDick["crossPointB" + chartnumber]
            self.masterDick["crossPointB" + chartnumber] = 0
            self.masterDick["firstcross" + chartnumber] = self.masterDick["count" + chartnumber]
            self.masterDick["crosstime" + chartnumber] = False
        
        self.masterDick["count" + chartnumber] += 1
        
        
        #End of historical klines
        #DO NOT DELETE, THIS LAUNCHES THE GRAPH
        #if statement checks if is live and current chart hit the last iteration, self.last
        if (self.masterDick["count" + chartnumber] == self.chartlen[int(chartnumber) - 1]) and (not self.live):
            print("so this is the last item in chart" + chartnumber)
            #total percentage gain
            availableBasePlaceHolder = 0
            if self.dentry["placedOrder1" + chartnumber]:
                if self.largerpair:
                    availableBasePlaceHolder = self.availablebase + self.amtofalt * float(price) * .999
                else:
                    availableBasePlaceHolder = self.availablebase + int(self.amtofalt) * float(price) * .999
            else:
                availableBasePlaceHolder = self.availablebase
            #percentageee = (availableBasePlaceHolder - self.startbase) * 100 / self.startbase
            percentageee = (availableBasePlaceHolder - self.startbase) * 100 / self.startbase
            if self.graphics:
                self.graph.listadd(ma5list, ma15list, bigmalist, self.masterDick["percentlist" + chartnumber], percentageee, rsilist, chartnumber, boluplist, bollowlist, bolmidlist, bandwidth)
            
            #change to if(chartnumber == "1"):
            print("just ran listadd" + chartnumber)
            if(self.last):
                #RETURN################################################^&*&^%$#$%^&*^%$#@$%^&*&^%$#
                #mas
                print("mas")
                #print("ma5",self.prevma5,"ma5list",self.prevma5list,"ma15",self.prevma15,"ma15list",self.prevma15list)
                #ema
                print('ema')
                print("prevEma",self.prevPrevEma,"ema",self.prevEma)
                #stochastic
                print('stochastic')
                print("k",self.prevk,"fast",self.prevfast)
                print("highs",self.prevhighs,"lows",self.prevlows)
                
                #RSI
                print('rsi')
                print("rsi",self.prevrsi,"pag",self.prevpag,"pal",self.prevpal)
                #Timestamps  ??????
                
                #if u use this code for liverun, DON'T ACTUALLY SELL
                if self.dentry["orderPrice1" + self.chartnumber] != 0:
                    self.sell(final=True)
                print("Started with:", self.startbase, "Ended with:", self.availablebase)
                print("percent win:",percentageee)
                print("first entries:",self.totalentries)
                print("Times the price went up during market order buys:",self.amtofups)
                for keyz in self.downsnups:
                    print(keyz)
                    sumb = 0
                    for numb in self.downsnups[keyz]:
                        sumb += numb
                    sumb /= len(self.downsnups[keyz])
                    print(sumb)
                        
                print( )
                for poop in range(2,self.entries + 1):
                    print(str(poop) + "entries:",self.dentry["tradeEntries" + str(poop) + chartnumber])
                if self.graphics:
                    self.graph.anal()
                    
        #return data for further analysis
        #run with a spec strat for marketcomb?
        
        
        #analysis
        
        if len(prices) > 1:
            #add this in
            
            if float(price) == prices[-2]:
                #decide what to do
                pass
            #goin down
            elif float(price) - prices[-2] < 0:
                if self.upcount != 0:
                    #add shit to dict
                    if str(self.downcount) in self.downsnups:
                        self.downsnups[str(self.downcount)].append(self.upcount)
                    else:
                        self.downsnups[str(self.downcount)] = [self.upcount]
                    self.downcount = 0
                    self.upcount = 0
                self.downcount += 1
            #goin up
            else:
                #if it hasn't gone down hyet we don't care - decide what to do if price doesnt change above
                if self.downcount != 0:
                    self.upcount += 1
        
            print(self.downsnups)
            print("upc",self.upcount)
            print("downc",self.downcount)
        
    
    #####################
    #####END OF TICK#####
    #####################
    
    
    def buy(self):
        price = float(self.price)
        print("buy")
        print('avbl BTC:',self.availablebase)
        self.totalentries += 1
        self.dentry["placedOrder1" + self.chartnumber] = True
        #self.orders["orderPrice" + chartnumber] = self.masterDick["currentPrice" + chartnumber]
        
        
        #######IMPLEMENTING NEXTTRADE
        #self.dentry["orderPrice1" + chartnumber] = price
        self.dentry["orderPrice1" + self.chartnumber] = self.nextTrade
        
        #if btc to usd, etc
        if self.largerpair:
            altbuy = self.dentry["buy1" + self.chartnumber] / self.nextTrade
        else:
            #altbuy = int(self.dentry["buy1" + chartnumber] / price)
            altbuy = int(self.dentry["buy1" + self.chartnumber] / self.nextTrade)
        
        #janky way of using nextTrade
        #Do I need this? already setting altbuy to nextTrade price
        secondattempt = False
        if price < self.nextTrade:
            altbuy = int(altbuy * .9)
            secondattempt = True
            self.amtofups += 1
        
        #Hmmmmmm BTCUSDT etc pops this
        if altbuy * self.nextTrade > self.availablebase:
            print("ERROR ERROR ERROR ERROR ERROR")
        
        #COMBINE THIS TO IF STATEMENT A FEW LINES UP
        #also idk if will work
        self.availablebase -= altbuy * self.nextTrade
        altbuy -= altbuy * .0026
        self.amtofalt += altbuy
        
        #self.entryprices.append(price)
        self.entryprices.append(self.nextTrade)
        print(self.entryprices)
        if self.graphics:
            self.graph.buy(self.masterDick["currentPrice" + self.chartnumber], self.masterDick["count" + self.chartnumber], self.chartnumber, 1)
        print("Fun:",self.amtofalt)
        print("Buy1",self.dentry["buy1" + self.chartnumber])
        print("NextPrice:",self.nextTrade)
        if secondattempt:
            print("On second attempt")
        else:
            print("On first attempt")
        
    def sell(self, final=False, stopped=False):
        price = float(self.price)
        self.dentry["placedOrder1" + self.chartnumber] = False
        self.dentry["orderGain1" + self.chartnumber] = ((self.masterDick["currentPrice" + self.chartnumber] - self.dentry["orderPrice1" + self.chartnumber]) / self.dentry["orderPrice1" + self.chartnumber]) * 100
        self.dentry["orderGain1" + self.chartnumber] = self.dentry["orderGain1" + self.chartnumber] / float(self.entries)
        for x in range(2, self.entries + 1):
            if self.dentry["placedOrder" + str(x) + self.chartnumber]:
                self.dentry["placedOrder" + str(x) + self.chartnumber] = False
                self.dentry["orderGain" + str(x) + self.chartnumber] = ((self.masterDick["currentPrice" + self.chartnumber] - self.dentry["orderPrice" + str(x) + self.chartnumber]) / self.dentry["orderPrice" + str(x) + self.chartnumber]) * 100
                self.dentry["orderGain" + str(x) + self.chartnumber] = self.dentry["orderGain" + str(x) + self.chartnumber] / float(self.entries)
        
        #may or may not work
        if self.largerpair:
            self.availablebase += self.amtofalt * price * .9984
            self.amtofalt -= self.amtofalt
        else:
            #self.availablebase += int(self.amtofalt) * nextTradeSeller
            self.availablebase += int(self.amtofalt) * price * .9984
            self.amtofalt -= int(self.amtofalt)
        if self.graphics and not final:
            self.graph.sell(self.masterDick["currentPrice" + self.chartnumber], self.masterDick["count" + self.chartnumber], self.dentry["orderGain1" + self.chartnumber], self.chartnumber, stopped)
        print("sell",self.price)
        print("NextPrice:",self.nextTrade)
        print("BTC:",self.availablebase)
        #this gon fuck it up
        self.entryprices = []
    
    def stoploss(self):
        """
        Gets out of the buy if price dips below predetermined percent
        """
        price = float(self.price)
        print("orderPrice1:",self.dentry["orderPrice1" + self.chartnumber])
        if (self.dentry["orderPrice1" + self.chartnumber] - price) / self.dentry["orderPrice1" + self.chartnumber] * 100 >= self.stopPercent:
            self.sell(stopped=True)
    
    def entrycalc(self, lows, o):
        """
        I think this has something to do with how many times you go in, might wanna leave it to the strats
        """
        price = float(self.price)
        
        #print(nextTrade==price,nextTradeSeller==price)
        for i in range(2, self.entries + 1):
            if len(self.entryprices) > 0:
                avgentryprice = sum(self.entryprices) / len(self.entryprices)
                #if previous entry has been placed and current hasn't and other args are met
                if self.dentry["placedOrder" + str(i - 1) + self.chartnumber] and price < avgentryprice and float(price) < lows[-2] and float(price) < float(o) and not self.dentry["placedOrder" + str(i) + self.chartnumber]:
                    self.dentry["placedOrder" + str(i) + self.chartnumber] = True
                    #add these to dict
                    print("trade number",str(i))
                    self.dentry["tradeEntries" + str(i) + self.chartnumber] += 1
                    #self.totalentries += 1
                    
                    #I changed these from price to nextTrade
                    self.dentry["orderPrice" + str(i) + self.chartnumber] = price
                    #self.dentry["orderPrice" + str(i) + chartnumber] = self.nextTrade
                    
                    #altbuy = int(self.dentry["buy" + str(i) + chartnumber] / price)
                    altbuy = int(self.dentry["buy" + str(i) + self.chartnumber] / self.nextTrade)
                    
                    #self.availablebase -= altbuy * price
                    self.availablebase -= altbuy * self.nextTrade
                    altbuy -= altbuy * .001
                    self.amtofalt += altbuy
                    ###HOW LONG TO WE WANT ENTRYPRICES TO BE??
                    
                    #self.entryprices.append(price)
                    self.entryprices.append(self.nextTrade)
                    if self.graphics:
                        self.graph.buy(self.masterDick["currentPrice" + self.chartnumber], self.masterDick["count" + self.chartnumber], self.chartnumber, i)
                    #print("Fun:",self.amtofalt)
                    print("Buy" + str(i),self.dentry["buy" + str(i) + self.chartnumber])
                    break
    
    def checkCross(self, price):
        #if moving avgs cross
        if (self.masterDick["count" + self.chartnumber] > 0):
            
            ma5list = self.masterDick["ma5list" + self.chartnumber]
            ma15list = self.masterDick["ma15list" + self.chartnumber]
            self.masterDick["ma5lower" + self.chartnumber] = ma15list[-2] <= ma5list[-2] and ma15list[-1] > ma5list[-1]
            self.masterDick["ma5higher" + self.chartnumber] = ma15list[-2] >= ma5list[-2] and ma15list[-1] < ma5list[-1]
            
            #This buys or sells due to a cross in the MAs, you'll want to
            #move this out of this if statement eventually bcoz it will
            #evaluate other factors as well
            #self.evaluatePositions(chartnumber)
                    
            if(self.masterDick["ma5lower" + self.chartnumber] or self.masterDick["ma5higher" + self.chartnumber]):
                self.masterDick["crossPointA" + self.chartnumber], self.masterDick["crossPointB" + self.chartnumber] = self.indicators.MACross(ma5list[-2:], ma15list[-2:], self.masterDick["crossPointA" + self.chartnumber], price)
                
                self.masterDick["crosstime" + self.chartnumber] = True
                    
    #evaluate the position of a chart only when it's gained an item. use smaller chart changes
    #to influence current buys in the bigger charts
    '''
    def evaluatePositions(self, price, nextTrade, lows, high, highs, k, o, rsi, chartnumber, t, nextTradeSeller=None):
        prices = self.masterDick["prices" + chartnumber]
        
        if((self.masterDick["currentPrice" + chartnumber] < self.ma5) and (self.masterDick["currentPrice" + chartnumber] < self.ma15)):
            if(self.masterDick["currentPrice" + chartnumber] > prices[-2] or self.masterDick["currentPrice" + chartnumber] == prices[-2]):
                #print("BUY")
                pass
        
        #you need to make sure the btc in your account matches up with availablebtc
        #could have rounding errors and say you have more than you actually do, shouldn't be significant tho-
        #especially if you check your bitcoin funds after every sell
        if not self.dentry["placedOrder1" + chartnumber]:
            for y in range(1, self.entries + 1):
                self.dentry["buy" + str(y) + chartnumber] = self.availablebase / float(self.entries)
                #print("vbuy" + str(y),self.dentry["buy" + str(y) + chartnumber])
        
        #trying moving entrycalc outside strats, check history to see if entrycalc is same in each
        self.entrycalc(self, price, chartnumber, nextTrade, lows, o)
        if self.strat > 0:
            eval(self.stratlist[self.strat])
            
            #error check
            if self.availablebase < 0:
                print("FUCK BITCOIN IS IN THE NEGATIVES-ERROR")
                print(str(self.availablebase))
            
    '''
    
    ######Strategies########################################################
    
    #THIS ONE IS FUCKING GREAT FOR FUNBTC
    def firstone(self, lows, highs, k, o):#, nextTradeSeller):
        price = float(self.price)
        prices = self.masterDick["prices" + self.chartnumber]
        #self.entrycalc(price, chartnumber, nextTrade, lows, o)
            
        #buy/sell
        #need 2 change stochastic
        #just added rsi for testing
        #print(self.price,self.dentry["orderPrice1" + self.chartnumber])
        #print(type(self.dentry["orderPrice1" + self.chartnumber]), "butt")
        if price < prices[-2] and prices[-2] < prices[-3] and self.high < highs[-2] and k[-1] < self.masterDick["fast" + self.chartnumber] and not self.dentry["placedOrder1" + self.chartnumber]:# and rsi < 50:
            self.buy()
        
        elif price > self.ma15 and price > highs[-2] and self.dentry["placedOrder1" + self.chartnumber]:# and (self.dentry["orderPrice1" + self.chartnumber] * 1.001 < price * 1.001 or price < self.bigma):
            self.sell()
        
    
    ##############################################################################################################
    ##############################################################################################################
    
    def secondone(self, lows, highs, k, o):
        price = float(self.price)
        prices = self.masterDick["prices" + self.chartnumber]
        #self.entrycalc(price, chartnumber, nextTrade, lows, o)
            
        #buy/sell
        #need 2 change stochastic
        #just added rsi for testing
        if price < prices[-2] and prices[-2] < prices[-3] and prices[-3] < prices[-4] and self.high < highs[-2] and k[-1] < self.masterDick["fast" + self.chartnumber] and not self.dentry["placedOrder1" + self.chartnumber]:# and rsi < 50:
            self.buy()
        
        elif price > self.ma15 and price > highs[-2] and self.dentry["placedOrder1" + self.chartnumber]:
            self.sell()
        
        
        
    #BTCUSDT on 12 hour interval
    def thirdone(self):
        #setting vars to simple names to reduce clutter
        price = float(self.price)
        rsi = self.masterDick["rsi" + self.chartnumber]
        
        #could do this or put something in botIndicators to check? - Maybe not
        if len(self.masterDick["prices" + self.chartnumber]) > self.bollingerper + 2:
            
            bws = self.masterDick["bandwidth" + self.chartnumber]
            if self.bandwidth < 14 and price > self.bolup and not self.dentry["placedOrder1" + self.chartnumber]:
                self.buy()
                
            #bandwidth less than last one AND rsi/stoch calmed down AND price is greater or smaller than last one
            elif self.bandwidth < bws[-2] and rsi > 50 and self.dentry["placedOrder1" + self.chartnumber]:
                self.sell()
    
    
    #######################################################
    #############YOU ARE AT THE BOTTOM#####################
    #######################################################
        