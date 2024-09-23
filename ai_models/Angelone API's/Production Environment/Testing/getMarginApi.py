import AppLogin


obj = AppLogin.obj
def get_margin():
    params = {
        "positions": [
            {
                "exchange": "NFO",
                "qty": 50,
                "price": 0,
                "productType": "INTRADAY",
                "token": "67300",  # Replace with correct token
                "tradeType": "BUY"
            }
        ]
    }
    response = obj._postRequest("https://apiconnect.angelbroking.com/rest/secure/angelbroking/margin/v1/batch", params)
    return response

# Example usage
margin_data = get_margin()
print(margin_data)

'''Try only in market Hours'''