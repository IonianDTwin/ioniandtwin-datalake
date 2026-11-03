#!/usr/bin/env python3
"""Build and verify the Option A per-indicator folders (data/indicators/data01..data34).

Industry Best Practice (Medallion / Bronze-Silver-Gold Separation of Concerns):
Every indicator directory `data/indicators/dataXX-<slug>/` contains exactly 3 files:
  1. `raw-source-description.json` (Bronze / Upstream Contract):
     - Direct upstream URL(s), provider name, access method, local `data/raw/` or
       `data/samples/` file path, SHA-256 checksum, raw file format (`.csv`, `.zip`,
       `.nc`, `.geojson`, `.json`), raw schema description, whitelisted raw fields
       (`raw_variables_kept`), dropped/redacted fields (`raw_variables_dropped`), and
       the exact `conversion_script` + `conversion_command` that converts the raw file
       into JSON.
  2. `refined-data.json` (Silver/Gold Curated Payload):
     - Self-describing JSON containing the indicator's metadata, upstream source links,
       `conversion_script` reference, `transformation_rule`, `feature_dictionary`
       (type, unit, role, description for every key), `refined_data` (rich structured
       summary/breakdown), and `observations` (strict `schemas/observation-schema.json`
       compliant records).
  3. `README.md` (Human & Agent Companion Reference):
     - Clear tables showing (1) Raw Source & Conversion Script, (2) Raw Schema &
       Variable Whitelist, (3) Refined Data Feature Dictionary, and (4) Normalized
       Observations.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # verification refuses to pass without a real schema validator
    jsonschema = None

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
INDICATORS_DIR = DATA / "indicators"
CURATED_DIR = DATA / "curated"
SAMPLES_DIR = DATA / "samples"
SCHEMA_PATH = ROOT / "schemas" / "observation-schema.json"
# Single source of truth for observations (rebuilt by build_dashboard.py; D-026 added the Data29 series).
MASTER_SNAPSHOT = "observations-2026-11-03.json"
# Observation files kept OUTSIDE the master snapshot but merged into their indicator folder:
# Data07 daily forecasts (PROPOSAL) and Data29 monthly nights (owner decision 2026-11-03).
SEPARATE_OBS_FILES = {
    "Data07": ["observations-data07-anticipated-congestion-2026-10-14.json"],
    "Data29": ["monthly-data29-nights-2026-11-03.json"],
}


def curated_file_problems() -> list[str]:
    """Missing separate files, and observation files in data/curated that nothing consumes (review F4)."""
    problems = [f"separate observation file missing: data/curated/{n}"
                for names in SEPARATE_OBS_FILES.values() for n in names if not (CURATED_DIR / n).exists()]
    merged = ("observations-data06-airport-congestion-", "observations-data19-platform-rental-share-",
              "observations-data20-internet-speed-", "observations-data02-bathing-water-",
              "observations-data29-seasonality-", "observations-data05-certifications-",
              "observations-data15-air-quality-")          # build_dashboard.py additional_series_observations()
    listed = {n for names in SEPARATE_OBS_FILES.values() for n in names}
    for p in sorted(CURATED_DIR.glob("*.json")):
        n = p.name
        if not (n.startswith("observations-") or n.startswith("monthly-")):
            continue
        if n == MASTER_SNAPSHOT or n in listed or n.startswith(merged):
            continue
        problems.append(f"orphan observation file (not merged, not checked): data/curated/{n}")
    return problems


def load_separate_obs() -> list[dict]:
    out: list[dict] = []
    for iid, names in SEPARATE_OBS_FILES.items():
        for name in names:
            if not (CURATED_DIR / name).exists():
                continue                                   # reported by curated_file_problems()
            for o in load_json(CURATED_DIR / name):
                if o.get("indicator_id") != iid:
                    raise ValueError(f"{name}: observation {o.get('observation_id')} is not {iid}")
                out.append(o)
    return out
MAP_PATH = ROOT / "indicators" / "source-indicator-map.json"

SLUGS = {
    "Data01": "data01-airport-co2",
    "Data02": "data02-bathing-water",
    "Data03": "data03-clean-beach-water",
    "Data04": "data04-blue-flags",
    "Data05": "data05-emas-ecolabel",
    "Data06": "data06-airport-congestion",
    "Data07": "data07-port-congestion",
    "Data08": "data08-road-congestion",
    "Data09": "data09-beach-congestion",
    "Data10": "data10-city-congestion",
    "Data11": "data11-ktel-bus-congestion",
    "Data12": "data12-urban-transit-congestion",
    "Data13": "data13-weather-conditions",
    "Data14": "data14-uv-index",
    "Data15": "data15-air-quality",
    "Data16": "data16-tourism-intensity",
    "Data17": "data17-hospital-infrastructure-congestion",
    "Data18": "data18-power-water-outage",
    "Data19": "data19-short-term-rental-share",
    "Data20": "data20-internet-speed",
    "Data21": "data21-4g-5g-availability",
    "Data22": "data22-tourist-diversity",
    "Data23": "data23-cultural-assets-density",
    "Data24": "data24-protected-land",
    "Data25": "data25-high-nature-value-accommodation",
    "Data26": "data26-arrivals-overnight-stays",
    "Data27": "data27-tourism-capacity-beds",
    "Data28": "data28-occupancy-rate",
    "Data29": "data29-seasonality",
    "Data30": "data30-average-length-of-stay",
    "Data31": "data31-tourism-density",
    "Data32": "data32-dominant-tourism-typology",
    "Data33": "data33-foreign-tourist-share",
    "Data34": "data34-user-feedback",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _jsonschema_version() -> str:
    from importlib.metadata import version
    return version("jsonschema")


def manifest_hashes() -> dict[str, set[str]]:
    """Map manifest file name -> every sha256 it records (any checksum field, plus .sha256 lists)."""
    out: dict[str, set[str]] = {}
    for f in sorted(glob.glob(str(DATA / "manifests" / "*.json"))):
        hashes: set[str] = set()
        doc = load_json(Path(f))
        for e in doc.get("evidence", []) if isinstance(doc, dict) else []:
            if isinstance(e, dict):
                for k in ("checksum_sha256", "sample_checksum_sha256"):
                    if e.get(k):
                        hashes.add(e[k])
        out[Path(f).name] = hashes
    for f in sorted(glob.glob(str(DATA / "manifests" / "*.sha256"))):
        out[Path(f).name] = {ln.split()[0] for ln in Path(f).read_text().splitlines() if ln.strip()}
    return out


def build_specs(master_obs: list[dict], extra_obs: list[dict]) -> dict[str, dict]:
    """Return per-indicator raw source descriptions, conversion refs, and refined data."""
    cams_summary = load_json(SAMPLES_DIR / "cams-ionian-20260930-summary.json")
    bwd_el62 = load_json(CURATED_DIR / "data02-bathing-water-el62-2024.json")
    bwd_series = load_json(SAMPLES_DIR / "eea-bathing-water-EL-1990-2024.json")
    bwd_qual = load_json(SAMPLES_DIR / "eea-bathing-water-quality-EL-2024.json")
    eutd_el62 = load_json(SAMPLES_DIR / "eutd-tourism-dashboard-2024-el62.json")
    emas_gr = load_json(SAMPLES_DIR / "emas-register-greece-2026-10-02.json")
    ecolabel_gr = load_json(SAMPLES_DIR / "eu-ecolabel-catalogue-greece-2026-10-02.json")
    d06_audit = load_json(CURATED_DIR / "data06-airport-congestion.json")
    d07_sched = load_json(CURATED_DIR / "scheduled-port-traffic-el62.json")
    open_meteo = load_json(SAMPLES_DIR / "open-meteo-corfu-forecast-2026-09-22.json")
    d19_audit = load_json(CURATED_DIR / "data19-platform-rental-share.json")
    d20_audit = load_json(CURATED_DIR / "data20-internet-speed.json")
    d22_derived = load_json(SAMPLES_DIR / "derived-data22-data25-2021-2025.json")
    d24_audit = load_json(CURATED_DIR / "data24-protected-land.json")
    elstat_beds = load_json(SAMPLES_DIR / "elstat-sto12-ionian-bedplaces-2021-2025.json")
    d28_derived = load_json(SAMPLES_DIR / "derived-data28-nights-per-hotel-bed-index-2021-2025.json")

    obs_by_ind: dict[str, list[dict]] = {f"Data{i:02d}": [] for i in range(1, 35)}
    for o in master_obs + extra_obs:
        obs_by_ind.setdefault(o["indicator_id"], []).append(o)

    def obs_series_dict(iid: str) -> list[dict]:
        return [
            {
                "observation_id": o["observation_id"],
                "series_label": o.get("series_label"),
                "observed_at": o["observed_at"],
                "spatial_level": o["spatial_ref"]["level"],
                "spatial_code": o["spatial_ref"]["code"],
                "value": o["value"],
                "unit": o["unit"],
            }
            for o in obs_by_ind.get(iid, [])
        ]

    # Reusable source descriptors
    def eutd_source(code: str, year: int) -> dict:
        return {
            "source_id": "EU_Tourism_Dashboard_2024",
            "provider": "European Commission / Joint Research Centre (JRC) — EU Tourism Dashboard",
            "upstream_url": "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv",
            "access_method": "GET (public CSV bulk export)",
            "raw_file_path": "data/raw/eutd-tourism-dashboard-2024-indicators.csv",
            "raw_format": "text/csv (UTF-8, comma-delimited, 81,939 rows)",
            "manifest": "data/manifests/source-verification-2026-10-03.json",
            "sha256": "ab45bb4b2b0b831df183684a05adb52f5bca0270d3b90f1993af0bd77d35aa12",
            "raw_schema_description": {
                "pillar": "Dashboard sustainability pillar ('Green', 'Digital', 'Socio-economic', 'Basic descriptors')",
                "code": f"Indicator code (filtered to '{code}')",
                "indicator": "Human-readable indicator title in the JRC export",
                "year": f"Reference calendar year (filtered to {year})",
                "nuts_code_2021": "Eurostat NUTS 2021 code (filtered to 'EL62' Ionian Islands)",
                "unit": "Unit of measure string",
                "value": "Numeric indicator value",
            },
            "raw_variables_kept": [f"code ('{code}')", "nuts_code_2021 ('EL62')", f"year ({year})", "value", "unit"],
            "raw_variables_dropped": ["pillar", "component", "non_EL62_rows", "other_indicator_codes"],
            "conversion_script": "scripts/verification/extract-eutd-dashboard-csv.py",
            "conversion_command": "python3 scripts/verification/extract-eutd-dashboard-csv.py && python3 scripts/verification/build_indicator_folders.py",
        }

    nin2_source = {
        "source_id": "Eurostat_tour_occ_nin2",
        "provider": "Eurostat (European Commission)",
        "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023",
        "access_method": "GET (SDMX 2.1 / JSON-stat 2.0 REST API, no key)",
        "raw_file_path": "data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json",
        "raw_format": "application/json (SDMX 2.1 JSON-stat 2.0 cube)",
        "manifest": "data/manifests/source-verification-2026-09-22.json",
        "sha256": "46821a04c9061b605a1e324f9af55e87dba73856fd190dcb7e78ae8bc75f860d",
        "raw_schema_description": {
            "id": "Ordered array of cube dimensions: ['freq', 'c_resid', 'unit', 'nace_r2', 'geo', 'time']",
            "size": "Array of dimension cardinalities used for flat-index decoding",
            "dimension.c_resid": "Country of residence ('TOTAL', 'DOM', 'FOR')",
            "dimension.unit": "Unit ('NR' nights, 'P_THAB' nights/1000 residents, 'P_KM2' nights/km2, 'PC_TOT' % share)",
            "dimension.nace_r2": "Accommodation NACE Rev. 2 activity ('I551-I553' total, 'I551' hotels, 'I552' short-stay, 'I553' camping)",
            "dimension.geo": "NUTS2 code ('EL62' = Ionia Nisia)",
            "dimension.time": "Reference year ('2022', '2023')",
            "value": "Sparse map {flat_index_string: numeric_value}",
        },
        "raw_variables_kept": ["dimension.c_resid", "dimension.unit", "dimension.nace_r2", "dimension.geo (EL62)", "dimension.time", "value"],
        "raw_variables_dropped": ["status_flags", "PCH_PRE (year-on-year % change unit)"],
        "conversion_script": "scripts/verification/build_dashboard.py (via render_pull_reports.decode)",
        "conversion_command": "bash scripts/verification/pull-eurostat-tourism.sh && python3 scripts/verification/build_dashboard.py && python3 scripts/verification/build_indicator_folders.py",
    }

    specs: dict[str, dict] = {}

    # Data01
    specs["Data01"] = {
        "conversion_script": "scripts/verification/extract-cams-summary.py (NetCDF zip -> data/samples/cams-ionian-20260930-summary.json)",
        "raw_sources": [
            {
                "source_id": "CAMS_ADS_air_quality",
                "provider": "Copernicus Atmosphere Monitoring Service (CAMS) — Atmosphere Data Store (ADS)",
                "upstream_url": "https://ads.atmosphere.copernicus.eu/api/retrieve/v1/processes/cams-europe-air-quality-forecasts/execution",
                "access_method": "POST via cads-api-client (CAMS_API_KEY in untracked .env)",
                "raw_file_path": "data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip",
                "raw_format": "application/zip containing NetCDF classic (ENS_ANALYSIS.nc)",
                "manifest": "data/manifests/source-verification-2026-10-01.json",
                "sha256": "ecc26d470cdfa5c9ecd65b7dd6b1104e8692d23b998083a402951ddaa9d11574",
                "raw_schema_description": {
                    "longitude": "1D float array (30 grid cells, 19.0E to 22.0E, 0.1 deg resolution)",
                    "latitude": "1D float array (35 grid cells, 37.0N to 40.5N, 0.1 deg resolution)",
                    "level": "Vertical altitude level in meters (filtered to surface 0 m)",
                    "time": "Analysis timestamp (2026-09-30T00:00:00Z)",
                    "no2_conc": "Surface nitrogen dioxide concentration (ug/m3)",
                    "co_conc": "Surface carbon monoxide concentration (ug/m3)",
                    "pm10_conc": "Surface PM10 concentration (ug/m3)",
                    "pm2p5_conc": "Surface PM2.5 concentration (ug/m3)",
                },
                "raw_variables_kept": ["no2_conc", "co_conc", "pm10_conc", "pm2p5_conc", "latitude", "longitude", "level", "time"],
                "raw_variables_dropped": ["upper_level_layers (filtered to surface level=0)"],
                "conversion_script": "scripts/verification/extract-cams-summary.py",
                "conversion_command": "python3 scripts/verification/extract-cams-summary.py --check && python3 scripts/verification/build_indicator_folders.py",
                "lineage_note": "The summary JSON was first produced ad hoc on 2026-10-01 without a retained script. scripts/verification/extract-cams-summary.py (2026-11-03) reproduces all 12 summary values from the retained zip.",
            }
        ],
        "transformation_rule": "Slice CAMS European regional ensemble analysis NetCDF grid (37.0-40.5N, 19.0-22.0E, level=0m) at the 0.1-degree grid cell centred 39.65N 19.95E (the cell nearest Corfu International Airport, approx. 39.60N 19.91E) and compute regional mean/max over all 35x30 cells (scripts/verification/extract-cams-summary.py). Note: CAMS regional does not include CO2; NO2 and CO are retained as combustion proxies while point CO2 awaits local IoT sensors.",
        "feature_dictionary": {
            "refined_data.corfu_airport.lat": {"type": "number", "unit": "degrees_north", "role": "spatial_dimension", "description": "Latitude of nearest CAMS grid cell to Corfu Airport (CFU)."},
            "refined_data.corfu_airport.lon": {"type": "number", "unit": "degrees_east", "role": "spatial_dimension", "description": "Longitude of nearest CAMS grid cell to Corfu Airport (CFU)."},
            "refined_data.values_ug_m3.NO2.at_corfu_airport": {"type": "number", "unit": "ug/m3", "role": "proxy_indicator", "description": "Surface NO2 concentration at Corfu Airport grid cell (combustion proxy for airport emissions)."},
            "refined_data.values_ug_m3.CO.at_corfu_airport": {"type": "number", "unit": "ug/m3", "role": "proxy_indicator", "description": "Surface CO concentration at Corfu Airport grid cell."},
            "refined_data.values_ug_m3.PM10.at_corfu_airport": {"type": "number", "unit": "ug/m3", "role": "context_metric", "description": "Surface PM10 concentration at Corfu Airport grid cell."},
            "refined_data.values_ug_m3.PM2.5.at_corfu_airport": {"type": "number", "unit": "ug/m3", "role": "context_metric", "description": "Surface PM2.5 concentration at Corfu Airport grid cell."},
        },
        "data": cams_summary,
    }

    # Data02
    specs["Data02"] = {
        "conversion_script": "scripts/verification/pull-data02-bathing-water-el62.py",
        "raw_sources": [
            {
                "source_id": "EEA_BWD_Discomap_2024",
                "provider": "European Environment Agency (EEA) — Water Discomap ArcGIS REST",
                "upstream_url": "https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2024/MapServer/3/query?where=countryCode%3D%27EL%27&outFields=*&f=geojson",
                "access_method": "GET (ArcGIS REST GeoJSON query, no key)",
                "raw_file_path": "data/raw/eea-bwd-greece-2024.geojson",
                "raw_format": "application/geo+json (1,729 Point features across Greece)",
                "manifest": "data/manifests/source-verification-2026-10-20.json",
                "sha256": "ae444f3a26aa9b206c134b1e5a03fc9dd808dabb1c078d498ed3e0d28a04c5bf",
                "raw_schema_description": {
                    "properties.countryCode": "ISO country code ('EL')",
                    "properties.bathingWaterIdentifier": "Unique WISE bathing water station ID",
                    "properties.quality2024": "2024 season classification ('1 - Excellent', '2 - Good', '3 - Sufficient', '4 - Poor', '0 - Not classified')",
                    "geometry": "WGS84 Point coordinates [lon, lat]",
                },
                "raw_variables_kept": ["countryCode", "bathingWaterIdentifier", "quality2024", "lat", "lon", "geometry"],
                "raw_variables_dropped": ["historical_quality_1990_2023_columns", "management_links"],
                "conversion_script": "scripts/verification/pull-data02-bathing-water-el62.py",
                "conversion_command": "python3 scripts/verification/pull-data02-bathing-water-el62.py",
            },
            {
                "source_id": "Eurostat_GISCO_NUTS_2021",
                "provider": "Eurostat GISCO",
                "upstream_url": "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_3035_LEVL_2.geojson",
                "access_method": "GET (GeoJSON boundary download)",
                "raw_file_path": "data/raw/gisco-nuts-2021-3035-EL62.geojson",
                "raw_format": "application/geo+json (EPSG:3035 equal-area MultiPolygon)",
                "manifest": "data/manifests/source-verification-2026-10-03.json",
                "sha256": "6b53f249bf425424c0f19eaba403c3183ef378432a6408a0e93e6d9d1fdca35d",
                "raw_schema_description": {
                    "properties.NUTS_ID": "NUTS2 code ('EL62')",
                    "properties.NAME_LATN": "Region name ('Ionia Nisia')",
                    "geometry": "MultiPolygon in EPSG:3035 LAEA projection",
                },
                "raw_variables_kept": ["NUTS_ID", "NAME_LATN", "geometry"],
                "raw_variables_dropped": ["CNTR_CODE", "MOUNT_TYPE", "URBN_TYPE", "COAST_TYPE"],
                "conversion_script": "scripts/verification/pull-data02-bathing-water-el62.py",
                "conversion_command": "python3 scripts/verification/pull-data02-bathing-water-el62.py",
            },
            eutd_source("TOUR_ENV_05", 2023),
        ],
        "transformation_rule": "Spatial join of EEA 2024 Greece bathing water monitoring points with Eurostat GISCO EL62 land polygon buffered 3,000 m seaward (EPSG:3035) via scripts/verification/pull-data02-bathing-water-el62.py. Compute pct_excellent_classified = excellent / classified_sites * 100 (170 / 171 = 99.42%) and pct_excellent_total = excellent / total_sites * 100 (170 / 173 = 98.27%). Reconciled with EU Tourism Dashboard TOUR_ENV_05 (2023 EL62 = 98.82%) and national 1990-2024 Discodata SQL series.",
        "feature_dictionary": {
            "refined_data.el62_spatial_join_2024.el62_regional_nuts2.total_sites": {"type": "integer", "unit": "sites", "role": "input_variable", "description": "Total EEA bathing water monitoring points inside the 3 km EL62 coastal buffer (173)."},
            "refined_data.el62_spatial_join_2024.el62_regional_nuts2.classified_sites": {"type": "integer", "unit": "sites", "role": "input_variable", "description": "Classified bathing water sites in EL62 in 2024 (171)."},
            "refined_data.el62_spatial_join_2024.el62_regional_nuts2.excellent": {"type": "integer", "unit": "sites", "role": "input_variable", "description": "Sites rated '1 - Excellent' in EL62 in 2024 (170)."},
            "refined_data.el62_spatial_join_2024.el62_regional_nuts2.pct_excellent_classified": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Share of classified bathing waters in EL62 rated Excellent (99.42%)."},
            "refined_data.el62_spatial_join_2024.by_nuts3_island": {"type": "object", "unit": "sites_and_pct", "role": "internal_disaggregation", "description": "NUTS3 island breakdown (EL621 Zakynthos, EL622 Kerkyra, EL623 Ithaki/Kefallinia, EL624 Lefkada)."},
            "refined_data.dashboard_benchmark_2023": {"type": "object", "unit": "%", "role": "target_indicator", "description": "EU Tourism Dashboard TOUR_ENV_05 2023 value for EL62 (98.82%)."},
            "refined_data.national_series_1990_2024": {"type": "array", "unit": "%", "role": "target_indicator", "description": "35-year national Greece bathing water series from EEA Discodata SQL."},
        },
        "data": {
            "el62_spatial_join_2024": bwd_el62,
            "dashboard_benchmark_2023": eutd_el62["el62"]["excellent_bathing_water"],
            "national_series_1990_2024": bwd_series.get("series", []),
        },
    }

    # Data03
    specs["Data03"] = {
        "conversion_script": "scripts/verification/pull-data02-bathing-water-el62.py",
        "raw_sources": [specs["Data02"]["raw_sources"][0]],
        "transformation_rule": "Under documented ASSUMPTION, 'clean beach water' is operationalized as the share of classified bathing waters meeting at least EU minimum standards: (Excellent + Good + Sufficient) / classified_sites * 100, computed by scripts/verification/pull-data02-bathing-water-el62.py. For EL62 in 2024: (170 + 1 + 0) / 171 = 100.0%. For Greece overall in 2024: (1677 + 15 + 1) / 1694 = 99.94%.",
        "feature_dictionary": {
            "refined_data.el62_2024.classified_sites": {"type": "integer", "unit": "sites", "role": "input_variable", "description": "Total classified bathing water sites in EL62 (171)."},
            "refined_data.el62_2024.pct_clean_water_classified": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Share of classified EL62 sites rated Excellent, Good, or Sufficient (100.0%)."},
            "refined_data.greece_2024_quality_breakdown": {"type": "array", "unit": "sites", "role": "input_variable", "description": "National Greece 2024 quality counts from EEA Discodata SQL."},
        },
        "data": {
            "el62_2024": bwd_el62["el62_regional_nuts2"],
            "greece_2024_quality_breakdown": bwd_qual.get("results", []),
        },
    }

    # Data04
    specs["Data04"] = {
        "conversion_script": "scripts/verification/extract-eutd-dashboard-csv.py",
        "raw_sources": [eutd_source("TOUR_DES_10", 2024)],
        "transformation_rule": "Filter raw CSV `data/raw/eutd-tourism-dashboard-2024-indicators.csv` via `scripts/verification/extract-eutd-dashboard-csv.py` to `code == 'TOUR_DES_10'` ('Blue Flag sites') and `nuts_code_2021 == 'EL62'` (year 2024), then emit schema-validated observation via `scripts/verification/build_dashboard.py`.",
        "feature_dictionary": {
            "refined_data.blue_flag_sites.code": {"type": "string", "unit": "code", "role": "filter_dimension", "description": "EU Tourism Dashboard indicator code (TOUR_DES_10)."},
            "refined_data.blue_flag_sites.year": {"type": "integer", "unit": "year", "role": "temporal_dimension", "description": "Reference year of award count (2024)."},
            "refined_data.blue_flag_sites.value": {"type": "number", "unit": "number", "role": "target_indicator", "description": "Number of Blue Flag awarded beaches/marinas in EL62 (51.0)."},
        },
        "data": {"blue_flag_sites": eutd_el62["el62"]["blue_flag_sites"]},
    }

    # Data05
    specs["Data05"] = {
        "conversion_script": "scripts/verification/compute-data05-certifications.py (observations from the Greece extracts); extraction of the extracts themselves: none retained (2026-10-02)",
        "raw_sources": [
            {
                "source_id": "EMAS_register_REST",
                "provider": "European Commission — EU EMAS Register",
                "upstream_url": "https://webgate.ec.europa.eu/emas2/public/rest/registration/list",
                "access_method": "GET (REST JSON list, no key)",
                "raw_file_path": "data/samples/emas-register-greece-2026-10-02.json",
                "raw_format": "application/json (4,523 EU records filtered to 37 Greece records)",
                "manifest": "data/manifests/source-verification-2026-10-02.json",
                "sha256": "93a97b63c7d8bc59addb9ee8b15c4f449e99acccad1f667d6c7cee66efd6f059",
                "upstream_response_sha256": "c8546768319f2f35796698a729b29c1375995f556b146877dca61ff2678e3288",
                "lineage_note": "The local file is a Greece-only extract (37 records) of the full 14,650,764-byte EU register response. The full response was not retained; its hash is upstream_response_sha256 (manifest checksum_sha256). The extract hash matches the manifest's sample_checksum_sha256, which was updated after the 2026-10-14 PII redaction (commit 640336d). No extraction script was kept.",
                "raw_schema_description": {
                    "registrationNumber": "EMAS registration code (e.g. 'EL-000120')",
                    "organisationName": "Registered legal entity name",
                    "organisationCountryName": "Country name (filtered to 'Greece')",
                    "city": "Municipality / city name (checked against Ionian Islands)",
                    "postalCode": "Postal code (checked against 49xxx/28xxx/29xxx/31xxx Ionian prefixes)",
                    "nacesAsString": "NACE economic activity classification string",
                },
                "raw_variables_kept": ["registrationNumber", "organisationName", "organisationCountryName", "city", "postalCode", "sitesCount", "nacesAsString"],
                "raw_variables_dropped": ["email (GDPR PII, redacted 2026-10-14)", "phone (GDPR PII, redacted 2026-10-14)", "all non-Greece records"],
                "conversion_script": "none retained (ad hoc extraction 2026-10-02)",
                "conversion_command": "none retained; reproduce by re-pulling upstream_url and filtering as in transformation_rule",
            },
            {
                "source_id": "EU_Ecolabel_catalogue_CSV",
                "provider": "European Commission — EU Ecolabel Catalogue",
                "upstream_url": "https://publicstorage.data.env.service.ec.europa.eu/ecolabel/exports/most-recent-export.csv",
                "access_method": "GET (semicolon-delimited CSV export, no key)",
                "raw_file_path": "data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json",
                "raw_format": "text/csv (89,298 rows, semicolon-delimited) -> summarized to JSON",
                "manifest": "data/manifests/source-verification-2026-11-03.json",
                "sha256": "6ed15e62b9fdbe0de4fc00480fe444b222a244ce68e86249f4bf454d9beebe59",
                "upstream_response_sha256": "7a3d424d7d8b031b1516416e923b024cd47b83e3417308870b37334b9235592d",
                "lineage_note": "The local file is a JSON summary of the full 17,153,575-byte CSV export (89,298 licences). The full export was not retained; its hash is upstream_response_sha256 (manifest checksum_sha256). The summary's own hash was first recorded in data/manifests/source-verification-2026-11-03.json from the copy committed in 82bf2f4. No extraction script was kept.",
                "raw_schema_description": {
                    "group_name": "Product/service group (checked for 'Tourist accommodation')",
                    "company_country": "Country of licence holder ('Greece')",
                    "licence_number": "Unique EU Ecolabel licence identifier",
                    "extract_date": "Export snapshot date ('2026-10-01')",
                },
                "raw_variables_kept": ["group_name", "company_country", "licence_number", "extract_date"],
                "raw_variables_dropped": ["vat_number", "company_contact_details"],
                "conversion_script": "none retained (ad hoc extraction 2026-10-02)",
                "conversion_command": "none retained; reproduce by re-pulling upstream_url and filtering as in transformation_rule",
            },
        ],
        "transformation_rule": "Filter EU EMAS REST registration list to organisationCountryName=='Greece' (37 records) and match city/postalCode against Ionian Islands (EL62 = 0 records). Filter EU Ecolabel CSV export (89,298 licences) to Greece (450 licences) and group_name=='Tourist accommodation' (0 in Greece / 0 in EL62). Contact PII (email/phone) stripped before storage.",
        "feature_dictionary": {
            "refined_data.emas.greece_records": {"type": "integer", "unit": "organisations", "role": "context_metric", "description": "Total EMAS-registered organisations in Greece (37)."},
            "refined_data.emas.ionian_islands_el62_records": {"type": "integer", "unit": "organisations", "role": "target_indicator", "description": "Verified EMAS-registered organisations in Ionian Islands EL62 (0)."},
            "refined_data.eu_ecolabel.greece_licences": {"type": "integer", "unit": "licences", "role": "context_metric", "description": "Total EU Ecolabel licences in Greece across all product groups (450)."},
            "refined_data.eu_ecolabel.ionian_islands_el62_tourist_accommodation": {"type": "integer", "unit": "licences", "role": "target_indicator", "description": "Verified EU Ecolabel tourist-accommodation licences in Ionian Islands EL62 (0)."},
        },
        "data": {
            "emas": {k: v for k, v in emas_gr.items() if k != "greece_sample"},
            "emas_greece_sample_count": len(emas_gr.get("greece_sample", [])),
            "eu_ecolabel": ecolabel_gr,
        },
    }

    # Data06
    specs["Data06"] = {
        "conversion_script": "scripts/verification/pull-data06-airport-congestion.py",
        "raw_sources": [
            {
                "source_id": "OpenSky_States_live",
                "provider": "OpenSky Network",
                "upstream_url": "https://opensky-network.org/api/states/all?lamin=37.0&lomin=19.0&lamax=40.5&lomax=22.0",
                "access_method": "GET (anonymous REST JSON API)",
                "raw_file_path": "data/raw/opensky-ionian-states-20261020-105525.json",
                "raw_format": "application/json (OpenSky state-vector array)",
                "manifest": "data/manifests/source-verification-2026-10-20.json",
                "sha256": "9c8b228401c53d74ab25ad92e83264af574613745bb2d7f3586377e5cccb610a",
                "raw_schema_description": {
                    "time": "Unix epoch timestamp of state poll",
                    "states[][0] (icao24)": "24-bit ICAO transponder hex address",
                    "states[][1] (callsign)": "Flight callsign string",
                    "states[][2] (origin_country)": "Aircraft registration country",
                    "states[][5..6] (lon, lat)": "WGS84 longitude and latitude",
                    "states[][7] (baro_altitude)": "Barometric altitude in meters",
                    "states[][8] (on_ground)": "Boolean flag indicating surface status",
                    "states[][9] (velocity)": "Ground speed in m/s",
                },
                "raw_variables_kept": ["icao24", "callsign", "origin_country", "longitude", "latitude", "baro_altitude", "on_ground", "velocity"],
                "raw_variables_dropped": ["sensors", "spi", "position_source", "squawk"],
                "conversion_script": "scripts/verification/pull-data06-airport-congestion.py",
                "conversion_command": "python3 scripts/verification/pull-data06-airport-congestion.py",
            }
        ],
        "transformation_rule": "Filter live OpenSky state vectors in the Ionian bounding box (37.0-40.5N, 19.0-22.0E) via `scripts/verification/pull-data06-airport-congestion.py` to aircraft within a 25 km approach radius and baro_altitude <= 3,000 m (or on_ground=true) of each gateway airport (CFU, ZTH, EFL, PVK). Compute congestion_score = min(1.0, aircraft_in_approach_count / capacity_threshold).",
        "feature_dictionary": {
            "refined_data.observed_at": {"type": "string", "unit": "ISO-8601 UTC", "role": "temporal_dimension", "description": "Timestamp of the OpenSky state-vector snapshot."},
            "refined_data.total_aircraft_in_ionian_bbox": {"type": "integer", "unit": "aircraft", "role": "context_metric", "description": "Total aircraft detected in the Ionian Sea bounding box (26)."},
            "refined_data.airports.<IATA>.aircraft_in_approach_count": {"type": "integer", "unit": "aircraft", "role": "input_variable", "description": "Aircraft within 25 km radius and <=3,000 m altitude of the airport."},
            "refined_data.airports.<IATA>.capacity_threshold": {"type": "integer", "unit": "aircraft", "role": "input_variable", "description": "Approach buffer saturation threshold (CFU=4, ZTH=3, EFL=3, PVK=3)."},
            "refined_data.airports.<IATA>.congestion_score": {"type": "number", "unit": "score (0-1)", "role": "target_indicator", "description": "Normalized airport approach congestion score S = min(1.0, count / threshold)."},
            "refined_data.airports.<IATA>.congestion_level": {"type": "string", "unit": "category", "role": "context_metric", "description": "Qualitative congestion band (low < 0.50, medium < 0.85, high >= 0.85)."},
        },
        "data": d06_audit,
    }

    # Data07
    specs["Data07"] = {
        "conversion_script": "scripts/verification/compute-data07-anticipated-congestion.py",
        "raw_sources": [
            {
                "source_id": "CruiseMapper_schedules",
                "provider": "CruiseMapper (one-time schedule capture; OLKE port authority candidate for production)",
                "upstream_url": "https://www.cruisemapper.com/ports/<port-slug>?month=<yyyy-mm>#schedule",
                "access_method": "One-time bounded read parsed to JSON",
                "raw_file_path": "scratch/cruise-pressure/schedules.json",
                "raw_format": "application/json (117 planned cruise calls across Ionian ports)",
                "manifest": "data/manifests/source-verification-2026-10-14.json",
                "sha256": "1490dd5a7fabf8dc265fafa127cac6cfa77cfba59e15293c1b2c333ea496ae98",
                "raw_schema_description": {
                    "ports[].id": "Port identifier ('corfu', 'kefalonia', 'zakynthos', 'lefkada', 'paxos', 'ithaki')",
                    "ports[].calls[].date": "Planned call date (YYYY-MM-DD)",
                    "ports[].calls[].ship": "Vessel name",
                    "ports[].calls[].arrival / departure": "Scheduled berth arrival and departure window",
                },
                "raw_variables_kept": ["port_id", "date", "ship", "arrival", "departure"],
                "raw_variables_dropped": ["igoumenitsa_mainland_calls (outside EL62)"],
                "conversion_script": "scripts/verification/compute-data07-anticipated-congestion.py",
                "conversion_command": "python3 scripts/verification/compute-data07-anticipated-congestion.py",
            },
            {
                "source_id": "GreekNAP_sailing_traffic",
                "provider": "Greek National Access Point (NAP) — Domestic Ferry Sailing Traffic",
                "upstream_url": "UNDOCUMENTED: Greek National Access Point (NAP) sailing-traffic CSV export; the download address is still to be recorded (open item). Local copy: scratch/ais-routes/export_sailing_traffic.csv",
                "access_method": "CSV bulk export (184,436 domestic ferry legs, Mar-Nov 2025)",
                "raw_file_path": "scratch/ais-routes/export_sailing_traffic.csv",
                "raw_format": "text/csv (184,436 rows)",
                "manifest": "data/manifests/source-verification-2026-10-14.json",
                "sha256": "b756f6eb2c4eac53f996983ee215e0289bfab6fe53827696806abe2393f5fa7b",
                "raw_schema_description": {
                    "date": "Sailing date",
                    "arrivalport": "Destination port code (CFU/LFK, PKE/SAI/FIS, ZTH, VSS/LEV, PAX, PIS)",
                    "passengercount": "Disembarking passenger count on leg",
                    "vehiclecount": "Disembarking vehicle count on leg",
                },
                "raw_variables_kept": ["date", "arrivalport", "passengercount", "vehiclecount"],
                "raw_variables_dropped": ["routecode", "routecodenames", "mainland_arrival_ports (IGO, KYL, GPA)"],
                "conversion_script": "scripts/verification/compute-data07-anticipated-congestion.py",
                "conversion_command": "python3 scripts/verification/compute-data07-anticipated-congestion.py",
            },
        ],
        "transformation_rule": "PROPOSAL (held pending sign-off, D-019): Fuse planned cruise calls with empirical Greek NAP inbound ferry passenger/vehicle daily baselines across 6 EL62 ports via `scripts/verification/compute-data07-anticipated-congestion.py`. S(P,D) = min(1, 0.4*N_ships/B_max + 0.4*(L_cruise+L_ferry_pax)/C_pax + 0.2*L_ferry_veh/C_veh).",
        "feature_dictionary": {
            "refined_data.assumptions.weights": {"type": "object", "unit": "weights", "role": "input_variable", "description": "PROPOSAL formula weights: berth=0.4, pax=0.4, veh=0.2."},
            "refined_data.assumptions.capacities": {"type": "object", "unit": "ships_pax_veh", "role": "input_variable", "description": "PROPOSAL daily port berth, passenger, and vehicle capacity thresholds."},
            "refined_data.forecast_window": {"type": "object", "unit": "ISO-8601 date", "role": "temporal_dimension", "description": "61-day evaluation window (2026-10-01 to 2026-11-30; 366 port-days)."},
            "refined_data.ports[].daily_schedule[].congestion_score": {"type": "number", "unit": "score (0-1)", "role": "target_indicator", "description": "Anticipated daily port congestion score (0.0 to 1.0)."},
        },
        "data": d07_sched,
    }

    # Unverified placeholders
    unverified_defs = {
        "Data08": ("Road congestion", "Google Maps Platform (paid) / OpenRouteService (routing fallback)", "Travel-time delay ratio per road segment (pending live-traffic feed or partner telemetry)."),
        "Data09": ("Beach congestion", "IonianDTwin Mobile App citizen reports", "Aggregated user crowd-density reports per beach polygon, cross-verified before alert generation."),
        "Data10": ("City congestion", "Google Maps Platform + Mobile App citizen reports", "Urban zone traffic delay index fused with geolocated citizen congestion reports."),
        "Data11": ("KTEL (bus) congestion", "Intercity KTEL operator telematics (partner feed)", "Occupancy / delay telemetry per intercity bus route on Corfu, Zakynthos, Kefalonia, Lefkada."),
        "Data12": ("Urban transit congestion", "Municipal bus operator telematics (partner feed)", "Occupancy / headway delay telemetry on municipal transit lines."),
        "Data17": ("Hospital / infrastructure congestion", "Official civil-protection announcements + Mobile App citizen reports", "Healthcare/facility load alerts cross-verified against official announcements."),
        "Data18": ("Power / water outage", "Utility announcements (DEDDIE / municipal water boards) + Mobile App citizen reports", "Geolocated utility outage incident counts and duration per municipality."),
        "Data21": ("4G/5G availability", "Mobile App citizen network-problem reports + Ookla tile coverage", "Share of territory/reports with active 4G/5G connectivity."),
        "Data34": ("User feedback", "TripAdvisor / Google Reviews API + Mobile App feedback", "Sentiment score and topic classification of visitor reviews (deferred on ToS/privacy governance)."),
    }
    for iid, (name, src_desc, rule_desc) in unverified_defs.items():
        specs[iid] = {
            "conversion_script": "None (UNVERIFIED source track — no synthetic data invented)",
            "raw_sources": [],
            "transformation_rule": f"UNVERIFIED source track: {rule_desc} No values are invented.",
            "feature_dictionary": {
                "refined_data.status": {"type": "string", "unit": "enum", "role": "quality_metric", "description": "Verification status ('UNVERIFIED' - no synthetic data emitted)."},
                "refined_data.candidate_source": {"type": "string", "unit": "text", "role": "context_metric", "description": f"Candidate provider: {src_desc}."},
            },
            "data": {
                "status": "UNVERIFIED",
                "candidate_source": src_desc,
                "note": "Intentionally empty until a free public substitute, partner feed, or mobile-app telemetry stream is verified.",
            },
        }

    # Open-Meteo source descriptor for Data13 & Data14
    open_meteo_source = {
        "source_id": "OpenMeteo_forecast",
        "provider": "Open-Meteo (open-meteo.com)",
        "upstream_url": "https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1",
        "access_method": "GET (public REST JSON API, no key)",
        "raw_file_path": "data/samples/open-meteo-corfu-forecast-2026-09-22.json",
        "raw_format": "application/json",
        "manifest": "data/manifests/source-verification-2026-09-22.json",
        "sha256": "e16e6108febd130fbab834a943df510a3d982714d4d7e18a7f01ac5e50f93e23",
        "raw_schema_description": {
            "latitude / longitude": "WGS84 grid coordinate (39.625N, 19.875E for Corfu)",
            "current.time": "ISO-8601 current observation timestamp in Europe/Athens timezone",
            "current.temperature_2m": "Air temperature at 2 meters (°C)",
            "current.relative_humidity_2m": "Relative humidity at 2 meters (%)",
            "current.apparent_temperature": "Feels-like apparent temperature (°C)",
            "daily.uv_index_max": "Daily maximum UV index array",
        },
        "raw_variables_kept": ["latitude", "longitude", "current.time", "current.temperature_2m", "current.relative_humidity_2m", "current.apparent_temperature", "daily.uv_index_max"],
        "raw_variables_dropped": ["generationtime_ms", "utc_offset_seconds", "elevation"],
        "conversion_script": "scripts/verification/pull-open-meteo.sh -> scripts/verification/build_dashboard.py",
        "conversion_command": "bash scripts/verification/pull-open-meteo.sh && python3 scripts/verification/build_dashboard.py && python3 scripts/verification/build_indicator_folders.py",
    }

    # Data13
    specs["Data13"] = {
        "conversion_script": "scripts/verification/pull-open-meteo.sh -> scripts/verification/build_dashboard.py",
        "raw_sources": [open_meteo_source],
        "transformation_rule": "Extract current surface meteorological observations (temperature_2m, relative_humidity_2m, apparent_temperature) at the Corfu reference point (39.62N, 19.92E) via `scripts/verification/build_dashboard.py`.",
        "feature_dictionary": {
            "refined_data.current.time": {"type": "string", "unit": "ISO-8601", "role": "temporal_dimension", "description": "Observation timestamp in Europe/Athens timezone."},
            "refined_data.current.temperature_2m": {"type": "number", "unit": "°C", "role": "target_indicator", "description": "Air temperature at 2 meters above ground (26.5 °C)."},
            "refined_data.current.relative_humidity_2m": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Relative humidity at 2 meters above ground (57%)."},
            "refined_data.current.apparent_temperature": {"type": "number", "unit": "°C", "role": "target_indicator", "description": "Apparent (feels-like) temperature combining wind and humidity (28.8 °C)."},
        },
        "data": {
            "latitude": open_meteo["latitude"],
            "longitude": open_meteo["longitude"],
            "timezone": open_meteo["timezone"],
            "current_units": open_meteo["current_units"],
            "current": open_meteo["current"],
        },
    }

    # Data14
    specs["Data14"] = {
        "conversion_script": "scripts/verification/pull-open-meteo.sh -> scripts/verification/build_dashboard.py",
        "raw_sources": [open_meteo_source],
        "transformation_rule": "Extract daily.uv_index_max for the Corfu reference coordinate (39.62N, 19.92E) from Open-Meteo daily forecast array via `scripts/verification/build_dashboard.py`.",
        "feature_dictionary": {
            "refined_data.daily.time": {"type": "array", "unit": "ISO-8601 date", "role": "temporal_dimension", "description": "Forecast date array (['2026-09-22'])."},
            "refined_data.daily.uv_index_max": {"type": "array", "unit": "UV index", "role": "target_indicator", "description": "Daily maximum UV index ([5.9])."},
        },
        "data": {
            "latitude": open_meteo["latitude"],
            "longitude": open_meteo["longitude"],
            "daily_units": open_meteo["daily_units"],
            "daily": open_meteo["daily"],
        },
    }

    # Data15
    specs["Data15"] = {
        "conversion_script": "scripts/verification/compute-data15-air-quality.py (observations); scripts/verification/extract-cams-summary.py (summary)",
        "raw_sources": [specs["Data01"]["raw_sources"][0], {
            **[rs for rs in specs["Data02"]["raw_sources"] if rs["source_id"] == "Eurostat_GISCO_NUTS_2021"][0],
            "conversion_script": "scripts/verification/compute-data15-air-quality.py",
            "conversion_command": "python3 scripts/verification/compute-data15-air-quality.py && python3 scripts/verification/build_dashboard.py <manifests>",
            "lineage_note": "EL62 land polygon used to area-weight the CAMS 0.1-degree cells (86 cells, 2,304.80 km2 intersected).",
        }],
        "transformation_rule": "Surface NO2, PM10, PM2.5, CO (ug/m3) from the CAMS European ensemble analysis, 2026-09-30T00Z (D-008: Data15 = ambient air quality). Observations (scripts/verification/compute-data15-air-quality.py): EL62 value = mean over 0.1-degree cells weighted by each cell's intersection area with EL62 land (EPSG:3035); point value = cell nearest Corfu airport. refined_data keeps the bounding-box summary (37.0-40.5N, 19.0-22.0E), which includes mainland and sea and is not the EL62 value. Caveat: a CAMS cell holds one concentration for land and sea together; land-area weighting assumes the land part equals the cell value, so for NO2 (cleaner over sea) the EL62 mean may slightly understate land concentrations (unweighted cell mean 2.39 vs weighted 2.67).",
        "feature_dictionary": {
            "refined_data.values_ug_m3.NO2.region_mean": {"type": "number", "unit": "ug/m3", "role": "target_indicator", "description": "Regional mean surface NO2 across the Ionian bounding box (1.96 ug/m3)."},
            "refined_data.values_ug_m3.PM10.region_mean": {"type": "number", "unit": "ug/m3", "role": "target_indicator", "description": "Regional mean surface PM10 across the Ionian bounding box (8.99 ug/m3)."},
            "refined_data.values_ug_m3.PM2.5.region_mean": {"type": "number", "unit": "ug/m3", "role": "target_indicator", "description": "Regional mean surface PM2.5 across the Ionian bounding box (5.76 ug/m3)."},
            "refined_data.values_ug_m3.CO.region_mean": {"type": "number", "unit": "ug/m3", "role": "target_indicator", "description": "Regional mean surface CO across the Ionian bounding box (158.14 ug/m3)."},
        },
        "data": cams_summary,
    }

    # Data16
    specs["Data16"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [nin2_source],
        "transformation_rule": "Filter Eurostat SDMX dataset tour_occ_nin2 via `scripts/verification/build_dashboard.py` to geo='EL62', c_resid='TOTAL', nace_r2='I551-I553', and unit='P_THAB' (nights spent per thousand inhabitants).",
        "feature_dictionary": {
            "refined_data.filter_dims": {"type": "object", "unit": "SDMX codes", "role": "filter_dimension", "description": "Exact SDMX dimension filter: geo=EL62, c_resid=TOTAL, unit=P_THAB, nace_r2=I551-I553."},
            "refined_data.series[].observed_at": {"type": "string", "unit": "year", "role": "temporal_dimension", "description": "Reference calendar year."},
            "refined_data.series[].value": {"type": "number", "unit": "nights per 1000 residents", "role": "target_indicator", "description": "Annual tourism intensity in EL62 (80,912.16 in 2022; 97,705.53 in 2023)."},
        },
        "data": {
            "filter_dims": {"geo": "EL62", "c_resid": "TOTAL", "unit": "P_THAB", "nace_r2": "I551-I553"},
            "extended_2024_2025_note": "Peaked at 103,440 in 2024 and eased to 102,629 in 2025 (D-012).",
            "series": obs_series_dict("Data16"),
        },
    }

    # Data19
    specs["Data19"] = {
        "conversion_script": "scripts/verification/pull-data19-platform-rentals.py",
        "raw_sources": [
            {
                "source_id": "Eurostat_tour_ce_omn12",
                "provider": "Eurostat — Short-stay accommodation offered via online platforms (EC agreement with Airbnb, Booking, Expedia, Tripadvisor)",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_ce_omn12?geo=EL62&indic_to=NGT_SP&c_resid=TOTAL&month=TOTAL&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023&time=2024&time=2025&lang=en",
                "access_method": "GET (JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/raw/eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json",
                "raw_format": "application/json (JSON-stat 2.0 cube)",
                "manifest": "data/manifests/source-verification-2026-10-15.json",
                "sha256": "421338a3a15d9db86ef98b2ff1138e82b3a9c7b7c37aacf27427dca6d998abbd",
                "raw_schema_description": {
                    "dimension.indic_to": "Tourism indicator ('NGT_SP' = Guest nights spent)",
                    "dimension.c_resid": "Guest residence ('TOTAL')",
                    "dimension.month": "Month ('TOTAL' annual or 'M01'..'M12')",
                    "dimension.geo": "NUTS2 code ('EL62')",
                    "dimension.time": "Reference years ('2018'..'2025')",
                    "value": "Sparse map of platform guest nights",
                },
                "raw_variables_kept": ["indic_to (NGT_SP)", "c_resid (TOTAL)", "month (TOTAL)", "geo (EL62)", "time (2018..2025)", "value"],
                "raw_variables_dropped": ["STAY (stays count)", "guest_nights_by_origin_breakdown"],
                "conversion_script": "scripts/verification/pull-data19-platform-rentals.py",
                "conversion_command": "python3 scripts/verification/pull-data19-platform-rentals.py",
            },
            {
                "source_id": "Eurostat_tour_occ_nin2_2018_2025",
                "provider": "Eurostat — Conventional tourist accommodation nights",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?geo=EL62&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023&time=2024&time=2025&lang=en",
                "access_method": "GET (JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json",
                "raw_format": "application/json (JSON-stat 2.0 cube)",
                "manifest": "data/manifests/source-verification-2026-10-15.json",
                "sha256": "474ba9c359e92830964e2ad4d1c83f11d841b2d1e2d8dda20bf66dea9e14f158",
                "raw_schema_description": {
                    "dimension.c_resid": "'TOTAL'",
                    "dimension.unit": "'NR' (number of nights)",
                    "dimension.nace_r2": "'I551-I553'",
                    "dimension.geo": "'EL62'",
                    "dimension.time": "'2018'..'2025'",
                    "value": "Sparse map of conventional accommodation nights",
                },
                "raw_variables_kept": ["c_resid (TOTAL)", "unit (NR)", "nace_r2 (I551-I553)", "geo (EL62)", "time (2018..2025)", "value"],
                "raw_variables_dropped": ["sub_nace_breakdowns"],
                "conversion_script": "scripts/verification/pull-data19-platform-rentals.py",
                "conversion_command": "python3 scripts/verification/pull-data19-platform-rentals.py",
            },
        ],
        "transformation_rule": "D-020: Compute annual short-term rental share for EL62 (2018-2025) via `scripts/verification/pull-data19-platform-rentals.py` as platform_nights / (conventional_nights + platform_nights) * 100.",
        "feature_dictionary": {
            "refined_data.series[].year": {"type": "string", "unit": "year", "role": "temporal_dimension", "description": "Reference year (2018-2025)."},
            "refined_data.series[].platform_nights": {"type": "integer", "unit": "nights", "role": "input_variable", "description": "Guest nights booked via online platforms (tour_ce_omn12)."},
            "refined_data.series[].conventional_nights": {"type": "integer", "unit": "nights", "role": "input_variable", "description": "Guest nights at conventional tourist accommodation (tour_occ_nin2)."},
            "refined_data.series[].total_tourism_nights": {"type": "integer", "unit": "nights", "role": "input_variable", "description": "Combined platform + conventional guest nights in EL62."},
            "refined_data.series[].share_pct": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Platform share of total tourism nights (14.50% in 2018 -> 29.80% in 2025)."},
            "refined_data.seasonality_2025": {"type": "array", "unit": "nights", "role": "context_metric", "description": "2025 monthly platform guest nights showing 52.4% concentration in July-August."},
        },
        "data": d19_audit,
    }

    # Data20
    specs["Data20"] = {
        "conversion_script": "scripts/verification/compute-data20-internet-speed.py",
        "raw_sources": [
            {
                "source_id": "Ookla_OpenData_fixed",
                "provider": "Ookla (Speedtest Global Performance Open Data on AWS S3)",
                "upstream_url": "https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=fixed/year=2024/quarter=3/2024-07-01_performance_fixed_tiles.zip",
                "access_method": "GET (AWS S3 public shapefile ZIP archive)",
                "raw_file_path": "data/raw/ookla-performance-fixed-2024Q3.zip",
                "raw_format": "application/zip containing ESRI Shapefile (gps_fixed_tiles.shp, 240 MB)",
                "manifest": "data/manifests/source-verification-2026-10-20.json",
                "sha256": "00b610cfcbc8d58ae4856fdbe2f69ebdd06df2b27ab6dd79452ce092df39de8e",
                "raw_schema_description": {
                    "quadkey": "Zoom-16 Bing Maps slippy-map tile identifier",
                    "avg_d_kbps": "Mean download throughput in tile (kilobits/sec)",
                    "avg_u_kbps": "Mean upload throughput in tile (kilobits/sec)",
                    "avg_lat_ms": "Mean round-trip latency in tile (milliseconds)",
                    "tests": "Number of Speedtest measurements taken in tile",
                    "devices": "Unique testing devices in tile",
                    "geometry": "WGS84 tile polygon",
                },
                "raw_variables_kept": ["avg_d_kbps", "avg_u_kbps", "avg_lat_ms", "tests", "devices", "geometry"],
                "raw_variables_dropped": ["quadkey", "tiles_outside_EL62"],
                "conversion_script": "scripts/verification/compute-data20-internet-speed.py",
                "conversion_command": "python3 scripts/verification/compute-data20-internet-speed.py",
            },
            {
                "source_id": "Ookla_OpenData_mobile",
                "provider": "Ookla (Speedtest Global Performance Open Data on AWS S3)",
                "upstream_url": "https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=mobile/year=2024/quarter=3/2024-07-01_performance_mobile_tiles.zip",
                "access_method": "GET (AWS S3 public shapefile ZIP archive)",
                "raw_file_path": "data/raw/ookla-performance-mobile-2024Q3.zip",
                "raw_format": "application/zip containing ESRI Shapefile (gps_mobile_tiles.shp, 138 MB)",
                "manifest": "data/manifests/source-verification-2026-10-20.json",
                "sha256": "08f8a3d4c1cae257f69416474455033851f6fdab472dba628c23b7e69c1828f5",
                "raw_schema_description": {
                    "quadkey": "Zoom-16 Bing Maps slippy-map tile identifier",
                    "avg_d_kbps": "Mean mobile download throughput in tile (kilobits/sec)",
                    "avg_u_kbps": "Mean mobile upload throughput in tile (kilobits/sec)",
                    "avg_lat_ms": "Mean mobile round-trip latency in tile (milliseconds)",
                    "tests": "Number of mobile Speedtest measurements in tile",
                    "devices": "Unique mobile testing devices in tile",
                    "geometry": "WGS84 tile polygon",
                },
                "raw_variables_kept": ["avg_d_kbps", "avg_u_kbps", "avg_lat_ms", "tests", "devices", "geometry"],
                "raw_variables_dropped": ["quadkey", "tiles_outside_EL62"],
                "conversion_script": "scripts/verification/compute-data20-internet-speed.py",
                "conversion_command": "python3 scripts/verification/compute-data20-internet-speed.py",
            },
        ],
        "transformation_rule": "Spatially join Ookla 2024-Q3 zoom-16 slippy-map tile shapefiles (fixed and mobile) against the Eurostat GISCO NUTS2 EL62 polygon via `scripts/verification/compute-data20-internet-speed.py`. Compute test-weighted mean download/upload throughput in Mbps: sum(avg_d_kbps * tests) / sum(tests) / 1000.",
        "feature_dictionary": {
            "refined_data.networks.<type>.regional_nuts2_el62.tiles_count": {"type": "integer", "unit": "tiles", "role": "quality_metric", "description": "Number of Ookla zoom-16 tiles intersecting EL62 (fixed=2,795; mobile=1,880)."},
            "refined_data.networks.<type>.regional_nuts2_el62.tests_count": {"type": "integer", "unit": "tests", "role": "input_variable", "description": "Total Speedtest measurements inside EL62 tiles (fixed=41,552; mobile=11,296)."},
            "refined_data.networks.<type>.regional_nuts2_el62.weighted_avg_download_mbps": {"type": "number", "unit": "Mbps", "role": "target_indicator", "description": "Test-weighted mean download speed across EL62 (fixed=42.29 Mbps; mobile=107.48 Mbps)."},
            "refined_data.networks.<type>.regional_nuts2_el62.weighted_avg_upload_mbps": {"type": "number", "unit": "Mbps", "role": "target_indicator", "description": "Test-weighted mean upload speed across EL62 (fixed=9.55 Mbps; mobile=15.31 Mbps)."},
            "refined_data.networks.<type>.regional_nuts2_el62.weighted_avg_latency_ms": {"type": "number", "unit": "ms", "role": "context_metric", "description": "Test-weighted mean round-trip latency across EL62 (fixed=49.6 ms; mobile=59.1 ms)."},
            "refined_data.networks.<type>.by_nuts3_island": {"type": "object", "unit": "Mbps", "role": "internal_disaggregation", "description": "Per-island (EL621..EL624) download, upload, latency, and test counts."},
        },
        "data": d20_audit,
    }

    # Data22
    specs["Data22"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [
            {
                "source_id": "Eurostat_tour_occ_nin3",
                "provider": "Eurostat (European Commission)",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin3?format=JSON&geo=EL621..EL624&c_resid=TOTAL&unit=NR&nace_r2=I551-I553",
                "access_method": "GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/samples/eurostat-tour_occ_nin3-EL621-624-2021-2025.json",
                "raw_format": "application/json (wrapper of 4 NUTS3 SDMX cubes)",
                "manifest": "data/manifests/source-verification-2026-10-01.json",
                "sha256": "ee9c29ff4ecce9aabc23b1b9b360096c004213ed6e2a6b30c257f0934517e916",
                "raw_schema_description": {
                    "EL621..EL624": "Top-level keys for Zakynthos (EL621), Kerkyra (EL622), Ithaki/Kefallinia (EL623), Lefkada (EL624)",
                    "dimension.time": "Reference years ('2021'..'2025')",
                    "value": "Annual overnight stays per NUTS3 island unit",
                },
                "raw_variables_kept": ["geo (EL621, EL622, EL623, EL624)", "c_resid (TOTAL)", "unit (NR)", "nace_r2 (I551-I553)", "time (2021..2025)", "value"],
                "raw_variables_dropped": ["foreign_vs_domestic_split"],
                "conversion_script": "scripts/verification/build_dashboard.py",
                "conversion_command": "python3 scripts/verification/build_dashboard.py --manifest data/manifests/source-verification-2026-10-01.json",
            }
        ],
        "transformation_rule": "D-014 & D-016: Compute NUTS3 island shares s_i = nights_i / sum(nights) across the 4 Ionian NUTS3 units (EL621 Zakynthos, EL622 Kerkyra, EL623 Ithaki/Kefallinia, EL624 Lefkada) via `scripts/verification/build_dashboard.py`, then aggregate to a single NUTS2 EL62 diversity index: Diversity = 1 - sum(s_i^2) (1 - Herfindahl-Hirschman Index).",
        "feature_dictionary": {
            "refined_data.data22_tourist_diversity.<year>.nights": {"type": "object", "unit": "nights", "role": "input_variable", "description": "Total annual overnight stays per NUTS3 island unit."},
            "refined_data.data22_tourist_diversity.<year>.shares": {"type": "object", "unit": "ratio (0-1)", "role": "input_variable", "description": "Fraction of EL62 regional nights hosted by each NUTS3 unit."},
            "refined_data.data22_tourist_diversity.<year>.HHI": {"type": "number", "unit": "index (0-1)", "role": "input_variable", "description": "Herfindahl-Hirschman concentration index sum(s_i^2)."},
            "refined_data.data22_tourist_diversity.<year>.diversity_1_minus_HHI": {"type": "number", "unit": "index (0-1)", "role": "target_indicator", "description": "Regional spatial diversity index 1 - HHI emitted for NUTS2/EL62 (0.631 to 0.651)."},
        },
        "data": {"data22_tourist_diversity": d22_derived["data22_tourist_diversity"]},
    }

    # Data23
    specs["Data23"] = {
        "conversion_script": "scripts/verification/extract-eutd-dashboard-csv.py",
        "raw_sources": [eutd_source("TOUR_DES_14", 2023)],
        "transformation_rule": "Filter raw CSV `data/raw/eutd-tourism-dashboard-2024-indicators.csv` via `scripts/verification/extract-eutd-dashboard-csv.py` to `code == 'TOUR_DES_14'` ('Cultural assets density') and `nuts_code_2021 == 'EL62'` (year 2023).",
        "feature_dictionary": {
            "refined_data.cultural_assets_density.code": {"type": "string", "unit": "code", "role": "filter_dimension", "description": "EU Tourism Dashboard indicator code (TOUR_DES_14)."},
            "refined_data.cultural_assets_density.year": {"type": "integer", "unit": "year", "role": "temporal_dimension", "description": "Reference year (2023)."},
            "refined_data.cultural_assets_density.value": {"type": "number", "unit": "no. of cultural assets / 100 km²", "role": "target_indicator", "description": "Density of cultural assets in EL62 (9.073 per 100 km²)."},
        },
        "data": {"cultural_assets_density": eutd_el62["el62"]["cultural_assets_density"]},
    }

    # Data24
    specs["Data24"] = {
        "conversion_script": "scripts/verification/compute-data24-protected-land.py",
        "raw_sources": [
            specs["Data02"]["raw_sources"][1],
            {
                "source_id": "EEA_ArcGIS_ProtectedSites_Natura2000_Habitats",
                "provider": "European Environment Agency (EEA) — Natura 2000 Discomap ArcGIS REST",
                "upstream_url": "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer/0/query",
                "access_method": "GET (ArcGIS REST GeoJSON query via scripts/verification/pull-data24-protected-land.py)",
                "raw_file_path": "data/raw/eea-natura2000-el62-envelope-habitats-4326.geojson",
                "raw_format": "application/geo+json (34 polygon features in EPSG:4326)",
                "manifest": "data/manifests/source-verification-2026-10-03.json",
                "sha256": "f3ea28641afac9d75171d7799febc6c902071137cd23fb4422bb8c8a8aa2d756",
                "raw_schema_description": {
                    "properties.SITECODE": "Natura 2000 site identifier (e.g. 'GR2210001', 'GR2310001')",
                    "properties.SITENAME": "Official site name",
                    "properties.Area_ha": "Total site area including marine waters (hectares)",
                    "geometry": "Polygon/MultiPolygon site boundary",
                },
                "raw_variables_kept": ["SITECODE", "SITENAME", "Area_ha", "geometry"],
                "raw_variables_dropped": ["marine_portion_outside_EL62_land_polygon"],
                "conversion_script": "scripts/verification/compute-data24-protected-land.py",
                "conversion_command": "python3 scripts/verification/compute-data24-protected-land.py",
            },
            {
                "source_id": "EEA_ArcGIS_ProtectedSites_Natura2000_Birds",
                "provider": "European Environment Agency (EEA) — Natura 2000 Discomap ArcGIS REST",
                "upstream_url": "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer/1/query",
                "access_method": "GET (ArcGIS REST GeoJSON query via scripts/verification/pull-data24-protected-land.py)",
                "raw_file_path": "data/raw/eea-natura2000-el62-envelope-birds-4326.geojson",
                "raw_format": "application/geo+json (25 polygon features in EPSG:4326)",
                "manifest": "data/manifests/source-verification-2026-10-03.json",
                "sha256": "1f4966760df6cabcec4f49101b6685be02a9023d714828e30069f5aad6fe212d",
                "raw_schema_description": {
                    "properties.SITECODE": "Natura 2000 SPA site identifier",
                    "properties.SITENAME": "Official site name",
                    "properties.Area_ha": "Total SPA area including marine waters (hectares)",
                    "geometry": "Polygon/MultiPolygon site boundary",
                },
                "raw_variables_kept": ["SITECODE", "SITENAME", "Area_ha", "geometry"],
                "raw_variables_dropped": ["marine_portion_outside_EL62_land_polygon"],
                "conversion_script": "scripts/verification/compute-data24-protected-land.py",
                "conversion_command": "python3 scripts/verification/compute-data24-protected-land.py",
            },
        ],
        "transformation_rule": "Reproject EEA Natura 2000 Habitats (34 envelope sites) and Birds (25 envelope sites) polygons to equal-area EPSG:3035 via `scripts/verification/compute-data24-protected-land.py`, intersect with Eurostat GISCO EL62 land polygon (removing marine waters and capturing the 1,608.2 ha Echinades/Petalas islets under GR23-coded Acheloos sites), dissolve union(Habitats U Birds), and compute protected_land_pct = combined_protected_land_ha / el62_land_ha * 100.",
        "feature_dictionary": {
            "refined_data.el62_land_km2": {"type": "number", "unit": "km²", "role": "input_variable", "description": "Total terrestrial area of EL62 polygon in EPSG:3035 (2,304.87 km²)."},
            "refined_data.habitats_protected_land_ha": {"type": "number", "unit": "ha", "role": "input_variable", "description": "Terrestrial area under Habitats Directive (pSCI/SAC) within EL62 (22,049.2 ha)."},
            "refined_data.birds_protected_land_ha": {"type": "number", "unit": "ha", "role": "input_variable", "description": "Terrestrial area under Birds Directive (SPA) within EL62 (29,744.22 ha)."},
            "refined_data.combined_protected_land_km2": {"type": "number", "unit": "km²", "role": "input_variable", "description": "De-duplicated union of Habitats and Birds terrestrial area in EL62 (386.41 km²)."},
            "refined_data.protected_land_pct": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Share of EL62 terrestrial area protected under Natura 2000 (16.76%)."},
            "refined_data.nongr22_sites_with_land_overlap": {"type": "array", "unit": "ha", "role": "quality_metric", "description": "Completeness audit showing GR23 Acheloos-delta sites overlapping EL62 via Echinades islets (1,608.2 ha)."},
        },
        "data": d24_audit,
    }

    # Data25
    specs["Data25"] = {
        "conversion_script": "scripts/verification/extract-eutd-dashboard-csv.py",
        "raw_sources": [eutd_source("TOUR_DES_13", 2023)],
        "transformation_rule": "Filter raw CSV `data/raw/eutd-tourism-dashboard-2024-indicators.csv` via `scripts/verification/extract-eutd-dashboard-csv.py` to `code == 'TOUR_DES_13'` ('Share of accommodations in areas with high-nature value') for NUTS2 region EL62 (43.0% in 2023) and NUTS3 disaggregation.",
        "feature_dictionary": {
            "refined_data.el62_regional.value": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Share of tourist accommodations located in high-nature-value areas in EL62 (43.0%)."},
            "refined_data.by_nuts3_island": {"type": "object", "unit": "%", "role": "internal_disaggregation", "description": "NUTS3 island breakdown (Zakynthos 59%, Kerkyra 34%, Ithaki/Kefallinia 34%, Lefkada 57%)."},
        },
        "data": {
            "el62_regional": eutd_el62["el62"]["high_nature_value_accommodation"],
            "by_nuts3_island": {
                "EL621_Zakynthos": 59.0,
                "EL622_Kerkyra": 34.0,
                "EL623_Ithaki_Kefallinia": 34.0,
                "EL624_Lefkada": 57.0,
            },
        },
    }

    # Data26
    arn2_source = {
        "source_id": "Eurostat_tour_occ_arn2",
        "provider": "Eurostat (European Commission)",
        "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023",
        "access_method": "GET (SDMX 2.1 / JSON-stat 2.0 REST API, no key)",
        "raw_file_path": "data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json",
        "raw_format": "application/json (SDMX 2.1 JSON-stat 2.0 cube)",
        "manifest": "data/manifests/source-verification-2026-09-22.json",
        "sha256": "0855dc90f5b85a3f4251318da56456cec0585fe55843caf434f26c499f72b724",
        "raw_schema_description": {
            "dimension.c_resid": "Country of residence ('TOTAL', 'DOM', 'FOR')",
            "dimension.unit": "'NR' (number of arrivals)",
            "dimension.nace_r2": "'I551-I553'",
            "dimension.geo": "'EL62' (Ionia Nisia)",
            "dimension.time": "'2022', '2023'",
            "value": "Sparse map of tourist arrivals",
        },
        "raw_variables_kept": ["dimension.c_resid", "dimension.unit (NR)", "dimension.nace_r2 (I551-I553)", "dimension.geo (EL62)", "dimension.time", "value"],
        "raw_variables_dropped": ["PCH_PRE (percentage change)"],
        "conversion_script": "scripts/verification/build_dashboard.py",
        "conversion_command": "bash scripts/verification/pull-eurostat-tourism.sh && python3 scripts/verification/build_dashboard.py && python3 scripts/verification/build_indicator_folders.py",
    }

    specs["Data26"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [nin2_source, arn2_source],
        "transformation_rule": "Extract total annual overnight stays (tour_occ_nin2) and arrivals (tour_occ_arn2) at tourist accommodation establishments in EL62 via `scripts/verification/build_dashboard.py` for c_resid='TOTAL', unit='NR', nace_r2='I551-I553'.",
        "feature_dictionary": {
            "refined_data.series[].series_label": {"type": "string", "unit": "label", "role": "filter_dimension", "description": "Distinguishes 'overnight stays' vs 'arrivals' and sub-series."},
            "refined_data.series[].observed_at": {"type": "string", "unit": "year", "role": "temporal_dimension", "description": "Reference year."},
            "refined_data.series[].value": {"type": "number", "unit": "nights or arrivals", "role": "target_indicator", "description": "Total EL62 nights (16.51M in 2022; 19.76M in 2023; 20.52M in 2024; 20.36M in 2025) and arrivals (2.79M in 2022; 3.33M in 2023)."},
        },
        "data": {
            "annual_nights_2018_2025": {r["year"]: r["conventional_nights"] for r in d19_audit["series"]},
            "series": obs_series_dict("Data26"),
        },
    }

    # Data27
    specs["Data27"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [
            {
                "source_id": "Eurostat_tour_cap_nuts2",
                "provider": "Eurostat (European Commission)",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023",
                "access_method": "GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/samples/eurostat-tour_cap_nuts2-EL62-2022-2023.json",
                "raw_format": "application/json (SDMX 2.1 JSON-stat 2.0 cube)",
                "manifest": "data/manifests/source-verification-2026-09-22.json",
                "sha256": "90d5c376d69fad77a36e7d077cc63545a4ba0e68afc2e8017578418395495ae3",
                "raw_schema_description": {
                    "dimension.accomunit": "Capacity unit ('BEDPL' bed-places, 'ESTBL' establishments, 'BEDRM' bedrooms)",
                    "dimension.unit": "'NR' (count)",
                    "dimension.nace_r2": "'I551-I553'",
                    "dimension.geo": "'EL62'",
                    "dimension.time": "'2022', '2023'",
                    "value": "Sparse map of capacity counts",
                },
                "raw_variables_kept": ["dimension.accomunit (BEDPL, ESTBL, BEDRM)", "dimension.unit (NR)", "dimension.nace_r2", "dimension.geo (EL62)", "dimension.time", "value"],
                "raw_variables_dropped": ["PCH_PRE"],
                "conversion_script": "scripts/verification/build_dashboard.py",
                "conversion_command": "bash scripts/verification/pull-eurostat-tourism.sh && python3 scripts/verification/build_dashboard.py && python3 scripts/verification/build_indicator_folders.py",
            },
            {
                "source_id": "ELSTAT_STO12_capacity",
                "provider": "Hellenic Statistical Authority (ELSTAT) — Table STO12",
                "upstream_url": "https://www.statistics.gr/en/statistics/-/publication/STO12/",
                "access_method": "GET (annual XLSX editions 2021-2025)",
                "raw_file_path": "data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json",
                "raw_format": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (elstat-sto12-2021..2025-capacity.xlsx) -> JSON",
                "manifest": "data/manifests/source-verification-2026-10-01.json",
                "sha256": "68e1a44e39df1698f46b66c6ae32d054febb1d6e813c5e7e554153e5b59d81be",
                "raw_schema_description": {
                    "year": "Edition year ('2021'..'2025')",
                    "KERKYRA / ZAKYNTHOS / KEFALLINIA / LEFKADA / ITHAKI": "Hotel & similar establishment bed-places by regional unit",
                },
                "raw_variables_kept": ["year", "regional_unit", "bed_places_hotels_and_similar"],
                "raw_variables_dropped": ["non_Ionian_regional_units"],
                "conversion_script": "scripts/verification/reproduce-derived-samples.py",
                "conversion_command": "python3 scripts/verification/reproduce-derived-samples.py --check && python3 scripts/verification/build_indicator_folders.py",
                "lineage_note": "The JSON was extracted ad hoc on 2026-10-01 from data/samples/elstat-sto12-{2021..2025}-capacity.xlsx (sheet ENG, 'REGIONAL UNIT OF ...' rows, hotels-and-similar bed-places column). scripts/verification/reproduce-derived-samples.py (2026-11-03) reproduces all 25 values from the retained workbooks.",
            },
        ],
        "transformation_rule": "Extract total tourist accommodation bed-places (accomunit='BEDPL', unit='NR', nace_r2='I551-I553') for NUTS2 EL62 from Eurostat tour_cap_nuts2 via `scripts/verification/build_dashboard.py`, supplemented by ELSTAT STO12 regional-unit hotel bed capacity (2021-2025).",
        "feature_dictionary": {
            "refined_data.series[].series_label": {"type": "string", "unit": "label", "role": "filter_dimension", "description": "Capacity metric label ('bed-places', 'establishments', 'bedrooms')."},
            "refined_data.series[].value": {"type": "number", "unit": "count", "role": "target_indicator", "description": "Total bed-places in EL62 (159,790 in 2022; 155,968 in 2023)."},
            "refined_data.elstat_hotels_by_island_2021_2025": {"type": "object", "unit": "bed-places", "role": "internal_disaggregation", "description": "ELSTAT STO12 hotel bed-places by regional unit (Kerkyra, Zakynthos, Kefallinia, Lefkada, Ithaki)."},
        },
        "data": {
            "series": obs_series_dict("Data27"),
            "elstat_hotels_by_island_2021_2025": elstat_beds,
        },
    }

    # Data28
    specs["Data28"] = {
        "conversion_script": "scripts/verification/extract-eutd-dashboard-csv.py",
        "raw_sources": [eutd_source("TOUR_DES_04", 2023)],
        "transformation_rule": "Adopt EU Tourism Dashboard indicator TOUR_DES_04 ('Net occupancy rate of bed-places') for NUTS2 EL62 (65.4% in 2023) via `scripts/verification/extract-eutd-dashboard-csv.py`, superseding gross annual nights/(beds*365) estimates.",
        "feature_dictionary": {
            "refined_data.net_occupancy_el62.value": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Net occupancy rate of bed-places in EL62 (65.4% in 2023)."},
            "refined_data.nights_per_hotel_bed_index_2021_2025": {"type": "object", "unit": "%", "role": "internal_disaggregation", "description": "NOT an occupancy rate. Index = 100 x NUTS3 nights in all accommodation (Eurostat tour_occ_nin3, I551-I553) / (ELSTAT STO12 hotel-only bed-places x 365). Numerator and denominator cover different supply, so values overstate occupancy (Lefkada 2025 = 82.4). Reproduced by scripts/verification/reproduce-derived-samples.py. Context only; not used for the Data28 observation."},
        },
        "data": {
            "net_occupancy_el62": eutd_el62["el62"]["net_occupancy"],
            "nights_per_hotel_bed_index_2021_2025": d28_derived,
        },
    }

    # Data29
    specs["Data29"] = {
        "conversion_script": "scripts/verification/compute-data29-seasonality.py -> scripts/verification/build_dashboard.py",
        "raw_sources": [
            {
                "source_id": "Eurostat_tour_occ_nin2m",
                "provider": "Eurostat (European Commission)",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2m?format=JSON&lang=EN&geo=EL62&geo=EL&unit=NR&c_resid=TOTAL",
                "access_method": "GET (JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json",
                "raw_format": "application/json (JSON-stat 2.0; month is a dimension M01..M12 + TOTAL, time is the year)",
                "manifest": "data/manifests/source-verification-2026-11-03.json",
                "sha256": "78c4e09fc4317cc0521c998a84434c071d010affec5f5a3b9b0bee54e727c60f",
                "raw_schema_description": {
                    "dimension.month": "'TOTAL' and 'M01'..'M12'",
                    "dimension.geo": "'EL62' (Ionia Nisia) and 'EL' (Greece)",
                    "dimension.time": "Reference year '2020'..'2025'",
                    "dimension.nace_r2": "'I551-I553' (all tourist accommodation; no type split at NUTS 2)",
                    "value": "Nights spent (unit NR)",
                },
                "raw_variables_kept": ["month", "geo", "time", "value"],
                "raw_variables_dropped": ["freq (A)", "c_resid (TOTAL only)", "unit (NR only)"],
                "conversion_script": "scripts/verification/compute-data29-seasonality.py",
                "conversion_command": "python3 scripts/verification/compute-data29-seasonality.py && python3 scripts/verification/build_dashboard.py <manifests> && python3 scripts/verification/build_indicator_folders.py",
            },
            {
                "source_id": "Eurostat_tour_ce_omn12_monthly",
                "provider": "Eurostat (data shared by Airbnb, Booking.com, Expedia Group)",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_ce_omn12?format=JSON&lang=EN&geo=EL62&geo=EL&indic_to=NGT_SP&c_resid=TOTAL&time=2020&time=2021&time=2022&time=2023",
                "access_method": "GET (JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/raw/eurostat-tour_ce_omn12-EL62-EL-monthly-2020-2023.json",
                "raw_format": "application/json (JSON-stat 2.0; month dimension)",
                "manifest": "data/manifests/source-verification-2026-11-03.json",
                "sha256": "4e2ec7512fa29d69410ac2b78694ccab9fa2765789cad949f3d1225bb3fba4c1",
                "raw_schema_description": {
                    "dimension.month": "'M01'..'M12'",
                    "dimension.geo": "'EL62', 'EL'",
                    "value": "Guest nights in short-stay accommodation booked via online platforms",
                },
                "raw_variables_kept": ["month", "geo", "time", "value"],
                "raw_variables_dropped": ["indic_to (NGT_SP only)", "c_resid (TOTAL only)"],
                "conversion_script": "scripts/verification/compute-data29-seasonality.py",
                "conversion_command": "python3 scripts/verification/compute-data29-seasonality.py --check",
                "lineage_note": "Used only to reconcile the dashboard EL62 value; no observation is emitted from it.",
            },
            eutd_source("TOUR_SOE_02", 2023),
            {
                "source_id": "Eurostat_tour_occ_nim",
                "provider": "Eurostat (European Commission)",
                "upstream_url": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&geo=EL&freq=M&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2023-01..2023-12",
                "access_method": "GET (SDMX 2.1 JSON-stat 2.0 REST API, no key)",
                "raw_file_path": "data/samples/eurostat-tour_occ_nim-EL-2023.json",
                "raw_format": "application/json (SDMX 2.1 JSON-stat 2.0 cube)",
                "manifest": "data/manifests/source-verification-2026-09-24.json",
                "sha256": "e07a17f98f18f87f94e31d35993f34c9b44eda95c60632ce1c4e0b729955198b",
                "raw_schema_description": {
                    "dimension.geo": "'EL' (Greece country-level monthly series)",
                    "dimension.time": "Monthly timestamps '2023-01' through '2023-12'",
                    "value": "Monthly overnight stays in Greece",
                },
                "raw_variables_kept": ["geo (EL)", "freq (M)", "c_resid (TOTAL)", "unit (NR)", "nace_r2 (I551-I553)", "time (2023-01..2023-12)", "value"],
                "raw_variables_dropped": ["PCH_SM", "PCH_SM_2Y"],
                "conversion_script": "scripts/verification/build_dashboard.py",
                "conversion_command": "python3 scripts/verification/build_dashboard.py --manifest data/manifests/source-verification-2026-09-24.json",
            },
        ],
        "transformation_rule": (
            "D-026. Headline: share of annual nights in the 3 busiest months (EU Tourism Dashboard TOUR_SOE_02 definition), "
            "computed over ALL accommodation from Eurostat tour_occ_nin2m monthly nights for EL62 and EL, 2020-2025: "
            "top3_share = sum(3 largest monthly nights) / sum(12 monthly nights) * 100 (EL62 2023 = 63.81 %). "
            "Seasonality Index: Gini coefficient of the 12 monthly nights (EL62 2023 = 0.5827). Context: peak-month share, "
            "share of nights outside June-September, and EL62 monthly nights. Computed by "
            "scripts/verification/compute-data29-seasonality.py, which first checks the definition against the dashboard: "
            "EL 2021-2023 match on all accommodation; EL62 2020-2023 match only on online-platform nights (tour_ce_omn12). "
            "The dashboard EL62 value (71.08 % in 2023) is therefore kept as a separate platform-only series."
        ),
        "feature_dictionary": {
            "refined_data.results.<geo>.<year>.top3_share_pct": {"type": "number", "unit": "%", "role": "target_indicator", "description": "Headline Data29: share of annual nights (all accommodation) in the 3 busiest months. EL62 2023 = 63.81."},
            "refined_data.results.<geo>.<year>.gini": {"type": "number", "unit": "index (0-1)", "role": "target_indicator", "description": "Seasonality Index: Gini coefficient of the 12 monthly nights; 0 = even year-round, 0.917 = all nights in one month. EL62 2023 = 0.5827."},
            "refined_data.results.<geo>.<year>.peak_month_share_pct": {"type": "number", "unit": "%", "role": "context_metric", "description": "Share of annual nights in the single busiest month (August in every year)."},
            "refined_data.results.<geo>.<year>.share_outside_jun_sep_pct": {"type": "number", "unit": "%", "role": "context_metric", "description": "Share of annual nights in January-May and October-December; tracks off-season growth."},
            "refined_data.results.<geo>.<year>.monthly_nights": {"type": "object", "unit": "nights", "role": "input_variable", "description": "Monthly nights M01..M12 from tour_occ_nin2m (all accommodation, I551-I553)."},
            "refined_data.results.EL62.<year>.platform_top3_share_pct": {"type": "number", "unit": "%", "role": "context_metric", "description": "Same measure over online-platform nights only (tour_ce_omn12); equals the dashboard TOUR_SOE_02 EL62 value."},
            "refined_data.dashboard_reconciliation": {"type": "array", "unit": "%", "role": "quality_check", "description": "Per geo/year: dashboard value, recomputed value, basis, match flag."},
            "refined_data.dashboard_el62_platform_only": {"type": "object", "unit": "%", "role": "context_metric", "description": "EU Tourism Dashboard TOUR_SOE_02 EL62 2023 (71.08 %), relabelled as online-platform-only seasonality."},
        },
        "data": {
            **{k: v for k, v in load_json(CURATED_DIR / "data29-seasonality.json").items()
               if k in ("definition", "dashboard_reconciliation", "dashboard_note", "caveats", "results")},
            "dashboard_el62_platform_only": eutd_el62["el62"]["peak_season_share"],
        },
    }

    # Data30
    specs["Data30"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [nin2_source, arn2_source],
        "transformation_rule": "D-016: Compute average length of stay in EL62 via `scripts/verification/build_dashboard.py` as total overnight stays (tour_occ_nin2) divided by total arrivals (tour_occ_arn2): LOS = nights / arrivals.",
        "feature_dictionary": {
            "refined_data.series[].observed_at": {"type": "string", "unit": "year", "role": "temporal_dimension", "description": "Reference year."},
            "refined_data.series[].value": {"type": "number", "unit": "nights", "role": "target_indicator", "description": "Average length of stay per tourist arrival in EL62 (5.928 in 2022; 5.930 in 2023; 5.58 in 2025)."},
        },
        "data": {
            "formula": "nights / arrivals",
            "series": obs_series_dict("Data30"),
        },
    }

    # Data31
    specs["Data31"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [nin2_source],
        "transformation_rule": "Filter Eurostat SDMX dataset tour_occ_nin2 via `scripts/verification/build_dashboard.py` to geo='EL62', c_resid='TOTAL', nace_r2='I551-I553', and unit='P_KM2' (overnight stays per square kilometre).",
        "feature_dictionary": {
            "refined_data.filter_dims": {"type": "object", "unit": "SDMX codes", "role": "filter_dimension", "description": "Exact SDMX dimension filter: geo=EL62, c_resid=TOTAL, unit=P_KM2, nace_r2=I551-I553."},
            "refined_data.series[].value": {"type": "number", "unit": "nights per km²", "role": "target_indicator", "description": "Annual tourism density in EL62 (7,176.29 in 2022; 8,588.79 in 2023)."},
        },
        "data": {
            "filter_dims": {"geo": "EL62", "c_resid": "TOTAL", "unit": "P_KM2", "nace_r2": "I551-I553"},
            "series": obs_series_dict("Data31"),
        },
    }

    # Data32
    specs["Data32"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [nin2_source],
        "transformation_rule": "D-009 & D-016: Compare overnight stays across NACE Rev. 2 accommodation categories in EL62 via `scripts/verification/build_dashboard.py` (I551 hotels ~70-73%, I552 short-stay ~26-30%, I553 camping <1%) and assign the argmax category ('hotels') as the dominant tourism typology.",
        "feature_dictionary": {
            "refined_data.nace_r2_shares_el62": {"type": "object", "unit": "%", "role": "input_variable", "description": "Share of EL62 overnight stays by NACE Rev. 2 category."},
            "refined_data.series[].value": {"type": "string", "unit": "category", "role": "target_indicator", "description": "Dominant accommodation typology in EL62 ('hotels')."},
        },
        "data": {
            "nace_r2_shares_el62": {
                "2022": {"I551_hotels": 73.1, "I552_holiday_short_stay": 26.0, "I553_camping": 0.9},
                "2023": {"I551_hotels": 69.8, "I552_holiday_short_stay": 29.3, "I553_camping": 0.9},
            },
            "series": obs_series_dict("Data32"),
        },
    }

    # Data33
    specs["Data33"] = {
        "conversion_script": "scripts/verification/build_dashboard.py",
        "raw_sources": [nin2_source],
        "transformation_rule": "Filter Eurostat SDMX dataset tour_occ_nin2 via `scripts/verification/build_dashboard.py` to geo='EL62', c_resid='FOR' (foreign/non-resident tourists), nace_r2='I551-I553', and unit='PC_TOT' (percentage of total nights).",
        "feature_dictionary": {
            "refined_data.filter_dims": {"type": "object", "unit": "SDMX codes", "role": "filter_dimension", "description": "Exact SDMX dimension filter: geo=EL62, c_resid=FOR, unit=PC_TOT, nace_r2=I551-I553."},
            "refined_data.series[].value": {"type": "number", "unit": "% of total", "role": "target_indicator", "description": "Foreign tourist share of overnight stays in EL62 (93.72% in 2022; 93.58% in 2023)."},
        },
        "data": {
            "filter_dims": {"geo": "EL62", "c_resid": "FOR", "unit": "PC_TOT", "nace_r2": "I551-I553"},
            "series": obs_series_dict("Data33"),
        },
    }

    return specs


def _raw_ext(path_str: str, fmt_str: str) -> str:
    """Extract clean file extension badge (e.g. '.csv', '.zip (Shapefile)', '.geojson', '.json')."""
    p = Path(path_str)
    suf = p.suffix.lower()
    if suf == ".zip" and "shapefile" in fmt_str.lower():
        return ".zip (Shapefile)"
    if suf == ".zip" and "netcdf" in fmt_str.lower():
        return ".zip (NetCDF .nc)"
    if suf:
        return suf
    return "API/stream"


def render_indicator_readme(iid: str, ind_meta: dict, raw_doc: dict, refined_doc: dict) -> str:
    """Render the Option A per-indicator README.md companion file."""
    name = ind_meta.get("name", iid)
    name_el = ind_meta.get("name_el") or "—"
    cat = ind_meta.get("category", "")
    status = ind_meta.get("status", "UNVERIFIED")
    cadence = ind_meta.get("cadence", "—")
    obs_list = refined_doc.get("observations", [])
    note = ind_meta.get("note") or "—"
    raw_sources = raw_doc.get("raw_sources", [])

    if raw_sources:
        exts = sorted({f"`{_raw_ext(rs.get('raw_file_path', ''), rs.get('raw_format', ''))}`" for rs in raw_sources})
        ext_summary = " + ".join(exts)
        flow_lines = []
        for rs in raw_sources:
            ext_badge = _raw_ext(rs.get("raw_file_path", ""), rs.get("raw_format", ""))
            flow_lines.append(
                f"  {rs.get('raw_file_path')} [{ext_badge}]  ──( {rs.get('conversion_script')} )──>  refined-data.json [.json]"
            )
        pipeline_block = "```text\n" + "\n".join(flow_lines) + "\n```"
    else:
        ext_summary = "`None (UNVERIFIED)`"
        pipeline_block = "```text\n  [UNVERIFIED source track — no raw file or conversion script active yet]\n```"

    lines = [
        f"# {iid} — {name}",
        "",
        "## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)",
        "",
        pipeline_block,
        "",
        "## Quick Navigation (Option A Folder Layout)",
        "",
        "| File in this folder | Extension | Purpose |",
        "| :--- | :--- | :--- |",
        "| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |",
        "| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |",
        "| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |",
        "",
        f"- **Status:** `{status}`",
        f"- **Greek Proposal Name:** {name_el}",
        f"- **Category:** `{cat}`",
        f"- **Refresh Cadence:** `{cadence}`",
        f"- **Raw Input File Extension(s):** {ext_summary}",
        f"- **Primary Conversion / Builder Script:** `{raw_doc.get('conversion_script')}`",
        f"- **Refined Output Format:** `.json` (`refined-data.json`)",
        f"- **Observations Emitted:** `{len(obs_list)}`",
        "",
        "## 1. Overview & Key Note",
        "",
        f"{note}",
        "",
        "## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)",
        "",
    ]

    if not raw_sources:
        lines.append("No raw payload ingested yet (`UNVERIFIED` source track — no synthetic data invented).")
    else:
        for idx, rs in enumerate(raw_sources, 1):
            ext_badge = _raw_ext(rs.get("raw_file_path", ""), rs.get("raw_format", ""))
            lines.extend([
                f"### Source {idx}: `{rs.get('source_id')}` ({rs.get('provider')})",
                f"- **Upstream URL:** `{rs.get('upstream_url')}`",
                f"- **Access Method:** `{rs.get('access_method')}`",
                f"- **Local Raw File (`data/raw/` or `data/samples/`):** `{rs.get('raw_file_path')}`",
                f"- **Raw File Extension & Format:** `{ext_badge}` — `{rs.get('raw_format')}`",
                f"- **SHA-256 Checksum (of the local file, recomputed at build):** `{rs.get('sha256')}`",
                f"- **Evidence Manifest:** `{rs.get('manifest')}`",
            ])
            if rs.get("upstream_response_sha256"):
                lines.append(f"- **SHA-256 of the full upstream response (not retained):** `{rs.get('upstream_response_sha256')}`")
            if rs.get("lineage_note"):
                lines.append(f"- **Lineage Note:** {rs.get('lineage_note')}")
            lines.extend([
                f"- **Conversion Script (`{ext_badge}` -> `.json`):** `{rs.get('conversion_script')}`",
                f"- **Conversion Command:** `{rs.get('conversion_command')}`",
                f"- **Whitelisted Raw Variables (`kept`):** " + ", ".join(f"`{k}`" for k in rs.get("raw_variables_kept", [])),
                f"- **Dropped / Redacted Fields:** " + ", ".join(f"`{d}`" for d in rs.get("raw_variables_dropped", [])),
                "",
                "| Raw Field / Column | Raw Source Description |",
                "| :--- | :--- |",
            ])
            for k, desc in rs.get("raw_schema_description", {}).items():
                lines.append(f"| `{k}` | {desc} |")
            lines.append("")

    lines.extend([
        "## 3. Transformation & Refined Data Dictionary (`refined-data.json`)",
        "",
        f"**Transformation Rule:** {refined_doc.get('transformation_rule', '')}",
        "",
        "| Refined JSONPath | Type | Unit | Role | Description |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ])

    for fpath, fdesc in refined_doc.get("feature_dictionary", {}).items():
        lines.append(
            f"| `{fpath}` | `{fdesc.get('type')}` | `{fdesc.get('unit')}` | `{fdesc.get('role')}` | {fdesc.get('description')} |"
        )

    lines.extend([
        "",
        "## 4. Normalized Observations (`refined-data.json -> observations[]`)",
        "",
        "All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.",
        "",
    ])
    if not obs_list:
        lines.append("_No observations emitted for this indicator yet._")
    else:
        lines.append("| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for o in obs_list[:15]:
            sr = f"`{o['spatial_ref']['level']}/{o['spatial_ref']['code']}`"
            lines.append(
                f"| `{o['observation_id']}` | `{o['observed_at']}` | {sr} | **{o['value']}** | `{o['unit']}` | `{o['temporal_granularity']}` |"
            )
        if len(obs_list) > 15:
            lines.append(f"| _… ({len(obs_list) - 15} more observations in `refined-data.json`)_ | | | | | |")

    lines.append("")
    return "\n".join(lines)


def verify_indicator_folder(folder: Path, schema: dict, man_hashes: dict[str, set[str]],
                            expected_obs: dict[str, dict]) -> list[str]:
    """Independent checks on one indicator folder, reading only what is on disk.

    1. Structure: the three files exist and carry the required keys.
    2. Provenance: every raw file exists; its sha256, recomputed now, equals the recorded
       value and appears in the cited manifest (or in any manifest, reported separately).
    3. Observations: each validates against schemas/observation-schema.json with a real
       JSON Schema validator, and is identical to the record in the master snapshot.
    4. Domain bounds for percentages and 0-1 scores.
    """
    errors: list[str] = []
    raw_desc_path = folder / "raw-source-description.json"
    refined_path = folder / "refined-data.json"
    readme_path = folder / "README.md"

    for p in (raw_desc_path, refined_path, readme_path):
        if not p.exists():
            errors.append(f"{folder.name}: missing required file {p.name}")
            return errors

    raw_doc = load_json(raw_desc_path)
    for req_key in ("indicator_id", "indicator_name", "status", "conversion_script", "raw_sources"):
        if req_key not in raw_doc:
            errors.append(f"{folder.name}: raw-source-description.json missing '{req_key}'")
    for rs in raw_doc.get("raw_sources", []):
        for k in ("source_id", "provider", "upstream_url", "raw_file_path", "sha256", "raw_schema_description", "conversion_script"):
            if k not in rs:
                errors.append(f"{folder.name}: raw_source missing '{k}'")
        rel = rs.get("raw_file_path", "")
        fp = ROOT / rel
        if not fp.is_file():
            errors.append(f"{folder.name}: raw file not on disk: {rel}")
            continue
        actual = sha256_file(fp)
        if actual != rs.get("sha256"):
            errors.append(f"{folder.name}: sha256 of {rel} is {actual[:12]}…, recorded {str(rs.get('sha256'))[:12]}…")
        cited = Path(rs.get("manifest", "")).name
        if cited not in man_hashes:
            errors.append(f"{folder.name}: cited manifest not found: {rs.get('manifest')}")
        elif actual not in man_hashes[cited]:
            elsewhere = sorted(m for m, hs in man_hashes.items() if actual in hs)
            if elsewhere:
                errors.append(f"{folder.name}: {rel} hash not in cited manifest {cited}; found in {elsewhere} (update 'manifest')")
            else:
                errors.append(f"{folder.name}: {rel} hash {actual[:12]}… is not recorded in any manifest")
        for script in [s for s in str(rs.get("conversion_script", "")).split() if s.startswith("scripts/")]:
            if not (ROOT / script).exists():
                errors.append(f"{folder.name}: conversion script does not exist: {script}")

    refined_doc = load_json(refined_path)
    for req_key in ("indicator_id", "indicator_name", "status", "source_citations", "conversion_script", "transformation_rule", "feature_dictionary", "refined_data", "observations"):
        if req_key not in refined_doc:
            errors.append(f"{folder.name}: refined-data.json missing '{req_key}'")

    obs_list = refined_doc.get("observations", [])
    if not isinstance(obs_list, list):
        errors.append(f"{folder.name}: refined-data.json 'observations' must be a JSON array")
        return errors
    if refined_doc.get("observations_count") != len(obs_list):
        errors.append(f"{folder.name}: observations_count {refined_doc.get('observations_count')} != {len(obs_list)}")

    iid = raw_doc.get("indicator_id")
    want_ids = sorted(oid for oid, o in expected_obs.items() if o.get("indicator_id") == iid)
    have_ids = sorted(o.get("observation_id", "?") for o in obs_list)
    if want_ids != have_ids:
        errors.append(f"{folder.name}: observation ids differ from master snapshot ({len(have_ids)} in folder, {len(want_ids)} in master)")

    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema, format_checker=validator_cls.FORMAT_CHECKER)
    for o in obs_list:
        oid = o.get("observation_id", "?")
        for err in validator.iter_errors(o):
            path = "/".join(str(x) for x in err.absolute_path) or "(root)"
            errors.append(f"{folder.name} ({oid}): schema: {path}: {err.message[:160]}")
        if oid in expected_obs and expected_obs[oid] != o:
            errors.append(f"{folder.name} ({oid}): differs from the master snapshot record")
        val = o.get("value")
        unit = o.get("unit") or ""
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            if unit in ("%", "% of total", "% of bathing waters") and not (0.0 <= float(val) <= 100.0):
                errors.append(f"{folder.name} ({oid}): percentage out of [0,100]: {val}")
            if unit in ("score (0-1)", "index (0-1)") and not (0.0 <= float(val) <= 1.0):
                errors.append(f"{folder.name} ({oid}): score out of [0,1]: {val}")

    return errors


def check_all(schema: dict, master_obs: list[dict], extra_obs: list[dict]) -> list[str]:
    expected = {o["observation_id"]: o for o in master_obs}
    dup = [o["observation_id"] for o in extra_obs if o["observation_id"] in expected]
    expected.update({o["observation_id"]: o for o in extra_obs})
    man = manifest_hashes()
    errors: list[str] = curated_file_problems()
    errors += [f"observation id in both master and a separate file: {d}" for d in dup]
    if len(expected) != len(master_obs) + len(extra_obs) - len(dup):
        errors.append("duplicate observation ids inside the master or separate files")
    folders = [INDICATORS_DIR / SLUGS[f"Data{i:02d}"] for i in range(1, 35)]
    extra = sorted(p.name for p in INDICATORS_DIR.iterdir() if p.is_dir() and p not in folders)
    if extra:
        errors.append(f"unexpected folders under data/indicators/: {extra}")
    for folder in folders:
        if not folder.is_dir():
            errors.append(f"missing indicator folder {folder.name}")
            continue
        errors.extend(verify_indicator_folder(folder, schema, man, expected))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="verify the existing folders against raw files, manifests and the master snapshot; write nothing")
    args = ap.parse_args()

    if jsonschema is None:
        print("ERROR: the 'jsonschema' package is required (pip install -e '.[verify]').", file=sys.stderr)
        return 2

    mapping = load_json(MAP_PATH)
    schema = load_json(SCHEMA_PATH)
    ind_map = {item["indicator_id"]: item for item in mapping["indicators"]}

    master_obs_path = CURATED_DIR / MASTER_SNAPSHOT
    master_obs = load_json(master_obs_path)
    extra_obs = load_separate_obs()

    if not args.check:
        specs = build_specs(master_obs, extra_obs)

        obs_by_ind: dict[str, list[dict]] = {f"Data{i:02d}": [] for i in range(1, 35)}
        for o in master_obs + extra_obs:
            obs_by_ind.setdefault(o["indicator_id"], []).append(o)

        INDICATORS_DIR.mkdir(parents=True, exist_ok=True)
        for i in range(1, 35):
            iid = f"Data{i:02d}"
            folder = INDICATORS_DIR / SLUGS[iid]
            folder.mkdir(parents=True, exist_ok=True)

            # Remove old Option B filenames if present
            for old_name in ("extracted-summary.json", "observations.json"):
                old_p = folder / old_name
                if old_p.exists():
                    old_p.unlink()

            ind_meta = ind_map[iid]
            spec = specs[iid]
            obs_list = obs_by_ind.get(iid, [])

            # Record the hash of the file as it is on disk now. A pinned value in the spec
            # that disagrees is a hard error: the raw file changed since it was described.
            for rs in spec["raw_sources"]:
                fp = ROOT / rs["raw_file_path"]
                if fp.is_file():
                    actual = sha256_file(fp)
                    if rs.get("sha256") and rs["sha256"] != actual:
                        print(f"ERROR: {iid}: {rs['raw_file_path']} sha256 {actual[:12]}… differs from pinned "
                              f"{rs['sha256'][:12]}…; investigate before rebuilding.", file=sys.stderr)
                        return 1
                    rs["sha256"] = actual

            raw_doc = {
                "schema_version": "1.0",
                "file_role": "raw_source_description",
                "indicator_id": iid,
                "indicator_name": ind_meta.get("name"),
                "indicator_name_el": ind_meta.get("name_el"),
                "category": ind_meta.get("category"),
                "status": ind_meta.get("status"),
                "conversion_script": spec["conversion_script"],
                "raw_sources": spec["raw_sources"],
            }
            source_citations = [
                {
                    "source_id": rs["source_id"],
                    "provider": rs["provider"],
                    "upstream_url": rs["upstream_url"],
                    "raw_file_path": rs["raw_file_path"],
                    "sha256": rs["sha256"],
                    "conversion_script": rs["conversion_script"],
                }
                for rs in spec["raw_sources"]
            ]
            refined_doc = {
                "schema_version": "1.0",
                "file_role": "refined_indicator_data",
                "indicator_id": iid,
                "indicator_name": ind_meta.get("name"),
                "indicator_name_el": ind_meta.get("name_el"),
                "category": ind_meta.get("category"),
                "status": ind_meta.get("status"),
                "cadence": ind_meta.get("cadence"),
                "source_citations": source_citations,
                "conversion_script": spec["conversion_script"],
                "transformation_rule": spec["transformation_rule"],
                "feature_dictionary": spec["feature_dictionary"],
                "refined_data": spec["data"],
                "observations_count": len(obs_list),
                "observations": obs_list,
            }
            (folder / "raw-source-description.json").write_text(
                json.dumps(raw_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            (folder / "refined-data.json").write_text(
                json.dumps(refined_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            (folder / "README.md").write_text(
                render_indicator_readme(iid, ind_meta, raw_doc, refined_doc), encoding="utf-8")
        print(f"Built 34 indicator folders under {INDICATORS_DIR.relative_to(ROOT)}/")

    # Verification re-reads everything from disk, independently of the build step above.
    errors = check_all(schema, master_obs, extra_obs)
    if errors:
        print(f"VERIFICATION FAILED ({len(errors)} problems):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"CHECK PASSED: 34 folders; every raw file present and its sha256 recorded in the cited manifest; "
          f"{len(master_obs) + len(extra_obs)} observations ({len(master_obs)} master + {len(extra_obs)} in separate files) "
          f"schema-valid (jsonschema {_jsonschema_version()}) and identical to their source files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
