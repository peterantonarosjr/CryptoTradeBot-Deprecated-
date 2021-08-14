import Utilities
from TradingStrategies import GoldenDeathCross
from TradingStrategies import RSIDivergence
from TradingStrategies import Scalping
from Utilities import *
import pyotp
import time
import datetime

#User authentication and login for a specified number of days
def login(numOfDays):
    seconds = 60
    secPerMinute = seconds*60
    secPerHour = secPerMinute*60
    secPerDay = secPerHour*24
    loginDuration = numOfDays*secPerDay

    credentialFile = open('D:\\Pycharm-Workspace\\CryptoTradeBot\\RH.txt').read().splitlines()
    EMAIL = credentialFile[0]
    PASSWORD = credentialFile[1]
    KEY = credentialFile[2]
    CODE = credentialFile[3]
    totp = pyotp.TOTP(KEY).now()
    try:
        r.login(EMAIL, PASSWORD, mfa_code=totp, expiresIn=loginDuration,store_session=False)
        c.authentication.login(KEY, CODE)
        c.authentication.heartbeat(jsonify=None)
        print("Successful Login/Authentication")
    except:
        print("Failed Login/Authentication")

#User logout
def logout():
    r.logout()

#Takes in loginDuration (# of days) and updateFrequency (# of minutes)
def main(loginDuration,updateFrequency):
    login(loginDuration)
    loginTime = datetime.datetime.now()
    logoutTime = loginTime + datetime.timedelta(loginDuration)
    currentTime = datetime.datetime.now()

    cryptoTickerList = cryptosToTrade()

    crossStrategy = GoldenDeathCross.CrossStrategy(cryptoTickerList)

    while currentTime<logoutTime:
        cash = getLiquidity()
        equity = getCryptoEquity()

        print(getCryptoPrices(cryptoTickerList))
        print(crossStrategy.getShortMovingAverage()[1])
        print(crossStrategy.getLongMovingAverage()[1])



        #MAIN TRADING STUFF GOES HERE

        time.sleep(updateFrequency)
        crossStrategy.update()
        currentTime = datetime.datetime.now()

    logout()


if __name__ == "__main__":
    #Input # days login, # seconds update delta
    main(1,5)

