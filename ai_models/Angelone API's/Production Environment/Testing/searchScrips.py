import AppLogin

obj = AppLogin.obj

def search_scrip(search_scrip):
    response = obj.searchScrip("NSE", search_scrip)
    return response

# Example usage
search_result = search_scrip("SBIN")
print(search_result)
