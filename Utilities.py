import robin_stocks.robinhood as r
import robin_stocks.gemini as c

def getEthHistorical(length):
    return r.get_crypto_historicals('eth',interval='day',span=length,bounds='24_7', info='close_price')