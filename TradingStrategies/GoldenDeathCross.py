import Utilities

class CrossStrategy:
    def __init__(self,cryptoList):
        self.cryptoList = cryptoList
        self.cryptoPriceList = None
        self.cryptoTradeList = None
        self.setCryptoTradeList()


    def setCryptoPriceList(self):
        self.cryptoPriceList = Utilities.getCryptoPrices(self.cryptoList)

    def getCryptoPriceList(self):
        return self.cryptoPriceList

    def setCryptoTradeList(self):
        self.setCryptoPriceList()
        self.cryptoTradeList = dict(zip(self.cryptoList, self.cryptoPriceList))

    def getCryptoTradeList(self):
        return self.cryptoTradeList

    def update(self):
        self.setCryptoTradeList()
        Utilities.graphDatabase([self.getShortMovingAverage()[0],self.getLongMovingAverage()[0]])

    def getShortMovingAverage(self):
        cryptosShortDatabases = []
        cryptosShortAverages = {}
        i=0
        for crypto in self.cryptoList:
            cryptosShortDatabases.append(Utilities.buildDatabase(crypto[:3],"day","month"))
            cryptosShortAverages.update({crypto: cryptosShortDatabases[i]['mean_price'].mean()})
            i+=1
        return cryptosShortDatabases,cryptosShortAverages


    def getLongMovingAverage(self):
        cryptosLongDatabases = []
        cryptosLongAverages = {}
        i=0
        for crypto in self.cryptoList:
            cryptosLongDatabases.append(Utilities.buildDatabase(crypto[:3], "day", "3month"))
            cryptosLongAverages.update({crypto: cryptosLongDatabases[i]['mean_price'].mean()})
            i+=1
        return cryptosLongDatabases,cryptosLongAverages




