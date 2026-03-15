// ---------------------------------------------------------------------------
// User
// ---------------------------------------------------------------------------

export interface User {
  id: string;
  email: string;
  display_name: string;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  expires_in: number;
}

// ---------------------------------------------------------------------------
// Stock
// ---------------------------------------------------------------------------

export interface StockQuote {
  ticker: string;
  company_name: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  market_cap: number | null;
  pe_ratio: number | null;
  week_52_high: number;
  week_52_low: number;
  timestamp: string;
}

export interface StockSearchResult {
  ticker: string;
  company_name: string;
  exchange: string;
  asset_type: string;
}

export interface OHLCVDataPoint {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface StockHistoricalData {
  ticker: string;
  time_range: TimeRange;
  data_points: OHLCVDataPoint[];
}

export interface StockCompanyInfo {
  ticker: string;
  company_name: string;
  description: string;
  sector: string;
  industry: string;
  country: string;
  employees: number | null;
  website: string | null;
  logo_url: string | null;
}

export type TimeRange = "1D" | "1W" | "1M" | "3M" | "6M" | "1Y" | "5Y";

// ---------------------------------------------------------------------------
// Watchlist
// ---------------------------------------------------------------------------

export interface WatchlistItem {
  id: string;
  ticker: string;
  company_name: string;
  added_at: string;
  // Hydrated from quotes at request time
  price?: number;
  change_percent?: number;
}

export interface Watchlist {
  id: string;
  name: string;
  user_id: string;
  items: WatchlistItem[];
  created_at: string;
  updated_at: string;
}

// ---------------------------------------------------------------------------
// Portfolio
// ---------------------------------------------------------------------------

export interface Holding {
  id: string;
  portfolio_id: string;
  ticker: string;
  company_name: string;
  quantity: number;
  average_cost: number;
  // Computed fields hydrated at request time
  current_price?: number;
  current_value?: number;
  unrealized_pnl?: number;
  unrealized_pnl_percent?: number;
}

export interface Transaction {
  id: string;
  portfolio_id: string;
  ticker: string;
  transaction_type: "buy" | "sell";
  quantity: number;
  price: number;
  total_value: number;
  executed_at: string;
  notes: string | null;
}

export interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  holdings: Holding[];
  total_value: number;
  total_cost: number;
  total_pnl: number;
  total_pnl_percent: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioAllocationItem {
  ticker: string;
  company_name: string;
  value: number;
  allocation_percent: number;
}

// ---------------------------------------------------------------------------
// Insights (Claude API)
// ---------------------------------------------------------------------------

export type InsightSentiment = "bullish" | "bearish" | "neutral";

export interface TrendInsight {
  summary: string;
  sentiment: InsightSentiment;
  confidence: number;
  key_points: string[];
  generated_at: string;
  tokens_used: number;
}

export interface SuggestionInsight {
  suggestions: PortfolioSuggestion[];
  overall_assessment: string;
  generated_at: string;
  tokens_used: number;
  disclaimer: string;
}

export interface PortfolioSuggestion {
  type: "buy" | "sell" | "rebalance" | "watchlist_add";
  ticker: string;
  company_name: string;
  reasoning: string;
  confidence: number;
}

// ---------------------------------------------------------------------------
// Alerts
// ---------------------------------------------------------------------------

export type AlertCondition = "price_above" | "price_below" | "percent_change_up" | "percent_change_down";
export type AlertStatus = "active" | "triggered" | "disabled";

export interface Alert {
  id: string;
  user_id: string;
  ticker: string;
  condition: AlertCondition;
  threshold: number;
  status: AlertStatus;
  triggered_at: string | null;
  created_at: string;
}

// ---------------------------------------------------------------------------
// API response envelope
// ---------------------------------------------------------------------------

export interface ApiResponse<T> {
  data: T;
  error: string | null;
  meta: Record<string, unknown>;
}

export interface PaginatedApiResponse<T> {
  data: T[];
  error: string | null;
  meta: {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  };
}

// ---------------------------------------------------------------------------
// UI helpers
// ---------------------------------------------------------------------------

export type LoadingState = "idle" | "loading" | "success" | "error";
