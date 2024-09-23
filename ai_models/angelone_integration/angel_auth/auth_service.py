import pyotp
from SmartApi.smartConnect import SmartConnect
from fastapi import HTTPException

# Replace with your actual credentials
username = '***REDACTED***'
password = '***REDACTED***'
apiKey = '***REDACTED***'
totp_secret = '***REDACTED***'

# Generate TOTP
def generate_totp(totp_secret):
    return pyotp.TOTP(totp_secret).now()

# Login function
def login():
    obj = SmartConnect(api_key=apiKey)
    try:
        data = obj.generateSession(username, password, generate_totp(totp_secret))
        return obj, data['data']['refreshToken'], obj.getfeedToken()
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error during login: {e}")
