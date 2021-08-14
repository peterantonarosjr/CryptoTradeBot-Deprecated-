import robin_stocks.robinhood as r
import pandas as pd
import robin_stocks.gemini as c
import pyotp

def getLiquidity():
    userAssets = r.load_account_profile()
    liquidity = float(userAssets["portfolio_cash"])
    return liquidity

def getCryptoEquity():
    userAssets = r.load_phoenix_account()
    equity = float(userAssets["portfolio_equity"].get("amount"))
    return equity

def cryptosToWatch():
    cryptoList = list()
    cryptoList.append("eth")
    return cryptoList

def buyCrypto(ticker,amount,currentPrice,testing):
    cashAvailable = getLiquidity()
    maxOver = 0.15
    buyLimitPrice = round(currentPrice + maxOver, 2)
    if testing:
        print("Bought "+amount+" "+ticker+" at "+buyLimitPrice)
    else:
        if amount*currentPrice<=cashAvailable:
            r.order_buy_crypto_limit(symbol=ticker,quantity=amount,limitPrice=buyLimitPrice)
        else:
            print("Not enough cash available in account to purchase")

def sellCrypto(ticker,amount,currentPrice,testing):
    maxUnder = 0.15
    sellLimitPrice = round(currentPrice - maxUnder, 2)
    if testing:
        print("Sold "+amount+" "+ticker+" at "+sellLimitPrice)
    else:
        r.order_sell_crypto_limit(symbol=ticker,quantity=amount,limitPrice=sellLimitPrice)

def buildDatabase(ticker,interval,length):
    cryptoInfo = getCryptoHistorical(ticker,interval,length)
    cryptoFrame = pd.DataFrame(cryptoInfo)

    dateTimes = pd.to_datetime(cryptoFrame.loc[:, 'begins_at'])
    openPrices = cryptoFrame.loc[:, 'open_price'].astype('float')
    closePrices = cryptoFrame.loc[:, 'close_price'].astype('float')

    cryptoPriceFrame = pd.concat([dateTimes,openPrices,closePrices], axis=1)
    cryptoPriceFrame = cryptoPriceFrame.set_index('begins_at')
    cryptoPriceFrame['mean_price'] = cryptoPriceFrame.mean(axis=1)

    return cryptoPriceFrame

def graphDatabase():
    return

def getCryptoHistorical(ticker,interval,length):
    return r.get_crypto_historicals(ticker, interval=interval, span=length, bounds="24_7")

