# Data03 — Clean beach water (reports)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/eea-bwd-greece-2024.geojson [.geojson]  ──( scripts/verification/pull-data02-bathing-water-el62.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** Καθαρό νερό παραλίας (Reports)
- **Category:** `environmental_health_pollutants`
- **Refresh Cadence:** `annual`
- **Raw Input File Extension(s):** `.geojson`
- **Primary Conversion / Builder Script:** `scripts/verification/pull-data02-bathing-water-el62.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `2`

## 1. Overview & Key Note

ASSUMPTION: clean = classified Excellent/Good/Sufficient (Greece 2024: 99.94% of classified). Citizen reports are the app's own feed.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `EEA_BWD_Discomap_2024` (European Environment Agency (EEA) — Water Discomap ArcGIS REST)
- **Upstream URL:** `https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2024/MapServer/3/query?where=countryCode%3D%27EL%27&outFields=*&f=geojson`
- **Access Method:** `GET (ArcGIS REST GeoJSON query, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eea-bwd-greece-2024.geojson`
- **Raw File Extension & Format:** `.geojson` — `application/geo+json (1,729 Point features across Greece)`
- **SHA-256 Checksum:** `ae444f3a26aa9b206c134b1e5a03fc9dd808dabb1c078d498ed3e0d28a04c5bf` (verified in `data/manifests/source-verification-2026-10-20.json`)
- **Conversion Script (`.geojson` -> `.json`):** `scripts/verification/pull-data02-bathing-water-el62.py`
- **Conversion Command:** `python3 scripts/verification/pull-data02-bathing-water-el62.py`
- **Whitelisted Raw Variables (`kept`):** `countryCode`, `bathingWaterIdentifier`, `quality2024`, `lat`, `lon`, `geometry`
- **Dropped / Redacted Fields:** `historical_quality_1990_2023_columns`, `management_links`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `properties.countryCode` | ISO country code ('EL') |
| `properties.bathingWaterIdentifier` | Unique WISE bathing water station ID |
| `properties.quality2024` | 2024 season classification ('1 - Excellent', '2 - Good', '3 - Sufficient', '4 - Poor', '0 - Not classified') |
| `geometry` | WGS84 Point coordinates [lon, lat] |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Under documented ASSUMPTION, 'clean beach water' is operationalized as the share of classified bathing waters meeting at least EU minimum standards: (Excellent + Good + Sufficient) / classified_sites * 100, computed by scripts/verification/pull-data02-bathing-water-el62.py. For EL62 in 2024: (170 + 1 + 0) / 171 = 100.0%. For Greece overall in 2024: (1677 + 15 + 1) / 1694 = 99.94%.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.el62_2024.classified_sites` | `integer` | `sites` | `input_variable` | Total classified bathing water sites in EL62 (171). |
| `refined_data.el62_2024.pct_clean_water_classified` | `number` | `%` | `target_indicator` | Share of classified EL62 sites rated Excellent, Good, or Sufficient (100.0%). |
| `refined_data.greece_2024_quality_breakdown` | `array` | `sites` | `input_variable` | National Greece 2024 quality counts from EEA Discodata SQL. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EEA_WISE_BWD:Data03:clean_beach_share:2024` | `2024` | `country/EL` | **99.94** | `%` | `annual` |
| `EEA_BWD_Discomap_2024:Data03:clean_share_classified:EL62:2024` | `2024-01-01` | `NUTS2/EL62` | **100.0** | `%` | `annual` |
