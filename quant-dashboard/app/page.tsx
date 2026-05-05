"use client";

import { useEffect, useState } from "react";
import axios from "axios";

const symbols = ["AAPL", "MSFT", "NVDA", "SPY"];

export default function Home() {
  const [prices, setPrices] = useState<any>({});
  const [portfolio, setPortfolio] = useState<any>(null);

  // Fetch live prices
  const fetchPrices = async () => {
    let result: any = {};

    for (let symbol of symbols) {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/live/${symbol}`
        );
        result[symbol] = res.data.live_close;
      } catch {
        result[symbol] = "Error";
      }
    }

    setPrices(result);
  };

  // Fetch portfolio analytics
  const fetchPortfolio = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/portfolio/analytics",
        {
          symbols: symbols,
        }
      );

      setPortfolio(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPrices();
    fetchPortfolio();

    const interval = setInterval(() => {
      fetchPrices();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold">
        Quant Dashboard
      </h1>

      {/* Live Prices */}
      <div>
        <h2 className="text-xl mb-4 font-semibold">
          Live Market Prices
        </h2>

        <div className="grid grid-cols-4 gap-4">
          {symbols.map((symbol) => (
            <div
              key={symbol}
              className="p-4 border rounded-xl shadow"
            >
              <h3 className="font-semibold">{symbol}</h3>
              <p className="text-xl mt-2">
                {prices[symbol] ?? "Loading..."}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Portfolio Analytics */}
      <div>
        <h2 className="text-xl mb-4 font-semibold">
          Portfolio Analytics
        </h2>

        {portfolio ? (
          <div className="grid grid-cols-4 gap-4">
            <div className="p-4 border rounded-xl">
              <p>Mean Return</p>
              <p className="font-bold">
                {portfolio.mean_return}
              </p>
            </div>

            <div className="p-4 border rounded-xl">
              <p>Volatility</p>
              <p className="font-bold">
                {portfolio.volatility}
              </p>
            </div>

            <div className="p-4 border rounded-xl">
              <p>Sharpe Ratio</p>
              <p className="font-bold">
                {portfolio.sharpe_ratio}
              </p>
            </div>

            <div className="p-4 border rounded-xl">
              <p>Max Drawdown</p>
              <p className="font-bold">
                {portfolio.max_drawdown}
              </p>
            </div>
          </div>
        ) : (
          <p>Loading portfolio...</p>
        )}
      </div>
    </div>
  );
}