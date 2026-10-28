# Data32 — Dominant tourism typology

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json [.json]  ──( scripts/verification/build_dashboard.py (via render_pull_reports.decode) )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `density_typology`
- **Refresh Cadence:** `annual`
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/build_dashboard.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `1`

## 1. Overview & Key Note

Dominant typology = hotels (~73 % nace_r2 nights). Flag: dashboard TOUR_DES_07 is a categorical 6-class typology (EL62 = class 4); class label to confirm.

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

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** D-009 & D-016: Compare overnight stays across NACE Rev. 2 accommodation categories in EL62 via `scripts/verification/build_dashboard.py` (I551 hotels ~70-73%, I552 short-stay ~26-30%, I553 camping <1%) and assign the argmax category ('hotels') as the dominant tourism typology.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.nace_r2_shares_el62` | `object` | `%` | `input_variable` | Share of EL62 overnight stays by NACE Rev. 2 category. |
| `refined_data.series[].value` | `string` | `category` | `target_indicator` | Dominant accommodation typology in EL62 ('hotels'). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Eurostat_tour_occ_nin2:Data32:dominant_typology:2023` | `2023` | `NUTS2/EL62` | **hotels** | `None` | `annual` |
