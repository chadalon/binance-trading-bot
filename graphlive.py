from graphics import *
#from pynput import mouse

class GraphLive(object):
    def __init__(self, chartmax, chartmin, chartlen, pair, numofcharts, rsiper, stochper):
        self.lists = {}
        self.vars = {}
        
        
        #Constant variables go here
        self.rsiper = rsiper
        self.stochper = stochper
        self.val = 0
        self.numberOfCharts = numofcharts
        self.height = 800
        self.realwidth = 1400
        self.win = GraphWin("THE END OF BEING BROKE",self.realwidth,self.height, autoflush=False)
        self.win.setBackground("#747474")
        #const X
        self.width = self.realwidth / numofcharts - 50
        self.edges = 20
        #const Y
        self.lowergraphst = self.height - 200
        self.lowergraphsb = self.height - 50
        self.lscale = (self.lowergraphsb - self.lowergraphst) / 100
        self.top = 100
        self.chartmax = chartmax
        self.chartmin = chartmin
        self.bot = self.height - (50 + self.height - self.lowergraphst)
        self.scale = (self.height - self.top * 2)/2
        #constants that would become variable during a live run
        self.chartlen = chartlen
        
        #Draw top and bottom lines
        topline = Line(Point(0, self.top),Point(self.width * self.numberOfCharts,self.top))
        topline.draw(self.win)
        botline = Line(Point(0,self.bot),Point(self.width * self.numberOfCharts,self.bot))
        botline.draw(self.win)
        #Bottom graph
        topline = Line(Point(0, self.lowergraphst),Point(self.width * self.numberOfCharts,self.lowergraphst))
        topline.draw(self.win)
        botline = Line(Point(0,self.lowergraphsb),Point(self.width * self.numberOfCharts,self.lowergraphsb))
        botline.draw(self.win)
        midline = Line(Point(0, self.lowergraphst + self.lscale * 50),Point(self.width * self.numberOfCharts,self.lowergraphst + self.lscale * 50))
        midline.draw(self.win)
        overboughtline = Line(Point(0,self.lowergraphst + self.lscale * 30),Point(self.width * self.numberOfCharts,self.lowergraphst + self.lscale * 30))
        overboughtline.setFill("White")
        overboughtline.draw(self.win)
        underboughtline = Line(Point(0,self.lowergraphst + self.lscale * 70),Point(self.width * self.numberOfCharts,self.lowergraphst + self.lscale * 70))
        underboughtline.setFill("White")
        underboughtline.draw(self.win)
        
        #anal variables
        self.clickedsubcount = 0
        self.lastclicked = [0, 0, 0]
        
        #initialize the constant Xs in every chart
        for x in range(self.numberOfCharts):
            self.vars["xfront" + str(x + 1)] = self.edges + self.width * x
            self.vars["xback" + str(x + 1)] = self.width * (x + 1) - self.edges
            self.vars["xscale" + str(x + 1)] = (self.vars["xback" + str(x + 1)] - self.vars["xfront" + str(x + 1)]) / (self.chartlen - 1)
            self.vars["x" + str(x + 1)] = self.vars["xfront" + str(x + 1)]
        
        #Titles
        self.title = Text(Point(self.width / 2, self.top / 2),pair)
        self.title.setSize(18)
        self.title.setFace('arial')
        self.title.draw(self.win)
        
        
        #Lines that are drawn when the graph is clicked
        self.mline = []
        self.mhline = []
        self.words = []
        for item in range(self.numberOfCharts):
            self.mline.append(Line(Point(0,0),Point(0,0)))
            self.mhline.append(Line(Point(0,0),Point(0,0)))
            self.words.append(Text(Point(0,0),""))
            lin = Line(Point(self.vars["xfront" + str(item + 1)],self.top),Point(self.vars["xfront" + str(item + 1)],self.bot))
            lin.draw(self.win)
            lin2 = Line(Point(self.vars["xback" + str(item + 1)],self.top),Point(self.vars["xback" + str(item + 1)],self.bot))
            lin2.draw(self.win)
        
        
        #first add the constants, then add another for loop to calculate and append other values
        namelist = ["prev","ma5prev","ma15prev","count","up","emaprev","rsiprev","kprev","fastprev"]
        values = [0,0,0,0,False,0,0,0,0]
        for i in range(1,self.numberOfCharts + 1):
            for name in range(len(namelist)):
                key = namelist[name] + str(i)
                self.vars[key] = values[name]
            
        
    def add(self, val, ma5, ma15, pchange, ca, cb, gotime, firstcross, chartnumber, ema, rsi, h, l, k, fast, notRe = True):
        xscale = self.vars["xscale" + chartnumber]
        
        #graph the MAcross line
        if(gotime):
            
            
            firstval = (self.chartmax - ca.getY()) * self.scale + self.top
            secondval = (self.chartmax - cb.getY()) * self.scale + self.top
            
            x1 = xscale * (firstcross) - (xscale - ca.getX() * xscale) + self.vars["xfront" + chartnumber]
            x2 = xscale * (self.vars["count" + chartnumber]) - (xscale - cb.getX() * xscale) + self.vars["xfront" + chartnumber]
            #Done with this shit, taking the easy way out
            if(firstcross == 0):
                x1 = self.vars["xfront" + chartnumber]
            crossline = Line(Point(x1, firstval),Point(x2, secondval))
            if (firstval - secondval > 0):
                crossline.setFill("#00f642")
            else:
                crossline.setFill("#f200f4")
            crossline.draw(self.win)
            
        
        self.val = (self.chartmax - float(val)) * self.scale + self.top
        
        if(not self.vars["count" + chartnumber] == 0):
            a = Point(self.vars["x" + chartnumber], self.vars["prev" + chartnumber])
            self.vars["x" + chartnumber] += xscale
        else:
            a = Point(self.vars["xfront" + chartnumber], self.val)
            
        b = Point(self.vars["x" + chartnumber], self.val)
        lin = Line(a,b)
        lin.setFill("Black")
        
        olin = Line(Point(self.vars["x" + chartnumber],self.bot),Point(self.vars["x" + chartnumber],self.bot - 5))
        olin.draw(self.win)
        
        #Highs'n'lows
        hpoint = Point(self.vars["x" + chartnumber],(self.chartmax - h) * self.scale + self.top)
        lpoint = Point(self.vars["x" + chartnumber],(self.chartmax - l) * self.scale + self.top)
        hpoint.setFill("Green")
        lpoint.setFill("Red")
        hpoint.draw(self.win)
        lpoint.draw(self.win)
        
        '''
        #Percent
        if (self.vars["up" + chartnumber] == True):
            bob = 10
            self.vars["up" + chartnumber] = False
        else:
            bob = -10
            self.vars["up" + chartnumber] = True
        
        thep = Text(Point(self.vars["x" + chartnumber], self.bot + bob), "%.2f" % (pchange))
        thep.setSize(8)
        thep.draw(self.win)
        
        #Print local maximums
        if (self.vars["count" + chartnumber] in self.lmaxes[int(chartnumber) - 1]):
            ind = Line(Point(self.vars["x" + chartnumber],self.val - 10),Point(self.vars["x" + chartnumber],self.val))
            ind.setFill("Red")
            ind.draw(self.win)
        '''
        lin.draw(self.win)
        self.vars["prev" + chartnumber] = self.val
        
        print(ma5,ma15)
        #ma5
        self.graphMA(ma5, "#e8ea00", self.vars["ma5prev" + chartnumber], chartnumber)
        self.vars["ma5prev" + chartnumber] = self.val
        
        #ma15
        self.graphMA(ma15, "#01e0f2", self.vars["ma15prev" + chartnumber], chartnumber)
        self.vars["ma15prev" + chartnumber] = self.val
        
        #ema
        self.graphMA(ema, "Purple", self.vars["emaprev" + chartnumber], chartnumber)
        self.vars["emaprev" + chartnumber] = self.val
        
        #rsi
        
        #if self.vars["count" + chartnumber] >= self.rsiper:
        self.lowergraph(rsi, "Blue", self.vars["rsiprev" + chartnumber], chartnumber, self.rsiper)
        self.vars["rsiprev" + chartnumber] = self.val
        
        #stochastic
        #if self.vars["count" + chartnumber] >= self.stochper:
        self.lowergraph(k[-1], "Purple", self.vars["kprev" + chartnumber], chartnumber, self.stochper)
        self.vars["kprev" + chartnumber] = self.val
        self.lowergraph(fast, "Orange", self.vars["fastprev" + chartnumber], chartnumber, self.stochper)
        self.vars["fastprev" + chartnumber] = self.val
        
        self.vars["count" + chartnumber] += 1
        if notRe:
            update()
    
    
    def graphMA(self, value, color, maprev, chartnumber):
        self.val = (self.chartmax - float(value)) * self.scale + self.top
        if (self.vars["count" + chartnumber] == 0):
            a = Point(self.vars["x" + chartnumber],self.val)
        else:
            a = Point(self.vars["x" + chartnumber] - self.vars["xscale" + chartnumber], maprev)
        b = Point(self.vars["x" + chartnumber], self.val)
        lin = Line(a,b)
        lin.setFill(color)
        lin.draw(self.win)
    
    def lowergraph(self, value, color, prev, chartnumber, period):
        self.val = (100 - float(value)) * self.lscale + self.lowergraphst
        if self.vars["count" + chartnumber] == period:
            a = Point(self.vars["x" + chartnumber], self.val)
        else:
            a = Point(self.vars["x" + chartnumber] - self.vars["xscale" + chartnumber], prev)
        b = Point(self.vars["x" + chartnumber], self.val)
        lin = Line(a,b)
        lin.setFill(color)
        lin.draw(self.win)
            
            
    
    def buy(self, price, position, chartnumber, n):
        x = position * self.vars["xscale" + chartnumber] + self.vars["xfront" + chartnumber]
        y = (self.chartmax - price) * self.scale + self.top - 200
        message = Text(Point(x,y),"B" + str(n))
        message.setFill("#d48b00")
        message.setSize(10)
        theline = Line(Point(x,y),Point(x,y + 200))
        theline.draw(self.win)
        message.draw(self.win)
        
    def sell(self, price, position, gain, chartnumber):
        x = position * self.vars["xscale" + chartnumber] + self.vars["xfront" + chartnumber]
        y = (self.chartmax - price) * self.scale + self.top - 200
        message = Text(Point(x,y),"Sell order" + "\nPC: %.3f" % (gain))
        if (gain >= 0):
            message.setFill("#0d9800")
        else:
            message.setFill("#980000")
        message.setSize(10)
        theline = Line(Point(x,y),Point(x,y + 200))
        theline.draw(self.win)
        message.draw(self.win)
        
    def removelastitem(self):
        for item in self.win.items[-5:]:
            item.undraw()
        
    #this will update the graph if the max or min changes, and maybe if chartlen is exceeded
    def regraph(self, prices, ma5list, ma15list, percentlist, Alist, Blist,crossTimelist, firstCrosslist, chartnumber, ema, rsi, h, l, k, fast, buys, sells, startingpos, ordgains):
        for item in self.win.items[7:]:
            item.undraw()
        print(k)
        self.vars["x" + chartnumber] = self.vars["xfront" + chartnumber]
        self.vars["count" + chartnumber] = 0
        self.scale = (self.bot - self.top) / (self.chartmax - self.chartmin)
        print(len(prices),len(ma5list),len(ma15list),len(percentlist),len(Alist),len(Blist),len(crossTimelist),len(firstCrosslist),len(ema),len(rsi),len(h),len(l),len(k),len(fast))

        for i in range(len(ema)):
            butt = len(prices)  - len(ema)
            self.add(prices[i + butt],ma5list[i + butt],ma15list[i + butt],percentlist[i],Alist[i],Blist[i],crossTimelist[i],firstCrosslist[i],chartnumber, ema[i], rsi[i], h[i], l[i], k[i], fast[i], False)
            if i + startingpos in buys and i + startingpos != 0:
                self.buy(prices[i],i,chartnumber,1)
            if i + startingpos in sells and (ordgains[i] != 0 or i != 0):
                self.sell(prices[i],i,ordgains[i],chartnumber)
        
        update()