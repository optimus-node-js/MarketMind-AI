# Contains methods to fetch market data such as LTP, OHLC, quotes, and market depth.




from SmartApi.smartConnect import SmartConnect
from angel_auth.auth_service import AuthService

class MarketDataService:
    def __init__(self):
        self.auth_service = AuthService()
        self.obj, self.feed_token = self.auth_service.login()

    def get_ltp(self, symbol, token):
        # Ensure that we are using a valid session
        if not self.obj:
            self.obj, self.feed_token = self.auth_service.login()

        try:
            LTP = self.obj.ltpData('NSE', symbol, token)
            if LTP and 'data' in LTP and 'ltp' in LTP['data']:
                return LTP['data']['ltp']
            else:
                return f"No LTP data found for {symbol}"
        except Exception as e:
            return f"Error fetching LTP data for {symbol}: {e}"

    def get_ohlc(self, symbol, token):
        # You can implement OHLC fetching here similar to the LTP method
        pass

    def get_market_depth(self, symbol, token):
        # You can implement market depth fetching here similar to the LTP method
        pass
