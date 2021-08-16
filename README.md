# CryptoTradeBot
A cryptocurrency trade bot using the [Robin Stocks API].

## File Information

### 📃 BotExecutor.py

* Recieve user credentials/key and login to RobinHood.  Main "trading loop" is contained within this file.


### 📃 Utilities.py 

* Provide basic helper functions that will be used throughout the program.


### 📁 Indicators 

* Implement different trade indicators that return a Buy,Hold,Sell command. Currently implementing GoldenCross/DeathCross, RSI Divergence, and "dumb" scalping.



[Robin Stocks API]: https://robin-stocks.readthedocs.io/en/latest/index.html
