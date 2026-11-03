#!/usr/bin/env python3
"""Reproduce data/samples/cams-ionian-20260930-summary.json from the retained CAMS zip.

Lineage for Data01 (airport CO2 proxy) and Data15 (air quality):
    data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip  (ENS_ANALYSIS.nc)
      --( this script )--> data/samples/cams-ionian-20260930-summary.json

The summary was first produced ad hoc on 2026-10-01 and no script was kept.
This script was written on 2026-11-03 to make that step reproducible.

Method (unchanged from the 2026-10-01 summary):
  * surface level (0 m), single analysis time 2026-09-30T00:00Z;
  * "at_corfu_airport" = the grid cell centred 39.65N 19.95E (0.1 deg grid), the cell
    nearest to Corfu airport (LGKR, approx. 39.60N 19.91E);
  * "region_mean" / "region_max" = mean / max over all 35 x 30 cells of the
    request box 37.0-40.5N, 19.0-22.0E (land and sea cells alike);
  * values in ug/m3, rounded to 2 decimals.

Usage:
    python3 scripts/verification/extract-cams-summary.py           # --check (default): compare, write nothing
    python3 scripts/verification/extract-cams-summary.py --write   # rewrite the summary file
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path

import xarray as xr

ROOT = Path(__file__).resolve().parent.parent.parent
ZIP_PATH = ROOT / "data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip"
SUMMARY_PATH = ROOT / "data/samples/cams-ionian-20260930-summary.json"
CELL_LAT, CELL_LON = 39.65, 19.95
VARS = {"NO2": "no2_conc", "PM10": "pm10_conc", "PM2.5": "pm2p5_conc", "CO": "co_conc"}


def build() -> dict:
    with zipfile.ZipFile(ZIP_PATH) as z:
        ds = xr.open_dataset(io.BytesIO(z.read("ENS_ANALYSIS.nc")))
    surf = ds.isel(time=0, level=0)
    cell = surf.sel(latitude=CELL_LAT, longitude=CELL_LON, method="nearest")
    values = {}
    for label, var in VARS.items():
        values[label] = {
            "at_corfu_airport": round(float(cell[var]), 2),
            "region_max": round(float(surf[var].max()), 2),
            "region_mean": round(float(surf[var].mean()), 2),
        }
    return {
        "source": "CAMS European air quality forecasts (ADS), ensemble analysis",
        "date": "2026-09-30T00:00:00Z",
        "level": "surface (0 m)",
        "bbox": {"north": 40.5, "west": 19.0, "south": 37.0, "east": 22.0},
        "corfu_airport": {"lat": float(cell.latitude), "lon": float(cell.longitude)},
        "values_ug_m3": values,
        "note": "CO2 is NOT a CAMS regional variable; nearest airport-level pollutants are NO2/PM10/PM2.5/CO.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="rewrite the summary file")
    args = ap.parse_args()
    rebuilt = build()
    if args.write:
        SUMMARY_PATH.write_text(json.dumps(rebuilt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {SUMMARY_PATH.relative_to(ROOT)}")
        return 0
    existing = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    diffs = []
    for label in VARS:
        for k in ("at_corfu_airport", "region_max", "region_mean"):
            a = existing["values_ug_m3"][label][k]
            b = rebuilt["values_ug_m3"][label][k]
            status = "OK" if abs(a - b) < 0.005 else "DIFF"
            print(f"{status:4} {label:5} {k:16} existing={a:<8} rebuilt={b}")
            if status == "DIFF":
                diffs.append((label, k, a, b))
    for k in ("lat", "lon"):
        if abs(existing["corfu_airport"][k] - rebuilt["corfu_airport"][k]) > 1e-4:
            diffs.append(("corfu_airport", k, existing["corfu_airport"][k], rebuilt["corfu_airport"][k]))
    print("REPRODUCED" if not diffs else f"NOT REPRODUCED: {diffs}")
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
