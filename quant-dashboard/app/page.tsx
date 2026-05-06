"use client";

import { useEffect, useState } from "react";
import axios from "axios";

const symbols = ["AAPL", "MSFT", "NVDA", "SPY"];

export default function Home() {
  const [prices, setPrices] = useState<any>({});
  const [prevPrices, setPrevPrices] = useState<any>({});
  const [portfolio, setPortfolio] = useState<any>(null);
  const [correlation, setCorrelation] = useState<any>(null);

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
        result[symbol] = null;
      }
    }

    setPrevPrices(prices);
    setPrices(result);
  };

  // Portfolio analytics
  const fetchPortfolio = async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/portfolio/analytics",
      { symbols }
    );
    setPortfolio(res.data);
  };

  // Correlation matrix
  const fetchCorrelation = async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/portfolio/correlation",
      { symbols }
    );
    setCorrelation(res.data.correlation_matrix);
  };

  useEffect(() => {
    fetchPrices();
    fetchPortfolio();
    fetchCorrelation();

    const interval = setInterval(fetchPrices, 5000);
    return () => clearInterval(interval);
  }, []);

  const getColor = (symbol: string) => {
    if (!prevPrices[symbol]) return "text-gray-500";
    return prices[symbol] > prevPrices[symbol]
      ? "text-green-500"
      : "text-red-500";
  };

  return (
    <div className="p-8 space-y-10">
      <h1 className="text-3xl font-bold">
        Quant Market Dashboard
      </h1>

      {/* LIVE PRICES */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Live Market Prices
        </h2>

        <div className="grid grid-cols-4 gap-4">
          {symbols.map((symbol) => (
            <div
              key={symbol}
              className="p-4 border rounded-xl shadow hover:shadow-lg transition"
            >
              <h3 className="font-semibold">{symbol}</h3>

              <p className={`text-xl mt-2 ${getColor(symbol)}`}>
                {prices[symbol] ?? "Loading..."}
              </p>

              <p className="text-sm text-gray-500">
                {prevPrices[symbol]
                  ? ((prices[symbol] - prevPrices[symbol]) /
                      prevPrices[symbol] *
                      100
                    ).toFixed(2) + "%"
                  : "-"}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* PORTFOLIO */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Portfolio Analytics
        </h2>

        {portfolio && (
          <div className="grid grid-cols-4 gap-4">
            <div className="p-4 border rounded-xl">
              <p>Mean Return</p>
              <p className="font-bold">{portfolio.mean_return}</p>
            </div>

            <div className="p-4 border rounded-xl">
              <p>Volatility</p>
              <p className="font-bold">{portfolio.volatility}</p>
            </div>

            <div className="p-4 border rounded-xl">
              <p>Sharpe Ratio</p>
              <p className="font-bold">{portfolio.sharpe_ratio}</p>
            </div>

            <div className="p-4 border rounded-xl">
              <p>Max Drawdown</p>
              <p className="font-bold">
                {portfolio.max_drawdown}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* CORRELATION HEATMAP */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Correlation Matrix
        </h2>

        {correlation && (
          <div className="overflow-auto">
            <table className="border-collapse">
              <thead>
                <tr>
                  <th></th>
                  {symbols.map((s) => (
                    <th key={s} className="p-2 border">
                      {s}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {symbols.map((row) => (
                  <tr key={row}>
                    <td className="p-2 border font-semibold">
                      {row}
                    </td>

                    {symbols.map((col) => {
                      const val =
                        correlation[row]?.[col] ?? 0;

                      const bg =
                        val > 0.7
                          ? "bg-green-400"
                          : val > 0.3
                          ? "bg-green-200"
                          : val < -0.7
                          ? "bg-red-400"
                          : val < -0.3
                          ? "bg-red-200"
                          : "bg-gray-100";

                      return (
                        <td
                          key={col}
                          className={`p-2 border text-center ${bg}`}
                        >
                          {val.toFixed(2)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}