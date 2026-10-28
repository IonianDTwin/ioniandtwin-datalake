# Sources — Index

`DECISION` This directory records every candidate data source, its verification state, and the Data01–Data34 resource mapping. Per-indicator raw variable whitelists, transformation rules, and JSON feature dictionaries live in `data/indicators/data01-<slug>/` … `data34-<slug>/`.

## Read order

1. `data-resources.md` — **Data01–Data34 resource list**: online link, access method, and ETL script per indicator.
2. `source-registry.md` — the reconciled source inventory (proposal + deployed app + verified free substitutes).
3. `source-verification-matrix.md` — one row per source with live verification status and manifest links.

## Evidence & Provenance

All pull checksums, HTTP statuses, and timestamps are recorded in `data/manifests/source-verification-*.json` and cross-referenced in `docs/data-preparation-progress.md`.
