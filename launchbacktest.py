from backtest import Backtest
from binance.client import Client


#add option to add more MAs and set what period they have
#also add option to change periods of any indicator
#Bollinger bandwidth is not aligned - might be fixed
#TRY DERIVATIVE/MA OF BANDWIDTH??
#MOVE ENTRYCALC OUTSIDE STRATEGIES
#MAKE A SELF.CHARTNUMBER IN BOTSTRATS SO STRATEGIES DON'T NEED THEM AS A PARAM, CLEAN UP OTHER PARAMS USED IN ALL OF THEM
#why do i need to float the price all the time in botstrat

#ok u gonna hate me but u need to GET RID OF STRATS - move them to tick because they fuckn take too many inputs man jesus//OR make overpassed params global - MOSTLY for strats
#Now try making every aspect of every indicator changeable to test them -- when u make this tester make it look at individual sells as they happen
#and test which variables would've been better - u gonna wanna make a huge list of all changeable items - even in pseudocode
 
#Pretty sure larger pair is off bc i don't understand leverage or know if they even use it
LaunchDict = {
    "pair": "ZILBTC",
    "strat": "1",
    "klineint": "Client.KLINE_INTERVAL_30MINUTE",
    "ss": "2 days ago UTC",
    "graphics": True,
    
    "handl": True,
    "bigma": True,
    "ema": True,
    "ma5": False,
    "ma15": True,
    "bollinger": True,
    "rsi": True,
    "stochastic": True
    
}
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
client = Client(apikey, secretkey)
f.close()
balances = client.get_account()['balances']
count = 0
for thing in balances:
    if thing['asset'] == "ZIL":
        print(count)
    count += 1
print(balances)
print(balances[120])

launchString = 'Backtest("' + LaunchDict["pair"] + '", strat=' + LaunchDict['strat'] + ', klineint=' + LaunchDict["klineint"] + ', ss="' + LaunchDict['ss'] + '"'

for thing in LaunchDict:
    if not LaunchDict[thing]:
        launchString += ", " + thing + "=False"

launchString += ")"
print(launchString)
#backtest = Backtest("BTCUSDT", strat=1, klineint=Client.KLINE_INTERVAL_12HOUR, ss="2 week ago UTC", graphics=True)#, ma5=False, handl=False)
backtest = eval(launchString)
#STOP LOSSES; ENTRIES
#for larger pairs: does usdt only trade in ints
#fix up aggtrades, default it to false but keep it in
#don't think I need self.last in botstrat, actually I do
#graph local mins - you already have it storing in masterDick
#local mins and maxes are based on closing price rn, should I do highs and lows of the kline?

#migrate all changeable variables to here - indicators on/off, kline intervals, chartnumbers, indicator periods, etc., but ur gonna want to make sure strats are using what works
#make a program that determines best parameters for indicators and which indicators to use to find the best strats for a given pair

#NEXT TASK: CHANGE AGGTRADES FROM BUYER IS MAKER TO JUST THE NEXT ONES/THE ONES THAT WOULD SELL
#FIND OUT IF UR DOING THE AGG TRADING RIGHT - SEARCH FOR THE CLOSING KLINE PRICES IN AGGREGATE TRADE LISTS
#IF U ARE USING AGGREGATED TRADES, SHOW WHERE ON THE GRAPH YOU BOUGHT
#^^^DIVIDE THE INTERVALS BY THE 1800000 AND USE THE TIMESTAMPS ON AGGREGATED TRADES TO PLOT THEM BROBROBROBROBROBROBRO
#REDUCE THE TIME IT TAKES TO GO THROUGH AGGTRADES - USE THE AGG TRADES ITERATTION FUNCTION

#MAKE THE GRAPHICS PERCENT LOSS/GAIN ACCURATE

#CONVERT TO LIMIT ORDERS

#MORE ANALYSIS POSSIBILITIES: DURING ANAL, WHEN U CLICK ON A PRICE IT WILL SHOW THE TRADE STATUS DURING THAT TIME (CURRENT BTC/ALT, LOSS/GAIN,ETC), ADD ZOOM IN