# Data26 — Arrivals & overnight stays

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json [.json]  ──( scripts/verification/build_dashboard.py (via render_pull_reports.decode) )──>  refined-data.json [.json]
  data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json [.json]  ──( scripts/verification/build_dashboard.py )──>  refined-data.json [.json]
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
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/build_dashboard.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `4`

## 1. Overview & Key Note

—

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Eurostat_tour_occ_nin2` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023`
- **Access Method:** `GET (SDMX 2.1 / JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
- **Raw File Extension & Format:** `.json` — `application/json (SDMX 2.1 JSON-stat 2.0 cube)`
- **SHA-256 Checksum:** `46821a04c9061b605a1e324f9af55e87dba73856fd190dcb7e78ae8bc75f860d` (verified in `data/manifests/source-verification-2026-09-22.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_dashboard.py (via render_pull_reports.decode)`
- **Conversion Command:** `bash scripts/verification/pull-eurostat-tourism.sh && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `dimension.c_resid`, `dimension.unit`, `dimension.nace_r2`, `dimension.geo (EL62)`, `dimension.time`, `value`
- **Dropped / Redacted Fields:** `status_flags`, `PCH_PRE (year-on-year % change unit)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `id` | Ordered array of cube dimensions: ['freq', 'c_resid', 'unit', 'nace_r2', 'geo', 'time'] |
| `size` | Array of dimension cardinalities used for flat-index decoding |
| `dimension.c_resid` | Country of residence ('TOTAL', 'DOM', 'FOR') |
| `dimension.unit` | Unit ('NR' nights, 'P_THAB' nights/1000 residents, 'P_KM2' nights/km2, 'PC_TOT' % share) |
| `dimension.nace_r2` | Accommodation NACE Rev. 2 activity ('I551-I553' total, 'I551' hotels, 'I552' short-stay, 'I553' camping) |
| `dimension.geo` | NUTS2 code ('EL62' = Ionia Nisia) |
| `dimension.time` | Reference year ('2022', '2023') |
| `value` | Sparse map {flat_index_string: numeric_value} |

### Source 2: `Eurostat_tour_occ_arn2` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023`
- **Access Method:** `GET (SDMX 2.1 / JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json`
- **Raw File Extension & Format:** `.json` — `application/json (SDMX 2.1 JSON-stat 2.0 cube)`
- **SHA-256 Checksum:** `0855dc90f5b85a3f4251318da56456cec0585fe55843caf434f26c499f72b724` (verified in `data/manifests/source-verification-2026-09-22.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_dashboard.py`
- **Conversion Command:** `bash scripts/verification/pull-eurostat-tourism.sh && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `dimension.c_resid`, `dimension.unit (NR)`, `dimension.nace_r2 (I551-I553)`, `dimension.geo (EL62)`, `dimension.time`, `value`
- **Dropped / Redacted Fields:** `PCH_PRE (percentage change)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.c_resid` | Country of residence ('TOTAL', 'DOM', 'FOR') |
| `dimension.unit` | 'NR' (number of arrivals) |
| `dimension.nace_r2` | 'I551-I553' |
| `dimension.geo` | 'EL62' (Ionia Nisia) |
| `dimension.time` | '2022', '2023' |
| `value` | Sparse map of tourist arrivals |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Extract total annual overnight stays (tour_occ_nin2) and arrivals (tour_occ_arn2) at tourist accommodation establishments in EL62 via `scripts/verification/build_dashboard.py` for c_resid='TOTAL', unit='NR', nace_r2='I551-I553'.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.series[].series_label` | `string` | `label` | `filter_dimension` | Distinguishes 'overnight stays' vs 'arrivals' and sub-series. |
| `refined_data.series[].observed_at` | `string` | `year` | `temporal_dimension` | Reference year. |
| `refined_data.series[].value` | `number` | `nights or arrivals` | `target_indicator` | Total EL62 nights (16.51M in 2022; 19.76M in 2023; 20.52M in 2024; 20.36M in 2025) and arrivals (2.79M in 2022; 3.33M in 2023). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Eurostat_tour_occ_nin2:Data26:overnight stays:2022` | `2022` | `NUTS2/EL62` | **16512634** | `nights` | `annual` |
| `Eurostat_tour_occ_nin2:Data26:overnight stays:2023` | `2023` | `NUTS2/EL62` | **19762799** | `nights` | `annual` |
| `Eurostat_tour_occ_arn2:Data26:arrivals:2022` | `2022` | `NUTS2/EL62` | **2785360** | `` | `annual` |
| `Eurostat_tour_occ_arn2:Data26:arrivals:2023` | `2023` | `NUTS2/EL62` | **3332407** | `` | `annual` |
