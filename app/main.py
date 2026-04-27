from fastapi import FastAPI
from pymongo.errors import DuplicateKeyError
from app.fetcher import fetch_ohlcv
from app.database import ohlcv_collection
from app.validator import validate_record
import pandas as pd
import numpy as np

app = FastAPI(title="Quant Market Engine")

@app.get("/")
def home():
    return {"message": "Quant Market Engine Running"}

@app.get("/fetch/{symbol}")
def fetch_store(symbol: str):

    data = fetch_ohlcv(symbol)

    inserted = 0
    duplicates = 0
    rejected = []

    for row in data:

        errors = validate_record(row)

        if errors:
            rejected.append({"row": row, "errors": errors})
            continue

        row["symbol"] = symbol.upper()

        try:
            ohlcv_collection.insert_one(row)
            inserted += 1

        except DuplicateKeyError:
            duplicates += 1

    return {
        "symbol": symbol.upper(),
        "inserted": inserted,
        "duplicates": duplicates,
        "rejected_count": len(rejected),
        "status": "completed"
    }
    
@app.get("/data/{symbol}")
def get_data(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0}
        ).sort("Date", -1)
    )

    return records



@app.get("/analytics/{symbol}/returns")
def get_returns(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0, "Date": 1, "Close": 1}
        ).sort("Date", 1)
    )

    df = pd.DataFrame(records)

    if df.empty:
        return {"error": "No data found"}

    df["return"] = df["Close"].pct_change()

    result = df[["Date", "Close", "return"]].fillna(0).to_dict(orient="records")

    return {
        "symbol": symbol.upper(),
        "data": result
    }
    
    
    

@app.get("/analytics/{symbol}/volatility")
def get_volatility(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0, "Close": 1}
        ).sort("Date", 1)
    )

    df = pd.DataFrame(records)

    if df.empty:
        return {"error": "No data found"}

    df["return"] = df["Close"].pct_change()

    vol = float(df["return"].std())

    return {
        "symbol": symbol.upper(),
        "volatility": round(vol, 6)
    }
    
    
    
@app.get("/analytics/{symbol}/moving-average")
def moving_average(symbol: str, window: int = 3):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0, "Date": 1, "Close": 1}
        ).sort("Date", 1)
    )

    df = pd.DataFrame(records)

    if df.empty:
        return {"error": "No data found"}

    df["ma"] = df["Close"].rolling(window=window).mean()

    result = df.fillna(0).to_dict(orient="records")

    return {
        "symbol": symbol.upper(),
        "window": window,
        "data": result
    }
    
    
    
    
@app.get("/analytics/{symbol}/summary")
def summary(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0}
        )
    )

    df = pd.DataFrame(records)

    if df.empty:
        return {"error": "No data found"}

    latest_close = float(df["Close"].iloc[-1])
    highest = float(df["High"].max())
    lowest = float(df["Low"].min())
    avg_volume = int(df["Volume"].mean())

    return {
        "symbol": symbol.upper(),
        "latest_close": latest_close,
        "highest_price": highest,
        "lowest_price": lowest,
        "avg_volume": avg_volume
    }