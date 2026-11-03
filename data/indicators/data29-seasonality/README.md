# Data29 — Seasonality (%)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json [.json]  ──( scripts/verification/compute-data29-seasonality.py )──>  refined-data.json [.json]
  data/raw/eurostat-tour_ce_omn12-EL62-EL-monthly-2020-2023.json [.json]  ──( scripts/verification/compute-data29-seasonality.py )──>  refined-data.json [.json]
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
- **Primary Conversion / Builder Script:** `scripts/verification/compute-data29-seasonality.py -> scripts/verification/build_dashboard.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `193`

## 1. Overview & Key Note

D-026 (2026-11-03): headline = share of annual nights in the 3 busiest months, all accommodation (EL62 2023 = 63.81 %, 2025 = 63.91 %); Seasonality Index = Gini of 12 monthly nights (EL62 2023 = 0.5827). TOUR_SOE_02 is a top-3-month share; its EL62 value (71.08 %, 2023) covers online-platform nights only and is kept as a separate series. Computed by scripts/verification/compute-data29-seasonality.py. Island-level monthly data: not published by Eurostat (PROPOSAL: Fraport monthly airport passengers). Monthly nights (EL62 + EL, 2020-2025) are kept outside the master snapshot in data/curated/monthly-data29-nights-*.json (owner decision 2026-11-03); the former tour_occ_nim EL 2023 base series was removed from the map (identical values are in that file).

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Eurostat_tour_occ_nin2m` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2m?format=JSON&lang=EN&geo=EL62&geo=EL&unit=NR&c_resid=TOTAL`
- **Access Method:** `GET (JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json`
- **Raw File Extension & Format:** `.json` — `application/json (JSON-stat 2.0; month is a dimension M01..M12 + TOTAL, time is the year)`
- **SHA-256 Checksum (of the local file, recomputed at build):** `78c4e09fc4317cc0521c998a84434c071d010affec5f5a3b9b0bee54e727c60f`
- **Evidence Manifest:** `data/manifests/source-verification-2026-11-03.json`
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/compute-data29-seasonality.py`
- **Conversion Command:** `python3 scripts/verification/compute-data29-seasonality.py && python3 scripts/verification/build_dashboard.py <manifests> && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `month`, `geo`, `time`, `value`
- **Dropped / Redacted Fields:** `freq (A)`, `c_resid (TOTAL only)`, `unit (NR only)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.month` | 'TOTAL' and 'M01'..'M12' |
| `dimension.geo` | 'EL62' (Ionia Nisia) and 'EL' (Greece) |
| `dimension.time` | Reference year '2020'..'2025' |
| `dimension.nace_r2` | 'I551-I553' (all tourist accommodation; no type split at NUTS 2) |
| `value` | Nights spent (unit NR) |

### Source 2: `Eurostat_tour_ce_omn12_monthly` (Eurostat (data shared by Airbnb, Booking.com, Expedia Group))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_ce_omn12?format=JSON&lang=EN&geo=EL62&geo=EL&indic_to=NGT_SP&c_resid=TOTAL&time=2020&time=2021&time=2022&time=2023`
- **Access Method:** `GET (JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eurostat-tour_ce_omn12-EL62-EL-monthly-2020-2023.json`
- **Raw File Extension & Format:** `.json` — `application/json (JSON-stat 2.0; month dimension)`
- **SHA-256 Checksum (of the local file, recomputed at build):** `4e2ec7512fa29d69410ac2b78694ccab9fa2765789cad949f3d1225bb3fba4c1`
- **Evidence Manifest:** `data/manifests/source-verification-2026-11-03.json`
- **Lineage Note:** Used only to reconcile the dashboard EL62 value; no observation is emitted from it.
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/compute-data29-seasonality.py`
- **Conversion Command:** `python3 scripts/verification/compute-data29-seasonality.py --check`
- **Whitelisted Raw Variables (`kept`):** `month`, `geo`, `time`, `value`
- **Dropped / Redacted Fields:** `indic_to (NGT_SP only)`, `c_resid (TOTAL only)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.month` | 'M01'..'M12' |
| `dimension.geo` | 'EL62', 'EL' |
| `value` | Guest nights in short-stay accommodation booked via online platforms |

### Source 3: `EU_Tourism_Dashboard_2024` (European Commission / Joint Research Centre (JRC) — EU Tourism Dashboard)
- **Upstream URL:** `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv`
- **Access Method:** `GET (public CSV bulk export)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eutd-tourism-dashboard-2024-indicators.csv`
- **Raw File Extension & Format:** `.csv` — `text/csv (UTF-8, comma-delimited, 81,939 rows)`
- **SHA-256 Checksum (of the local file, recomputed at build):** `ab45bb4b2b0b831df183684a05adb52f5bca0270d3b90f1993af0bd77d35aa12`
- **Evidence Manifest:** `data/manifests/source-verification-2026-10-03.json`
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

### Source 4: `Eurostat_tour_occ_nim` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&geo=EL&freq=M&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2023-01..2023-12`
- **Access Method:** `GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eurostat-tour_occ_nim-EL-2023.json`
- **Raw File Extension & Format:** `.json` — `application/json (SDMX 2.1 JSON-stat 2.0 cube)`
- **SHA-256 Checksum (of the local file, recomputed at build):** `e07a17f98f18f87f94e31d35993f34c9b44eda95c60632ce1c4e0b729955198b`
- **Evidence Manifest:** `data/manifests/source-verification-2026-09-24.json`
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

**Transformation Rule:** D-026. Headline: share of annual nights in the 3 busiest months (EU Tourism Dashboard TOUR_SOE_02 definition), computed over ALL accommodation from Eurostat tour_occ_nin2m monthly nights for EL62 and EL, 2020-2025: top3_share = sum(3 largest monthly nights) / sum(12 monthly nights) * 100 (EL62 2023 = 63.81 %). Seasonality Index: Gini coefficient of the 12 monthly nights (EL62 2023 = 0.5827). Context: peak-month share, share of nights outside June-September, and EL62 monthly nights. Computed by scripts/verification/compute-data29-seasonality.py, which first checks the definition against the dashboard: EL 2021-2023 match on all accommodation; EL62 2020-2023 match only on online-platform nights (tour_ce_omn12). The dashboard EL62 value (71.08 % in 2023) is therefore kept as a separate platform-only series.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.results.<geo>.<year>.top3_share_pct` | `number` | `%` | `target_indicator` | Headline Data29: share of annual nights (all accommodation) in the 3 busiest months. EL62 2023 = 63.81. |
| `refined_data.results.<geo>.<year>.gini` | `number` | `index (0-1)` | `target_indicator` | Seasonality Index: Gini coefficient of the 12 monthly nights; 0 = even year-round, 0.917 = all nights in one month. EL62 2023 = 0.5827. |
| `refined_data.results.<geo>.<year>.peak_month_share_pct` | `number` | `%` | `context_metric` | Share of annual nights in the single busiest month (August in every year). |
| `refined_data.results.<geo>.<year>.share_outside_jun_sep_pct` | `number` | `%` | `context_metric` | Share of annual nights in January-May and October-December; tracks off-season growth. |
| `refined_data.results.<geo>.<year>.monthly_nights` | `object` | `nights` | `input_variable` | Monthly nights M01..M12 from tour_occ_nin2m (all accommodation, I551-I553). |
| `refined_data.results.EL62.<year>.platform_top3_share_pct` | `number` | `%` | `context_metric` | Same measure over online-platform nights only (tour_ce_omn12); equals the dashboard TOUR_SOE_02 EL62 value. |
| `refined_data.dashboard_reconciliation` | `array` | `%` | `quality_check` | Per geo/year: dashboard value, recomputed value, basis, match flag. |
| `refined_data.dashboard_el62_platform_only` | `object` | `%` | `context_metric` | EU Tourism Dashboard TOUR_SOE_02 EL62 2023 (71.08 %), relabelled as online-platform-only seasonality. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EU_Tourism_Dashboard:Data29:peak_season_share:2023` | `2023` | `NUTS2/EL62` | **71.08** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:top3_share:EL62:2020` | `2020` | `NUTS2/EL62` | **86.25** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:gini:EL62:2020` | `2020` | `NUTS2/EL62` | **0.724** | `index (0-1)` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:peak_month_share:EL62:2020` | `2020` | `NUTS2/EL62` | **40.67** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:share_outside_jun_sep:EL62:2020` | `2020` | `NUTS2/EL62` | **12.8** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:top3_share:EL62:2021` | `2021` | `NUTS2/EL62` | **81.51** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:gini:EL62:2021` | `2021` | `NUTS2/EL62` | **0.6791** | `index (0-1)` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:peak_month_share:EL62:2021` | `2021` | `NUTS2/EL62` | **31.64** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:share_outside_jun_sep:EL62:2021` | `2021` | `NUTS2/EL62` | **8.95** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:top3_share:EL62:2022` | `2022` | `NUTS2/EL62` | **65.06** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:gini:EL62:2022` | `2022` | `NUTS2/EL62` | **0.5922** | `index (0-1)` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:peak_month_share:EL62:2022` | `2022` | `NUTS2/EL62` | **24.41** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:share_outside_jun_sep:EL62:2022` | `2022` | `NUTS2/EL62` | **18.0** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:top3_share:EL62:2023` | `2023` | `NUTS2/EL62` | **63.81** | `%` | `annual` |
| `Eurostat_tour_occ_nin2m:Data29:gini:EL62:2023` | `2023` | `NUTS2/EL62` | **0.5827** | `index (0-1)` | `annual` |
| _… (178 more observations in `refined-data.json`)_ | | | | | |
