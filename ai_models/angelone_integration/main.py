#  The entry point to the program, which will call the necessary services and execute API requests based on your requirements.

from auth.auth_service import AuthService

if __name__ == "__main__":
    auth_service = AuthService()

    # Attempt to log in and get the feed token
    jwt_token, feed_token = auth_service.login()

    if jwt_token:
        print(f"JWT Token: {jwt_token}")
        print(f"Feed Token: {feed_token}")
