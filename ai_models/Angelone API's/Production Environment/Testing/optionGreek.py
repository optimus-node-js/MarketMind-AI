import AppLogin

obj = AppLogin.obj


def get_option_greeks(symbol, expiry_date):
    try:
        params = {
            "name": symbol,  # Underlying stock symbol (e.g., "NIFTY")
            "expirydate": expiry_date  # Expiry date (e.g., "25JAN2024")
        }
        response = obj._postRequest("api.optionGreek", params)

        # Check if the response is successful
        if response['status']:
            print("Option Greeks data fetched successfully!")
            return response['data']
        else:
            print(f"Error: {response['message']}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Example usage to fetch Nifty's option greeks for expiry 25JAN2024
option_greeks = get_option_greeks("NIFTY", "19SEP2024")
print(option_greeks)
'''Try only in market Hours'''
