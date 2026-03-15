"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { stocksApi, watchlistApi } from "@/lib/api-client";
import type { StockQuote, OHLCVDataPoint, TimeRange } from "@/types";
import { formatCurrency, formatPercent, formatVolume, pnlColorClass, pnlArrow, formatRelativeTime } from "@/lib/utils";
import PriceChart from "@/components/charts/PriceChart";

const TIME_RANGES: TimeRange[] = ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"];

interface StockPageProps {
  params: { ticker: string };
}

export default function StockPage({ params }: StockPageProps) {
  const ticker = params.ticker.toUpperCase();

  const [quote, setQuote] = useState<StockQuote | null>(null);
  const [dataPoints, setDataPoints] = useState<OHLCVDataPoint[]>([]);
  const [timeRange, setTimeRange] = useState<TimeRange>("1M");
  const [loading, setLoading] = useState(true);
  const [chartLoading, setChartLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [addedToWatchlist, setAddedToWatchlist] = useState(false);

  // Initial load: quote + history
  useEffect(() => {
    async function fetchAll() {
      setLoading(true);
      setError(null);
      try {
        const [quoteData, histData] = await Promise.all([
          stocksApi.getQuote(ticker),
          stocksApi.getHistorical(ticker, timeRange),
        ]);
        setQuote(quoteData);
        setDataPoints(histData.data_points);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load data");
      } finally {
        setLoading(false);
      }
    }
    fetchAll();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ticker]);

  // Time range switch: history only
  useEffect(() => {
    if (loading) return;
    async function fetchHistory() {
      setChartLoading(true);
      try {
        const histData = await stocksApi.getHistorical(ticker, timeRange);
        setDataPoints(histData.data_points);
      } catch {
        // keep existing data on error
      } finally {
        setChartLoading(false);
      }
    }
    fetchHistory();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeRange]);

  async function handleAddToWatchlist() {
    try {
      const watchlists = await watchlistApi.list();
      const first = watchlists[0];
      if (!first) {
        await watchlistApi.create("My Watchlist");
        const refreshed = await watchlistApi.list();
        await watchlistApi.addItem(refreshed[0]!.id, ticker);
      } else {
        await watchlistApi.addItem(first.id, ticker);
      }
      setAddedToWatchlist(true);
    } catch {
      // silently fail — user isn't logged in or ticker already exists
    }
  }

  if (loading) return <LoadingSkeleton ticker={ticker} />;

  if (error) {
    return (
      <main className="flex flex-1 flex-col items-center justify-center gap-4 p-8">
        <p className="text-sm text-red-500">{error}</p>
        <p className="text-sm text-muted-foreground">
          Unable to load data for <strong>{ticker}</strong>. Check the ticker symbol and try again.
        </p>
        <Link href="/dashboard" className="text-sm text-primary hover:underline">← Back to Dashboard</Link>
      </main>
    );
  }

  const isPositive = (quote?.change ?? 0) >= 0;

  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8 max-w-5xl">
      {/* Back */}
      <Link href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground transition-colors w-fit">
        ← Dashboard
      </Link>

      {/* Quote header */}
      {quote && (
        <div className="rounded-xl border border-border bg-card shadow-sm p-6 space-y-4">
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <div className="flex items-baseline gap-3">
                <h1 className="font-mono text-3xl font-bold">{ticker}</h1>
                <span className="text-muted-foreground text-sm">{quote.company_name}</span>
              </div>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="text-4xl font-semibold">{formatCurrency(quote.price)}</span>
                <span className={pnlColorClass(quote.change)}>
                  {pnlArrow(quote.change)} {formatCurrency(Math.abs(quote.change))} ({formatPercent(Math.abs(quote.change_percent))})
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Updated {formatRelativeTime(quote.timestamp)}
              </p>
            </div>
            <button
              onClick={handleAddToWatchlist}
              disabled={addedToWatchlist}
              className="shrink-0 rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors disabled:opacity-60"
            >
              {addedToWatchlist ? "✓ Added" : "+ Watchlist"}
            </button>
          </div>

          {/* Key stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2 border-t border-border">
            {[
              { label: "Volume", value: formatVolume(quote.volume) },
              { label: "High", value: formatCurrency(quote.week_52_high) },
              { label: "Low", value: formatCurrency(quote.week_52_low) },
              { label: "Market Cap", value: quote.market_cap ? formatCurrency(quote.market_cap) : "—" },
            ].map(({ label, value }) => (
              <div key={label}>
                <p className="text-xs text-muted-foreground">{label}</p>
                <p className="text-sm font-medium">{value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="rounded-xl border border-border bg-card shadow-sm p-4">
        {/* Time range selector */}
        <div className="flex gap-1 mb-4">
          {TIME_RANGES.map((r) => (
            <button
              key={r}
              onClick={() => setTimeRange(r)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                timeRange === r
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              {r}
            </button>
          ))}
        </div>

        {chartLoading ? (
          <div className="h-[400px] flex items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-muted border-t-foreground" />
          </div>
        ) : (
          <PriceChart data={dataPoints} isPositive={isPositive} />
        )}
      </div>

      {/* AI insights placeholder */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <h2 className="text-sm font-semibold mb-2">AI Trend Analysis</h2>
        <p className="text-sm text-muted-foreground">
          Claude-powered insights coming in Sprint 4.
        </p>
      </div>
    </main>
  );
}

function LoadingSkeleton({ ticker }: { ticker: string }) {
  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8 max-w-5xl">
      <div className="h-4 w-24 rounded bg-muted animate-pulse" />
      <div className="rounded-xl border border-border bg-card shadow-sm p-6 space-y-4">
        <div className="space-y-2">
          <div className="h-8 w-32 rounded bg-muted animate-pulse" />
          <div className="h-10 w-48 rounded bg-muted animate-pulse" />
        </div>
        <div className="grid grid-cols-4 gap-4 pt-2 border-t border-border">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-10 rounded bg-muted animate-pulse" />
          ))}
        </div>
      </div>
      <div className="rounded-xl border border-border bg-card shadow-sm p-4">
        <div className="h-[400px] rounded bg-muted animate-pulse" aria-label={`Loading chart for ${ticker}`} />
      </div>
    </main>
  );
}
