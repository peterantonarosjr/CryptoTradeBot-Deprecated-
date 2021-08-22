import robin_stocks.robinhood as r
import robin_stocks.gemini as c
import matplotlib.pyplot as plt
import pandas as pd

#Returns available cash for authenticated user
def getLiquidity():
    userAssets = r.load_account_profile()
    liquidity = float(userAssets["portfolio_cash"])
    return liquidity

#Returns the value of all held cryptocurrencies for authenticated user
def getCryptoEquity():
    userAssets = r.load_phoenix_account()
    equity = userAssets["crypto"].get("equity").get("amount")
    return equity

#Specifies a crypto of interest list for the authenticated user
def cryptosToTrade():
    cryptoList = list()
    cryptoList.append("ETHUSD")
    cryptoList.append("LTCUSD")
    return cryptoList

#Get prices for all interested crypto currencies of the authenticated user
def getCryptoPrices(cryptoList):
    cryptoPrices = []
    for crypto in cryptoList:
        cryptoPrices.append(c.get_price(crypto,side='buy'))
    return cryptoPrices

#Buy for a particular crypto currency with max overage willing to pay for authenticated user
def buyCrypto(ticker,amount,currentPrice,maxOver):
    cashAvailable = getLiquidity()
    buyLimitPrice = round(currentPrice + maxOver, 2)
    if amount*buyLimitPrice<=cashAvailable:
        r.order_buy_crypto_limit(symbol=ticker,quantity=amount,limitPrice=buyLimitPrice)
    else:
        print("Not enough cash available in account to purchase")

def buyCryptoTEST(ticker,amount,currentPrice,maxOver):
    cashAvailable = getLiquidity()
    buyLimitPrice = round(currentPrice + maxOver, 2)
    if amount*buyLimitPrice<=cashAvailable:
        print("Bought " + str(amount) + " " + ticker + "@ " + str(buyLimitPrice))
    else:
        print("Not enough cash available in account to purchase")
    pass

def sellCryptoTEST(ticker,amount,currentPrice,maxUnder):
    sellLimitPrice = round(currentPrice - maxUnder, 2)
    print("Sold " + str(amount) + " " + ticker + "@ " + str(sellLimitPrice))

#Sell for a particular crypto currency with max underage willing to pay for authenticated user
def sellCrypto(ticker,amount,currentPrice,maxUnder):
    sellLimitPrice = round(currentPrice - maxUnder, 2)
    r.order_sell_crypto_limit(symbol=ticker,quantity=amount,limitPrice=sellLimitPrice)

#Returns a list of specified crypto price
def getCryptoHistorical(ticker,interval,length):
    return r.get_crypto_historicals(symbol=ticker, interval=interval, span=length, bounds="24_7")

#Uses getCryptoHistorical() to build data frame of dates/openPrice/closePrice/meanPrice
def buildIndicatorDatabase(ticker,interval,length):
    cryptoInfo = getCryptoHistorical(ticker,interval,length)
    cryptoFrame = pd.DataFrame(cryptoInfo)

    dateTimes = pd.to_datetime(cryptoFrame.loc[:, 'begins_at'])
    openPrices = cryptoFrame.loc[:, 'open_price'].astype('float')
    closePrices = cryptoFrame.loc[:, 'close_price'].astype('float')

    cryptoPriceFrame = pd.concat([dateTimes,openPrices,closePrices], axis=1)
    cryptoPriceFrame = cryptoPriceFrame.set_index('begins_at')
    cryptoPriceFrame['mean_price'] = cryptoPriceFrame.mean(axis=1)

    cryptoPriceFrame.rename(columns={'open_price': ticker+'_open_price', 'close_price': ticker+'_close_price', 'mean_price': ticker+'_mean_price'}, inplace=True)
    return cryptoPriceFrame

def buildTradeDatabase():
    cols = ['date', 'crypto_ticker', 'transaction_price', 'trade_status']
    cryptoTradeFrame = pd.DataFrame(columns=cols)
    cryptoTradeFrame.set_index('date')
    return cryptoTradeFrame

def updateActiveGraph(xSize,ySize,cryptoList,smaDB,lmaDB,pause=1):
    plt.rcParams['figure.figsize'] = (xSize, ySize)
    plt.clf()
    plt.ion()
    plt.title('Statistic Logger')

    cryptoPlots = []

    for crypto in cryptoList:
        unique_cols = smaDB.get(crypto).columns.difference(lmaDB.get(crypto).columns)
        sma_lma_mergeDB = pd.merge(lmaDB.get(crypto), smaDB.get(crypto)[unique_cols], left_index=True, right_index=True, how='outer')
        cryptoPlots.append(sma_lma_mergeDB)

    finalStatsPlot = pd.concat(cryptoPlots, axis=1)
    plt.plot(finalStatsPlot)
    plt.legend(finalStatsPlot.columns.values.tolist(),
               bbox_to_anchor=(0.5, 1.16),ncol=5,fontsize=16/len(cryptoList),loc='upper center')

    plt.draw()
    plt.pause(pause)
