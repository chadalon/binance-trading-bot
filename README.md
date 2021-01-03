# binance-trading-bot
Backtesting and live trading

# Usage
This program uses the twilio api to send text messages while live trading.
pip install twilio

The Python Binance api package is used to connect to the rest api.
pip install python-binance

Files you need to add (until generation gets coded in):
token.txt - your binance api secret and key. Put your secret on top line, key on second.
twiliotoken.txt - your twilio api account and token. Top line/second line

As of now trading pairs have to be hardcoded in.

launchbacktest.py launches the backtest (WOw)
botstrategies.py has the backtest strategies. Strategies will be able to be changed in the program during runtime in the future

Experimenting.py starts a live run

# Important
All the code needs to be cleaned up. Also more features need to be added to make this practical (strategy design mostly)