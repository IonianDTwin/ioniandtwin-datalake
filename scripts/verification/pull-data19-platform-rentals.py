#!/usr/bin/env python3
"""Pull and compute Data19 — Short-term rental (platform) share — for EL62.

Durable implementation of the resolution in ``daily/2026-10-15/research-notes.md``
§7. InsideAirbnb is non-viable for EL62 (no Ionian coverage; Greece key returned
HTTP 403). The authoritative substitute is Eurostat ``tour_ce_omn12`` — "Short-stay
accommodation offered via online platforms by months, residence of the guest and
NUTS 1 and NUTS 2 region" — published under the European Commission data-sharing
agreement with Airbnb, Booking.com, Expedia Group and Tripadvisor (open JSON-stat
REST API, no key).

Method
------
For each year Y in 2018..2025::

    platform_nights(Y)    = tour_ce_omn12, indic_to=NGT_SP, c_resid=TOTAL,
                            month=TOTAL, geo=EL62            (platform guest nights)
    conventional_nights(Y)= tour_occ_nin2, c_resid=TOTAL, unit=NR,
                            nace_r2=I551-I553, geo=EL62      (conventional nights)
    total_nights(Y)       = platform_nights(Y) + conventional_nights(Y)
    Data19(Y)             = platform_nights(Y) / total_nights(Y) * 100

``Data19`` is the share of platform-mediated nights within **total** tourism
nights (conventional + platform) — the market-share formulation in research-notes
§7E. A 2025 monthly breakdown of ``tour_ce_omn12`` is also retained as the
seasonality profile (§7D).

Outputs
-------
* ``data/raw/eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json``   (raw, git-ignored)
* ``data/raw/eurostat-tour_ce_omn12-el62-ngtsp-2025-monthly.json``       (raw, git-ignored)
* ``data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json``      (raw, git-ignored)
* ``data/curated/data19-platform-rental-share.json``                      (full audit)
* ``data/curated/observations-data19-platform-rental-share-<date>.json`` / ``.csv``
  — schema-compliant annual observations (one per year 2018..2025, NUTS2/EL62).

Usage
-----
    python3 scripts/verification/pull-data19-platform-rentals.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RAW = ROOT / "data" / "raw"
CURATED = ROOT / "data" / "curated"
SCHEMA_PATH = ROOT / "schemas" / "observation-schema.json"

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

YEARS = [str(y) for y in range(2018, 2026)]  # 2018..2025

GEO = "EL62"           # Ionia Nisia (NUTS 2021)
INDIC = "NGT_SP"       # Nights spent (platform guest nights)
RESID = "TOTAL"
CONV_UNIT = "NR"
NACE = "I551-I553"     # hotels + short-stay + camping (conventional accommodation)

USER_AGENT = "IonianDTwin-data19/1.0 (read-only, no-key Eurostat pull)"

# Raw payload paths (immutable, git-ignored under data/raw/).
RAW_PLATFORM_ANNUAL = RAW / "eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json"
RAW_PLATFORM_MONTHLY = RAW / "eurostat-tour_ce_omn12-el62-ngtsp-2025-monthly.json"
RAW_CONVENTIONAL = RAW / "eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path, timeout: int = 90, retries: int = 3) -> int:
    """GET ``url`` to ``dest``; return byte length. Raises on persistent failure."""
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            dest.write_bytes(data)
            return len(data)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise SystemExit(f"fetch failed after {retries} tries: {url} -> {last}")


def iter_cells(doc: dict):
    """Yield one dict per populated JSON-stat cell: dimension label -> value plus 'value'.

    JSON-stat packs cells into a flat ``value`` dict keyed by a dense integer index
    over the dimension product (first dimension in ``id`` varies slowest).
    """
    ids = doc["id"]
    sizes = doc["size"]
    index = {name: doc["dimension"][name]["category"]["index"] for name in ids}
    label_of = {name: {i: lab for lab, i in idx.items()} for name, idx in index.items()}

    for flat, value in doc.get("value", {}).items():
        i = int(flat)
        row = {}
        for name in reversed(ids):  # innermost dimension first
            size = sizes[ids.index(name)]
            row[name] = label_of[name][i % size]
            i //= size
        row["value"] = value
        yield row


def platform_annual_url() -> str:
    q = [("geo", GEO), ("indic_to", INDIC), ("c_resid", RESID), ("month", "TOTAL")]
    q += [("time", y) for y in YEARS]
    q.append(("lang", "en"))
    return f"{BASE}/tour_ce_omn12?{urllib.parse.urlencode(q)}"


def platform_monthly_url() -> str:
    q = [("geo", GEO), ("indic_to", INDIC), ("c_resid", RESID),
         ("time", "2025"), ("lang", "en")]
    return f"{BASE}/tour_ce_omn12?{urllib.parse.urlencode(q)}"


def conventional_url() -> str:
    q = [("geo", GEO), ("c_resid", RESID), ("unit", CONV_UNIT),
         ("nace_r2", NACE)]
    q += [("time", y) for y in YEARS]
    q.append(("lang", "en"))
    return f"{BASE}/tour_occ_nin2?{urllib.parse.urlencode(q)}"


def parse_annual_platform(doc: dict) -> dict:
    """Return {year: int nights} for the annual NGT_SP series."""
    out = {}
    for row in iter_cells(doc):
        out[row["time"]] = int(row["value"])
    return out


def parse_monthly_platform(doc: dict) -> dict:
    """Return {month: int nights} for the 2025 monthly breakdown (TOTAL + M01..M12)."""
    out = {}
    for row in iter_cells(doc):
        if row.get("time") == "2025":
            out[row["month"]] = int(row["value"])
    return out


def parse_conventional(doc: dict) -> dict:
    out = {}
    for row in iter_cells(doc):
        out[row["time"]] = int(row["value"])
    return out


def _obs(year: str, share_pct: float, platform_sha: str, formula_url: str,
         ingested_at: str) -> dict:
    return {
        "observation_id": f"Eurostat_tour_ce_omn12:Data19:platform_rental_share:{year}",
        "indicator_id": "Data19",
        "indicator_name": "Short-term rental share (Airbnb)",
        "series_label": "platform rental share",
        "source_id": "Eurostat_tour_ce_omn12",
        "observed_at": year,
        "observed_period_end": f"{year}-12-31",
        "temporal_granularity": "annual",
        "ingested_at": ingested_at,
        "spatial_ref": {"level": "NUTS2", "code": "EL62", "geometry": None},
        "value": share_pct,
        "unit": "%",
        "polarity": None,
        "provenance": {
            "raw_checksum_sha256": platform_sha,
            "raw_manifest": "source-verification-2026-10-15",
            "access_method": "derived",
            "request_url": formula_url,
        },
    }


def validate_against_schema(obs: list[dict], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = schema.get("required", [])
    allowed = set(schema.get("properties", {}))
    problems = []
    for o in obs:
        for k in required:
            if k not in o:
                problems.append(f"{o.get('observation_id', '?')}: missing '{k}'")
        for k in o:
            if k not in allowed:
                problems.append(f"{o.get('observation_id', '?')}: unknown key '{k}'")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, default=CURATED)
    ap.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    ap.add_argument("--run-date", default=None, help="override output-file date stamp")
    ap.add_argument("--no-fetch", action="store_true",
                    help="reuse already-downloaded raw payloads instead of re-fetching")
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # --- acquire (read-only, no credentials) --------------------------------
    platform_url = platform_annual_url()
    monthly_url = platform_monthly_url()
    conv_url = conventional_url()

    if not args.no_fetch or not RAW_PLATFORM_ANNUAL.exists():
        n = fetch(platform_url, RAW_PLATFORM_ANNUAL)
        print(f"tour_ce_omn12 (annual)  -> {RAW_PLATFORM_ANNUAL.relative_to(ROOT)} ({n} bytes)")
    if not args.no_fetch or not RAW_PLATFORM_MONTHLY.exists():
        n = fetch(monthly_url, RAW_PLATFORM_MONTHLY)
        print(f"tour_ce_omn12 (2025 monthly) -> {RAW_PLATFORM_MONTHLY.relative_to(ROOT)} ({n} bytes)")
    if not args.no_fetch or not RAW_CONVENTIONAL.exists():
        n = fetch(conv_url, RAW_CONVENTIONAL)
        print(f"tour_occ_nin2 (annual) -> {RAW_CONVENTIONAL.relative_to(ROOT)} ({n} bytes)")

    platform_doc = json.loads(RAW_PLATFORM_ANNUAL.read_text(encoding="utf-8"))
    monthly_doc = json.loads(RAW_PLATFORM_MONTHLY.read_text(encoding="utf-8"))
    conv_doc = json.loads(RAW_CONVENTIONAL.read_text(encoding="utf-8"))

    platform_sha = sha256(RAW_PLATFORM_ANNUAL)
    monthly_sha = sha256(RAW_PLATFORM_MONTHLY)
    conv_sha = sha256(RAW_CONVENTIONAL)

    platform = parse_annual_platform(platform_doc)
    monthly = parse_monthly_platform(monthly_doc)
    conventional = parse_conventional(conv_doc)

    missing = [y for y in YEARS if y not in platform or y not in conventional]
    if missing:
        print(f"error: missing years {missing}", file=sys.stderr)
        return 2

    # --- transform ----------------------------------------------------------
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_date = args.run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    series = []
    observations = []
    for y in YEARS:
        p = platform[y]
        c = conventional[y]
        total = p + c
        share = round(p / total * 100, 2) if total else None
        series.append({
            "year": y,
            "platform_nights": p,
            "conventional_nights": c,
            "total_tourism_nights": total,
            "share_pct": share,
        })
        observations.append(_obs(
            y, share, platform_sha,
            f"Data19(Y)=tour_ce_omn12[NGT_SP,TOTAL]({y})/"
            f"(tour_occ_nin2[NR,TOTAL]({y})+tour_ce_omn12[NGT_SP,TOTAL]({y}))*100",
            ingested_at,
        ))

    # 2025 monthly breakdown (seasonality profile, research-notes §7D)
    month_order = ["TOTAL"] + [f"M{i:02d}" for i in range(1, 13)]
    seasonality = [{"month": m, "platform_nights": monthly.get(m)}
                   for m in month_order if m in monthly]

    # --- curated audit dataset ---------------------------------------------
    dataset = {
        "title": "Data19 — Short-term rental (platform) share of tourism nights (EL62)",
        "indicator_id": "Data19",
        "indicator_name": "Short-term rental share (Airbnb)",
        "status": "VERIFIED",
        "computed_at_utc": datetime.now(timezone.utc).isoformat(),
        "spatial_ref": {"level": "NUTS2", "code": "EL62"},
        "method": ("Data19(Y) = NGT_SP_platform(EL62,Y) / "
                   "(NGT_conventional(EL62,Y) + NGT_SP_platform(EL62,Y)) * 100; "
                   "share of platform-mediated nights within total tourism nights "
                   "(research-notes 2026-10-15 §7E)."),
        "sources": [
            {
                "source_id": "Eurostat_tour_ce_omn12",
                "dataset": "tour_ce_omn12",
                "dimensions": {"indic_to": INDIC, "c_resid": RESID,
                               "month": "TOTAL", "geo": GEO, "time": YEARS},
                "url": platform_url,
                "raw_path": str(RAW_PLATFORM_ANNUAL.relative_to(ROOT)),
                "sha256": platform_sha,
                "updated": platform_doc.get("updated"),
                "note": ("Nights spent in short-stay accommodation offered via online "
                         "platforms (Airbnb, Booking.com, Expedia, Tripadvisor), under "
                         "the EC platform data-sharing agreement."),
            },
            {
                "source_id": "Eurostat_tour_ce_omn12_monthly_2025",
                "dataset": "tour_ce_omn12",
                "dimensions": {"indic_to": INDIC, "c_resid": RESID,
                               "month": "M01..M12+TOTAL", "geo": GEO, "time": "2025"},
                "url": monthly_url,
                "raw_path": str(RAW_PLATFORM_MONTHLY.relative_to(ROOT)),
                "sha256": monthly_sha,
                "updated": monthly_doc.get("updated"),
                "note": "2025 monthly breakdown (seasonality profile).",
            },
            {
                "source_id": "Eurostat_tour_occ_nin2",
                "dataset": "tour_occ_nin2",
                "dimensions": {"c_resid": RESID, "unit": CONV_UNIT,
                               "nace_r2": NACE, "geo": GEO, "time": YEARS},
                "url": conv_url,
                "raw_path": str(RAW_CONVENTIONAL.relative_to(ROOT)),
                "sha256": conv_sha,
                "updated": conv_doc.get("updated"),
                "note": "Conventional accommodation nights (the denominator's "
                        "conventional component, also used by Data16/26/31/33).",
            },
        ],
        "series": series,
        "seasonality_2025": seasonality,
        "flags": [
            ("2025 step change: platform nights 8,644,420 vs 4,400,084 in 2024 (+96%). "
             "Likely a coverage/onboarding change in the EC platform agreement rather "
             "than true market growth; treat the 2025 share (29.80 %) with caution and "
             "re-verify against the next Eurostat release before policy use."),
            ("InsideAirbnb is superseded: it has no Ionian Islands coverage (Greece "
             "covers Athens/Crete only; guessed Athens key returned HTTP 403)."),
            ("Polarity is left null: the proposal does not specify direction for Data19 "
             "(higher platform share is expected to signal more social/infrastructure "
             "pressure, but that mapping is not yet signed off)."),
        ],
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = args.out_dir / "data19-platform-rental-share.json"
    obs_json = args.out_dir / f"observations-data19-platform-rental-share-{run_date}.json"
    obs_csv = args.out_dir / f"observations-data19-platform-rental-share-{run_date}.csv"

    dataset_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    obs_json.write_text(json.dumps(observations, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")

    fields = ["observation_id", "indicator_id", "indicator_name", "series_label",
              "source_id", "temporal_granularity", "observed_at", "observed_period_end",
              "value", "unit", "spatial_level", "spatial_code", "polarity"]
    with obs_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for o in observations:
            w.writerow({
                "observation_id": o["observation_id"],
                "indicator_id": o["indicator_id"],
                "indicator_name": o["indicator_name"],
                "series_label": o["series_label"],
                "source_id": o["source_id"],
                "temporal_granularity": o["temporal_granularity"],
                "observed_at": o["observed_at"],
                "observed_period_end": o["observed_period_end"],
                "value": o["value"],
                "unit": o["unit"],
                "spatial_level": o["spatial_ref"]["level"],
                "spatial_code": o["spatial_ref"]["code"],
                "polarity": o["polarity"],
            })

    problems = validate_against_schema(observations, args.schema)

    # --- summary ------------------------------------------------------------
    print("\n=== Data19 platform rental share (EL62) ===")
    print(f"{'year':6s} {'platform':>12s} {'conventional':>14s} {'total':>12s} {'share %':>8s}")
    for r in series:
        print(f"{r['year']:6s} {r['platform_nights']:>12,d} "
              f"{r['conventional_nights']:>14,d} {r['total_tourism_nights']:>12,d} "
              f"{r['share_pct']:>8.2f}")
    if seasonality:
        peak = max((s for s in seasonality if s["month"] != "TOTAL"),
                   key=lambda s: s["platform_nights"] or 0)
        total_2025 = next(s["platform_nights"] for s in seasonality if s["month"] == "TOTAL")
        julaug = sum(s["platform_nights"] for s in seasonality
                     if s["month"] in ("M07", "M08"))
        print(f"2025 seasonality: Jul+Aug = {julaug:,} nights "
              f"({julaug / total_2025 * 100:.1f} % of {total_2025:,}); "
              f"peak month {peak['month']} = {peak['platform_nights']:,}")

    print(f"\nwrote {dataset_path.relative_to(ROOT)}")
    print(f"wrote {obs_json.relative_to(ROOT)}")
    print(f"wrote {obs_csv.relative_to(ROOT)}")
    print("\nmanifest checksums:")
    print(f"  tour_ce_omn12 annual   sha256 {platform_sha}")
    print(f"  tour_ce_omn12 2025-m   sha256 {monthly_sha}")
    print(f"  tour_occ_nin2 annual   sha256 {conv_sha}")

    if problems:
        print(f"\nSCHEMA PROBLEMS ({len(problems)}):", file=sys.stderr)
        for p in problems[:20]:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"\nobservations schema-valid: {len(observations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
