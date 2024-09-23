from SmartApi.webSocket import WebSocket
from SmartApi.smartConnect import SmartConnect

clientcode = '***REDACTED***'
password = '***REDACTED***'
apiKey = '***REDACTED***'
totp_secret = '***REDACTED***'


# Setup credentials
obj = SmartConnect(api_key=apiKey)
data = obj.generateSession(clientcode, password, totp_secret)
feed_token = obj.getfeedToken()
token = "nse_cm|2029"  # Example token

# Initialize WebSocket
ws = WebSocket(feed_token, clientcode)

def on_tick(ws, tick):
    for i in tick:
        print(f"LTP: {i.get('ltp')}")

def on_connect(ws, response):
    ws.send_request(token)

def on_close(ws, code, reason):
    ws.stop()

ws.on_ticks = on_tick
ws.on_connect = on_connect
ws.on_close = on_close

ws.connect()