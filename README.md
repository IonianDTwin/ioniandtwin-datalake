# IonianDTwin

Digital Twin for the sustainable management of tourism and urban/environmental systems in the **Ionian Islands Region** (Περιφέρεια Ιονίων Νήσων, NUTS 2, Greece).

The system monitors, predicts, and balances the region's tourism and urban ecosystems across the three sustainability dimensions - economy, society-culture, and environment. It is built around a central Web Dashboard (spatial/analytics twin with an LLM natural-language interface) and a mobile app (real-time alerts and citizen field reports).

## What this repository contains

This is the shared, publication-ready subset of the IonianDTwin project: the indicator model, the data-source catalogue, the verification and transformation scripts, and the verified data produced so far.

| Area | Where | What |
|---|---|---|
| Indicators | `indicators/` | Data01-Data34 catalogue, metadata, derived formulas, composites, and the source-indicator map |
| Sources | `sources/` | source registry, verification matrix, and the **Data01-34 resource list** (`data-resources.md`) |
| Schemas | `schemas/` | indicator / source / observation JSON schemas |
| Data | `data/` | holistic data contract (`data/README.md`), per-indicator folders (`data/indicators/data01..34`), master roll-ups (`data/curated/`), and provenance manifests (`data/manifests/`) |
| Scripts | `scripts/verification/` | reproducible pullers, spatial joins, master dashboard builder, and per-indicator verifier |
| Docs | `docs/` | master progress report (`docs/data-preparation-progress.md`), requirements, architecture, and validation reports |

## Start here

1. **`docs/data-preparation-progress.md`** - the go-to tracker: current status of all Data01-Data34, JSON payload structure, a dated change history per indicator, and the "what's next" work queue.
2. **`data/README.md`** - the holistic data-handling contract: zero-duplication `data/raw/` lake, all-JSON edited rule, dual feature descriptions (`_meta.feature_dictionary` + `README.md`), and spatial rule (`D-014`).
3. **`data/indicators/data01-<slug>/` … `data34-<slug>/`** - per-indicator folders, each containing `raw-source-description.json` (raw source URL, `sha256`, raw schema, variable whitelist & conversion script), `refined-data.json` (project-ready JSON, feature dictionary & normalized observations), and `README.md`.
4. **`data/curated/observations-2026-10-20.json`** / `.csv` - the canonical master snapshot across all verified indicators.
5. **`sources/data-resources.md`** - one entry per Data01-Data34: online source link, access method, and ETL path.

## Data status

The current status of all 34 indicators, their dated change history, and the "what's next" work queue live in **`docs/data-preparation-progress.md`** (Section 1 = snapshot, Section 2 = per-indicator technical reference, Section 3 = work queue). The machine-readable twin is `indicators/source-indicator-map.json`; per-indicator detail is in `data/indicators/dataXX-<slug>/README.md` and `sources/data-resources.md`. No value is invented for an unverified indicator.

## Label convention

Substantive statements are marked with exactly one of: `REQUIREMENT`, `PROPOSAL`, `VERIFIED`, `ASSUMPTION`, `DECISION`, `RISK`, `BLOCKER`.

## Not included

Workstation-internal operational material - agent operating rules, operational logs, task tracking, and machine-specific paths - is intentionally excluded from this repository.
