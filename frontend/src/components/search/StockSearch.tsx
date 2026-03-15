"use client";

import { useEffect, useRef, useState } from "react";
import { stocksApi } from "@/lib/api-client";
import type { StockSearchResult } from "@/types";
import { cn } from "@/lib/utils";

interface StockSearchProps {
  onSelect: (ticker: string) => void;
  placeholder?: string;
  className?: string;
}

export default function StockSearch({ onSelect, placeholder = "Search stocks…", className }: StockSearchProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<StockSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [open, setOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);

  const containerRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Debounced search
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (query.length === 0) {
      setResults([]);
      setOpen(false);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      setError(false);
      try {
        const data = await stocksApi.search(query);
        setResults(data);
        setOpen(true);
        setHighlightedIndex(-1);
      } catch {
        setError(true);
        setResults([]);
        setOpen(true);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query]);

  // Close on outside click
  useEffect(() => {
    function handleMouseDown(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleMouseDown);
    return () => document.removeEventListener("mousedown", handleMouseDown);
  }, []);

  function handleSelect(ticker: string) {
    setQuery("");
    setOpen(false);
    setResults([]);
    onSelect(ticker);
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (!open) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightedIndex((i) => Math.min(i + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && highlightedIndex >= 0) {
      e.preventDefault();
      const result = results[highlightedIndex];
      if (result) handleSelect(result.ticker);
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  }

  const activeDescendant = highlightedIndex >= 0 ? `search-result-${highlightedIndex}` : undefined;

  return (
    <div ref={containerRef} className={cn("relative w-full", className)}>
      <div className="relative">
        <input
          type="text"
          role="combobox"
          aria-label="Search for a stock"
          aria-expanded={open}
          aria-autocomplete="list"
          aria-controls="search-listbox"
          aria-activedescendant={activeDescendant}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => query.length > 0 && setOpen(true)}
          placeholder={placeholder}
          className="w-full rounded-lg border border-input bg-background px-4 py-2 pr-10 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-ring"
        />
        {loading && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2" aria-hidden="true">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-muted border-t-foreground" />
          </div>
        )}
      </div>

      {open && (
        <ul
          id="search-listbox"
          role="listbox"
          aria-label="Stock search results"
          className="absolute z-50 mt-1 w-full max-h-80 overflow-y-auto rounded-lg border border-border bg-background shadow-lg"
        >
          {error ? (
            <li className="px-4 py-3 text-sm text-muted-foreground">Search unavailable</li>
          ) : results.length === 0 && !loading ? (
            <li className="px-4 py-3 text-sm text-muted-foreground">
              No results for &ldquo;{query}&rdquo;
            </li>
          ) : (
            results.map((result, i) => (
              <li
                key={result.ticker}
                id={`search-result-${i}`}
                role="option"
                aria-selected={i === highlightedIndex}
                onClick={() => handleSelect(result.ticker)}
                onMouseEnter={() => setHighlightedIndex(i)}
                className={cn(
                  "flex cursor-pointer items-center gap-3 px-4 py-3 border-b border-border last:border-0",
                  i === highlightedIndex ? "bg-blue-50 dark:bg-blue-950" : "hover:bg-muted/50"
                )}
              >
                <span className="font-mono text-sm font-semibold w-16 shrink-0">{result.ticker}</span>
                <span className="truncate text-sm text-muted-foreground flex-1">{result.company_name}</span>
                <span className="shrink-0 rounded bg-muted px-1.5 py-0.5 text-xs text-muted-foreground">{result.exchange}</span>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
