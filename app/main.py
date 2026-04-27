from fastapi import FastAPI
from pymongo.errors import DuplicateKeyError
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