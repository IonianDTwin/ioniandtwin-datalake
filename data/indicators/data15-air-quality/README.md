# Data15 — Air quality

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip [.zip (NetCDF .nc)]  ──( scripts/verification/build_indicator_folders.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** Ποιότητα Αέρα
- **Category:** `climate_adaptation`
- **Refresh Cadence:** `daily`
- **Raw Input File Extension(s):** `.zip (NetCDF .nc)`
- **Primary Conversion / Builder Script:** `scripts/verification/build_indicator_folders.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `0`

## 1. Overview & Key Note

CAMS ensemble analysis pulled 2026-10-01 (NO2 5.80 / PM10 7.40 / PM2.5 5.51 / CO 158.70 ug/m3, Corfu-airport grid point). D-008: Data15 = ambient air quality.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `CAMS_ADS_air_quality` (Copernicus Atmosphere Monitoring Service (CAMS) — Atmosphere Data Store (ADS))
- **Upstream URL:** `https://ads.atmosphere.copernicus.eu/api/retrieve/v1/processes/cams-europe-air-quality-forecasts/execution`
- **Access Method:** `POST via cads-api-client (CAMS_API_KEY in untracked .env)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip`
- **Raw File Extension & Format:** `.zip (NetCDF .nc)` — `application/zip containing NetCDF classic (ENS_ANALYSIS.nc)`
- **SHA-256 Checksum:** `ecc26d470cdfa5c9ecd65b7dd6b1104e8692d23b998083a402951ddaa9d11574` (verified in `data/manifests/source-verification-2026-10-01.json`)
- **Conversion Script (`.zip (NetCDF .nc)` -> `.json`):** `scripts/verification/build_indicator_folders.py`
- **Conversion Command:** `python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `no2_conc`, `co_conc`, `pm10_conc`, `pm2p5_conc`, `latitude`, `longitude`, `level`, `time`
- **Dropped / Redacted Fields:** `upper_level_layers (filtered to surface level=0)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `longitude` | 1D float array (30 grid cells, 19.0E to 22.0E, 0.1 deg resolution) |
| `latitude` | 1D float array (35 grid cells, 37.0N to 40.5N, 0.1 deg resolution) |
| `level` | Vertical altitude level in meters (filtered to surface 0 m) |
| `time` | Analysis timestamp (2026-09-30T00:00:00Z) |
| `no2_conc` | Surface nitrogen dioxide concentration (ug/m3) |
| `co_conc` | Surface carbon monoxide concentration (ug/m3) |
| `pm10_conc` | Surface PM10 concentration (ug/m3) |
| `pm2p5_conc` | Surface PM2.5 concentration (ug/m3) |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Extract ambient surface air pollutant concentrations (NO2, PM10, PM2.5, CO in ug/m3) over the Ionian Islands bounding box (37.0-40.5N, 19.0-22.0E) from CAMS European air quality ensemble analysis (D-008 confirmed Data15 = Ambient Air Quality).

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.values_ug_m3.NO2.region_mean` | `number` | `ug/m3` | `target_indicator` | Regional mean surface NO2 across the Ionian bounding box (1.96 ug/m3). |
| `refined_data.values_ug_m3.PM10.region_mean` | `number` | `ug/m3` | `target_indicator` | Regional mean surface PM10 across the Ionian bounding box (8.99 ug/m3). |
| `refined_data.values_ug_m3.PM2.5.region_mean` | `number` | `ug/m3` | `target_indicator` | Regional mean surface PM2.5 across the Ionian bounding box (5.76 ug/m3). |
| `refined_data.values_ug_m3.CO.region_mean` | `number` | `ug/m3` | `target_indicator` | Regional mean surface CO across the Ionian bounding box (158.14 ug/m3). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

_No observations emitted for this indicator yet._
