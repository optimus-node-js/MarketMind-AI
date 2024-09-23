from fastapi import FastAPI
from market_data.market_data_service import fetch_ltp, fetch_ohlc

app = FastAPI()

@app.get("/ltp/{symbol}/{token}")
def get_ltp(symbol: str, token: str):
    return fetch_ltp(symbol, token)

@app.get("/ohlc/{symbol}/{token}")
def get_ohlc(symbol: str, token: str, interval: str, from_date: str, to_date: str):
    return fetch_ohlc(symbol, token, interval, from_date, to_date)
