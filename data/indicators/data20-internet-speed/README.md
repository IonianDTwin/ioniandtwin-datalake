# Data20 — Internet speed (>100 Mb/s)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/ookla-performance-fixed-2024Q3.zip [.zip (Shapefile)]  ──( scripts/verification/compute-data20-internet-speed.py )──>  refined-data.json [.json]
  data/raw/ookla-performance-mobile-2024Q3.zip [.zip (Shapefile)]  ──( scripts/verification/compute-data20-internet-speed.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `digital_infrastructure`
- **Refresh Cadence:** `quarterly`
- **Raw Input File Extension(s):** `.zip (Shapefile)`
- **Primary Conversion / Builder Script:** `scripts/verification/compute-data20-internet-speed.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `4`

## 1. Overview & Key Note

VERIFIED 2026-10-20: Ookla 2024-Q3 performance slippy-map tiles clipped to GISCO EL62 polygon via scripts/verification/compute-data20-internet-speed.py. EL62 test-weighted download: 42.29 Mbps (fixed, 41,552 tests) and 107.48 Mbps (mobile, 11,296 tests). Evidence: data/manifests/source-verification-2026-10-20.json.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Ookla_OpenData_fixed` (Ookla (Speedtest Global Performance Open Data on AWS S3))
- **Upstream URL:** `https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=fixed/year=2024/quarter=3/2024-07-01_performance_fixed_tiles.zip`
- **Access Method:** `GET (AWS S3 public shapefile ZIP archive)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/ookla-performance-fixed-2024Q3.zip`
- **Raw File Extension & Format:** `.zip (Shapefile)` — `application/zip containing ESRI Shapefile (gps_fixed_tiles.shp, 240 MB)`
- **SHA-256 Checksum:** `00b610cfcbc8d58ae4856fdbe2f69ebdd06df2b27ab6dd79452ce092df39de8e` (verified in `data/manifests/source-verification-2026-10-20.json`)
- **Conversion Script (`.zip (Shapefile)` -> `.json`):** `scripts/verification/compute-data20-internet-speed.py`
- **Conversion Command:** `python3 scripts/verification/compute-data20-internet-speed.py`
- **Whitelisted Raw Variables (`kept`):** `avg_d_kbps`, `avg_u_kbps`, `avg_lat_ms`, `tests`, `devices`, `geometry`
- **Dropped / Redacted Fields:** `quadkey`, `tiles_outside_EL62`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `quadkey` | Zoom-16 Bing Maps slippy-map tile identifier |
| `avg_d_kbps` | Mean download throughput in tile (kilobits/sec) |
| `avg_u_kbps` | Mean upload throughput in tile (kilobits/sec) |
| `avg_lat_ms` | Mean round-trip latency in tile (milliseconds) |
| `tests` | Number of Speedtest measurements taken in tile |
| `devices` | Unique testing devices in tile |
| `geometry` | WGS84 tile polygon |

### Source 2: `Ookla_OpenData_mobile` (Ookla (Speedtest Global Performance Open Data on AWS S3))
- **Upstream URL:** `https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=mobile/year=2024/quarter=3/2024-07-01_performance_mobile_tiles.zip`
- **Access Method:** `GET (AWS S3 public shapefile ZIP archive)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/ookla-performance-mobile-2024Q3.zip`
- **Raw File Extension & Format:** `.zip (Shapefile)` — `application/zip containing ESRI Shapefile (gps_mobile_tiles.shp, 138 MB)`
- **SHA-256 Checksum:** `08f8a3d4c1cae257f69416474455033851f6fdab472dba628c23b7e69c1828f5` (verified in `data/manifests/source-verification-2026-10-20.json`)
- **Conversion Script (`.zip (Shapefile)` -> `.json`):** `scripts/verification/compute-data20-internet-speed.py`
- **Conversion Command:** `python3 scripts/verification/compute-data20-internet-speed.py`
- **Whitelisted Raw Variables (`kept`):** `avg_d_kbps`, `avg_u_kbps`, `avg_lat_ms`, `tests`, `devices`, `geometry`
- **Dropped / Redacted Fields:** `quadkey`, `tiles_outside_EL62`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `quadkey` | Zoom-16 Bing Maps slippy-map tile identifier |
| `avg_d_kbps` | Mean mobile download throughput in tile (kilobits/sec) |
| `avg_u_kbps` | Mean mobile upload throughput in tile (kilobits/sec) |
| `avg_lat_ms` | Mean mobile round-trip latency in tile (milliseconds) |
| `tests` | Number of mobile Speedtest measurements in tile |
| `devices` | Unique mobile testing devices in tile |
| `geometry` | WGS84 tile polygon |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Spatially join Ookla 2024-Q3 zoom-16 slippy-map tile shapefiles (fixed and mobile) against the Eurostat GISCO NUTS2 EL62 polygon via `scripts/verification/compute-data20-internet-speed.py`. Compute test-weighted mean download/upload throughput in Mbps: sum(avg_d_kbps * tests) / sum(tests) / 1000.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.networks.<type>.regional_nuts2_el62.tiles_count` | `integer` | `tiles` | `quality_metric` | Number of Ookla zoom-16 tiles intersecting EL62 (fixed=2,795; mobile=1,880). |
| `refined_data.networks.<type>.regional_nuts2_el62.tests_count` | `integer` | `tests` | `input_variable` | Total Speedtest measurements inside EL62 tiles (fixed=41,552; mobile=11,296). |
| `refined_data.networks.<type>.regional_nuts2_el62.weighted_avg_download_mbps` | `number` | `Mbps` | `target_indicator` | Test-weighted mean download speed across EL62 (fixed=42.29 Mbps; mobile=107.48 Mbps). |
| `refined_data.networks.<type>.regional_nuts2_el62.weighted_avg_upload_mbps` | `number` | `Mbps` | `target_indicator` | Test-weighted mean upload speed across EL62 (fixed=9.55 Mbps; mobile=15.31 Mbps). |
| `refined_data.networks.<type>.regional_nuts2_el62.weighted_avg_latency_ms` | `number` | `ms` | `context_metric` | Test-weighted mean round-trip latency across EL62 (fixed=49.6 ms; mobile=59.1 ms). |
| `refined_data.networks.<type>.by_nuts3_island` | `object` | `Mbps` | `internal_disaggregation` | Per-island (EL621..EL624) download, upload, latency, and test counts. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Ookla_OpenData:Data20:fixed_download_mbps:2024-Q3` | `2024-07-01` | `NUTS2/EL62` | **42.29** | `Mbps` | `quarterly` |
| `Ookla_OpenData:Data20:fixed_upload_mbps:2024-Q3` | `2024-07-01` | `NUTS2/EL62` | **9.55** | `Mbps` | `quarterly` |
| `Ookla_OpenData:Data20:mobile_download_mbps:2024-Q3` | `2024-07-01` | `NUTS2/EL62` | **107.48** | `Mbps` | `quarterly` |
| `Ookla_OpenData:Data20:mobile_upload_mbps:2024-Q3` | `2024-07-01` | `NUTS2/EL62` | **15.31** | `Mbps` | `quarterly` |
