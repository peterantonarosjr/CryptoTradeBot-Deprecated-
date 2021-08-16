import Utilities

class CrossStrategy:
    def __init__(self,cryptoList):
        self.cryptoList = cryptoList
        self.cryptoPriceList = None
        self.cryptoTradeList = None
        self.signalStatus = None
        self.setCryptoTradeList()


    #Set instance variable cryptoPriceList
    def setCryptoPriceList(self):
        self.cryptoPriceList = Utilities.getCryptoPrices(self.cryptoList)

    #Get instance variable cryptoPriceList
    def getCryptoPriceList(self):
        return self.cryptoPriceList

    #Set instance variable cryptoTradeList
    def setCryptoTradeList(self):
        self.setCryptoPriceList()
        self.cryptoTradeList = dict(zip(self.cryptoList, self.cryptoPriceList))

    #Get instance variable cryptoTradeList
    def getCryptoTradeList(self):
        return self.cryptoTradeList

    #Get the short moving average past 30 days for each crypto in cryptoList
    def getShortMovingAverage(self):
        cryptosShortDatabases = {}
        i = 0
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildDatabase(crypto[:3], "day", "3month")
            cryptoDB['short_moving_average'] = cryptoDB['mean_price'].rolling(window=30).mean()
            cryptosShortDatabases.update({crypto: cryptoDB.dropna().iloc[-30:]})
            i += 1
        return cryptosShortDatabases

    #Get the long moving average past 100 days for each crypto in cryptoList
    def getLongMovingAverage(self):
        cryptosLongDatabases = {}
        i = 0
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildDatabase(crypto[:3], "day", "year")
            cryptoDB['long_moving_average'] = cryptoDB['mean_price'].rolling(window=100).mean()
            cryptosLongDatabases.update({crypto: cryptoDB.dropna().iloc[-100:]})
            i += 1
        return cryptosLongDatabases

    #Decides whether or not to return Buy/Sell/Hold signal
    def decideToTrade(self, shortDBs, longDBs):
        for crypto in self.cryptoList:
            shortDB = shortDBs.get(crypto)
            longDB = longDBs.get(crypto)
            if shortDB.iloc[-1]['short_moving_average'] > longDB.iloc[-1]['long_moving_average']:
                print("SMA: "+str(shortDB.iloc[-1]['short_moving_average']) + " " + "LMA: "+str(longDB.iloc[-1]['long_moving_average']))
                print("Buy Signal")
                self.signalStatus = "BUY"
            else:
                print("SMA: "+str(shortDB.iloc[-1]['short_moving_average']) + " " + "LMA: "+str(longDB.iloc[-1]['long_moving_average']))
                print("Sell Signal")
                self.signalStatus = "SELL"

    #Main updateFunction to refresh based on new Robinhood data
    def update(self):
        shortMovingDatabases = self.getShortMovingAverage()
        longMovingDatabases = self.getLongMovingAverage()
        self.decideToTrade(shortMovingDatabases, longMovingDatabases)
        self.setCryptoTradeList()