#  The entry point to the program, which will call the necessary services and execute API requests based on your requirements.

import sys
import os

# Add the parent directory of angelone_integration to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from angel_auth.auth_service import AuthService
from market_data.market_data_service import MarketDataService

if __name__ == "__main__":
    # Step 1: Authenticate and get tokens
    auth_service = AuthService()
    jwt_token, feed_token = auth_service.login()

    if jwt_token:
        print(f"JWT Token: {jwt_token}")
        print(f"Feed Token: {feed_token}")

        # Step 2: Initialize MarketDataService
        market_data_service = MarketDataService()

        # Test LTP
        ltp = market_data_service.get_ltp("CIPLA-EQ", "694")
        print(f"LTP: {ltp}")

        # Test OHLC
        ohlc = market_data_service.get_ohlc("CIPLA-EQ", "694")
        print(f"OHLC: {ohlc}")

        # Test Market Depth
        market_depth = market_data_service.get_market_depth("CIPLA-EQ", "694")
        print(f"Market Depth: {market_depth}")
    else:
        print("Authentication failed. Please check your credentials.")
