from pymongo import MongoClient, ASCENDING
from app.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)

db = client[DB_NAME]
ohlcv_collection = db["ohlcv"]

# Unique index
ohlcv_collection.create_index(
    [("symbol", ASCENDING), ("Date", ASCENDING)],
    unique=True
)