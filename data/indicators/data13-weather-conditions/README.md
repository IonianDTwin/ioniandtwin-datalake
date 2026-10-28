# Data13 — Weather conditions (temp, rain, …)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/open-meteo-corfu-forecast-2026-09-22.json [.json]  ──( scripts/verification/pull-open-meteo.sh -> scripts/verification/build_dashboard.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `climate_adaptation`
- **Refresh Cadence:** `daily`
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/pull-open-meteo.sh -> scripts/verification/build_dashboard.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `3`

## 1. Overview & Key Note

—

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `OpenMeteo_forecast` (Open-Meteo (open-meteo.com))
- **Upstream URL:** `https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1`
- **Access Method:** `GET (public REST JSON API, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/open-meteo-corfu-forecast-2026-09-22.json`
- **Raw File Extension & Format:** `.json` — `application/json`
- **SHA-256 Checksum:** `e16e6108febd130fbab834a943df510a3d982714d4d7e18a7f01ac5e50f93e23` (verified in `data/manifests/source-verification-2026-09-22.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/pull-open-meteo.sh -> scripts/verification/build_dashboard.py`
- **Conversion Command:** `bash scripts/verification/pull-open-meteo.sh && python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `latitude`, `longitude`, `current.time`, `current.temperature_2m`, `current.relative_humidity_2m`, `current.apparent_temperature`, `daily.uv_index_max`
- **Dropped / Redacted Fields:** `generationtime_ms`, `utc_offset_seconds`, `elevation`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `latitude / longitude` | WGS84 grid coordinate (39.625N, 19.875E for Corfu) |
| `current.time` | ISO-8601 current observation timestamp in Europe/Athens timezone |
| `current.temperature_2m` | Air temperature at 2 meters (°C) |
| `current.relative_humidity_2m` | Relative humidity at 2 meters (%) |
| `current.apparent_temperature` | Feels-like apparent temperature (°C) |
| `daily.uv_index_max` | Daily maximum UV index array |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Extract current surface meteorological observations (temperature_2m, relative_humidity_2m, apparent_temperature) at the Corfu reference point (39.62N, 19.92E) via `scripts/verification/build_dashboard.py`.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.current.time` | `string` | `ISO-8601` | `temporal_dimension` | Observation timestamp in Europe/Athens timezone. |
| `refined_data.current.temperature_2m` | `number` | `°C` | `target_indicator` | Air temperature at 2 meters above ground (26.5 °C). |
| `refined_data.current.relative_humidity_2m` | `number` | `%` | `target_indicator` | Relative humidity at 2 meters above ground (57%). |
| `refined_data.current.apparent_temperature` | `number` | `°C` | `target_indicator` | Apparent (feels-like) temperature combining wind and humidity (28.8 °C). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OpenMeteo_forecast:Data13:air temperature:2026-09-22T14:15` | `2026-09-22T14:15` | `point/39.62,19.92` | **26.5** | `°C` | `instant` |
| `OpenMeteo_forecast:Data13:relative humidity:2026-09-22T14:15` | `2026-09-22T14:15` | `point/39.62,19.92` | **57** | `%` | `instant` |
| `OpenMeteo_forecast:Data13:apparent (feels-like) temperature:2026-09-22T14:15` | `2026-09-22T14:15` | `point/39.62,19.92` | **28.8** | `°C` | `instant` |
