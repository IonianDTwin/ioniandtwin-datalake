#!/usr/bin/env python3
"""Export verified pull samples into a clean, schema-aligned observations dataset.

Produces:
  data/curated/observations-<date>.json  — one record per verified data point,
                                            aligned with schemas/observation-schema.json.
  data/curated/observations-<date>.csv   — flattened, human-readable view.

Driven by the same source-indicator map and manifest as the visual reports, so the
numbers here always match data/samples/INDEX.md.

Usage:
  python3 scripts/verification/export_observations.py \
      --manifest data/manifests/source-verification-2026-09-22.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_pull_reports import decode, load_map, series_for, _match_series, indicators_by_id  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--map", default="indicators/source-indicator-map.json")
    args = ap.parse_args()

    mapping = load_map(args.map)
    ind_by_id = indicators_by_id(mapping)
    series_map = series_for(mapping)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    root = Path(args.manifest).resolve().parent.parent.parent

    obs: list[dict] = []
    seen: set[str] = set()

    for ev in manifest.get("evidence", []):
        p = ev.get("sample_path")
        if not p or not p.lower().endswith(".json"):
            continue
        path = root / p
        if not path.exists():
            continue
        kind, cols, rows, labels = decode(json.loads(path.read_text(encoding="utf-8")))
        src_key = ev.get("source_id", "")
        src_series = series_map.get(src_key, [])
        url = ev.get("url", "")
        checksum = ev.get("checksum_sha256", "")
        accessed_at = ev.get("accessed_at", "")

        for s in src_series:
            for r in rows:
                if not _match_series(kind, r, [s]):
                    continue
                iid = s["indicator_id"]
                if kind == "sdmx":
                    t = r.get("time", "")
                    value = r.get("value")
                else:
                    t = r.get("time", "")  # open-meteo current/daily time
                    value = r.get("value")
                oid = f"{src_key}:{iid}:{s.get('label','')}:{t}"
                if oid in seen:
                    continue
                seen.add(oid)
                ind = ind_by_id.get(iid, {})
                obs.append({
                    "observation_id": oid,
                    "indicator_id": iid,
                    "indicator_name": ind.get("name", iid),
                    "source_id": src_key,
                    "observed_at": t,
                    "ingested_at": accessed_at,
                    "spatial_ref": {
                        "level": "NUTS2" if kind == "sdmx" else "point",
                        "code": r.get("geo", "") if kind == "sdmx" else "39.62,19.92",
                        "geometry": None,
                    },
                    "value": value,
                    "unit": s.get("unit", "") or (r.get("unit", "") if kind != "sdmx" else ""),
                    "series_label": s.get("label", ""),
                    "polarity": None,
                    "provenance": {
                        "raw_checksum_sha256": checksum,
                        "access_method": "api",
                        "request_url": url,
                    },
                })

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = root / "data" / "curated"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"observations-{date}.json"
    csv_path = out_dir / f"observations-{date}.csv"
    json_path.write_text(json.dumps(obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fieldnames = ["observation_id", "indicator_id", "indicator_name", "series_label",
                  "source_id", "observed_at", "value", "unit", "spatial_level", "spatial_code"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for o in obs:
            w.writerow({
                "observation_id": o["observation_id"],
                "indicator_id": o["indicator_id"],
                "indicator_name": o["indicator_name"],
                "series_label": o["series_label"],
                "source_id": o["source_id"],
                "observed_at": o["observed_at"],
                "value": o["value"],
                "unit": o["unit"],
                "spatial_level": o["spatial_ref"]["level"],
                "spatial_code": o["spatial_ref"]["code"],
            })

    print(f"exported {len(obs)} observations")
    print(f"  {json_path}")
    print(f"  {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
