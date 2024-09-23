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

def place_dynamic_order(symbol, symbol_token, transaction_type, quantity, order_type="LIMIT", price=None, product_type="INTRADAY", duration="DAY", squareoff="0", stoploss="0", triggerprice="0", variety="NORMAL"):
    try:
        order_params = {
            "variety": variety,  # NORMAL, STOPLOSS, etc.
            "tradingsymbol": symbol,  # Dynamic symbol like "SBIN-EQ"
            "symboltoken": symbol_token,  # Dynamic symbol token like "3045"
            "transactiontype": transaction_type,  # "BUY" or "SELL"
            "exchange": "NSE",  # NSE or BSE
            "ordertype": order_type,  # LIMIT, MARKET, SL, SL-M, etc.
            "producttype": product_type,  # INTRADAY, CNC, etc.
            "duration": duration,  # DAY, IOC, etc.
            "quantity": str(quantity),  # Quantity as string
            "squareoff": squareoff,  # Square off value for intraday
            "stoploss": stoploss,  # Stop loss value
            "triggerprice": triggerprice  # Trigger price for SL orders
        }

        # Handle price for LIMIT and SL orders
        if order_type in ["LIMIT", "SL"] and price:
            order_params["price"] = str(price)

        # For SL-M orders, price should not be included
        if order_type == "SL-M":
            order_params.pop("price", None)

        # Placing the order
        order_id = obj.placeOrderFullResponse(order_params)
        print("The order id is: {}".format(order_id))

    except Exception as e:
        print("Order placement failed: {}".format(e))


# Example usage
symbol = "SBIN-EQ"
symbol_token = "3045"
transaction_type = "BUY"
quantity = 1


'''Modify, Cancel Orders function is yet to implement in this'''


# For LIMIT order
place_dynamic_order(symbol, symbol_token, transaction_type, quantity, order_type="LIMIT", price=195)

# For MARKET order
place_dynamic_order(symbol, symbol_token, transaction_type, quantity, order_type="MARKET")

