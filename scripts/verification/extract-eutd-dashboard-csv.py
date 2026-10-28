#!/usr/bin/env python3
"""Extract EL62 & Ionian NUTS3 indicators from the EU Tourism Dashboard 2024 CSV export.

Reads the immutable raw CSV (`data/raw/eutd-tourism-dashboard-2024-indicators.csv`),
filters rows for `EL62` (and `EL621`..`EL624`), and writes:
  - `data/samples/eutd-tourism-dashboard-2024-el62.json`
  - `data/samples/eutd-tourism-dashboard-2024-ionian.json`

Covers indicators: Data02 (TOUR_ENV_05), Data04 (TOUR_DES_10), Data23 (TOUR_DES_14),
Data25 (TOUR_DES_13), Data28 (TOUR_DES_04), Data29 (TOUR_SOE_02).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RAW_CSV = ROOT / "data" / "raw" / "eutd-tourism-dashboard-2024-indicators.csv"
OUT_EL62 = ROOT / "data" / "samples" / "eutd-tourism-dashboard-2024-el62.json"
OUT_IONIAN = ROOT / "data" / "samples" / "eutd-tourism-dashboard-2024-ionian.json"

CODE_MAP = {
    "TOUR_ENV_05": ("excellent_bathing_water", "Data02"),
    "TOUR_DES_10": ("blue_flag_sites", "Data04"),
    "TOUR_DES_14": ("cultural_assets_density", "Data23"),
    "TOUR_DES_13": ("high_nature_value_accommodation", "Data25"),
    "TOUR_DES_04": ("net_occupancy", "Data28"),
    "TOUR_SOE_02": ("peak_season_share", "Data29"),
}


def main() -> int:
    if not RAW_CSV.exists():
        raise SystemExit(f"Missing raw CSV: {RAW_CSV}")

    el62_out: dict[str, dict] = {}
    with RAW_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nuts = (row.get("nuts_code_2021") or "").strip()
            code = (row.get("code") or "").strip()
            if nuts == "EL62" and code in CODE_MAP:
                key, data_id = CODE_MAP[code]
                year = int(row["year"])
                val = float(row["value"])
                if key not in el62_out or year >= el62_out[key]["year"]:
                    el62_out[key] = {
                        "data_id": data_id,
                        "code": code,
                        "year": year,
                        "unit": row.get("unit", ""),
                        "value": val,
                    }

    payload = {
        "source": "EU Tourism Dashboard - 2024 release",
        "csv_url": "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv",
        "dataset_id": "9564824a-7f16-4efa-82fb-d4e176350026",
        "accessed_at": "2026-10-03",
        "el62": el62_out,
    }
    OUT_EL62.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_EL62.relative_to(ROOT)} ({len(el62_out)} indicators)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
