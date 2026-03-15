"use client";

import { useRouter } from "next/navigation";
import { StockSearch } from "@/components/search";
import { WatchlistPanel } from "@/components/watchlist";

export default function DashboardPage() {
  const router = useRouter();

  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8">
      {/* Page header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Search for stocks, manage your watchlists, and track your portfolio.
        </p>
      </div>

      {/* Search — prominent at top of page body too */}
      <div className="max-w-xl">
        <StockSearch
          onSelect={(ticker) => router.push(`/stock/${ticker}`)}
          placeholder="Search stocks by name or ticker…"
        />
      </div>

      {/* Summary stat cards (portfolio data in Sprint 3) */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {["Total Value", "Today's P&L", "All-Time P&L"].map((label) => (
          <div
            key={label}
            className="rounded-xl border border-border bg-card p-4 shadow-sm space-y-2"
            aria-label={`${label} card`}
          >
            <p className="text-sm font-medium text-muted-foreground">{label}</p>
            <div className="h-6 w-24 rounded bg-muted animate-pulse" aria-hidden="true" />
          </div>
        ))}
      </div>

      {/* Main content grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Watchlists */}
        <WatchlistPanel />

        {/* Portfolio summary placeholder */}
        <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
          <h2 className="font-semibold text-sm mb-3">Portfolio</h2>
          <p className="text-sm text-muted-foreground text-center py-8">
            Portfolio tracking coming in Sprint 3.
          </p>
        </div>
      </div>
    </main>
  );
}
