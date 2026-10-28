# Data28 — Occupancy rate (%)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/eutd-tourism-dashboard-2024-indicators.csv [.csv]  ──( scripts/verification/extract-eutd-dashboard-csv.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `tourism_performance`
- **Refresh Cadence:** `annual`
- **Raw Input File Extension(s):** `.csv`
- **Primary Conversion / Builder Script:** `scripts/verification/extract-eutd-dashboard-csv.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `1`

## 1. Overview & Key Note

EL62 = 65.4 % net occupancy (2023) - from EU Tourism Dashboard TOUR_DES_04. Supersedes earlier gross nights/(beds*365) ~28-36 %.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `EU_Tourism_Dashboard_2024` (European Commission / Joint Research Centre (JRC) — EU Tourism Dashboard)
- **Upstream URL:** `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv`
- **Access Method:** `GET (public CSV bulk export)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eutd-tourism-dashboard-2024-indicators.csv`
- **Raw File Extension & Format:** `.csv` — `text/csv (UTF-8, comma-delimited, 81,939 rows)`
- **SHA-256 Checksum:** `ab45bb4b2b0b831df183684a05adb52f5bca0270d3b90f1993af0bd77d35aa12` (verified in `data/manifests/source-verification-2026-10-03.json`)
- **Conversion Script (`.csv` -> `.json`):** `scripts/verification/extract-eutd-dashboard-csv.py`
- **Conversion Command:** `python3 scripts/verification/extract-eutd-dashboard-csv.py && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `code ('TOUR_DES_04')`, `nuts_code_2021 ('EL62')`, `year (2023)`, `value`, `unit`
- **Dropped / Redacted Fields:** `pillar`, `component`, `non_EL62_rows`, `other_indicator_codes`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `pillar` | Dashboard sustainability pillar ('Green', 'Digital', 'Socio-economic', 'Basic descriptors') |
| `code` | Indicator code (filtered to 'TOUR_DES_04') |
| `indicator` | Human-readable indicator title in the JRC export |
| `year` | Reference calendar year (filtered to 2023) |
| `nuts_code_2021` | Eurostat NUTS 2021 code (filtered to 'EL62' Ionian Islands) |
| `unit` | Unit of measure string |
| `value` | Numeric indicator value |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Adopt EU Tourism Dashboard indicator TOUR_DES_04 ('Net occupancy rate of bed-places') for NUTS2 EL62 (65.4% in 2023) via `scripts/verification/extract-eutd-dashboard-csv.py`, superseding gross annual nights/(beds*365) estimates.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.net_occupancy_el62.value` | `number` | `%` | `target_indicator` | Net occupancy rate of bed-places in EL62 (65.4% in 2023). |
| `refined_data.gross_seasonal_island_proxy_2021_2025` | `object` | `%` | `internal_disaggregation` | Supplementary 180-day operating-season gross occupancy proxy across NUTS3 islands. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EU_Tourism_Dashboard:Data28:net_occupancy:2023` | `2023` | `NUTS2/EL62` | **65.4** | `%` | `annual` |
