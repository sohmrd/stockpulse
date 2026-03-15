"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { watchlistApi } from "@/lib/api-client";
import { isAuthenticated } from "@/lib/auth";
import type { Watchlist, WatchlistItem } from "@/types";
import { cn, formatCurrency, formatPercent, pnlColorClass, pnlArrow } from "@/lib/utils";

// ---------------------------------------------------------------------------
// WatchlistRow
// ---------------------------------------------------------------------------

interface WatchlistRowProps {
  item: WatchlistItem;
  onRemove: (itemId: string) => void;
  onNavigate: (ticker: string) => void;
}

function WatchlistRow({ item, onRemove, onNavigate }: WatchlistRowProps) {
  return (
    <div
      className="flex cursor-pointer items-center gap-3 border-b border-border py-3 last:border-0 hover:bg-muted/40 px-2 rounded"
      onClick={() => onNavigate(item.ticker)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && onNavigate(item.ticker)}
      aria-label={`View ${item.ticker}`}
    >
      <span className="font-mono text-sm font-semibold w-16 shrink-0">{item.ticker}</span>
      <span className="flex-1 truncate text-sm text-muted-foreground">{item.company_name || "—"}</span>

      {item.price != null ? (
        <span className="shrink-0 text-sm font-medium">{formatCurrency(item.price)}</span>
      ) : (
        <span className="shrink-0 text-sm text-muted-foreground">—</span>
      )}

      {item.change_percent != null ? (
        <span className={cn("shrink-0 text-xs w-16 text-right", pnlColorClass(item.change_percent))}>
          {pnlArrow(item.change_percent)} {formatPercent(item.change_percent)}
        </span>
      ) : (
        <span className="shrink-0 w-16" />
      )}

      <button
        onClick={(e) => { e.stopPropagation(); onRemove(item.id); }}
        className="shrink-0 text-muted-foreground hover:text-red-500 transition-colors text-lg leading-none"
        aria-label={`Remove ${item.ticker} from watchlist`}
      >
        ×
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// AddTickerForm
// ---------------------------------------------------------------------------

interface AddTickerFormProps {
  onAdd: (ticker: string) => Promise<void>;
  onCancel: () => void;
}

function AddTickerForm({ onAdd, onCancel }: AddTickerFormProps) {
  const [value, setValue] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const ticker = value.trim().toUpperCase();
    if (!/^[A-Z]{1,5}$/.test(ticker)) {
      setError("Enter a valid ticker (1–5 letters)");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await onAdd(ticker);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to add ticker");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 mt-2">
      <input
        autoFocus
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value.toUpperCase())}
        placeholder="AAPL"
        maxLength={5}
        className="w-24 rounded border border-input bg-background px-2 py-1 text-sm font-mono uppercase focus:outline-none focus:ring-2 focus:ring-ring"
        aria-label="Ticker symbol"
      />
      <button
        type="submit"
        disabled={loading}
        className="rounded bg-primary px-2 py-1 text-xs font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
      >
        {loading ? "…" : "Add"}
      </button>
      <button type="button" onClick={onCancel} className="text-xs text-muted-foreground hover:text-foreground">
        Cancel
      </button>
      {error && <span className="text-xs text-red-500">{error}</span>}
    </form>
  );
}

// ---------------------------------------------------------------------------
// WatchlistCard
// ---------------------------------------------------------------------------

interface WatchlistCardProps {
  watchlist: Watchlist;
  onRefresh: () => void;
}

function WatchlistCard({ watchlist, onRefresh }: WatchlistCardProps) {
  const router = useRouter();
  const [showAddForm, setShowAddForm] = useState(false);

  async function handleAdd(ticker: string) {
    await watchlistApi.addItem(watchlist.id, ticker);
    setShowAddForm(false);
    onRefresh();
  }

  async function handleRemove(itemId: string) {
    await watchlistApi.removeItem(watchlist.id, itemId);
    onRefresh();
  }

  return (
    <div className="rounded-xl border border-border bg-card shadow-sm p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="font-semibold text-sm">{watchlist.name}</h3>
          <p className="text-xs text-muted-foreground">{watchlist.items.length} stocks</p>
        </div>
        <button
          onClick={() => setShowAddForm((v) => !v)}
          className="rounded-full w-7 h-7 flex items-center justify-center border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition-colors text-lg leading-none"
          aria-label="Add stock to watchlist"
        >
          +
        </button>
      </div>

      {showAddForm && (
        <AddTickerForm onAdd={handleAdd} onCancel={() => setShowAddForm(false)} />
      )}

      {/* Items */}
      {watchlist.items.length === 0 ? (
        <p className="text-sm text-muted-foreground py-4 text-center">
          No stocks yet. Use + to add some.
        </p>
      ) : (
        <div>
          {watchlist.items.map((item) => (
            <WatchlistRow
              key={item.id}
              item={item}
              onRemove={handleRemove}
              onNavigate={(ticker) => router.push(`/stock/${ticker}`)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// WatchlistPanel (top-level export)
// ---------------------------------------------------------------------------

export default function WatchlistPanel() {
  const [watchlists, setWatchlists] = useState<Watchlist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchWatchlists() {
    if (!isAuthenticated()) {
      setLoading(false);
      return;
    }
    try {
      const data = await watchlistApi.list();
      setWatchlists(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load watchlists");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchWatchlists(); }, []);

  async function handleCreateWatchlist() {
    const name = window.prompt("Watchlist name:");
    if (!name?.trim()) return;
    try {
      await watchlistApi.create(name.trim());
      fetchWatchlists();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to create watchlist");
    }
  }

  if (!isAuthenticated()) {
    return (
      <div className="rounded-xl border border-border bg-card p-6 text-center">
        <p className="text-sm text-muted-foreground">Sign in to see your watchlist</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="rounded-xl border border-border bg-card p-4 space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-10 rounded bg-muted animate-pulse" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-border bg-card p-4">
        <p className="text-sm text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-base">Watchlists</h2>
        <button
          onClick={handleCreateWatchlist}
          className="text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          + New watchlist
        </button>
      </div>

      {watchlists.length === 0 ? (
        <div className="rounded-xl border border-border bg-card p-6 text-center">
          <p className="text-sm text-muted-foreground">No watchlists yet.</p>
          <button
            onClick={handleCreateWatchlist}
            className="mt-2 text-sm text-primary hover:underline"
          >
            Create your first watchlist
          </button>
        </div>
      ) : (
        watchlists.map((w) => (
          <WatchlistCard key={w.id} watchlist={w} onRefresh={fetchWatchlists} />
        ))
      )}
    </div>
  );
}
