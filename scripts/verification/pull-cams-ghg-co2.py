#!/usr/bin/env python3
"""Bounded pull of CAMS global greenhouse gas forecast surface CO2 over the Ionian Islands.

Data01 feasibility test (2026-11-06). Read-only request to the Atmosphere Data Store:
dataset cams-global-greenhouse-gas-forecasts, variable carbon_dioxide, model level 137
(lowest level = surface), one forecast day (lead times 0-21 h), bbox 37.0-40.5N 19.0-22.0E.
Key: CAMS_API_KEY in the untracked .env (never printed).

Usage: python3 -P scripts/verification/pull-cams-ghg-co2.py --date 2026-10-30 [--summarise ZIP]
Output: data/raw/cams-ghg-forecast-co2-ml137-IONIAN-<date>.zip
Status of outputs: PROPOSAL (feasibility only).
"""
import argparse
import hashlib
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = "cams-global-greenhouse-gas-forecasts"
ADS_URL = "https://ads.atmosphere.copernicus.eu/api"
AIRPORTS = {  # approximate aerodrome reference points
    "CFU": (39.6019, 19.9117),
    "EFL": (38.1201, 20.5005),
    "ZTH": (37.7509, 20.8843),
    "PVK": (38.9255, 20.7653),
}


def load_key():
    key = os.environ.get("CAMS_API_KEY")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith("CAMS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        sys.exit("CAMS_API_KEY not found in environment or .env")
    return key


def pull(date):
    import cads_api_client

    target = ROOT / f"data/raw/cams-ghg-forecast-co2-ml137-IONIAN-{date}.zip"
    if target.exists():
        sys.exit(f"refusing to overwrite existing raw file {target}")
    request = {
        "variable": ["carbon_dioxide"],
        "model_level": ["137"],
        "date": [f"{date}/{date}"],
        "leadtime_hour": [str(h) for h in range(0, 24, 3)],
        "area": [40.5, 19.0, 37.0, 22.0],
        "data_format": "netcdf_zip",
    }
    client = cads_api_client.ApiClient(url=ADS_URL, key=load_key())
    client.retrieve(DATASET, target=str(target), **request)
    print("request", request)
    print("wrote", target.relative_to(ROOT), target.stat().st_size, "bytes")
    print("sha256", hashlib.sha256(target.read_bytes()).hexdigest())
    return target


def summarise(path):
    import tempfile

    import xarray as xr

    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(path) as z:
        z.extractall(tmp)
        for nc in sorted(Path(tmp).glob("*.nc")):
            ds = xr.open_dataset(nc)
            print("file", nc.name, "vars", list(ds.data_vars), "dims", dict(ds.sizes))
            var = [v for v in ds.data_vars if "co2" in v.lower()][0]
            da = ds[var].squeeze()
            print("units", da.attrs.get("units"), "long_name", da.attrs.get("long_name"))
            lat = [c for c in da.dims if "lat" in c][0]
            lon = [c for c in da.dims if "lon" in c][0]
            print("grid step lat", float(abs(ds[lat][1] - ds[lat][0])), "lon", float(abs(ds[lon][1] - ds[lon][0])))
            # kg/kg -> ppm by volume: x * M_air / M_CO2 * 1e6
            ppm = da * (28.9644 / 44.0095) * 1e6 if da.attrs.get("units") == "kg kg**-1" else da
            print("region mean ppm", round(float(ppm.mean()), 2), "min", round(float(ppm.min()), 2), "max", round(float(ppm.max()), 2))
            for code, (la, lo) in AIRPORTS.items():
                cell = ppm.sel({lat: la, lon: lo}, method="nearest")
                vals = [round(float(x), 2) for x in cell.values.ravel()]
                print(code, "cell", round(float(cell[lat]), 2), round(float(cell[lon]), 2),
                      "mean", round(sum(vals) / len(vals), 2), "min", min(vals), "max", max(vals))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--summarise", type=Path)
    a = ap.parse_args()
    if a.summarise:
        summarise(a.summarise)
    elif a.date:
        summarise(pull(a.date))
    else:
        ap.error("give --date or --summarise")


if __name__ == "__main__":
    main()
