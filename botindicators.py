from graphics import Point
import math
from math import sqrt
class BotIndicators(object):
    def __init__(self):
        #rsi
        self.pag = 0
        self.pal = 0
    
    def movingAverage(self, dataPoints, period):
        #if (len(dataPoints) > 1):
        return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
    
    def expMovingAverage(self, price, period, prev):
        #sma = self.movingAverage(dataPoints, period)
        multiplier = 2 / (period + 1)
        ema = (price - prev) * multiplier + prev
        #ema = (price * multiplier) + (prev * (1 - multiplier))
        return ema
        
            
    def percentChange(self, dataPoints, period):
        if (len(dataPoints) >= period):
            return (dataPoints[-1] - dataPoints[-period]) / dataPoints[-1] * 100
        else:
            return 0.00
        
    def MACross(self, ma5list, ma15list, crossPointA, price):
        dy = ma5list[1] - ma5list[0]
        dx = 1
        m5 = dy/dx
        dy = ma15list[1] - ma15list[0]
        m15 = dy/dx
        xfact = m15 - m5
        otherside = ma5list[0] - ma15list[0]
        ans = otherside / xfact
        y5 = ans * m5 + ma5list[0]
        y15 = ans * m15 + ma15list[0]
        
        A = crossPointA
        if (A.getX() == 0.0 and A.getY() == 0.0):
            A = Point(0,price)
            B = Point(ans,y15)
        else:
            B = Point(ans,y15)
    
        return A, B
    
    
    def rsi(self, chglist, pg=False, pl=False):
        pos = 0
        neg = 0
        rs = 0
        leng = len(chglist)
        #print("leng",leng)
        currentgain = 0
        currentloss = 0
        if not (pg or pl):
            for item in chglist:
                if item > 0:
                    pos += item
                else:
                    neg -= item
            if neg:
                rs = (pos/leng)/(neg/leng)
        else:
            if chglist[-1] > 0:
                currentgain = chglist[-1]
            else:
                currentloss = chglist[-1] * -1
            pos = (pg * (leng - 1) + currentgain)/leng
            neg = (pl * (leng - 1) + currentloss)/leng
            if neg:
                rs = pos/neg
        
        self.pag = pos
        self.pal = neg
        #print(neg)
        #print(rs)
        if neg:
            rsi = 100 - (100/(1 + rs))
        else:
            rsi = 100
        return rsi
    
    def stochastic(self, c, l, h):
        return 100 * (c - l)/(h - l)
    
    def stddev(self, prices):
        mean = 0
        deviation = 0
        for item in prices:
            mean += item
        mean /= len(prices)
        
        for item in prices:
            deviation += (item - mean)**2
        deviation /= len(prices)
        deviation = sqrt(deviation)
        
        return deviation
    
    #calculates if last number was a max
    def maxes(self, points):
        if len(points) == 2:
            return points[1] < points[0]
        else:
            return points[0] < points[1] and points[2] < points[1]
        
    def mins(self, points):
        if len(points) == 2:
            return points[1] > points[0]
        else:
            return points[0] > points[1] and points[2] > points[1]
        