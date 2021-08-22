import Utilities

class DumbScalp:
    def __init__(self,cryptoList):
        self.cryptoList = cryptoList
        self.cryptoPriceList = None
        self.cryptoTradeList = None
        self.signalStatus = None
        self.setCryptoTradeList()
        self.buyInitialCrypto()

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


    def getScalping(self):
        scalpingDatabases = {}
        for crypto in self.cryptoList:
            cryptoDB = Utilities.buildIndicatorDatabase(crypto[:3], "day", "year")
            cryptoDB[crypto[:3]+'_trade_completed'] = None #Fill here

        return scalpingDatabases


    #Buy a small amount of initial crypto to "kickstart" the buying/selling
    def buyInitialCrypto(self):
        for crypto, price in self.cryptoTradeList.items():
            print("Bought X "+crypto+" at "+ price)

    def decideToTrade(self):

        pass

    def update(self):
        self.decideToTrade()
        self.setCryptoTradeList()