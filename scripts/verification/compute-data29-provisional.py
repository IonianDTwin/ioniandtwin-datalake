#!/usr/bin/env python3
"""Provisional current-year monthly nights for EL62 (Data29 context), with a backtest. `PROPOSAL`.

Why: Eurostat publishes EL62 monthly nights (tour_occ_nin2m) once a year, about 10 months after
year-end. Greece's monthly nights (tour_occ_nim) arrive about 2 months after each month. The twin
needs current-year monthly values, so this script estimates EL62 from the Greek figure.

Method (fixed in advance, not tuned to the result):
  share(y, m)         = EL62 nights(y, m) / EL nights(y, m)                 from tour_occ_nin2m
  share_hat(Y, m)     = mean of share(y, m) over the reference years before Y, excluding the
                        COVID years 2020-2021
  EL62_hat(Y, m)      = EL nights(Y, m) [tour_occ_nim]  x  share_hat(Y, m)

Backtest: the same rule is applied to each past year that has at least one earlier reference
year (2023 uses 2022; 2024 uses 2022-23; 2025 uses 2022-24) and compared with the published
EL62 values. Reported: absolute % error per month, error on the 3 busiest months, error on the
annual sum and on the top-3-month share.

Output: data/curated/provisional-data29-el62-monthly-<last month>.json
  * one observation per estimated month, series label "PROVISIONAL estimate ...";
  * the backtest table, so readers see how accurate the method has been;
  * replaced (not merged) when tour_occ_nin2m publishes the year.

Lineage:
  data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json   (shares, backtest truth)
  data/raw/eurostat-tour_occ_nim-EL-2020-01-2026-08.json    (Greek months to estimate from)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics as st
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
NIN2M = ROOT / "data/raw/eurostat-tour_occ_nin2m-EL62-EL-2020-2025.json"
NIM = ROOT / "data/raw/eurostat-tour_occ_nim-EL-2020-01-2026-08.json"
OUT_DIR = ROOT / "data/curated"
EXCLUDE = {2020, 2021}     # COVID years: not used as reference years
MONTHS = list(range(1, 13))


def getter(path: Path, expect_label: str, expect_dims: set[str]):
    d = json.loads(path.read_text(encoding="utf-8"))
    # Identity check: a candidate run must fail on the wrong dataset, not pass quietly.
    if not d.get("label", "").startswith(expect_label) or not expect_dims <= set(d.get("id", [])):
        raise SystemExit(f"FAIL: {path} is not the expected dataset ('{expect_label}', dims {sorted(expect_dims)}); "
                         f"got '{d.get('label')}' with dims {d.get('id')}")
    ids, size = d["id"], d["size"]
    cat = {k: d["dimension"][k]["category"]["index"] for k in ids}

    def get(**kw):
        idx = 0
        for k, s in zip(ids, size):
            if k in kw and kw[k] not in cat[k]:
                return None
            idx = idx * s + (cat[k][kw[k]] if k in kw else 0)
        return d["value"].get(str(idx))
    return get, cat


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--nin2m", type=Path, default=NIN2M, help="alternative tour_occ_nin2m raw file (scheduler candidate)")
    ap.add_argument("--nim", type=Path, default=NIM, help="alternative tour_occ_nim raw file (scheduler candidate)")
    args = ap.parse_args()
    if not args.check and (args.nin2m != NIN2M or args.nim != NIM):
        print("Alternative raw files are allowed only with --check (promotion is a reviewed step).", file=sys.stderr)
        return 2

    n2m, n2m_cat = getter(args.nin2m, "Nights spent at tourist accommodation establishments by month and NUTS 2 region",
                          {"month", "geo", "time"})
    nim, nim_cat = getter(args.nim, "Nights spent at tourist accommodation establishments - monthly data",
                          {"geo", "time"})
    if "month" in nim_cat or "EL" not in nim_cat["geo"]:
        raise SystemExit(f"FAIL: {args.nim} is not the Greek monthly series (tour_occ_nim)")
    official_years = sorted(int(y) for y in n2m_cat["time"])

    def el62(y, m): return n2m(geo="EL62", time=str(y), month=f"M{m:02d}")
    def el_n2m(y, m): return n2m(geo="EL", time=str(y), month=f"M{m:02d}")
    def el_nim(y, m): return nim(time=f"{y}-{m:02d}")

    share = {(y, m): el62(y, m) / el_n2m(y, m) for y in official_years for m in MONTHS}

    def share_hat(Y, m):
        refs = [y for y in official_years if y < Y and y not in EXCLUDE]
        return (st.mean(share[(y, m)] for y in refs), refs) if refs else (None, refs)

    def share_range(Y, m):
        refs = [y for y in official_years if y < Y and y not in EXCLUDE]
        vals = [share[(y, m)] for y in refs]
        return min(vals), max(vals)

    def top3(v): return sum(sorted(v)[-3:]) / sum(v) * 100

    # Backtest
    backtest = []
    for Y in official_years:
        sh = [share_hat(Y, m) for m in MONTHS]
        if Y in EXCLUDE or sh[0][0] is None:
            continue
        est = [el_n2m(Y, m) * sh[m - 1][0] for m in MONTHS]
        act = [el62(Y, m) for m in MONTHS]
        ape = [abs(e - a) / a * 100 for e, a in zip(est, act)]
        peak = sorted(range(12), key=lambda i: act[i])[-3:]
        row = {"year": Y, "reference_years": sh[0][1],
               "monthly_abs_pct_error": {f"M{m:02d}": round(x, 1) for m, x in zip(MONTHS, ape)},
               "top3_months_mean_abs_pct_error": round(st.mean(ape[i] for i in peak), 2),
               "annual_sum_pct_error": round((sum(est) - sum(act)) / sum(act) * 100, 2),
               "top3_share_actual": round(top3(act), 2), "top3_share_estimated": round(top3(est), 2)}
        backtest.append(row)
        print(f"backtest {Y} (refs {row['reference_years']}): annual sum error {row['annual_sum_pct_error']:+.2f} %, "
              f"busiest-3-month error {row['top3_months_mean_abs_pct_error']:.2f} %, top-3 share "
              f"{row['top3_share_estimated']} est vs {row['top3_share_actual']} actual")

    # Estimate months after the last official year
    Y = official_years[-1] + 1
    months = [m for m in MONTHS if el_nim(Y, m) is not None]
    if not months:
        print(f"No Greek monthly data yet for {Y}; nothing to estimate.")
        return 0
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    nim_sha = hashlib.sha256(NIM.read_bytes()).hexdigest()
    obs, rows = [], []
    for m in months:
        sh, refs = share_hat(Y, m)
        lo_s, hi_s = share_range(Y, m)
        est = round(el_nim(Y, m) * sh)
        lo, hi = round(el_nim(Y, m) * lo_s), round(el_nim(Y, m) * hi_s)
        latest = round(el_nim(Y, m) * share[(max(refs), m)])
        rows.append({"month": f"{Y}-{m:02d}", "el_nights": el_nim(Y, m), "el62_share": round(sh, 5), "el62_estimate": est,
                     "band_low": lo, "band_high": hi, "estimate_with_latest_year_share": latest})
        print(f"{Y}-{m:02d}: Greece {el_nim(Y, m):>11,} x share {sh:.4f} = EL62 estimate {est:>10,}  "
              f"(band {lo:,} - {hi:,}; latest-year share {latest:,})")
        obs.append({
            "observation_id": f"Provisional:Data29:monthly_nights_estimate:EL62:{Y}-{m:02d}",
            "indicator_id": "Data29", "indicator_name": "Seasonality (%)",
            "series_label": "PROVISIONAL estimate of monthly nights (all accommodation), replaced by tour_occ_nin2m on release",
            "source_id": "Derived_tour_occ_nim_x_EL62_share", "observed_at": f"{Y}-{m:02d}", "observed_period_end": None,
            "temporal_granularity": "monthly", "ingested_at": now,
            "spatial_ref": {"level": "NUTS2", "code": "EL62", "geometry": None},
            "value": est, "unit": "nights", "polarity": None,
            "provenance": {"raw_checksum_sha256": nim_sha, "raw_manifest": "source-verification-2026-11-03",
                           "access_method": "derived", "request_url": None,
                           "request_params": {"formula": f"EL nights {Y}-{m:02d} x mean EL62/EL share of month {m} over {refs}",
                                              "band": f"{lo}-{hi} (min-max of the reference-year shares)",
                                              "status": "PROPOSAL", "backtest": "see audit file"}},
        })
    last = f"{Y}-{months[-1]:02d}"
    audit = {"status": "PROPOSAL", "method": __doc__.split("Method")[1].split("Backtest")[0].strip(),
             "excluded_reference_years": sorted(EXCLUDE), "backtest": backtest, "estimates": rows,
             "uncertainty": ("Band per month = Greek nights x min/max of that month's EL62 share over the reference years. "
                             "It describes year-to-year share variation, not a statistical confidence interval."),
             "caveats": [
                 "The backtest errors were negative in 2023 (-8.56 %) and 2024 (-4.29 %): EL62's share of Greek nights rose after COVID, "
                 "and an equal-weight mean of past shares lags such a trend. Estimates for growing months are likely to lean low; "
                 "'estimate_with_latest_year_share' shows the trend-following alternative.",
                 "Only 1-3 reference years exist for the backtest (2023 used a single year), so the errors are indicative, not a calibration.",
             ],
             "note": "Partial-year estimates: no annual seasonality measure is computed from them until the year is complete."}
    print(f"{len(obs)} provisional observations ({Y}-{months[0]:02d} .. {last})")
    if args.check:
        return 0
    out = OUT_DIR / f"provisional-data29-el62-monthly-{last}.json"
    out.write_text(json.dumps({"audit": audit, "observations": obs}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
