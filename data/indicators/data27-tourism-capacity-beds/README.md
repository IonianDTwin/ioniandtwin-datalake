# Data27 — Tourism capacity (beds)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/eurostat-tour_cap_nuts2-EL62-2022-2023.json [.json]  ──( scripts/verification/build_dashboard.py )──>  refined-data.json [.json]
  data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json [.json]  ──( scripts/verification/build_indicator_folders.py )──>  refined-data.json [.json]
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
- **Observations Emitted:** `2`

## 1. Overview & Key Note

—

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Eurostat_tour_cap_nuts2` (Eurostat (European Commission))
- **Upstream URL:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023`
- **Access Method:** `GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eurostat-tour_cap_nuts2-EL62-2022-2023.json`
- **Raw File Extension & Format:** `.json` — `application/json (SDMX 2.1 JSON-stat 2.0 cube)`
- **SHA-256 Checksum:** `90d5c376d69fad77a36e7d077cc63545a4ba0e68afc2e8017578418395495ae3` (verified in `data/manifests/source-verification-2026-09-22.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_dashboard.py`
- **Conversion Command:** `bash scripts/verification/pull-eurostat-tourism.sh && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `dimension.accomunit (BEDPL, ESTBL, BEDRM)`, `dimension.unit (NR)`, `dimension.nace_r2`, `dimension.geo (EL62)`, `dimension.time`, `value`
- **Dropped / Redacted Fields:** `PCH_PRE`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `dimension.accomunit` | Capacity unit ('BEDPL' bed-places, 'ESTBL' establishments, 'BEDRM' bedrooms) |
| `dimension.unit` | 'NR' (count) |
| `dimension.nace_r2` | 'I551-I553' |
| `dimension.geo` | 'EL62' |
| `dimension.time` | '2022', '2023' |
| `value` | Sparse map of capacity counts |

### Source 2: `ELSTAT_STO12_capacity` (Hellenic Statistical Authority (ELSTAT) — Table STO12)
- **Upstream URL:** `https://www.statistics.gr/en/statistics/-/publication/STO12/`
- **Access Method:** `GET (annual XLSX editions 2021-2025)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json`
- **Raw File Extension & Format:** `.json` — `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (elstat-sto12-2021..2025-capacity.xlsx) -> JSON`
- **SHA-256 Checksum:** `68e1a44e39df1698f46b66c6ae32d054febb1d6e813c5e7e554153e5b59d81be` (verified in `data/manifests/source-verification-2026-10-01.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_indicator_folders.py`
- **Conversion Command:** `python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `year`, `regional_unit`, `bed_places_hotels_and_similar`
- **Dropped / Redacted Fields:** `non_Ionian_regional_units`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `year` | Edition year ('2021'..'2025') |
| `KERKYRA / ZAKYNTHOS / KEFALLINIA / LEFKADA / ITHAKI` | Hotel & similar establishment bed-places by regional unit |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Extract total tourist accommodation bed-places (accomunit='BEDPL', unit='NR', nace_r2='I551-I553') for NUTS2 EL62 from Eurostat tour_cap_nuts2 via `scripts/verification/build_dashboard.py`, supplemented by ELSTAT STO12 regional-unit hotel bed capacity (2021-2025).

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.series[].series_label` | `string` | `label` | `filter_dimension` | Capacity metric label ('bed-places', 'establishments', 'bedrooms'). |
| `refined_data.series[].value` | `number` | `count` | `target_indicator` | Total bed-places in EL62 (159,790 in 2022; 155,968 in 2023). |
| `refined_data.elstat_hotels_by_island_2021_2025` | `object` | `bed-places` | `internal_disaggregation` | ELSTAT STO12 hotel bed-places by regional unit (Kerkyra, Zakynthos, Kefallinia, Lefkada, Ithaki). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Eurostat_tour_cap_nuts2:Data27:bed-places:2022` | `2022` | `NUTS2/EL62` | **159790** | `` | `annual` |
| `Eurostat_tour_cap_nuts2:Data27:bed-places:2023` | `2023` | `NUTS2/EL62` | **155968** | `` | `annual` |
