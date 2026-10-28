# Data22 — Tourist diversity (zones)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/eurostat-tour_occ_nin3-EL621-624-2021-2025.json [.json]  ──( scripts/verification/build_dashboard.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `spatial_sustainability`
- **Refresh Cadence:** `annual`
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/build_dashboard.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `6`

## 1. Overview & Key Note

Spatial 1-HHI of NUTS3 island night shares (0.636-0.640). Flag: dashboard TOUR_SOE_04 "Tourism diversity" reads 0 for EL62 (different concept / possible Greece gap).

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Eurostat_tour_occ_nin3` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin3?format=JSON&geo=EL621..EL624&c_resid=TOTAL&unit=NR&nace_r2=I551-I553`
- **Access Method:** `GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eurostat-tour_occ_nin3-EL621-624-2021-2025.json`
- **Raw File Extension & Format:** `.json` — `application/json (wrapper of 4 NUTS3 SDMX cubes)`
- **SHA-256 Checksum:** `ee9c29ff4ecce9aabc23b1b9b360096c004213ed6e2a6b30c257f0934517e916` (verified in `data/manifests/source-verification-2026-10-01.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_dashboard.py`
- **Conversion Command:** `python3 scripts/verification/build_dashboard.py --manifest data/manifests/source-verification-2026-10-01.json`
- **Whitelisted Raw Variables (`kept`):** `geo (EL621, EL622, EL623, EL624)`, `c_resid (TOTAL)`, `unit (NR)`, `nace_r2 (I551-I553)`, `time (2021..2025)`, `value`
- **Dropped / Redacted Fields:** `foreign_vs_domestic_split`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `EL621..EL624` | Top-level keys for Zakynthos (EL621), Kerkyra (EL622), Ithaki/Kefallinia (EL623), Lefkada (EL624) |
| `dimension.time` | Reference years ('2021'..'2025') |
| `value` | Annual overnight stays per NUTS3 island unit |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** D-014 & D-016: Compute NUTS3 island shares s_i = nights_i / sum(nights) across the 4 Ionian NUTS3 units (EL621 Zakynthos, EL622 Kerkyra, EL623 Ithaki/Kefallinia, EL624 Lefkada) via `scripts/verification/build_dashboard.py`, then aggregate to a single NUTS2 EL62 diversity index: Diversity = 1 - sum(s_i^2) (1 - Herfindahl-Hirschman Index).

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.data22_tourist_diversity.<year>.nights` | `object` | `nights` | `input_variable` | Total annual overnight stays per NUTS3 island unit. |
| `refined_data.data22_tourist_diversity.<year>.shares` | `object` | `ratio (0-1)` | `input_variable` | Fraction of EL62 regional nights hosted by each NUTS3 unit. |
| `refined_data.data22_tourist_diversity.<year>.HHI` | `number` | `index (0-1)` | `input_variable` | Herfindahl-Hirschman concentration index sum(s_i^2). |
| `refined_data.data22_tourist_diversity.<year>.diversity_1_minus_HHI` | `number` | `index (0-1)` | `target_indicator` | Regional spatial diversity index 1 - HHI emitted for NUTS2/EL62 (0.631 to 0.651). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:2020` | `2020` | `NUTS2/EL62` | **0.663** | `index` | `annual` |
| `Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:2021` | `2021` | `NUTS2/EL62` | **0.636** | `index` | `annual` |
| `Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:2022` | `2022` | `NUTS2/EL62` | **0.651** | `index` | `annual` |
| `Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:2023` | `2023` | `NUTS2/EL62` | **0.632** | `index` | `annual` |
| `Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:2024` | `2024` | `NUTS2/EL62` | **0.631** | `index` | `annual` |
| `Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:2025` | `2025` | `NUTS2/EL62` | **0.64** | `index` | `annual` |
