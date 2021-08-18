from Utilities import *
from Indicators import GoldenDeathCross
from Indicators import RSIDivergence
from Indicators import Scalping
import pyotp
import time
import datetime

# User authentication and login for a specified number of days
def login(numOfDays):
    seconds = 60
    secPerMinute = seconds * 60
    secPerHour = secPerMinute * 60
    secPerDay = secPerHour * 24
    loginDuration = numOfDays * secPerDay

    credentialFile = open('/home/peterjr/Pycharm-Workspace/CryptoTradeBot/RH.txt').read().splitlines()
    EMAIL = credentialFile[0]
    PASSWORD = credentialFile[1]
    KEY = credentialFile[2]
    CODE = credentialFile[3]
    totp = pyotp.TOTP(KEY).now()
    try:
        r.login(EMAIL, PASSWORD, mfa_code=totp, expiresIn=loginDuration, store_session=False)
        c.authentication.login(KEY, CODE)
        c.authentication.heartbeat(jsonify=None)
        print("Successful Login/Authentication")
    except:
        print("Failed Login/Authentication")


# User logout
def logout():
    r.logout()


# Takes in loginDuration (# of days) and updateFrequency (# of seconds)
def main(loginDuration, mainUpdateDelta):
    #Times relevant to login and login duration
    login(loginDuration)
    loginTime = datetime.datetime.now()
    logoutTime = loginTime + datetime.timedelta(loginDuration)
    currentTime = datetime.datetime.now()

    #Build list of tickers for user
    cryptoTickerList = cryptosToTrade()

    #Cross Strategy
    crossStrategy = GoldenDeathCross.CrossStrategy(cryptoTickerList)
    crossStrategyTime = currentTime
    crossStrategyUpdateDelta = 10

    while currentTime < logoutTime:
        cash = getLiquidity()
        equity = getCryptoEquity()

        if(currentTime-crossStrategyTime).total_seconds()>= crossStrategyUpdateDelta:
            #print("Cross Strategy Update")
            crossStrategy.update() # Main Trading Logic for Golden/DeathCross
            crossTimeDelta = currentTime
        else:
            pass


        # DATE(Index)     CRYPTO_TICKER      PRICE       STATUS_OF_TRADE

        # Check each Indicator -> .signal attribute
        # Decide whether or not to complete a trade based on signals

        # Append information to TradeLogDataBase

        updateActiveGraph(crossStrategy.getShortMovingAverage().get('ETHUSD')
                          , crossStrategy.getLongMovingAverage().get('ETHUSD'))

        time.sleep(mainUpdateDelta)
        #print("Main Update")
        currentTime = datetime.datetime.now()

    logout()

if __name__ == "__main__":
    # Input # days login, # seconds update delta
    main(1, 5)
