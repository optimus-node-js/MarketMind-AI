import AppLogin


obj = AppLogin.obj

def estimate_charges():
    params = {
        "orders": [
            {
                "product_type": "DELIVERY",
                "transaction_type": "BUY",
                "quantity": "10",
                "price": "800",
                "exchange": "NSE",
                "symbol_name": "SBIN-EQ",
                "token": "3045"
            }
        ]
    }
    response = obj._postRequest("api.estimateCharges", params)
    return response

charges = estimate_charges()
print(charges)
