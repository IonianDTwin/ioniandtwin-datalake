#!/usr/bin/env python3
"""Compute Data29 (Seasonality) for EL62 and Greece from Eurostat monthly nights (D-026).

Lineage:
  data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json        (all accommodation, monthly, NUTS 2)
  data/raw/eurostat-tour_ce_omn12-EL62-EL-monthly-2020-2023.json (online platforms, monthly; reconciliation only)
  data/raw/eutd-tourism-dashboard-2024-indicators.csv             (TOUR_SOE_02; reconciliation only)
    --( this script )--> data/curated/data29-seasonality.json
                         data/curated/observations-data29-seasonality-2026-11-03.json / .csv

Measures per geo (EL62, EL) and year (2020-2025), from the 12 monthly nights N_1..N_12:
  headline   top3_share   = sum of the 3 largest N_m / sum N_m * 100
                            (EU Tourism Dashboard TOUR_SOE_02 definition, here over ALL accommodation)
  index      gini         = Gini coefficient of the 12 monthly values
                            = sum_i (2i - n - 1) * x_(i) / (n * sum x), x sorted ascending, n = 12
                            0 = nights spread evenly over the year; (n-1)/n = 0.917 = all nights in one month
  context    peak_month_share = max N_m / sum N_m * 100
  context    share_outside_jun_sep = (sum N_m for m not in Jun..Sep) / sum N_m * 100
  context    monthly nights for EL62 (one observation per month)

Before writing, the script checks the definition against the dashboard:
  * EL:   top3_share of all accommodation must equal TOUR_SOE_02 for 2021-2023 (within 0.01);
          2020 is a known revision, tested within 0.5 pp (69.79 vs 70.09);
  * EL62: top3_share of PLATFORM nights must equal TOUR_SOE_02 for 2020-2023 (within 0.01).
If either check fails it writes nothing and exits 1.

Usage:
  python3 scripts/verification/compute-data29-seasonality.py           # compute, check, write
  python3 scripts/verification/compute-data29-seasonality.py --check   # compute and check, write nothing
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RAW_NIN2M = ROOT / "data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json"
RAW_OMN12 = ROOT / "data/raw/eurostat-tour_ce_omn12-EL62-EL-monthly-2020-2023.json"
RAW_EUTD = ROOT / "data/raw/eutd-tourism-dashboard-2024-indicators.csv"
OUT_AUDIT = ROOT / "data/curated/data29-seasonality.json"
OUT_OBS = ROOT / "data/curated/observations-data29-seasonality-2026-11-03.json"
# Monthly inputs (EL62 + EL, 2020-2025). Deliberately named so build_dashboard.py's
# "observations-data29-seasonality-*" pattern does NOT merge them into the master snapshot.
OUT_MONTHLY = ROOT / "data/curated/monthly-data29-nights-2026-11-03.json"
MANIFEST_ID = "source-verification-2026-11-03"
NIN2M_URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2m"
             "?format=JSON&lang=EN&geo=EL62&geo=EL&unit=NR&c_resid=TOTAL")
MONTHS = [f"M{m:02d}" for m in range(1, 13)]
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]
GEOS = ["EL62", "EL"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonstat_getter(path: Path, expect_label: str):
    d = json.loads(path.read_text(encoding="utf-8"))
    # Identity check: a candidate run must fail on the wrong dataset, not pass quietly.
    if not d.get("label", "").startswith(expect_label) or not {"month", "geo", "time"} <= set(d.get("id", [])):
        raise SystemExit(f"FAIL: {path} is not the expected dataset ('{expect_label}'); got '{d.get('label')}'")
    ids, size = d["id"], d["size"]
    cat = {k: d["dimension"][k]["category"]["index"] for k in ids}

    def get(**kw):
        idx = 0
        for k, s in zip(ids, size):
            idx = idx * s + (cat[k][kw[k]] if k in kw else 0)
        return d["value"].get(str(idx))
    return get


def monthly(get, geo: str, year: str) -> list[float] | None:
    vals = [get(geo=geo, time=year, month=m) for m in MONTHS]
    return None if any(v is None for v in vals) else vals


def top3_share(v): return sum(sorted(v)[-3:]) / sum(v) * 100


def gini(v):
    s = sorted(v)
    n = len(s)
    return sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(s)) / (n * sum(s))


def dashboard_values() -> dict[tuple[str, str], float]:
    out = {}
    with RAW_EUTD.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["code"] == "TOUR_SOE_02" and r["nuts_code_2021"] in GEOS:
                out[(r["nuts_code_2021"], r["year"])] = float(r["value"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="compute and reconcile only; write nothing")
    ap.add_argument("--nin2m", type=Path, default=RAW_NIN2M, help="alternative tour_occ_nin2m raw file (scheduler candidate)")
    ap.add_argument("--omn12", type=Path, default=RAW_OMN12, help="alternative tour_ce_omn12 raw file (scheduler candidate)")
    args = ap.parse_args()
    if not args.check and (args.nin2m != RAW_NIN2M or args.omn12 != RAW_OMN12):
        print("Alternative raw files are allowed only with --check (promotion is a reviewed step).", file=sys.stderr)
        return 2

    nin2m = jsonstat_getter(args.nin2m, "Nights spent at tourist accommodation establishments by month and NUTS 2 region")
    omn12 = jsonstat_getter(args.omn12, "Short-stay accommodation")
    dash = dashboard_values()

    # 1. Reconcile the definition against the dashboard before computing anything else.
    # Exact match (<= 0.01) is required everywhere except KNOWN_REVISIONS. EL 2020 does not
    # reproduce: dashboard 69.79 vs 70.09 recomputed from the 2026-11-03 tour_occ_nin2m pull.
    # The likely cause is a Eurostat revision of the COVID-year series after the 2024 dashboard
    # export. It is tested with a 0.5 pp tolerance and the delta is recorded, not hidden
    # (DeepSeek review 2026-11-03, finding F1).
    KNOWN_REVISIONS = {("EL", "2020"): 0.5}
    problems, recon = [], []
    for (geo, year), dval in sorted(dash.items()):
        if geo == "EL" and year in ("2020", "2021", "2022", "2023"):
            ours, basis = top3_share(monthly(nin2m, geo, year)), "all accommodation (tour_occ_nin2m)"
        elif geo == "EL62" and year in ("2020", "2021", "2022", "2023"):
            ours, basis = top3_share(monthly(omn12, geo, year)), "online platforms (tour_ce_omn12)"
        else:
            continue
        tol = KNOWN_REVISIONS.get((geo, year), 0.01)
        delta = round(round(ours, 2) - dval, 2)
        ok = abs(delta) <= tol
        status = "OK  " if ok and tol == 0.01 else ("REV " if ok else "FAIL")
        recon.append({"geo": geo, "year": year, "dashboard": dval, "recomputed": round(ours, 2), "delta_pp": delta,
                      "tolerance_pp": tol, "basis": basis, "match": ok,
                      **({"note": "known revision: probable Eurostat revision after the 2024 dashboard export"} if tol != 0.01 else {})})
        print(f"{status} TOUR_SOE_02 {geo} {year}: dashboard {dval} vs {basis} {ours:.2f} (delta {delta:+.2f} pp, tolerance {tol})")
        if not ok:
            problems.append(f"{geo} {year}")
    if problems:
        print(f"Definition check FAILED for {problems}; nothing written.", file=sys.stderr)
        return 1

    # 2. Compute the measures.
    raw_sha = sha256(RAW_NIN2M)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results: dict[str, dict[str, dict]] = {}
    obs: list[dict] = []
    monthly_obs: list[dict] = []

    def add(oid, label, observed_at, gran, geo, value, unit, polarity, formula):
        obs.append({
            "observation_id": oid, "indicator_id": "Data29", "indicator_name": "Seasonality (%)",
            "series_label": label, "source_id": "Eurostat_tour_occ_nin2m",
            "observed_at": observed_at, "observed_period_end": None, "temporal_granularity": gran,
            "ingested_at": now,
            "spatial_ref": {"level": "NUTS2" if len(geo) == 4 else "country", "code": geo, "geometry": None},
            "value": value, "unit": unit, "polarity": polarity,
            "provenance": {"raw_checksum_sha256": raw_sha, "raw_manifest": MANIFEST_ID,
                           "access_method": "derived", "request_url": NIN2M_URL,
                           "request_params": {"formula": formula}},
        })

    for geo in GEOS:
        results[geo] = {}
        for year in YEARS:
            v = monthly(nin2m, geo, year)
            if v is None:
                continue
            total = sum(v)
            peak_i = v.index(max(v))
            r = {
                "nights_total": total,
                "monthly_nights": dict(zip(MONTHS, v)),
                "top3_months": [MONTHS[i] for i in sorted(range(12), key=lambda i: v[i])[-3:]][::-1],
                "top3_share_pct": round(top3_share(v), 2),
                "gini": round(gini(v), 4),
                "peak_month": MONTHS[peak_i],
                "peak_month_share_pct": round(max(v) / total * 100, 2),
                "share_outside_jun_sep_pct": round((total - sum(v[5:9])) / total * 100, 2),
            }
            if geo == "EL62" and year in ("2020", "2021", "2022", "2023"):
                p = monthly(omn12, geo, year)
                r["platform_top3_share_pct"] = round(top3_share(p), 2) if p else None
            results[geo][year] = r
            base = f"Eurostat_tour_occ_nin2m:Data29"
            add(f"{base}:top3_share:{geo}:{year}", "share of annual nights in the 3 busiest months (all accommodation)",
                year, "annual", geo, r["top3_share_pct"], "%", "negative",
                "sum(3 largest monthly nights) / sum(12 monthly nights) * 100")
            add(f"{base}:gini:{geo}:{year}", "Seasonality Index: Gini coefficient of monthly nights (all accommodation)",
                year, "annual", geo, r["gini"], "index (0-1)", "negative",
                "Gini over 12 monthly nights; 0 = even, 0.917 = one month")
            add(f"{base}:peak_month_share:{geo}:{year}", "peak-month share of annual nights (all accommodation)",
                year, "annual", geo, r["peak_month_share_pct"], "%", "negative",
                f"max(monthly nights) / sum * 100 (peak {r['peak_month']})")
            add(f"{base}:share_outside_jun_sep:{geo}:{year}", "share of annual nights outside June-September (all accommodation)",
                year, "annual", geo, r["share_outside_jun_sep_pct"], "%", "positive",
                "sum(nights Jan-May, Oct-Dec) / sum(12 monthly nights) * 100")
            # Monthly inputs go to a separate file (owner decision 2026-11-03, review B4/F9),
            # like Data07: merged into the Data29 folder, not into the master snapshot.
            n_annual = len(obs)
            for m, n in zip(MONTHS, v):
                add(f"{base}:monthly_nights:{geo}:{year}-{m[1:]}", "monthly nights (all accommodation)",
                    f"{year}-{m[1:]}", "monthly", geo, n, "nights", None, "as published")
            monthly_obs.extend(obs[n_annual:])
            del obs[n_annual:]

    audit = {
        "indicator_id": "Data29",
        "decision": "D-026",
        "computed_at": now,
        "definition": {
            "headline": "top3_share_pct: share of annual nights in the 3 busiest months, all accommodation (TOUR_SOE_02 definition)",
            "seasonality_index": "gini: Gini coefficient of the 12 monthly nights counts",
            "context": ["peak_month_share_pct", "share_outside_jun_sep_pct", "monthly_nights"],
        },
        "dashboard_reconciliation": recon,
        "dashboard_note": ("TOUR_SOE_02 for EL62 is computed from online-platform nights only (tour_ce_omn12); "
                           "for EL it uses all accommodation. The EL62 dashboard value 71.08 (2023) is kept as a "
                           "separate platform-only series; the headline here uses all accommodation."),
        "inputs": {
            "tour_occ_nin2m": {"path": str(RAW_NIN2M.relative_to(ROOT)), "sha256": raw_sha},
            "tour_ce_omn12_monthly": {"path": str(RAW_OMN12.relative_to(ROOT)), "sha256": sha256(RAW_OMN12)},
            "eutd_csv": {"path": str(RAW_EUTD.relative_to(ROOT)), "sha256": sha256(RAW_EUTD)},
        },
        "caveats": [
            "2020 and 2021 are distorted by COVID-19 restrictions.",
            "EL 2020 does not reproduce the dashboard exactly (69.79 vs 70.09, +0.30 pp). Probably a Eurostat revision; tested with a 0.5 pp tolerance and recorded in dashboard_reconciliation.",
            "Monthly totals are not normalised by days in month (Eurostat convention). Effect for EL62 2023: top-3 63.81 -> 63.59 per-day, Gini 0.5827 -> 0.5809 (DeepSeek review B4).",
            "No accommodation-type split exists in tour_occ_nin2m at NUTS 2.",
            "No monthly data exists for the NUTS 3 islands (tour_occ_nin3m, tour_ce_omn3: HTTP 404).",
        ],
        "results": results,
    }

    for geo in GEOS:
        for year, r in results[geo].items():
            print(f"{geo} {year}: top3 {r['top3_share_pct']:6.2f} %  gini {r['gini']:.4f}  "
                  f"peak {r['peak_month']} {r['peak_month_share_pct']:5.2f} %  outside Jun-Sep {r['share_outside_jun_sep_pct']:5.2f} %")
    print(f"{len(obs)} annual observations (master) + {len(monthly_obs)} monthly observations (separate file)")
    if args.check:
        return 0

    OUT_AUDIT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_OBS.write_text(json.dumps(obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MONTHLY.write_text(json.dumps(monthly_obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with OUT_OBS.with_suffix(".csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["observation_id", "series_label", "observed_at", "spatial_code", "value", "unit"])
        for o in obs:
            w.writerow([o["observation_id"], o["series_label"], o["observed_at"], o["spatial_ref"]["code"], o["value"], o["unit"]])
    print(f"wrote {OUT_AUDIT.relative_to(ROOT)}, {OUT_OBS.relative_to(ROOT)} (+ .csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
