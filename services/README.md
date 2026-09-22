# Services

`DECISION` Planned service modules. All are deferred until source access, data contracts, legal constraints, security, and data-quality checks are verified (per the project's priority order).

## Modules (currently `.gitkeep` placeholders)

- `api/` — dashboard-ready data/API responses.
- `ingestion/` — scheduled and event-driven source ingestion.
- `analytics/` — indicator computation and statistics.
- `forecasting/` — ML forecasts (deferred).
- `alerts/` — alerting (deferred; unverified data must not trigger alerts).
- `rag/` — vector/LLM retrieval (deferred).

## Why empty

`DECISION` The project forbids production-scale work before source access and contracts are verified. Creating the modules now would be placeholder code without a verified data contract.

## When to fill

Start with `api/` and `ingestion/` after the first verified source and data contract are produced.
