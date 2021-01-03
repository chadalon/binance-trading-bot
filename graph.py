from graphics import *
#from pynput import mouse

class Graph(object):
    def __init__(self, chartmax, chartmin, chartlen, pair, numofcharts, valuesAre, timestamps, extra, intervals, rsiper, stochper, bolper, ma5on=True, handlon=True):
        self.lists = {}
        self.vars = {}
        #gonna wanna put extra in the dict
        self.extra = extra
        self.rsiper = rsiper
        self.stochper = stochper
        self.bolper = bolper
        
        self.ma5on = ma5on
        self.handlon = handlon
        
        #Constant variables go here
        self.intervals = intervals
        self.val = 0
        self.numberOfCharts = numofcharts
        self.height = 800
        self.realwidth = 1400
        self.win = GraphWin("THE END OF BEING BROKE",self.realwidth,self.height, autoflush=False)
        self.win.setBackground("#ababab")#858585")
        #const X
        self.width = self.realwidth / numofcharts - 50
        self.edges = 20
        #const Y
        self.lowergraphst = self.height - 200
        self.lowergraphsb = self.height - 50
        self.lscale = (self.lowergraphsb - self.lowergraphst) / 100
        self.top = 100
        self.chartmax = chartmax
        #the constant number is the dist from upper graph
        self.bot = self.height - (50 + self.height - self.lowergraphst)
        self.scale = (self.bot - self.top) / (self.chartmax - chartmin)
        
        #constants that would become variable during a live run
        self.chartlen = chartlen
        self.timestamps = timestamps
        self.data = [[],[],[]]
        
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
            self.vars["xscale" + str(x + 1)] = (self.vars["xback" + str(x + 1)] - self.vars["xfront" + str(x + 1)]) / (self.chartlen[x] - 1)
            self.vars["x" + str(x + 1)] = self.vars["xfront" + str(x + 1)]
        
        #Titles
        self.title = Text(Point(self.width / 2, self.top / 2),pair)
        self.title.setSize(18)
        self.title.setFace('arial')
        self.title.draw(self.win)
        
        self.valuesAre = Text(Point(100, self.top / 2), valuesAre)
        self.valuesAre.draw(self.win)
        
        #Lines that are drawn when the graph is clicked
        self.mline = []
        self.mhline = []
        self.words = []
        self.lwords = []
        for item in range(self.numberOfCharts):
            self.mline.append(Line(Point(0,0),Point(0,0)))
            self.mhline.append(Line(Point(0,0),Point(0,0)))
            self.words.append(Text(Point(0,0),""))
            self.lwords.append(Text(Point(0,0),""))
            lin = Line(Point(self.vars["xfront" + str(item + 1)],self.top),Point(self.vars["xfront" + str(item + 1)],self.bot))
            lin.draw(self.win)
            lin2 = Line(Point(self.vars["xback" + str(item + 1)],self.top),Point(self.vars["xback" + str(item + 1)],self.bot))
            lin2.draw(self.win)
        
        
        #first add the constants, then add another for loop to calculate and append other values
        namelist = ["prev","hprev","lprev","ma5prev","ma15prev","bigmaprev","count","up","emaprev","rsiprev","kprev","fastprev", "bolmidprev", "bolupprev", "bollowprev", "bandwprev"]
        values = [0,0,0,0,0,0,0,False,0,0,0,0,0,0,0,0]
        for i in range(1,self.numberOfCharts + 1):
            for name in range(len(namelist)):
                key = namelist[name] + str(i)
                self.vars[key] = values[name]
            
        
    def add(self, val, ma5, ma15, bigma, pchange, ca, cb, gotime, firstcross, chartnumber, max, min, ema, rsi, h, l, k, fast, nTrade, bolmid, bolup, bollow, bandwidth):#, nTradeTime):
        xscale = self.vars["xscale" + chartnumber]
        self.data[int(chartnumber) - 1].append(val)
        
        #graph the MAcross line
        if gotime and self.ma5on:
            
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
        self.nTval = (self.chartmax - nTrade) * self.scale + self.top
        
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
        
        #Hope this was mostly pointless
        '''
        nexttrade = Line(Point(self.vars["x" + chartnumber] + xscale * nTradeTime, self.nTval + 2),Point(self.vars["x" + chartnumber] + xscale * nTradeTime, self.nTval - 2))
        nexttrade.setFill("blue")
        nexttrade.draw(self.win)
        '''
        #Highs'n'lows
        
        if self.handlon:
            #redrawing last line if it was a local max or min
            if self.vars["count" + chartnumber] > 0:
                if max == self.vars["count" + chartnumber] - 1:
                    #why does this need - xscale when the circles don't? i thik it's because we don't know the local maxes until the next tick
                    hpoint = Line(Point(self.vars["x" + chartnumber] - xscale,(self.chartmax - self.vars["hprev" + chartnumber]) * self.scale + self.top), Point(self.vars["x" + chartnumber] - xscale,self.vars["prev" + chartnumber]))
                    hpoint.setFill("#5ad833")
                    hpoint.draw(self.win)
                    
                elif min == self.vars["count" + chartnumber] - 1:
                    lpoint = Line(Point(self.vars["x" + chartnumber] - xscale,(self.chartmax - self.vars["lprev" + chartnumber]) * self.scale + self.top), Point(self.vars["x" + chartnumber] - xscale, self.vars["prev" + chartnumber]))
                    lpoint.setFill("#a70000")
                    lpoint.draw(self.win)
        
            #Circles
            hpoint = Circle(Point(self.vars["x" + chartnumber],(self.chartmax - h) * self.scale + self.top), 2)
            lpoint = Circle(Point(self.vars["x" + chartnumber],(self.chartmax - l) * self.scale + self.top), 2)
            hpoint.setFill("Green")
            hpoint.setOutline("Green")
            lpoint.setFill("Red")
            lpoint.setOutline("Red")
            hpoint.draw(self.win)
            lpoint.draw(self.win)
            
            #draw lines, they will be drawn over if local maxes/mins
            #changing to global vars to see if i can undraw them
            hpoint = Line(Point(self.vars["x" + chartnumber],(self.chartmax - h) * self.scale + self.top), Point(self.vars["x" + chartnumber],self.val))
            lpoint = Line(Point(self.vars["x" + chartnumber],(self.chartmax - l) * self.scale + self.top), Point(self.vars["x" + chartnumber],self.val))
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
        '''
        
        
        #Draw price, then store price, high, and low to previous for calc during next iteration
        lin.draw(self.win)
        self.vars["prev" + chartnumber] = self.val
        self.vars["hprev" + chartnumber] = h
        self.vars["lprev" + chartnumber] = l
        
        
        #NextTrade plot
        
        
        #ma5
        if self.ma5on:
            self.graphMA(ma5, "#e8ea00", self.vars["ma5prev" + chartnumber], chartnumber)
            self.vars["ma5prev" + chartnumber] = self.val
        
        #ma15
        self.graphMA(ma15, "#01e0f2", self.vars["ma15prev" + chartnumber], chartnumber)
        self.vars["ma15prev" + chartnumber] = self.val
        
        #bigma
        self.graphMA(bigma,"#f6a425", self.vars["bigmaprev" + chartnumber], chartnumber)
        self.vars["bigmaprev" + chartnumber] = self.val
        
        #ema
        self.graphMA(ema, "Purple", self.vars["emaprev" + chartnumber], chartnumber)
        self.vars["emaprev" + chartnumber] = self.val
        
        #rsi
        
        if self.vars["count" + chartnumber] >= self.rsiper:
            self.lowergraph(rsi, "Blue", self.vars["rsiprev" + chartnumber], chartnumber, self.rsiper)
            self.vars["rsiprev" + chartnumber] = self.val
        
        #stochastic
        if self.vars["count" + chartnumber] >= self.stochper:
            self.lowergraph(k[-1], "Purple", self.vars["kprev" + chartnumber], chartnumber, self.stochper)
            self.vars["kprev" + chartnumber] = self.val
            self.lowergraph(fast, "Orange", self.vars["fastprev" + chartnumber], chartnumber, self.stochper)
            self.vars["fastprev" + chartnumber] = self.val
            
        #bollinger YEET
        if self.vars["count" + chartnumber] > self.bolper:
            #mid
            self.graphMA(bolmid, "#BADA55", self.vars["bolmidprev" + chartnumber], chartnumber)
            self.vars["bolmidprev" + chartnumber] = self.val
            #up
            self.graphMA(bolup, "#673586", self.vars["bolupprev" + chartnumber], chartnumber)
            self.vars["bolupprev" + chartnumber] = self.val
            #down
            self.graphMA(bollow, "#673586", self.vars["bollowprev" + chartnumber], chartnumber)
            self.vars["bollowprev" + chartnumber] = self.val
            #bandwidth - idk if bolper should be used
            self.lowergraph(bandwidth, "Black", self.vars["bandwprev" + chartnumber], chartnumber, self.bolper)
            self.vars["bandwprev" + chartnumber] = self.val
            
        #change initial bollinger prev values for first time being graphed
        #the weird equation shit is taken from graphMA
        #Holy fuck I'm a genius
        elif self.vars["count" + chartnumber] == self.bolper:
            self.vars["bolmidprev" + chartnumber] = (self.chartmax - float(bolmid)) * self.scale + self.top
            self.vars["bolupprev" + chartnumber] = (self.chartmax - float(bolup)) * self.scale + self.top
            self.vars["bollowprev" + chartnumber] = (self.chartmax - float(bollow)) * self.scale + self.top
            
            self.vars["bandwprev" + chartnumber] = (100 - float(bandwidth)) * self.lscale + self.lowergraphst
        
        self.vars["count" + chartnumber] += 1
        #update()
        
    
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
    
    #The clicking an shit
    def anal(self):
        print(len(self.data))
        for i in range(1,2):#, self.numberOfCharts + 1):
            earnings = Text(Point((self.width * i) - self.width/4,self.top / 2),"%.3f" % self.lists["totalGainz" + str(i)])
            earnings.draw(self.win)
        while True:
            try:
                thex = self.win.getMouse()
            except GraphicsError:
                print("Closed window")
                break
            they = thex.getY()
            thex = thex.getX()
            currentx = thex
            
            if (thex <= self.width * self.numberOfCharts and thex >= self.edges):
                for i in range(1,self.numberOfCharts + 1):
                    
                    if(thex >= self.vars["xfront" + str(i)] and thex <= self.vars["xback" + str(i)]):
                        clicked = i
                
                #set thex to closest value in the chart that was clicked
                #set xfront and xscale to the value in vars because typing out the self.vars["blahblah" + str(clicked) sucks and is messy
                xfront = self.vars["xfront" + str(clicked)]
                xscale = self.vars["xscale" + str(clicked)]
                subcount = 0
                lilx = currentx
                #how many times does xscale go into the position - we take away xfront to get what we want
                while (lilx - xfront > xscale):
                    lilx -= xscale
                    subcount += 1
                #If the position rounds up
                if (((currentx - xfront) % xscale) / xscale >= .5):
                    subcount += 1
                #save the subcount, we don't know what position the graph is in
                self.clickedsubcount = subcount
                
                thex = xscale * subcount
                rightside = xscale * len(self.data[clicked - 1]) - thex
                #check if mouse is in x range
                for i in range(1, self.numberOfCharts + 1):
                    key = "xscale" + str(i)
                    xscale = self.vars[key]
                    
                    #probs need to do this for multiple charts
                    data = self.data[i - 1]
                    
                    timestamps = self.timestamps[i - 1]
                    
                    #making list references simple
                    highslist = self.lists["highs" + str(i)]
                    lowslist = self.lists["lows" + str(i)]
                    key = "ma5list" + str(i)
                    ma5list = self.lists[key]
                    key = "ma15list" + str(i)
                    ma15list = self.lists[key]
                    key = "bigmalist" + str(i)
                    bigmalist = self.lists[key]
                    key = "percentlist" + str(i)
                    percentlist = self.lists[key]
                    key = "xfront" + str(i)
                    xfront = self.vars[key]
                    key = "rsilist" + str(i)
                    rsilist = self.lists[key]
                    key = "bandwidth" + str(i)
                    bandwlist = self.lists[key]
                    
                    extra = self.extra[i - 1]
                    
                    #position x
                    ##Needs work
                    if (i == clicked):
                        currentx = thex + xfront
                        subcount = self.clickedsubcount
                    else:
                        
                        #3rd clicked and i==1
                        if (clicked - i == 2):
                            subcount = self.clickedsubcount * 30 + 29
                        if (clicked - i == 1):
                            if(clicked == 2):
                                subcount = self.clickedsubcount * 2 + 2
                            else:
                                #clicked == 3
                                subcount = self.clickedsubcount * 6 + 5
                        
                        if (clicked - i == -1):
                            if(clicked == 2):
                                #Just copying the commented code
                                #+5 is experimental
                                subcount = self.clickedsubcount + 5 - self.clickedsubcount % 6
                                subcount = subcount//6
                                
                            else:
                                #clicked == 1
                                subcount = self.clickedsubcount - 1 - self.clickedsubcount % 2
                                subcount = subcount//2
                        #1st clicked and i==3
                        if (clicked - i == -2):
                            subcount = self.clickedsubcount + 29 - self.clickedsubcount % 30
                            subcount = subcount//30
                            
                                
                        currentx = xscale * subcount + xfront
                    
                    print(len(data))
                    print("subcount:",str(subcount))
                    
                    clickpercent = (float(data[subcount]) - self.lastclicked[i - 1]) / float(data[subcount]) * 100
                    
                    self.mline[i - 1].undraw()
                    self.mline[i - 1] = Line(Point(currentx, self.top),Point(currentx, self.lowergraphsb))
                    self.mline[i - 1].draw(self.win)
                    
                
                        
                    if(i == clicked):
                        for x in range(self.numberOfCharts):
                            self.mhline[x].undraw()
                        self.mhline[i - 1] = Line(Point(0, (self.chartmax - float(data[subcount])) * self.scale + self.top), Point(self.width * self.numberOfCharts, (self.chartmax - float(data[subcount])) * self.scale + self.top))
                        
                        self.mhline[i - 1].draw(self.win)
                    
                    self.words[i - 1].undraw()
                    self.words[i - 1] = Text(Point(currentx, they - 35), "Timestamp: %i\nPosition: %i\nValue: %.8f\nHigh: %.8f\nLow: %.8f\nMA5: %.8f\nMA15: %.8f\n MA100: %.8f\n PercentChange: %.2f\nClick Percent: %.2f" % (timestamps[subcount],subcount, float(data[subcount]), float(highslist[subcount]), float(lowslist[subcount]), ma5list[subcount], ma15list[subcount], bigmalist[subcount], percentlist[subcount], clickpercent))
                    #self.words[i - 1].setFill("#0d9c00")
                    self.words[i - 1].setFill("Green")
                    self.words[i - 1].draw(self.win)
                    
                    self.lwords[i - 1].undraw()
                    myButt = ""
                    if subcount - self.bolper >= 0:
                        myButt = "\nBandwidth: %.2f" % bandwlist[subcount - self.bolper]
                    if subcount - self.rsiper >= 0:
                        self.lwords[i - 1] = Text(Point(currentx, ((self.height - self.lowergraphsb)/2) + self.lowergraphsb), ["RSI: %.3f" % rsilist[subcount - self.rsiper] + myButt])
                        self.lwords[i - 1].draw(self.win)
                        
                        
                    
                    self.lastclicked[i - 1] = float(data[subcount])
                    #print(self.lastclicked)
                    ##Should be same
                    print("length of rsilist",len(rsilist))
                    print("length of chart",len(data))
                    print("length of bandw",len(bandwlist))
                    print("bandwthing", str(subcount - self.bolper))
            
    
    def buy(self, price, position, chartnumber, n):
        x = position * self.vars["xscale" + chartnumber] + self.vars["xfront" + chartnumber]
        y = (self.chartmax - price) * self.scale + self.top - 200
        message = Text(Point(x,y),"B" + str(n))
        message.setFill("#d48b00")
        message.setSize(10)
        theline = Line(Point(x,y),Point(x,y + 200))
        theline.draw(self.win)
        message.draw(self.win)
        
    def sell(self, price, position, gain, chartnumber, stopped):
        x = position * self.vars["xscale" + chartnumber] + self.vars["xfront" + chartnumber]
        y = (self.chartmax - price) * self.scale + self.top - 200
        message = ""
        if stopped:
            message = Text(Point(x,y),"Sell order" + "\nPC: %.3f" % (gain) + "\nSTOPPED")
        else:
            message = Text(Point(x,y),"Sell order" + "\nPC: %.3f" % (gain))
        if (gain >= 0):
            message.setFill("#0d9800")
        else:
            message.setFill("#980000")
        message.setSize(10)
        theline = Line(Point(x,y),Point(x,y + 200))
        theline.draw(self.win)
        message.draw(self.win)
        
        
    def listadd(self, ma5list, ma15list, bigmalist, percentlist, totalGainz, rsilist, chartnumber, boluplist, bollowlist, bolmidlist, bandwidth):
        RN = chartnumber
        key = "ma5list" + RN
        self.lists[key] = ma5list
        key = "ma15list" + RN
        self.lists[key] = ma15list
        key = "bigmalist" + RN
        self.lists[key] = bigmalist
        key = "percentlist" + RN
        self.lists[key] = percentlist
        key = "totalGainz" + RN
        self.lists[key] = totalGainz
        key = "rsilist" + RN
        self.lists[key] = rsilist
        key = "boluplist" + RN
        self.lists[key] = boluplist
        key = "bollowlist" + RN
        self.lists[key] = bollowlist
        key = "bolmidlist" + RN
        self.lists[key] = bolmidlist
        key = "bandwidth" + RN
        self.lists[key] = bandwidth
        for item in self.lists:
            print(item)
    
    #I apologize to my future self. Maybe I should have done it this way in the first place
    def addLists(self, chartnumber, highs, lows):
        self.lists["highs" + chartnumber] = highs
        self.lists["lows" + chartnumber] = lows