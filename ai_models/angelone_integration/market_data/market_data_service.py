from fastapi import HTTPException
from angel_auth.auth_service import login

# Fetch LTP for a single symbol
def fetch_ltp(symbol: str, token: str):
    obj, refreshToken, feedToken = login()
    try:
        LTP = obj.ltpData('NSE', symbol, token)
        if LTP and 'data' in LTP and 'ltp' in LTP['data']:
            return {"symbol": symbol, "ltp": LTP['data']['ltp']}
        else:
            raise HTTPException(status_code=404, detail=f"No LTP data found for {symbol}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get LTP data for {symbol}: {e}")

# Fetch OHLC for a single symbol within a specific date range
def fetch_ohlc(symbol: str, token: str, interval: str, from_date: str, to_date: str):
    obj, refreshToken, feedToken = login()
    try:
        historical_params = {
            "exchange": "NSE",
            "symboltoken": token,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date
        }

        data = obj.getCandleData(historical_params)
        if data and 'data' in data:
            ohlc_data = data['data']
            ohlc_list = [
                {
                    "date": ohlc[0],
                    "open": ohlc[1],
                    "high": ohlc[2],
                    "low": ohlc[3],
                    "close": ohlc[4]
                }
                for ohlc in ohlc_data
            ]
            return {"symbol": symbol, "ohlc": ohlc_list}
        else:
            raise HTTPException(status_code=404, detail=f"No OHLC data found for {symbol}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get OHLC data for {symbol}: {e}")
