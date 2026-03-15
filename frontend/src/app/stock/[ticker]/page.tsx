import type { Metadata } from "next";

interface StockPageProps {
  params: {
    ticker: string;
  };
}

/**
 * Generate per-ticker metadata for SEO.
 * In Sprint 2 this will fetch real company names from the backend.
 */
export function generateMetadata({ params }: StockPageProps): Metadata {
  const ticker = params.ticker.toUpperCase();
  return {
    title: ticker,
    description: `Live price, chart, and AI-powered trend analysis for ${ticker}.`,
  };
}

/**
 * Stock detail page — stub.
 *
 * Sprint 2 deliverables:
 * - StockHeader (ticker, company name, price, change)
 * - Interactive OHLCV chart with time range selector (Lightweight Charts)
 * - Company info panel (sector, description, key stats)
 * - Add to watchlist button
 *
 * Sprint 4 deliverables:
 * - Claude trend analysis panel (streaming SSE)
 */
export default function StockPage({ params }: StockPageProps) {
  const ticker = params.ticker.toUpperCase();

  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight">{ticker}</h1>
          <p className="text-sm text-muted-foreground">Stock detail</p>
        </div>
      </div>

      {/* Chart placeholder — replaced by Lightweight Charts in Sprint 2 */}
      <div
        className="rounded-lg border border-border bg-card shadow-sm"
        role="img"
        aria-label={`Price chart for ${ticker} — loading`}
      >
        <div className="flex h-64 items-center justify-center">
          <p className="text-sm text-muted-foreground">
            Chart for <strong>{ticker}</strong> coming in Sprint 2.
          </p>
        </div>
      </div>

      {/* AI insights placeholder — replaced in Sprint 4 */}
      <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
        <h2 className="text-sm font-semibold mb-2">AI Trend Analysis</h2>
        <p className="text-sm text-muted-foreground">
          Claude-powered insights coming in Sprint 4.
        </p>
      </div>
    </main>
  );
}
