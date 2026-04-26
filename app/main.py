from fastapi import FastAPI
from app.fetcher import fetch_ohlcv
from app.database import ohlcv_collection
from app.validator import validate_record

app = FastAPI(title="Quant Market Engine")

@app.get("/")
def home():
    return {"message": "Quant Market Engine Running"}

@app.get("/fetch/{symbol}")
def fetch_store(symbol: str):
    data = fetch_ohlcv(symbol)

    inserted = 0
    rejected = []

    for row in data:
        errors = validate_record(row)

        if errors:
            rejected.append({"row": row, "errors": errors})
        else:
            row["symbol"] = symbol.upper()
            ohlcv_collection.insert_one(row)
            inserted += 1

    return {
        "symbol": symbol,
        "inserted": inserted,
        "rejected": rejected
    }

@app.get("/data/{symbol}")
def get_data(symbol: str):
    records = list(
        ohlcv_collection.find(
            {"symbol": symbol.upper()},
            {"_id": 0}
        )
    )
    return records