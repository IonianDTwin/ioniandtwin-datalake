# IonianDTwin

Digital Twin for the sustainable management of tourism and urban/environmental systems in the **Ionian Islands Region** (Περιφέρεια Ιονίων Νήσων, NUTS 2, Greece).

The system monitors, predicts, and balances the region's tourism and urban ecosystems across the three sustainability dimensions - economy, society-culture, and environment. It is built around a central Web Dashboard (spatial/analytics twin with an LLM natural-language interface) and a mobile app (real-time alerts and citizen field reports).

## What this repository contains

This is the shared, publication-ready subset of the IonianDTwin project: the indicator model, the data-source catalogue, the pull/ETL procedures, and the verified data produced so far.

| Area | Where | What |
|---|---|---|
| Indicators | `indicators/` | Data01-Data34 catalogue, metadata, composites, and the source-indicator map |
| Sources | `sources/` | source registry, verification matrix, and the **Data01-34 resource list** |
| Procedures | `sources/pull-workflow/`, `sources/procedures/` | API pull playbooks and document download+extract procedures |
| Schemas | `schemas/` | indicator / source / observation JSON schemas |
| Data | `data/` | verified samples + reports, navigation index, normalized observations, provenance manifests |
| Docs | `docs/` | requirements, architecture, validation reports, research context |

## Start here

1. **`docs/data-preparation-progress.md`** - the go-to tracker: current status of all Data01-Data34, a dated change history per indicator, and the "what's next" work queue.
2. **`sources/data-resources.md`** - one entry per Data01-Data34: online source link, the Markdown procedure to follow, and the ETL path.
3. **`data/samples/INDEX.html`** (or `INDEX.md`) - all 34 indicators grouped by category, with verified values and links to each sample's report.
4. **`data/curated/observations-*.json`** / `.csv` - the normalized, schema-aligned verified data.
5. **`sources/pull-workflow/`** and **`sources/procedures/`** - how to reproduce the pulls and extractions.

## Data status

The current status of all 34 indicators, their dated change history, and the "what's next" work queue live in **`docs/data-preparation-progress.md`** (Section 1 = snapshot, Section 2 = per-indicator history, Section 3 = work queue). The machine-readable twin is `indicators/source-indicator-map.json`; per-indicator detail is `sources/data-resources.md`. No value is invented for an unverified indicator.

## Label convention

Substantive statements are marked with exactly one of: `REQUIREMENT`, `PROPOSAL`, `VERIFIED`, `ASSUMPTION`, `DECISION`, `RISK`, `BLOCKER`.

## Not included

Workstation-internal operational material - agent operating rules, operational logs, task tracking, and machine-specific paths - is intentionally excluded from this repository.
