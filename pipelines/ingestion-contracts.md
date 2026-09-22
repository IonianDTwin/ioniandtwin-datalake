# Ingestion Contracts

`PROPOSAL` Per-source contracts to be completed only after a source is `VERIFIED`.

## Contract template

- `source_id` — references `sources/source-registry.md`.
- `endpoint` / `request` — exact method, params, headers.
- `schedule` — ~30-minute cron for asynchronous sources; real-time for mobile reports.
- `auth` — credential reference only (real values in `.env`).
- `response_shape` — observed schema notes.
- `idempotency` — deduplication key.
- `retention` — raw immutability and manifest policy.
- `failure_mode` — recorded as access constraint, never as "source absent".

## Priority contracts (first vertical slice)

1. Weather/UV (OpenWeatherMap / Meteo.gr).
2. EU Tourism Dashboard (official tourism statistics).
3. Copernicus CAMS / CMEMS (environmental).

## Status

`BLOCKER` No contract finalised until pull tests pass (see `sources/source-verification-matrix.md`).
