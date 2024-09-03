# Handles authentication, TOTP generation, session management, and refreshing sessions.
# This file will handle the authentication process, including generating TOTP and managing login sessions.

import pyotp
from SmartApi.smartConnect import SmartConnect
from .session_manager import SessionManager

class AuthService:
    def __init__(self):
        # Hardcoded credentials (we'll make these dynamic later)
        self.client_code = "***REDACTED***"
        self.password = "***REDACTED***"
        self.api_key = "***REDACTED***"
        self.totp_secret = "***REDACTED***"

        # Initialize the SmartConnect object
        self.obj = SmartConnect(api_key=self.api_key)

        # Initialize the session manager
        self.session_manager = SessionManager()

    def generate_totp(self):
        return pyotp.TOTP(self.totp_secret).now()

    def login(self):
        try:
            data = self.obj.generateSession(self.client_code, self.password, self.generate_totp())

            # Save tokens using the session manager
            self.session_manager.save_session(data['data']['jwtToken'], data['data']['refreshToken'])
            feed_token = self.obj.getfeedToken()
            self.session_manager.save_feed_token(feed_token)

            print("Login successful!")
            return self.obj, feed_token
        except Exception as e:
            print(f"Error during login: {e}")
            return None, None

    def refresh_session(self):
        refresh_token = self.session_manager.get_refresh_token()
        if not refresh_token:
            print("No refresh token found, please log in again.")
            return None

        try:
            # Refresh the session using the refresh token
            data = self.obj.refreshAccessToken(refresh_token)
            self.session_manager.save_session(data['data']['jwtToken'], refresh_token)
            print("Session refreshed!")
            return self.obj  # Returning the SmartConnect object after refreshing
        except Exception as e:
            print(f"Error during session refresh: {e}")
            return None
