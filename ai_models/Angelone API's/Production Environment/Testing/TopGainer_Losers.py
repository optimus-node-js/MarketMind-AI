import AppLogin
from time import sleep
obj = AppLogin.obj

def fetch_top_gainers_losers(data_type):
    params = {
        "datatype": data_type,  # Use "PercPriceGainers" or "PercPriceLosers"
        "expirytype": "NEAR"  # Remove this for equity, only needed for futures
    }

    response = obj._postRequest("api.gainersLosers", params)
    return response


# Example usage
gainers = fetch_top_gainers_losers("PercPriceGainers")
sleep(1)
losers = fetch_top_gainers_losers("PercPriceLosers")

print("Top Gainers:", gainers)
print("Top Losers:", losers)