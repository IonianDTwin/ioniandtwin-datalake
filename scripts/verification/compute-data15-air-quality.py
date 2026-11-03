#!/usr/bin/env python3
"""Emit Data15 (air quality) observations from the retained CAMS analysis, on the EL62 reference area (D-014).

Lineage:
  data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip  (ENS_ANALYSIS.nc, 0.1 deg grid)
  data/raw/gisco-nuts-2021-3035-EL62.geojson                           (EL62 land polygon, EPSG:3035)
    --( this script )--> data/curated/observations-data15-air-quality-2026-09-30.json / .csv

Measures per pollutant (NO2, PM10, PM2.5, CO; ug/m3; surface; 2026-09-30T00:00Z analysis):
  * NUTS2/EL62: area-weighted mean over the EL62 land polygon. Each 0.1-degree cell is weighted by
    its intersection area with EL62 land, so the result describes where the region is, not the
    rectangular request box (which also covers mainland Greece, Albania and open sea).
  * point (Corfu airport cell, 39.65N 19.95E): value of the grid cell nearest the airport,
    identical to data/samples/cams-ionian-20260930-summary.json (extract-cams-summary.py).

This is a single analysis time: a verified working source, not a climatology. The continuous
feed (daily) belongs to the scheduler (see pipelines/refresh-scheduler.md).

Usage:
  python3 scripts/verification/compute-data15-air-quality.py           # compute and write
  python3 scripts/verification/compute-data15-air-quality.py --check   # compute only
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import numpy as np
import xarray as xr
from shapely.geometry import box

ROOT = Path(__file__).resolve().parent.parent.parent
ZIP_PATH = ROOT / "data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip"
EL62_PATH = ROOT / "data/raw/gisco-nuts-2021-3035-EL62.geojson"
OUT = ROOT / "data/curated/observations-data15-air-quality-2026-09-30.json"
OBSERVED_AT = "2026-09-30T00:00:00+00:00"
CELL = (39.65, 19.95)
VARS = {"NO2": "no2_conc", "PM10": "pm10_conc", "PM2.5": "pm2p5_conc", "CO": "co_conc"}
URL = "https://ads.atmosphere.copernicus.eu/api/retrieve/v1/processes/cams-europe-air-quality-forecasts/execution"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    with zipfile.ZipFile(ZIP_PATH) as z:
        ds = xr.open_dataset(io.BytesIO(z.read("ENS_ANALYSIS.nc"))).isel(time=0, level=0)
    lats, lons = ds.latitude.values, ds.longitude.values
    half = 0.05

    # Cell polygons (WGS84) -> EPSG:3035, intersected with EL62 land.
    cells = [{"i": i, "j": j, "geometry": box(lon - half, lat - half, lon + half, lat + half)}
             for i, lat in enumerate(lats) for j, lon in enumerate(lons)]
    grid = gpd.GeoDataFrame(cells, crs="EPSG:4326").to_crs(3035)
    el62 = gpd.read_file(EL62_PATH).to_crs(3035).union_all()
    grid["w"] = grid.geometry.intersection(el62).area
    grid = grid[grid["w"] > 0]
    land_km2 = grid["w"].sum() / 1e6
    print(f"EL62 land covered by {len(grid)} grid cells, intersected area {land_km2:.2f} km2")

    raw_sha = sha256(ZIP_PATH)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    obs, results = [], {}
    for label, var in VARS.items():
        arr = ds[var].values
        vals = np.array([arr[i, j] for i, j in zip(grid["i"], grid["j"])], dtype=float)
        mean = float(np.average(vals, weights=grid["w"].values))
        point = float(ds[var].sel(latitude=CELL[0], longitude=CELL[1], method="nearest"))
        results[label] = {"el62_area_weighted_mean": round(mean, 2), "corfu_airport_cell": round(point, 2)}
        print(f"{label:5} EL62 area-weighted mean {mean:8.2f}  Corfu airport cell {point:8.2f} ug/m3")
        common = {
            "indicator_id": "Data15", "indicator_name": "Air quality", "source_id": "CAMS_ADS_air_quality",
            "observed_at": OBSERVED_AT, "observed_period_end": None, "temporal_granularity": "instant",
            "ingested_at": now, "unit": "ug/m3", "polarity": "negative",
        }
        obs.append({**common,
                    "observation_id": f"CAMS_ADS:Data15:{label}:EL62_mean:2026-09-30T00Z",
                    "series_label": f"surface {label}, area-weighted mean over EL62 land (CAMS ensemble analysis)",
                    "spatial_ref": {"level": "NUTS2", "code": "EL62", "geometry": None},
                    "value": round(mean, 2),
                    "provenance": {"raw_checksum_sha256": raw_sha, "raw_manifest": "source-verification-2026-10-01",
                                   "access_method": "derived", "request_url": URL,
                                   "request_params": {"formula": f"sum(cell_value * area(cell ∩ EL62 land)) / sum(area), {len(grid)} cells",
                                                      "boundary": "data/raw/gisco-nuts-2021-3035-EL62.geojson"}}})
        obs.append({**common,
                    "observation_id": f"CAMS_ADS:Data15:{label}:corfu_airport_cell:2026-09-30T00Z",
                    "series_label": f"surface {label} at the CAMS grid cell nearest Corfu airport (39.65N 19.95E)",
                    "spatial_ref": {"level": "point", "code": "39.65,19.95", "geometry": None},
                    "value": round(point, 2),
                    "provenance": {"raw_checksum_sha256": raw_sha, "raw_manifest": "source-verification-2026-10-01",
                                   "access_method": "derived", "request_url": URL,
                                   "request_params": {"formula": "nearest 0.1-degree grid cell"}}})

    summary = json.loads((ROOT / "data/samples/cams-ionian-20260930-summary.json").read_text())
    for label in VARS:
        if abs(summary["values_ug_m3"][label]["at_corfu_airport"] - results[label]["corfu_airport_cell"]) > 0.005:
            print(f"FAIL: Corfu cell {label} differs from the CAMS summary", file=sys.stderr)
            return 1
    print(f"{len(obs)} observations (airport-cell values agree with the CAMS summary)")
    if args.check:
        return 0
    OUT.write_text(json.dumps(obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with OUT.with_suffix(".csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["observation_id", "spatial_code", "value", "unit"])
        for o in obs:
            w.writerow([o["observation_id"], o["spatial_ref"]["code"], o["value"], o["unit"]])
    print(f"wrote {OUT.relative_to(ROOT)} (+ .csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
