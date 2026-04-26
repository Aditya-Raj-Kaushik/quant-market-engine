import yfinance as yf

def fetch_ohlcv(symbol="AAPL", period="5d", interval="1d"):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    return df.to_dict(orient="records")