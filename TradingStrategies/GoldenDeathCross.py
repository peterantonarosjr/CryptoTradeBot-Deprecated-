import Utilities
import matplotlib.pyplot as plt

class CrossStrategy:
    def __init__(self,cryptoList):
        self.cryptoList = cryptoList
        self.cryptoPriceList = None
        self.cryptoTradeList = None
        self.setCryptoTradeList()
        #self.tradeStatus = ''

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

    # Get the short moving average past 30 days for each crypto in cryptoList
    def getShortMovingAverage(self):
        cryptosShortDatabases = {}
        cryptosShortAverages = {}
        i = 0
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildDatabase(crypto[:3], "day", "3month")
            cryptoDB['short_moving_average'] = cryptoDB['mean_price'].rolling(window=30).mean()
            cryptosShortAverages.update({crypto: cryptoDB['short_moving_average'].dropna().iloc[-30:]})
            cryptosShortDatabases.update({crypto: cryptoDB.dropna().iloc[-30:]})
            i += 1
        return cryptosShortDatabases, cryptosShortAverages

    ##Get the long moving average past 100 days for each crypto in cryptoList
    def getLongMovingAverage(self):
        cryptosLongDatabases = {}
        cryptosLongAverages = {}
        i = 0
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildDatabase(crypto[:3], "day", "year")
            cryptoDB['long_moving_average'] = cryptoDB['mean_price'].rolling(window=100).mean()
            cryptosLongAverages.update({crypto: cryptoDB['long_moving_average'].dropna().iloc[-100:]})
            cryptosLongDatabases.update({crypto: cryptoDB.dropna().iloc[-100:]})
            i += 1
        return cryptosLongDatabases, cryptosLongAverages

    # Graph the dbs for each crypto in cryptoList (short/long) and their short/long avgs
    def graphMovingAverages(self):
        shortDBs, shortAVGs = self.getShortMovingAverage()
        longDBs, longAVGs = self.getLongMovingAverage()

        fig = plt.figure(figsize=(15,8))
        for crypto in self.cryptoList:
            ax1 = fig.add_subplot(221)
            ax1.title.set_text("Short Moving Average (30 Day)")
            plt.plot(shortDBs.get(crypto))
            plt.plot(shortAVGs.get(crypto))

            ax2 = fig.add_subplot(222)
            ax2.title.set_text("Long Moving Average (100 Day)")
            plt.plot(longDBs.get(crypto))
            plt.plot(longAVGs.get(crypto))

            ax3 = fig.add_subplot(223)
            ax3.title.set_text("Short Vs Long Moving Average")
            plt.plot(longDBs.get(crypto))
            plt.plot(shortAVGs.get(crypto))


        plt.tight_layout()
        plt.show()

    #Decides whether or not to trade based on Golden/Death Cross Idea
    def decideToTrade(self, shortDBs, shortAVGs, longDBs, longAVGs):
        for crypto in self.cryptoList:
            shortDB = shortDBs.get(crypto)
            shortAVG = shortAVGs.get(crypto)
            longDB = longDBs.get(crypto)
            longAVG = longAVGs.get(crypto)

            if shortAVG[-1] >= longAVG[-1]:
                print("SMA: "+str(shortAVG[-1]) + " " + "LMA: "+str(longAVG[-1]))
                print("Buy Signal")
                return 0
            else:
                print("SMA: "+str(shortAVG[-1]) + " " + "LMA: "+str(longAVG[-1]))
                print("Sell Signal")
                return 1

    #Main updateFunction to refresh based on new Robinhood data
    def update(self):
        shortMovingDatabases, shortMovingAverages = self.getShortMovingAverage()
        longMovingDatabases, longMovingAverages = self.getLongMovingAverage()
        self.decideToTrade(shortMovingDatabases, shortMovingAverages, longMovingDatabases, longMovingAverages)
        self.graphMovingAverages() #Uncomment to see graphs for short/long moving averages
        self.setCryptoTradeList()





