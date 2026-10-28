# Data24 — Protected land (%)

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/raw/gisco-nuts-2021-3035-EL62.geojson [.geojson]  ──( scripts/verification/pull-data02-bathing-water-el62.py )──>  refined-data.json [.json]
  data/raw/eea-natura2000-el62-envelope-habitats-4326.geojson [.geojson]  ──( scripts/verification/compute-data24-protected-land.py )──>  refined-data.json [.json]
  data/raw/eea-natura2000-el62-envelope-birds-4326.geojson [.geojson]  ──( scripts/verification/compute-data24-protected-land.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** —
- **Category:** `spatial_sustainability`
- **Refresh Cadence:** `on-change`
- **Raw Input File Extension(s):** `.geojson`
- **Primary Conversion / Builder Script:** `scripts/verification/compute-data24-protected-land.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `1`

## 1. Overview & Key Note

Spatial join complete: Natura 2000 Habitats ∪ Birds clipped to EL62 land (GISCO NUTS 2021, EPSG:3035), terrestrial split via land-polygon intersection. EL62 protected land = 386.41 km² of 2,304.87 km² = 16.76% (published EL62 area 2,307 km², delta -0.09%). Echinades islets captured via a GR23-coded Acheloos-delta site (1,608 ha) that overlaps EL62 - confirms clip-to-EL62 (not GR22 filter) is required. Evidence: data/curated/data24-protected-land.json + data/manifests/source-verification-2026-10-03.json.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `Eurostat_GISCO_NUTS_2021` (Eurostat GISCO)
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

### Source 2: `EEA_ArcGIS_ProtectedSites_Natura2000_Habitats` (European Environment Agency (EEA) — Natura 2000 Discomap ArcGIS REST)
- **Upstream URL:** `https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer/0/query`
- **Access Method:** `GET (ArcGIS REST GeoJSON query via scripts/verification/pull-data24-protected-land.py)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eea-natura2000-el62-envelope-habitats-4326.geojson`
- **Raw File Extension & Format:** `.geojson` — `application/geo+json (34 polygon features in EPSG:4326)`
- **SHA-256 Checksum:** `f3ea28641afac9d75171d7799febc6c902071137cd23fb4422bb8c8a8aa2d756` (verified in `data/manifests/source-verification-2026-10-03.json`)
- **Conversion Script (`.geojson` -> `.json`):** `scripts/verification/compute-data24-protected-land.py`
- **Conversion Command:** `python3 scripts/verification/compute-data24-protected-land.py`
- **Whitelisted Raw Variables (`kept`):** `SITECODE`, `SITENAME`, `Area_ha`, `geometry`
- **Dropped / Redacted Fields:** `marine_portion_outside_EL62_land_polygon`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `properties.SITECODE` | Natura 2000 site identifier (e.g. 'GR2210001', 'GR2310001') |
| `properties.SITENAME` | Official site name |
| `properties.Area_ha` | Total site area including marine waters (hectares) |
| `geometry` | Polygon/MultiPolygon site boundary |

### Source 3: `EEA_ArcGIS_ProtectedSites_Natura2000_Birds` (European Environment Agency (EEA) — Natura 2000 Discomap ArcGIS REST)
- **Upstream URL:** `https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer/1/query`
- **Access Method:** `GET (ArcGIS REST GeoJSON query via scripts/verification/pull-data24-protected-land.py)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/raw/eea-natura2000-el62-envelope-birds-4326.geojson`
- **Raw File Extension & Format:** `.geojson` — `application/geo+json (25 polygon features in EPSG:4326)`
- **SHA-256 Checksum:** `1f4966760df6cabcec4f49101b6685be02a9023d714828e30069f5aad6fe212d` (verified in `data/manifests/source-verification-2026-10-03.json`)
- **Conversion Script (`.geojson` -> `.json`):** `scripts/verification/compute-data24-protected-land.py`
- **Conversion Command:** `python3 scripts/verification/compute-data24-protected-land.py`
- **Whitelisted Raw Variables (`kept`):** `SITECODE`, `SITENAME`, `Area_ha`, `geometry`
- **Dropped / Redacted Fields:** `marine_portion_outside_EL62_land_polygon`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `properties.SITECODE` | Natura 2000 SPA site identifier |
| `properties.SITENAME` | Official site name |
| `properties.Area_ha` | Total SPA area including marine waters (hectares) |
| `geometry` | Polygon/MultiPolygon site boundary |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Reproject EEA Natura 2000 Habitats (34 envelope sites) and Birds (25 envelope sites) polygons to equal-area EPSG:3035 via `scripts/verification/compute-data24-protected-land.py`, intersect with Eurostat GISCO EL62 land polygon (removing marine waters and capturing the 1,608.2 ha Echinades/Petalas islets under GR23-coded Acheloos sites), dissolve union(Habitats U Birds), and compute protected_land_pct = combined_protected_land_ha / el62_land_ha * 100.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.el62_land_km2` | `number` | `km²` | `input_variable` | Total terrestrial area of EL62 polygon in EPSG:3035 (2,304.87 km²). |
| `refined_data.habitats_protected_land_ha` | `number` | `ha` | `input_variable` | Terrestrial area under Habitats Directive (pSCI/SAC) within EL62 (22,049.2 ha). |
| `refined_data.birds_protected_land_ha` | `number` | `ha` | `input_variable` | Terrestrial area under Birds Directive (SPA) within EL62 (29,744.22 ha). |
| `refined_data.combined_protected_land_km2` | `number` | `km²` | `input_variable` | De-duplicated union of Habitats and Birds terrestrial area in EL62 (386.41 km²). |
| `refined_data.protected_land_pct` | `number` | `%` | `target_indicator` | Share of EL62 terrestrial area protected under Natura 2000 (16.76%). |
| `refined_data.nongr22_sites_with_land_overlap` | `array` | `ha` | `quality_metric` | Completeness audit showing GR23 Acheloos-delta sites overlapping EL62 via Echinades islets (1,608.2 ha). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EEA_Natura2000:Data24:protected_land_pct:2026` | `2026` | `NUTS2/EL62` | **16.76** | `%` | `annual` |
