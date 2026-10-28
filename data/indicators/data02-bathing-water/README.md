# Data02 — Excellent bathing waters (%)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/eea-bwd-greece-2024.geojson [.geojson]  ──( scripts/verification/pull-data02-bathing-water-el62.py )──>  refined-data.json [.json]
  data/raw/gisco-nuts-2021-3035-EL62.geojson [.geojson]  ──( scripts/verification/pull-data02-bathing-water-el62.py )──>  refined-data.json [.json]
  data/raw/eutd-tourism-dashboard-2024-indicators.csv [.csv]  ──( scripts/verification/extract-eutd-dashboard-csv.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** Άριστα νερά κολύμβησης (%)
- **Category:** `environmental_health_pollutants`
- **Refresh Cadence:** `annual`
- **Raw Input File Extension(s):** `.csv` + `.geojson`
- **Primary Conversion / Builder Script:** `scripts/verification/pull-data02-bathing-water-el62.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `37`

## 1. Overview & Key Note

EL62 = 98.82 % excellent bathing water (2023, EU Tourism Dashboard TOUR_ENV_05). VERIFIED 2024 spatial join (2026-10-20): 170 / 171 classified sites rated Excellent (99.42% of classified, 98.27% of total 173 sites in EL62; Zakynthos 100%, Corfu 98.63%, Kefalonia/Ithaki 100%, Lefkada 100%) via scripts/verification/pull-data02-bathing-water-el62.py.

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

### Source 2: `Eurostat_GISCO_NUTS_2021` (Eurostat GISCO)
- **Upstream URL:** `https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_3035_LEVL_2.geojson`
- **Access Method:** `GET (GeoJSON boundary download)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/gisco-nuts-2021-3035-EL62.geojson`
- **Raw File Extension & Format:** `.geojson` — `application/geo+json (EPSG:3035 equal-area MultiPolygon)`
- **SHA-256 Checksum:** `6b53f249bf425424c0f19eaba403c3183ef378432a6408a0e93e6d9d1fdca35d` (verified in `data/manifests/source-verification-2026-10-03.json`)
- **Conversion Script (`.geojson` -> `.json`):** `scripts/verification/pull-data02-bathing-water-el62.py`
- **Conversion Command:** `python3 scripts/verification/pull-data02-bathing-water-el62.py`
- **Whitelisted Raw Variables (`kept`):** `NUTS_ID`, `NAME_LATN`, `geometry`
- **Dropped / Redacted Fields:** `CNTR_CODE`, `MOUNT_TYPE`, `URBN_TYPE`, `COAST_TYPE`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `properties.NUTS_ID` | NUTS2 code ('EL62') |
| `properties.NAME_LATN` | Region name ('Ionia Nisia') |
| `geometry` | MultiPolygon in EPSG:3035 LAEA projection |

### Source 3: `EU_Tourism_Dashboard_2024` (European Commission / Joint Research Centre (JRC) — EU Tourism Dashboard)
- **Upstream URL:** `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv`
- **Access Method:** `GET (public CSV bulk export)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eutd-tourism-dashboard-2024-indicators.csv`
- **Raw File Extension & Format:** `.csv` — `text/csv (UTF-8, comma-delimited, 81,939 rows)`
- **SHA-256 Checksum:** `ab45bb4b2b0b831df183684a05adb52f5bca0270d3b90f1993af0bd77d35aa12` (verified in `data/manifests/source-verification-2026-10-03.json`)
- **Conversion Script (`.csv` -> `.json`):** `scripts/verification/extract-eutd-dashboard-csv.py`
- **Conversion Command:** `python3 scripts/verification/extract-eutd-dashboard-csv.py && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `code ('TOUR_ENV_05')`, `nuts_code_2021 ('EL62')`, `year (2023)`, `value`, `unit`
- **Dropped / Redacted Fields:** `pillar`, `component`, `non_EL62_rows`, `other_indicator_codes`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `pillar` | Dashboard sustainability pillar ('Green', 'Digital', 'Socio-economic', 'Basic descriptors') |
| `code` | Indicator code (filtered to 'TOUR_ENV_05') |
| `indicator` | Human-readable indicator title in the JRC export |
| `year` | Reference calendar year (filtered to 2023) |
| `nuts_code_2021` | Eurostat NUTS 2021 code (filtered to 'EL62' Ionian Islands) |
| `unit` | Unit of measure string |
| `value` | Numeric indicator value |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Spatial join of EEA 2024 Greece bathing water monitoring points with Eurostat GISCO EL62 land polygon buffered 3,000 m seaward (EPSG:3035) via scripts/verification/pull-data02-bathing-water-el62.py. Compute pct_excellent_classified = excellent / classified_sites * 100 (170 / 171 = 99.42%) and pct_excellent_total = excellent / total_sites * 100 (170 / 173 = 98.27%). Reconciled with EU Tourism Dashboard TOUR_ENV_05 (2023 EL62 = 98.82%) and national 1990-2024 Discodata SQL series.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.el62_spatial_join_2024.el62_regional_nuts2.total_sites` | `integer` | `sites` | `input_variable` | Total EEA bathing water monitoring points inside the 3 km EL62 coastal buffer (173). |
| `refined_data.el62_spatial_join_2024.el62_regional_nuts2.classified_sites` | `integer` | `sites` | `input_variable` | Classified bathing water sites in EL62 in 2024 (171). |
| `refined_data.el62_spatial_join_2024.el62_regional_nuts2.excellent` | `integer` | `sites` | `input_variable` | Sites rated '1 - Excellent' in EL62 in 2024 (170). |
| `refined_data.el62_spatial_join_2024.el62_regional_nuts2.pct_excellent_classified` | `number` | `%` | `target_indicator` | Share of classified bathing waters in EL62 rated Excellent (99.42%). |
| `refined_data.el62_spatial_join_2024.by_nuts3_island` | `object` | `sites_and_pct` | `internal_disaggregation` | NUTS3 island breakdown (EL621 Zakynthos, EL622 Kerkyra, EL623 Ithaki/Kefallinia, EL624 Lefkada). |
| `refined_data.dashboard_benchmark_2023` | `object` | `%` | `target_indicator` | EU Tourism Dashboard TOUR_ENV_05 2023 value for EL62 (98.82%). |
| `refined_data.national_series_1990_2024` | `array` | `%` | `target_indicator` | 35-year national Greece bathing water series from EEA Discodata SQL. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EEA_WISE_BWD:Data02:pct_excellent:1990` | `1990` | `country/EL` | **22.19** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1991` | `1991` | `country/EL` | **68.55** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1992` | `1992` | `country/EL` | **89.82** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1993` | `1993` | `country/EL` | **91.84** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1994` | `1994` | `country/EL` | **89.37** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1995` | `1995` | `country/EL` | **94.99** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1996` | `1996` | `country/EL` | **95.57** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1997` | `1997` | `country/EL` | **94.45** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1998` | `1998` | `country/EL` | **95.86** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:1999` | `1999` | `country/EL` | **95.49** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:2000` | `2000` | `country/EL` | **94.94** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:2001` | `2001` | `country/EL` | **96.74** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:2002` | `2002` | `country/EL` | **97.38** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:2003` | `2003` | `country/EL` | **96.88** | `%` | `annual` |
| `EEA_WISE_BWD:Data02:pct_excellent:2004` | `2004` | `country/EL` | **97.49** | `%` | `annual` |
| _… (22 more observations in `refined-data.json`)_ | | | | | |
