import pyotp
from SmartApi.smartConnect import SmartConnect
from fastapi import FastAPI, HTTPException

# Replace with your actual credentials
clientcode = '***REDACTED***'
password = '***REDACTED***'
apiKey = '***REDACTED***'
totp_secret = '***REDACTED***'

app = FastAPI()

def generate_totp(totp_secret):
    return pyotp.TOTP(totp_secret).now()

def login(apiKey, clientcode, password, totp_secret):
    obj = SmartConnect(api_key=apiKey)
    try:
        data = obj.generateSession(clientcode, password, generate_totp(totp_secret))
        return obj, data['data']['refreshToken'], obj.getfeedToken()
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error during login: {e}")

obj, refreshToken, feedToken = login(apiKey, clientcode, password, totp_secret)