# Prompts CHANGELOG

All notable changes to Claude prompt templates are documented here. Every change — no matter how small — must be logged with a rationale. Prompt changes can significantly affect output quality, cost, and compliance, so this log is treated as a critical audit trail.

## Format

```
## [version] — [YYYY-MM-DD] — [prompt-name]

### Changed
- What was modified and why

### Impact
- Expected effect on outputs (quality, length, token usage, structure)

### Tested by
- Who reviewed the outputs before promoting this version to production
```

---

## [1.0.0] — 2026-03-15 — trend-explainer

### Added
- Initial version of the trend explainer system prompt.
- Defines the full output JSON schema for `TrendInsight`: `summary`, `sentiment`, `confidence`, `key_points`, `support_level`, `resistance_level`, `volume_signal`, `disclaimer`.
- Specifies exactly 5 analysis dimensions: trend direction, volume, key price levels, volatility, and news events.
- Mandates the financial disclaimer text verbatim in every response.
- Sets guardrails: no future price targets, no buy/sell recommendations, minimum 2 and maximum 6 key points.

### Impact
- Expected response length: 200-400 tokens for `summary` + `key_points` combined.
- Confidence scores calibrated to 0.0-1.0; strong trends expected at 0.75+.
- Responses must be valid JSON — no prose wrapping.

### Tested by
- TPM (initial review of few-shot examples in `few-shot/trend-examples.json`)

---

## [1.0.0] — 2026-03-15 — suggestion-engine

### Added
- Initial version of the portfolio suggestion engine system prompt.
- Defines the full output JSON schema: `overall_assessment`, `risk_flags`, `rebalancing_suggestions`, `watchlist_additions`, `disclaimer`.
- Implements risk-profile-aware analysis with distinct guidance for `conservative`, `moderate`, `aggressive`, and `unspecified` profiles.
- Concentration risk threshold: 25% (20% for conservative profiles).
- Sector overweight threshold: 40%.
- Watchlist suggestions capped at 3 per response.
- Mandates the financial disclaimer text verbatim; disclaimer is longer than in trend-explainer to include "past performance" language.
- Guardrails: no specific share counts, no price targets, no derivative products.

### Impact
- Expected response length: 400-700 tokens depending on portfolio size.
- `risk_flags` array will be empty for well-diversified portfolios.
- `rebalancing_suggestions` may recommend trim, consider_adding, or monitor actions only.

### Tested by
- TPM (initial review of few-shot examples in `few-shot/suggestion-examples.json`)

---
