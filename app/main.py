from fastapi import FastAPI
from pymongo.errors import DuplicateKeyError
from app.fetcher import fetch_ohlcv
from app.database import ohlcv_collection
from app.validator import validate_record
import pandas as pd
import numpy as np
from app.cache import r

app = FastAPI(title="Quant Market Engine")


# HOME API
@app.get("/")
def home():
    return {"message": "Quant Market Engine Running"}



# FETCH AND STORE OHLCV DATA API
@app.get("/fetch/{symbol}")
def fetch_store(symbol: str):

    data = fetch_ohlcv(symbol)

    inserted = 0
    duplicates = 0
    rejected = []

    for row in data:

        errors = validate_record(row)

        if errors:
            rejected.append({
                "row": row,
                "errors": errors
            })
            continue

        row["symbol"] = symbol.upper()

        try:
            ohlcv_collection.insert_one(row)
            inserted += 1

            # Store latest close price in Redis cache
            r.set(
                f"live:{symbol.upper()}",
                str(row["Close"])
            )

        except DuplicateKeyError:
            duplicates += 1

    return {
        "symbol": symbol.upper(),
        "inserted": inserted,
        "duplicates": duplicates,
        "rejected_count": len(rejected),
        "status": "completed"
    }
 
 
 
 # GET HISTORICAL MARKET DATA API   
@app.get("/data/{symbol}")
def get_data(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0}
        ).sort("Date", -1)
    )

    return records



# RETURNS API
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
    
    
    

# VOLATILITY API
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
    
    
    
# MOVING AVERAGE API
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
    
    
    
# SUMMARY API 
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
    
    
# ANOMALY DETECTION API
@app.get("/anomaly/{symbol}")
def detect_anomaly(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0, "Date": 1, "Close": 1, "Volume": 1}
        ).sort("Date", 1)
    )

    df = pd.DataFrame(records)

    if df.empty:
        return {"error": "No data found"}

    df["return"] = df["Close"].pct_change()

    price_anomalies = df[np.abs(df["return"]) > 0.10]

    avg_vol = df["Volume"].mean()
    volume_anomalies = df[df["Volume"] > avg_vol * 2]

    return {
        "symbol": symbol.upper(),
        "price_anomalies": price_anomalies.fillna(0).to_dict(orient="records"),
        "volume_anomalies": volume_anomalies.to_dict(orient="records")
    }
    
    
    
# DATA QUALITY API
@app.get("/quality/{symbol}")
def quality_score(symbol: str):

    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0}
        )
    )

    df = pd.DataFrame(records)

    if df.empty:
        return {"error": "No data found"}

    total_rows = len(df)

    missing_values = int(df.isnull().sum().sum())

    invalid_prices = int((df["High"] < df["Low"]).sum())

    zero_volume = int((df["Volume"] == 0).sum())

    penalties = missing_values + invalid_prices + zero_volume

    score = max(0, round(100 - (penalties / total_rows) * 100, 2))

    return {
        "symbol": symbol.upper(),
        "rows": total_rows,
        "missing_values": missing_values,
        "invalid_prices": invalid_prices,
        "zero_volume_rows": zero_volume,
        "quality_score": score
    }
    
    
    
    
    
 
 # LIVE PRICE API   
@app.get("/live/{symbol}")
def live_price(symbol: str):

    value = r.get(f"live:{symbol.upper()}")

    if value is None:
        return {"error": "No live data cached"}

    return {
        "symbol": symbol.upper(),
        "live_close": float(value),
        "source": "redis_cache"
    }