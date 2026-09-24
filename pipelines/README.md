# Pipelines

`DECISION` Ingestion and processing are defined as **contracts and rules**, not code (D-002: no production pipeline yet). Two contracts are finalised (Eurostat tourism, EEA bathing water).

## Subdirectories

- `jobs/` — scheduled ingestion jobs (empty until implementation).
- `ingestion-contracts.md` — per-source ingestion contracts (Eurostat + EEA finalised).
- `quality-rules.md` — data-quality checks (defined).

## Status

`DECISION` Contracts and quality rules are defined; implementation is deferred until the remaining credential-gated sources are verified and the first vertical slice is signed off.
