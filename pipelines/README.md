# Pipelines

`DECISION` Data-quality rules and ingestion standards are defined in `quality-rules.md` and `data/README.md`. Per-indicator ingestion contracts, whitelisted raw variables, and feature dictionaries live inside `data/indicators/data01-<slug>/README.md` … `data34-<slug>/README.md`.

## Files

- `quality-rules.md` — data-quality checks (coverage, freshness, completeness, plausibility, spatial consistency `D-014`, cross-verification).
- `jobs/` — scheduled ingestion jobs (empty until production scheduling is enabled).
