# Data29 — Seasonality (%)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/eutd-tourism-dashboard-2024-indicators.csv [.csv]  ──( scripts/verification/extract-eutd-dashboard-csv.py )──>  refined-data.json [.json]
  data/samples/eurostat-tour_occ_nim-EL-2023.json [.json]  ──( scripts/verification/build_dashboard.py )──>  refined-data.json [.json]
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
- **Raw Input File Extension(s):** `.csv` + `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/extract-eutd-dashboard-csv.py & scripts/verification/build_dashboard.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `14`

## 1. Overview & Key Note

EL62 = 71.08 % peak-season share (2023) - from EU Tourism Dashboard TOUR_SOE_02. Flag: exact month window (Jun-Sep vs Jul-Aug) to confirm.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `EU_Tourism_Dashboard_2024` (European Commission / Joint Research Centre (JRC) — EU Tourism Dashboard)
- **Upstream URL:** `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv`
- **Access Method:** `GET (public CSV bulk export)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eutd-tourism-dashboard-2024-indicators.csv`
- **Raw File Extension & Format:** `.csv` — `text/csv (UTF-8, comma-delimited, 81,939 rows)`
- **SHA-256 Checksum:** `ab45bb4b2b0b831df183684a05adb52f5bca0270d3b90f1993af0bd77d35aa12` (verified in `data/manifests/source-verification-2026-10-03.json`)
- **Conversion Script (`.csv` -> `.json`):** `scripts/verification/extract-eutd-dashboard-csv.py`
- **Conversion Command:** `python3 scripts/verification/extract-eutd-dashboard-csv.py && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `code ('TOUR_SOE_02')`, `nuts_code_2021 ('EL62')`, `year (2023)`, `value`, `unit`
- **Dropped / Redacted Fields:** `pillar`, `component`, `non_EL62_rows`, `other_indicator_codes`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `pillar` | Dashboard sustainability pillar ('Green', 'Digital', 'Socio-economic', 'Basic descriptors') |
| `code` | Indicator code (filtered to 'TOUR_SOE_02') |
| `indicator` | Human-readable indicator title in the JRC export |
| `year` | Reference calendar year (filtered to 2023) |
| `nuts_code_2021` | Eurostat NUTS 2021 code (filtered to 'EL62' Ionian Islands) |
| `unit` | Unit of measure string |
| `value` | Numeric indicator value |

### Source 2: `Eurostat_tour_occ_nim` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&geo=EL&freq=M&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2023-01..2023-12`
- **Access Method:** `GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eurostat-tour_occ_nim-EL-2023.json`
- **Raw File Extension & Format:** `.json` — `application/json (SDMX 2.1 JSON-stat 2.0 cube)`
- **SHA-256 Checksum:** `e07a17f98f18f87f94e31d35993f34c9b44eda95c60632ce1c4e0b729955198b` (verified in `data/manifests/source-verification-2026-09-24.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_dashboard.py`
- **Conversion Command:** `python3 scripts/verification/build_dashboard.py --manifest data/manifests/source-verification-2026-09-24.json`
- **Whitelisted Raw Variables (`kept`):** `geo (EL)`, `freq (M)`, `c_resid (TOTAL)`, `unit (NR)`, `nace_r2 (I551-I553)`, `time (2023-01..2023-12)`, `value`
- **Dropped / Redacted Fields:** `PCH_SM`, `PCH_SM_2Y`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.geo` | 'EL' (Greece country-level monthly series) |
| `dimension.time` | Monthly timestamps '2023-01' through '2023-12' |
| `value` | Monthly overnight stays in Greece |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Regional NUTS2 EL62 peak-season share (71.08% in 2023) is extracted from EU Tourism Dashboard TOUR_SOE_02 via `scripts/verification/extract-eutd-dashboard-csv.py`. National monthly profile (Greece geo='EL', peak month Aug = 21.53% of annual nights) is computed from Eurostat tour_occ_nim via `scripts/verification/build_dashboard.py` (D-010).

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.el62_peak_season_share.value` | `number` | `%` | `target_indicator` | Share of annual EL62 tourism nights concentrated in the peak season (71.08% in 2023). |
| `refined_data.greece_monthly_series_2023` | `array` | `nights and %` | `target_indicator` | 12 monthly national observations plus derived peak-month share (21.53%). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-01` | `2023-01` | `country/EL` | **1591829** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-02` | `2023-02` | `country/EL` | **1603094** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-03` | `2023-03` | `country/EL` | **2450684** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-04` | `2023-04` | `country/EL` | **6491390** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-05` | `2023-05` | `country/EL` | **14349293** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-06` | `2023-06` | `country/EL` | **22554193** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-07` | `2023-07` | `country/EL` | **29461403** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-08` | `2023-08` | `country/EL` | **31687354** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-09` | `2023-09` | `country/EL` | **22215646** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-10` | `2023-10` | `country/EL` | **10467410** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-11` | `2023-11` | `country/EL` | **2201951** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:monthly nights:2023-12` | `2023-12` | `country/EL` | **2135574** | `nights` | `monthly` |
| `Eurostat_tour_occ_nim:Data29:seasonality_peak_share:2023` | `2023` | `country/EL` | **21.53** | `%` | `annual` |
| `EU_Tourism_Dashboard:Data29:peak_season_share:2023` | `2023` | `NUTS2/EL62` | **71.08** | `%` | `annual` |
