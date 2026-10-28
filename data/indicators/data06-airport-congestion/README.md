# Data06 — Airport congestion

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/opensky-ionian-states-20261020-105525.json [.json]  ──( scripts/verification/pull-data06-airport-congestion.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `dynamic_congestion`
- **Refresh Cadence:** `live`
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/pull-data06-airport-congestion.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `4`

## 1. Overview & Key Note

VERIFIED 2026-10-20: OpenSky free REST states/all filtered to 25km buffer, alt<=3000m for 4 Ionian airports (CFU, ZTH, EFL, PVK). Congestion score S=min(1, count/threshold) -> observations emitted via scripts/verification/pull-data06-airport-congestion.py. Evidence: data/manifests/source-verification-2026-10-20.json.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `OpenSky_States_live` (OpenSky Network)
- **Upstream URL:** `https://opensky-network.org/api/states/all?lamin=37.0&lomin=19.0&lamax=40.5&lomax=22.0`
- **Access Method:** `GET (anonymous REST JSON API)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/opensky-ionian-states-20261020-105525.json`
- **Raw File Extension & Format:** `.json` — `application/json (OpenSky state-vector array)`
- **SHA-256 Checksum:** `9c8b228401c53d74ab25ad92e83264af574613745bb2d7f3586377e5cccb610a` (verified in `data/manifests/source-verification-2026-10-20.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/pull-data06-airport-congestion.py`
- **Conversion Command:** `python3 scripts/verification/pull-data06-airport-congestion.py`
- **Whitelisted Raw Variables (`kept`):** `icao24`, `callsign`, `origin_country`, `longitude`, `latitude`, `baro_altitude`, `on_ground`, `velocity`
- **Dropped / Redacted Fields:** `sensors`, `spi`, `position_source`, `squawk`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `time` | Unix epoch timestamp of state poll |
| `states[][0] (icao24)` | 24-bit ICAO transponder hex address |
| `states[][1] (callsign)` | Flight callsign string |
| `states[][2] (origin_country)` | Aircraft registration country |
| `states[][5..6] (lon, lat)` | WGS84 longitude and latitude |
| `states[][7] (baro_altitude)` | Barometric altitude in meters |
| `states[][8] (on_ground)` | Boolean flag indicating surface status |
| `states[][9] (velocity)` | Ground speed in m/s |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Filter live OpenSky state vectors in the Ionian bounding box (37.0-40.5N, 19.0-22.0E) via `scripts/verification/pull-data06-airport-congestion.py` to aircraft within a 25 km approach radius and baro_altitude <= 3,000 m (or on_ground=true) of each gateway airport (CFU, ZTH, EFL, PVK). Compute congestion_score = min(1.0, aircraft_in_approach_count / capacity_threshold).

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.observed_at` | `string` | `ISO-8601 UTC` | `temporal_dimension` | Timestamp of the OpenSky state-vector snapshot. |
| `refined_data.total_aircraft_in_ionian_bbox` | `integer` | `aircraft` | `context_metric` | Total aircraft detected in the Ionian Sea bounding box (26). |
| `refined_data.airports.<IATA>.aircraft_in_approach_count` | `integer` | `aircraft` | `input_variable` | Aircraft within 25 km radius and <=3,000 m altitude of the airport. |
| `refined_data.airports.<IATA>.capacity_threshold` | `integer` | `aircraft` | `input_variable` | Approach buffer saturation threshold (CFU=4, ZTH=3, EFL=3, PVK=3). |
| `refined_data.airports.<IATA>.congestion_score` | `number` | `score (0-1)` | `target_indicator` | Normalized airport approach congestion score S = min(1.0, count / threshold). |
| `refined_data.airports.<IATA>.congestion_level` | `string` | `category` | `context_metric` | Qualitative congestion band (low < 0.50, medium < 0.85, high >= 0.85). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OpenSky:Data06:airport_congestion:CFU:2026-10-20T10:55:16+00:00` | `2026-10-20T10:55:16+00:00` | `transport_node/CFU` | **0.0** | `score (0-1)` | `instant` |
| `OpenSky:Data06:airport_congestion:ZTH:2026-10-20T10:55:16+00:00` | `2026-10-20T10:55:16+00:00` | `transport_node/ZTH` | **0.0** | `score (0-1)` | `instant` |
| `OpenSky:Data06:airport_congestion:EFL:2026-10-20T10:55:16+00:00` | `2026-10-20T10:55:16+00:00` | `transport_node/EFL` | **0.333** | `score (0-1)` | `instant` |
| `OpenSky:Data06:airport_congestion:PVK:2026-10-20T10:55:16+00:00` | `2026-10-20T10:55:16+00:00` | `transport_node/PVK` | **0.0** | `score (0-1)` | `instant` |
