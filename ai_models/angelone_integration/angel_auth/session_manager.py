# Manages active sessions, including saving and loading session tokens.
# This file will manage the storage and retrieval of session tokens.
import os

class SessionManager:
    def __init__(self, session_file="session.txt"):
        self.session_file = session_file

    def save_session(self, jwt_token, refresh_token):
        with open(self.session_file, "w") as file:
            file.write(f"JWT_TOKEN={jwt_token}\n")
            file.write(f"REFRESH_TOKEN={refresh_token}\n")

    def save_feed_token(self, feed_token):
        with open(self.session_file, "a") as file:
            file.write(f"FEED_TOKEN={feed_token}\n")

    def get_jwt_token(self):
        return self._get_token("JWT_TOKEN")

    def get_refresh_token(self):
        return self._get_token("REFRESH_TOKEN")

    def get_feed_token(self):
        return self._get_token("FEED_TOKEN")

    def _get_token(self, token_type):
        if os.path.exists(self.session_file):
            with open(self.session_file, "r") as file:
                for line in file:
                    if line.startswith(token_type):
                        return line.split("=")[1].strip()
        return None

