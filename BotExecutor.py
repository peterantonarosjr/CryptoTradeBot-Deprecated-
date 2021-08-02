import robin_stocks.robinhood as r
import robin_stocks.gemini as c
import pyotp
from Utilities import *

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

def logout():
    r.logout()

def main():
    login(1)
    logout()

if __name__ == "__main__":
    main()

