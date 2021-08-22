import Utilities

class CrossStrategy:
    def __init__(self,cryptoList):
        self.cryptoList = cryptoList
        self.cryptoPriceList = None
        self.cryptoTradeList = None
        self.signalStatus = None
        self.shortMovingAverages = self.setShortMovingAverages()
        self.longMovingAverages = self.setLongMovingAverages()
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
    def setShortMovingAverages(self):
        cryptosShortDatabases = {}
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildIndicatorDatabase(crypto[:3], "day", "3month")
            cryptoDB[crypto[:3]+'_short_moving_average'] = cryptoDB[crypto[:3]+'_mean_price'].rolling(window=30).mean()
            cryptosShortDatabases.update({crypto: cryptoDB.dropna().iloc[-30:]})
        return cryptosShortDatabases

    #Get the long moving average past 100 days for each crypto in cryptoList
    def setLongMovingAverages(self):
        cryptosLongDatabases = {}
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildIndicatorDatabase(crypto[:3], "day", "year")
            cryptoDB[crypto[:3]+'_long_moving_average'] = cryptoDB[crypto[:3]+'_mean_price'].rolling(window=100).mean()
            cryptosLongDatabases.update({crypto: cryptoDB.dropna().iloc[-100:]})
        return cryptosLongDatabases

    #Decides whether or not to return Buy/Sell/Hold signal
    def decideToTrade(self, shortDBs, longDBs):
        for crypto in self.cryptoList:
            shortDB = shortDBs.get(crypto)
            longDB = longDBs.get(crypto)
            if shortDB.iloc[-1][crypto[:3]+'_short_moving_average'] > longDB.iloc[-1][crypto[:3]+'_long_moving_average']:
                print("SMA "+crypto[:3]+": "+str(shortDB.iloc[-1][crypto[:3]+'_short_moving_average']) + " " + "LMA "+crypto[:3]+": "+str(longDB.iloc[-1][crypto[:3]+'_long_moving_average']))
                print("Buy Signal")
                self.signalStatus = "BUY"
            else:
                print("SMA "+crypto[:3]+": "+str(shortDB.iloc[-1][crypto[:3]+'_short_moving_average']) + " " + "LMA "+crypto[:3]+": "+str(longDB.iloc[-1][crypto[:3]+'_long_moving_average']))
                print("Sell Signal")
                self.signalStatus = "SELL"

    #Main updateFunction to refresh based on new Robinhood data
    def update(self):
        self.shortMovingAverages = self.setShortMovingAverages()
        self.longMovingAverages = self.setLongMovingAverages()
        self.decideToTrade(self.shortMovingAverages, self.longMovingAverages)
        self.setCryptoTradeList()