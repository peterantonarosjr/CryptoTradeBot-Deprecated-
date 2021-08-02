import robin_stocks.robinhood as r
import robin_stocks.gemini as c
import pyotp
import time
from datetime import datetime

credentialFile = open('D:\\Pycharm-Workspace\\CryptoTradeBot\\RH.txt').read().splitlines()
EMAIL = credentialFile[0]
PASSWORD = credentialFile[1]
KEY = credentialFile[2]
CODE = credentialFile[3]
totp = pyotp.TOTP(KEY).now()
try:
    r.login(EMAIL,PASSWORD,mfa_code=CODE)
    c.authentication.login(KEY, CODE)
    c.authentication.heartbeat(jsonify=None)
    print("Successful Login/Authentication")
except:
    print("Failed Login/Authentication")


