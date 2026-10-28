# Data19 — Short-term rental share (Airbnb)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json [.json]  ──( scripts/verification/pull-data19-platform-rentals.py )──>  refined-data.json [.json]
  data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json [.json]  ──( scripts/verification/pull-data19-platform-rentals.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `social_pressure_infrastructure`
- **Refresh Cadence:** `annual`
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/pull-data19-platform-rentals.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `8`

## 1. Overview & Key Note

VERIFIED 2026-10-15: platform nights from Eurostat tour_ce_omn12 (EC agreement with Airbnb/Booking/Expedia/Tripadvisor; NGT_SP, TOTAL, EL62). Share % = platform / (conventional + platform) * 100, 2018-2025: 14.50 / 15.88 / 22.08 / 23.02 / 24.02 / 23.50 / 17.65 / 29.80. InsideAirbnb superseded (no Ionian coverage; Athens key 403). FLAG: 2025 platform nights +96 % vs 2024 (coverage/onboarding change, treat cautiously). Evidence: data/manifests/source-verification-2026-10-15.json.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Eurostat_tour_ce_omn12` (Eurostat — Short-stay accommodation offered via online platforms (EC agreement with Airbnb, Booking, Expedia, Tripadvisor))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_ce_omn12?geo=EL62&indic_to=NGT_SP&c_resid=TOTAL&month=TOTAL&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023&time=2024&time=2025&lang=en`
- **Access Method:** `GET (JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json`
- **Raw File Extension & Format:** `.json` — `application/json (JSON-stat 2.0 cube)`
- **SHA-256 Checksum:** `421338a3a15d9db86ef98b2ff1138e82b3a9c7b7c37aacf27427dca6d998abbd` (verified in `data/manifests/source-verification-2026-10-15.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/pull-data19-platform-rentals.py`
- **Conversion Command:** `python3 scripts/verification/pull-data19-platform-rentals.py`
- **Whitelisted Raw Variables (`kept`):** `indic_to (NGT_SP)`, `c_resid (TOTAL)`, `month (TOTAL)`, `geo (EL62)`, `time (2018..2025)`, `value`
- **Dropped / Redacted Fields:** `STAY (stays count)`, `guest_nights_by_origin_breakdown`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.indic_to` | Tourism indicator ('NGT_SP' = Guest nights spent) |
| `dimension.c_resid` | Guest residence ('TOTAL') |
| `dimension.month` | Month ('TOTAL' annual or 'M01'..'M12') |
| `dimension.geo` | NUTS2 code ('EL62') |
| `dimension.time` | Reference years ('2018'..'2025') |
| `value` | Sparse map of platform guest nights |

### Source 2: `Eurostat_tour_occ_nin2_2018_2025` (Eurostat — Conventional tourist accommodation nights)
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?geo=EL62&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023&time=2024&time=2025&lang=en`
- **Access Method:** `GET (JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json`
- **Raw File Extension & Format:** `.json` — `application/json (JSON-stat 2.0 cube)`
- **SHA-256 Checksum:** `474ba9c359e92830964e2ad4d1c83f11d841b2d1e2d8dda20bf66dea9e14f158` (verified in `data/manifests/source-verification-2026-10-15.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/pull-data19-platform-rentals.py`
- **Conversion Command:** `python3 scripts/verification/pull-data19-platform-rentals.py`
- **Whitelisted Raw Variables (`kept`):** `c_resid (TOTAL)`, `unit (NR)`, `nace_r2 (I551-I553)`, `geo (EL62)`, `time (2018..2025)`, `value`
- **Dropped / Redacted Fields:** `sub_nace_breakdowns`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.c_resid` | 'TOTAL' |
| `dimension.unit` | 'NR' (number of nights) |
| `dimension.nace_r2` | 'I551-I553' |
| `dimension.geo` | 'EL62' |
| `dimension.time` | '2018'..'2025' |
| `value` | Sparse map of conventional accommodation nights |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** D-020: Compute annual short-term rental share for EL62 (2018-2025) via `scripts/verification/pull-data19-platform-rentals.py` as platform_nights / (conventional_nights + platform_nights) * 100.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.series[].year` | `string` | `year` | `temporal_dimension` | Reference year (2018-2025). |
| `refined_data.series[].platform_nights` | `integer` | `nights` | `input_variable` | Guest nights booked via online platforms (tour_ce_omn12). |
| `refined_data.series[].conventional_nights` | `integer` | `nights` | `input_variable` | Guest nights at conventional tourist accommodation (tour_occ_nin2). |
| `refined_data.series[].total_tourism_nights` | `integer` | `nights` | `input_variable` | Combined platform + conventional guest nights in EL62. |
| `refined_data.series[].share_pct` | `number` | `%` | `target_indicator` | Platform share of total tourism nights (14.50% in 2018 -> 29.80% in 2025). |
| `refined_data.seasonality_2025` | `array` | `nights` | `context_metric` | 2025 monthly platform guest nights showing 52.4% concentration in July-August. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2018` | `2018` | `NUTS2/EL62` | **14.5** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2019` | `2019` | `NUTS2/EL62` | **15.88** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2020` | `2020` | `NUTS2/EL62` | **22.08** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2021` | `2021` | `NUTS2/EL62` | **23.02** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2022` | `2022` | `NUTS2/EL62` | **24.02** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2023` | `2023` | `NUTS2/EL62` | **23.5** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2024` | `2024` | `NUTS2/EL62` | **17.65** | `%` | `annual` |
| `Eurostat_tour_ce_omn12:Data19:platform_rental_share:2025` | `2025` | `NUTS2/EL62` | **29.8** | `%` | `annual` |
