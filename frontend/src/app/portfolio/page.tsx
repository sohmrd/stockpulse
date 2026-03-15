import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Portfolio",
  description: "Track your holdings, view unrealized P&L, and get AI-powered rebalancing suggestions.",
};

/**
 * Portfolio page — stub.
 *
 * Sprint 3 deliverables:
 * - Portfolio summary (total value, cost basis, P&L)
 * - Allocation pie chart (Recharts)
 * - Holdings table with sorting and filtering
 * - Add holding dialog (React Hook Form + Zod)
 * - Transaction history
 *
 * Sprint 4 deliverables:
 * - AI rebalancing suggestions panel
 */
export default function PortfolioPage() {
  return (
    <main className="flex flex-1 flex-col gap-6 p-4 md:p-6 lg:p-8">
      <div className="flex items-center justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight">Portfolio</h1>
          <p className="text-sm text-muted-foreground">
            Your holdings, performance, and allocation.
          </p>
        </div>

        <button
          type="button"
          disabled
          className="inline-flex h-9 items-center justify-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground shadow transition-colors disabled:pointer-events-none disabled:opacity-50"
        >
          Add holding
        </button>
      </div>

      {/* Summary cards placeholder */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {["Total Value", "Cost Basis", "Unrealized P&L", "P&L %"].map((label) => (
          <div
            key={label}
            className="rounded-lg border border-border bg-card p-4 shadow-sm space-y-2"
            aria-label={`${label} summary`}
          >
            <p className="text-sm font-medium text-muted-foreground">{label}</p>
            <div className="h-6 w-24 rounded bg-muted animate-pulse" aria-hidden="true" />
          </div>
        ))}
      </div>

      {/* Holdings table placeholder */}
      <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
        <p className="text-sm text-muted-foreground text-center py-8">
          Portfolio components coming in Sprint 3.
        </p>
      </div>
    </main>
  );
}
