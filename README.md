# IonianDTwin

Digital Twin for the sustainable management of tourism and urban/environmental systems in the **Ionian Islands Region** (Περιφέρεια Ιονίων Νήσων, NUTS 2, Greece).

The system monitors, predicts, and balances the region's tourism and urban ecosystems across the three sustainability dimensions — economy, society–culture, and environment. It is built around a central Web Dashboard (spatial/analytics twin with an LLM natural-language interface) and a mobile app (real-time alerts and citizen field reports).

## What this repository contains

This is the shared, publication-ready subset of the IonianDTwin project: the indicator model, the data-source catalogue, the pull/ETL procedures, and the verified data produced so far.

| Area | Where | What |
|---|---|---|
| Indicators | `indicators/` | Data01–Data34 catalogue, metadata, composites, and the source-indicator map |
| Sources | `sources/` | source registry, verification matrix, and the **Data01–34 resource list** |
| Procedures | `sources/pull-workflow/`, `sources/procedures/` | API pull playbooks and document download+extract procedures |
| Schemas | `schemas/` | indicator / source / observation JSON schemas |
| Data | `data/` | verified samples + reports, navigation index, normalized observations, provenance manifests |
| Docs | `docs/` | requirements, architecture, validation reports, research context |

## Start here

1. **`sources/data-resources.md`** — one entry per Data01–Data34: online source link, the Markdown procedure to follow, and the ETL path.
2. **`data/samples/INDEX.html`** (or `INDEX.md`) — all 34 indicators grouped by category, with verified values and links to each sample's report.
3. **`data/curated/observations-*.json`** / `.csv` — the normalized, schema-aligned verified data.
4. **`sources/pull-workflow/`** and **`sources/procedures/`** — how to reproduce the pulls and extractions.

## Data status (2026-09-22)

`VERIFIED` (live, read-only pull-tested):

- Eurostat tourism statistics, geo `EL62` (Ionia Nisia): nights, arrivals, bed-places — feeding Data16, Data26, Data27, Data31, Data32 (breakdown), Data33.
- Open-Meteo weather + UV (no-key substitute for the proposal's OpenWeatherMap/Meteo.gr) — feeding Data13, Data14.
- Copernicus Data Space catalogue (platform reachable; product download is token-gated).
- GSTC Destination Criteria v2.0 PDF (standards reference).

All other sources are `UNVERIFIED` (pending keys/registration) or internal/partner feeds — see `sources/source-verification-matrix.md`. No value is invented for an unverified indicator.

## Label convention

Substantive statements are marked with exactly one of: `REQUIREMENT`, `PROPOSAL`, `VERIFIED`, `ASSUMPTION`, `DECISION`, `RISK`, `BLOCKER`.

## Not included

Workstation-internal operational material — agent operating rules, session logs, task tracking, and machine-specific paths — is intentionally excluded from this public repository.
