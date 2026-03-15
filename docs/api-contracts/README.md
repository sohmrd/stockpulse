# API Contracts

This directory is the **source of truth** for all API contracts between the StockPulse frontend and backend. Every endpoint that the frontend consumes must have a contract file here before implementation begins.

## Why Contracts First

Defining contracts before writing code means:
- Frontend and backend can be developed in parallel against the same specification.
- Disagreements about field names, types, or HTTP semantics are resolved at design time, not integration time.
- Breaking changes are visible in PR diffs.

## File Naming

```
<resource>.yaml
```

Examples:
- `auth.yaml`
- `stocks.yaml`
- `portfolio.yaml`
- `watchlist.yaml`
- `insights.yaml`
- `alerts.yaml`

## Contract Format

Each contract file documents one or more related endpoints. Use the following YAML structure:

```yaml
# docs/api-contracts/<resource>.yaml

<HTTP_METHOD> /api/v1/<resource>/<action>:
  description: >
    Plain-English description of what this endpoint does.
  auth: required (Bearer JWT) | none
  rate_limit: <N> requests per minute per user (omit if not rate-limited)

  request:
    path_params:
      <name>: <type> (<constraints>)
    query_params:
      <name>: <type> (<constraints>, default: <value>)
    body:
      <field>: <type> (<constraints>, default: <value>)

  response:
    200:
      data:
        <field>: <type>   # description
      meta:
        <field>: <type>
    400:
      error: "<message describing the validation failure>"
    401:
      error: "Authentication required."
    403:
      error: "You do not have permission to access this resource."
    404:
      error: "<resource> not found."
    422:
      error: "<field>: <validation message>"
    429:
      error: "Rate limit exceeded. Try again in {retry_after} seconds."
    500:
      error: "An unexpected error occurred. Please try again."
```

## Response Envelope

All endpoints return a consistent JSON envelope:

```json
{
  "data": <payload or null>,
  "error": <string or null>,
  "meta": <object or null>
}
```

- `data` is non-null on success, null on error.
- `error` is non-null on failure, null on success.
- `meta` carries pagination, model info, or latency data when applicable.

## Field Naming

All field names use `snake_case` (Python / FastAPI convention). The frontend API client is responsible for any `camelCase` conversion if needed — but adopting `snake_case` throughout is preferred to avoid a transformation layer.

## Versioning

Contracts are versioned alongside the codebase. When a breaking change is required:

1. Create a new contract file (e.g., `insights.v2.yaml`).
2. Update the endpoint prefix to `/api/v2/...`.
3. Document the migration path in the contract file header.
4. Add an entry to `docs/decision-log.md`.

Non-breaking additions (new optional fields, new endpoints) do not require a version bump but must be reflected in the existing contract file.

## Amending a Contract

All contract amendments require TPM approval. To amend:

1. Open a PR with the modified contract YAML.
2. Tag the PR with `contract-change`.
3. The TPM reviews and approves before any implementation begins.

## Status

| Contract File | Status | Last Updated |
|---|---|---|
| `auth.yaml` | Pending | — |
| `stocks.yaml` | Pending | — |
| `portfolio.yaml` | Pending | — |
| `watchlist.yaml` | Pending | — |
| `insights.yaml` | Pending | — |
| `alerts.yaml` | Pending | — |
