import sys, getopt
from binance.client import Client

from botchart import BotChart
from botstrategy import BotStrategy
from threading import Thread
from graphics import Point
import time
from binance.enums import KLINE_INTERVAL_30MINUTE


#Implementations:
#Make number of entries variable

#Make the bot check through multiple coins to find best ones to buy first. maybe use volume and volatility as a factor
#Have the bot check other coins every once in a while so there's always something to buy
#^^^how to do this-check bollinger bands at higher intervals, same with rsi/stochastic

#Make multiple current buys possible rather than just one, analyze past trades to make profits off them
#when starting up
#Check how much bitcoin you have and use it

#Once you have micro-trading done (1% gains in short periods), focus on trades that last multiple days

#Add stop losses, and detect when the market crashes and when it recovers

#Monitor bitcoin constantly, remember how bitcoin determines altcoins. Use this information to help determine
#buying and selling-do tests to see how much it actually influences other markets

#Write down how the bot uses the information it's working with (macd, moving average crossings, etc)

#Get the MACD goin

#during live trading, have the most recent klines return the last trade instead of the first one during that period.
#analyze from 1hr-30min-5min-1min or something. run lotsa tests.

#get a better way to calculate local maxes or somethin

#When there is a time to sell, watch the other graphs closely

#Add y values on left side of graphs

#check volatility
#graph volume
#Fixes:

#do something about lining up the graphs

#When selling make it watch the graphs rather than just bailing at 1%. 
#Get it to buy right when the mas cross instead of after

#####CURRENT GOAL: ADD HIGHS AND LOWS TO DATA
#####GET BOTSTRATEGY TO INIT WITH AS LITTLE PARAMS AS POSSIBLE
#####GOTTA DEAL WITH EXTRAS!!!!
#####NEXT GOAL: CHANGE THE LAST ITEM IN LIST TO CURRENT PRICE, USE THIS TO
#####DETECT MACROSSES AS THEY HAPPEN INSTEAD OF AFTER
#####MAKE A FUNCTION THAT DETECTS CROSSES - MACROSSES AND PRICE/MA CROSSES
class Backtest(object):
    def __init__(self, pair, live=False, numberOfCharts=1, strat=0, klineint=0, ss="", es="", graphics=True, ma5=True, handl=True):
        #sets kline interval to what the selected strat uses
        stratintervals = [Client.KLINE_INTERVAL_30MINUTE]
        if klineint == 0:
            klineint = stratintervals[strat]
            
            
        
        #graphs = [Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_5MINUTE]
        
        
        #Set startstamp to the highest kline interval chart and then pass it to the other charts
        #this starts the graphs at the same time, will makes things 999999999x easier
        if numberOfCharts != 1:
            self.chart3 = BotChart(pair,300,klineint, stringy=ss, endstring=es)
            startstamp = self.chart3.timestamps[0] // 1000
            self.chart2 = BotChart(pair,300,klineint, startstamp, stringy=ss, endstring=es)
        #startstamp = chart2.timestamps[0] // 1000
        #print(startstamp)
        
        #Changed chart to global var so I can access list values
        if numberOfCharts == 1:
            self.chart = BotChart(pair,300,klineint, stringy=ss, endstring=es)
        else:
            self.chart = BotChart(pair,300,klineint, startstamp, stringy=ss, endstring=es)
        chartmax = self.chart.getMax()
        chartmin = self.chart.getMin()
        
        #Get how many times one interval goes into another by minutes
        intervals = {"1":[6],"2":[2],"3":[2]}
        intervals = [6,2]
        
        
        chartlen = len(self.chart.data)
        if numberOfCharts != 1:
            chartlen2 = len(self.chart2.data)
            chartlen3 = len(self.chart3.data)
        
        #either multiply chartlen by a factor (6) and subtract chart2len
        #to get the extra at the end or find the closest 30 minute and 
        #see how many 5 minutes go into it from the current time
        #I'll start by doing the first
        interval = intervals[0]
        if numberOfCharts != 1:
            #need multiple extras
            extra1 = (len(self.chart.data) - 1) - (len(self.chart3.data) - 1) * 30
            extra2 = (len(self.chart2.data) - 1) - (len(self.chart3.data) - 1) * 6
            extra3 = 0
            extra = [extra1, extra2, extra3]
        
        
            #delete these from valuelist
            chartlengths = [chartlen,chartlen2,chartlen3]
            timestamps = [self.chart.timestamps,self.chart2.timestamps,self.chart3.timestamps]
            data = [self.chart.data,self.chart2.data,self.chart3.data]
            '''
            lmaxes = [chart.lmaxes,chart2.lmaxes,chart3.lmaxes]
            highs = [chart.highs,chart2.highs,chart3.highs]
            lows = [chart.lows,chart2.lows,chart3.lows]
            '''
        else:
            extra = [0]
            chartlengths = [chartlen]
            timestamps = [self.chart.timestamps]
        print("data chart length",len(self.chart.data))
        begin = time.time()
        #Might need some cleanup here
        
        #There's gotta be a better way
        #I think i should make prices be its own list like lmaxes and data etc - maybe do this with all the lists
        #there has to be multiple lists in valuelist because the lists become the same if they're not duplicated
        #valuelist = [[False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],0,0,[],1,0,[],False,False,True,0,[],[],True,[],0,0,[],[],[],[]],[False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],0,0,[],1,0,[],False,False,True,0,[],[],True,[],0,0,[],[],[],[]],[False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],0,0,[],1,0,[],False,False,True,0,[],[],True,[],0,0,[],[],[],[]]]
        valuelist = [False,0,Point(0,0),0,[],0,"",[],[],[],0,0,0,False, False,[-1],[-1],0,0,[],1,0,[],False,False,True,[],[],True,[],0,0,[],[],[],[],[]]

        print("chart.data:",self.chart.data)
        self.strategy = BotStrategy(strat, chartmax, chartmin, chartlengths, pair, numberOfCharts, self.chart.valuesAre, timestamps, extra, valuelist, intervals, int(self.chart.timestamps[0]), int(self.chart.timestamps[-1]), len(self.chart.timestamps),live,aggTrades=False,aggisNext=False, graphics=graphics, ma5on=ma5, handlon=handl)
        
        #Before doing this first migrate all data from graph to botstrategy
        #pass through all the different chart vars in strategy and scrap reinit
        #for candlestick in range(len(chart.data)):
        #    if (chart.timestamps[candlestick] == chart2.timestamps[candlestick]):
        #        strategy.tick(chart2.data[candlestick], 2)
        #    strategy.tick(chart.data[candlestick], 1)
        print("extra",extra)
        #I think chart is supposed to have the most klines
        for candlestick in range(len(self.chart.data)):
            print("\nTick number:",candlestick)
            #print(len(self.chart.data))
            #print(chart.timestamps[candlestick],chart2.timestamps[candlestick//5])
            #if (chart.timestamps[candlestick] == chart2.timestamps[candlestick//2] ):
                #if (chart2.timestamps[candlestick//5] == chart3.timestamps[candlestick//30]):
                #   strategy.tick(chart3.data[candlestick//30], "3")
                #strategy.tick(chart2.data[candlestick//2], "2", float(chart2.highs[candlestick//2]), float(chart2.lows[candlestick//2]), float(chart2.opens[candlestick//2]))
            if (candlestick == len(self.chart.data) - 1):
                #
                self.strategy.last = True
                #this is so dirty and I feel dirty for doing it
                #could mess up live run, move highs and lows to masterDick in botstrategy if so
                if graphics:
                    self.strategy.graph.addLists("1", self.chart.highs, self.chart.lows)
                end = time.time()
                print("time taken:",end - begin)
            print("Candestick Data:",self.chart.data[candlestick])
            self.strategy.tick(self.chart.data[candlestick], "1", float(self.chart.highs[candlestick]), float(self.chart.lows[candlestick]), float(self.chart.opens[candlestick]), float(self.chart.timestamps[candlestick]))
            #maybe run strategy.graph.listadd(params) every iteration-think of other strategies tho
        
        
        '''
        self.charts = True
        strategy.reinit(self.charts)
        for candlestick in chart2.data:
            strategy.tick(candlestick, "2")
        '''
        #this is the last chart
        '''
        self.charts = True
        strategy.reinit(self.charts, chart3.lmaxes, chartlen3, chart3.data, chart3.timestamps)
        for candlestick in chart3.data:
            strategy.tick(candlestick)
        '''
    def getstuff(self):
        return self.strategy.prevPrices, self.strategy.prevma5, self.strategy.prevma5list, self.strategy.prevma15, self.strategy.prevma15list, self.strategy.prevPrevEma, self.strategy.prevEma, self.strategy.prevk, self.strategy.prevfast, self.strategy.prevhighs, self.strategy.prevlows, self.strategy.prevrsi, self.strategy.prevpag, self.strategy.prevpal, self.strategy.prevPriceChg

