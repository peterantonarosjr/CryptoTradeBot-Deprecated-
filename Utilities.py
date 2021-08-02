import robin_stocks.robinhood as r
import robin_stocks.gemini as c
import pyotp


def getLiquidity():
    userAssets = r.build_user_profile()
    liquidity = float(userAssets['cash'])
    return liquidity

def getEquity():
    userAssets = r.build_user_profile()
    equity = float(userAssets['equity'])
    return equity

def cryptosToWatch():
    cryptoList = list()
    cryptoList.append('eth')
    return cryptoList

def buyCrypto(ticker,amount,currentPrice,testing):
    cashAvailable = getLiquidity()
    maxOver = 0.15
    buyLimitPrice = round(currentPrice + maxOver, 2)
    if testing:
        print("Bought "+amount+" "+ticker+" at "+buyLimitPrice)
    else:
        if amount<=cashAvailable:
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

def buildDatabase():
    return

def graphDatabase():
    return

def getCryptoHistorical(ticker,length,type):
    info = type.lower()
    info.replace(' ','')
    for charPos in range(0,len(info)):
        if info[charPos]=='p':
            infoFormat = info[:charPos-1]+"_"+info[charPos:]
            return r.get_crypto_historicals(ticker, interval='day', span=length, bounds='24_7', info=infoFormat)
        else:
            print("Improperly formatted arguments")
