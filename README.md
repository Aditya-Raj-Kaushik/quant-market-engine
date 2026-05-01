# Quant Market Data & Analytics Engine

A **production-style quantitative finance backend system** that ingests, validates, stores, and analyzes **OHLCV (Open, High, Low, Close, Volume)** market data with **real-time caching** and **anomaly detection**.

---

# 🚀 Overview

This project simulates a **mini institutional market data platform** used in trading systems and quantitative research pipelines.

It provides:

- Reliable, validated financial data  
- Quant analytics (returns, volatility, moving averages)  
- Real-time cached prices  
- Data quality monitoring  

The system is designed with a **backend-first, scalable architecture** using APIs, caching, and automated ingestion workflows.

---

# 🧠 Key Features

## 📥 Data Ingestion

- Fetches OHLCV data from **Yahoo Finance**
- Supports **100+ global symbols** (US + NSE)
- Automated ingestion via scheduler

---

## ✅ Data Validation Engine

Detects:

- Invalid price relationships (High < Low)  
- Negative or zero volume  
- Missing values  

Ensures only **clean, reliable data** is stored.

---

## 🗄️ Data Storage

- Historical data stored in **MongoDB**
- Indexed on `(symbol, timestamp)` for fast queries
- Duplicate-safe ingestion using unique constraints

---

## ⚡ Real-Time Caching

- Uses **Redis**
- Stores latest price for instant retrieval
- Reduces database load

---

## 📈 Quant Analytics APIs

- Returns calculation  
- Volatility estimation  
- Moving averages  
- Market summary metrics  

---

## 🚨 Anomaly Detection

Flags:

- Price jumps greater than **10%**  
- Abnormal volume spikes  

Helps detect **data issues or unusual market activity**.

---

## 📊 Data Quality Scoring

Computes dataset reliability score by penalizing:

- Missing values  
- Invalid prices  
- Zero-volume rows  

---

## 🔄 Scheduler (Automation)

- Automatically fetches data for multiple symbols  
- Runs at configurable intervals  
- Keeps system updated continuously  

---

# 🏗️ Architecture

```
Market Data API (Yahoo Finance)
          ↓
      Scheduler
          ↓
       FastAPI
     ↙        ↘
MongoDB     Redis
(Historical) (Live Cache)
```

---

# 🛠️ Tech Stack

- **Backend:** FastAPI  
- **Database:** MongoDB  
- **Cache:** Redis  
- **Data Processing:** Pandas, NumPy  
- **Scheduler:** Python schedule  
- **Containerization:** Docker  

---

# 📂 Project Structure

```
project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── fetcher.py
│   ├── validator.py
│   └── cache.py
│
├── scheduler.py
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```
git clone <your-repo-url>
cd project
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Run MongoDB & Redis (Docker)

```
docker run -d --name quant-mongo -p 27017:27017 mongo
docker run -d --name quant-redis -p 6379:6379 redis
```

---

## 5️⃣ Configure Environment

Create a `.env` file:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=quantdb
```

---

## 6️⃣ Start Backend

```
uvicorn app.main:app --reload
```

---

## 7️⃣ Run Scheduler

```
python scheduler.py
```

---

# 📡 API Endpoints

## Core APIs

```
GET /fetch/{symbol}     → Fetch and store data
GET /data/{symbol}      → Retrieve historical data
GET /live/{symbol}      → Get latest cached price
```

---

## Analytics APIs

```
GET /analytics/{symbol}/returns
GET /analytics/{symbol}/volatility
GET /analytics/{symbol}/moving-average?window=5
GET /analytics/{symbol}/summary
```

---

## Quality & Anomaly APIs

```
GET /quality/{symbol}
GET /anomaly/{symbol}
```

---

# 📈 Example Use Case

Track and analyze assets such as:

- AAPL  
- MSFT  
- RELIANCE.NS  

Perform:

- Return analysis  
- Volatility estimation  
- Data reliability checks  
- Anomaly detection  

---

# 🧪 What This Project Demonstrates

- Backend system design for financial data  
- Data pipeline engineering  
- Time-series analysis  
- Real-time caching strategies  
- API design and scalability  
- Production-level practices (idempotency, indexing, validation)  

---

# 📌 Future Enhancements

- WebSocket-based live streaming  
- Portfolio optimization engine  
- Strategy backtesting module  
- Multi-source data reconciliation  
- Next.js dashboard visualization  
- ML-based anomaly detection  

---

# 🧾 Resume Line

Developed a real-time **quant market data engine** with automated ingestion, validation, anomaly detection, Redis caching, and analytics APIs using FastAPI and MongoDB.

---

# ⚠️ Disclaimer

This project is for **educational and research purposes only** and does not constitute financial advice.

---

# 👨‍💻 Author

**Aditya Raj Kaushik**
