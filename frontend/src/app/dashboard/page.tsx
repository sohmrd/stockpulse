import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Dashboard",
  description: "Your StockPulse dashboard — portfolio overview, watchlist, and market summary.",
};

/**
 * Dashboard page — stub.
 *
 * Sprint 3 deliverables:
 * - Portfolio summary card (total value, P&L, allocation chart)
 * - Watchlist table with live price tickers
 * - Market overview (indices, movers)
 * - AI suggestions panel
 */
export default function DashboardPage() {
  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Your portfolio overview and market summary.
        </p>
      </div>

      {/* Placeholder grid — replaced by real components in Sprint 3 */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {["Total Value", "Today's P&L", "All-Time P&L"].map((label) => (
          <div
            key={label}
            className="rounded-lg border border-border bg-card p-4 shadow-sm space-y-2"
            aria-label={`${label} card`}
          >
            <p className="text-sm font-medium text-muted-foreground">{label}</p>
            <div className="h-6 w-24 rounded bg-muted animate-pulse" aria-hidden="true" />
          </div>
        ))}
      </div>

      <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
        <p className="text-sm text-muted-foreground text-center py-8">
          Dashboard content coming in Sprint 3.
        </p>
      </div>
    </main>
  );
}
