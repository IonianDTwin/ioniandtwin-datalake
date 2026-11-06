#!/usr/bin/env python3
"""Reproduce Fraport Greece per-airport monthly traffic (Dec 2025 vs 2024 PDFs).

Read-only parse of the four retained PDFs in data/samples/fraport-2025/ (Channel A of
agy research-notes 2026-11-04 section 2). Emits monthly passengers and flights per
airport plus seasonality metrics, and compares them with the agy-reported values.

Usage: python3 -P scripts/verification/reproduce-fraport-airport-traffic.py [--json OUT]
Status of outputs: PROPOSAL (source adoption pending reuse terms and revision policy).
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import pypdf

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "data/samples/fraport-2025"
AIRPORTS = {
    "CFU": ("Kerkira", "EL622", "cfu", 2871),
    "EFL": ("Kefallinia", "EL623", "efl", 2875),
    "ZTH": ("Zakinthos", "EL621", "zth", 2877),
    "PVK": ("Aktion", "EL624 proxy (also serves Preveza)", "pvk", 2879),
}
MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY",
          "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
# Values reported by agy research-notes 2026-11-04 section 2 (for comparison only).
AGY = {
    ("CFU", 2024): (4343748, 91.9, "Aug", 21.35, 927328, 58.54, 0.5299),
    ("CFU", 2025): (4618810, 91.8, "Aug", 21.14, 976349, 58.05, 0.5253),
    ("EFL", 2024): (872536, 88.7, "Aug", 24.36, 212566, 65.80, 0.5901),
    ("EFL", 2025): (893697, 88.5, "Aug", 23.66, 211458, 64.82, 0.5837),
    ("ZTH", 2024): (2223010, 93.9, "Aug", 22.99, 511012, 63.67, 0.5823),
    ("ZTH", 2025): (2282774, 93.3, "Aug", 23.09, 527156, 63.70, 0.5843),
    ("PVK", 2024): (824894, 97.2, "Jul", 23.24, 191685, 64.48, 0.5920),
    ("PVK", 2025): (875962, 96.8, "Aug", 23.26, 203755, 64.49, 0.5934),
    ("ALL", 2024): (8264188, 92.6, "Aug", 22.27, 1840564, 61.26, 0.5582),
    ("ALL", 2025): (8671243, 92.3, "Aug", 22.13, 1918718, 60.87, 0.5546),
}


def num(tok):
    # Fraport uses '.' as thousands separator and ',' as decimal separator.
    return int(tok.replace(".", ""))


def parse_page(text):
    rows = {}
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        key = parts[0] if parts[0] in MONTHS else ("TOTAL" if parts[0] == "TOTAL" else None)
        if key is None:
            continue
        vals = [p for p in parts[1:] if re.fullmatch(r"-?[\d.]+(,\d+)?%?", p)]
        ints = [num(v) for v in vals if not v.endswith("%")]
        if len(ints) != 6:
            raise ValueError(f"unexpected row layout: {line!r}")
        dom25, dom24, int25, int24, tot25, tot24 = ints
        rows[key] = {2025: {"dom": dom25, "int": int25, "tot": tot25},
                     2024: {"dom": dom24, "int": int24, "tot": tot24}}
    missing = [m for m in MONTHS + ["TOTAL"] if m not in rows]
    if missing:
        raise ValueError(f"missing rows {missing}")
    return rows


def gini(xs):
    xs = sorted(xs)
    n = len(xs)
    return sum((2 * i - n - 1) * x for i, x in enumerate(xs, 1)) / (n * sum(xs))


def metrics(monthly_tot, monthly_int):
    total = sum(monthly_tot)
    peak_i = max(range(12), key=lambda i: monthly_tot[i])
    top3 = sorted(range(12), key=lambda i: monthly_tot[i], reverse=True)[:3]
    return {
        "annual_passengers": total,
        "international_share_pct": round(100 * sum(monthly_int) / total, 2),
        "peak_month": MONTHS[peak_i][:3].title(),
        "peak_month_passengers": monthly_tot[peak_i],
        "peak_month_share_pct": round(100 * monthly_tot[peak_i] / total, 2),
        "top3_months": [MONTHS[i][:3].title() for i in sorted(top3)],
        "top3_share_pct": round(100 * sum(monthly_tot[i] for i in top3) / total, 2),
        "monthly_gini": round(gini(monthly_tot), 4),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    out = {"airports": {}, "comparison_with_agy": []}
    combined = {y: {"tot": [0] * 12, "int": [0] * 12} for y in (2024, 2025)}
    for code, (stem, nuts, host, node) in AIRPORTS.items():
        pdf = SAMPLES / f"{stem}_12_Traffic_2025vs2024.pdf"
        reader = pypdf.PdfReader(pdf)
        pax = parse_page(reader.pages[0].extract_text())
        flt = parse_page(reader.pages[1].extract_text())
        rec = {"nuts3": nuts, "file": str(pdf.relative_to(ROOT)),
               "url": f"https://www.{host}-airport.gr/uploads/sys_nodelng/2/{node}/{pdf.name}",
               "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "years": {}}
        for y in (2024, 2025):
            tot = [pax[m][y]["tot"] for m in MONTHS]
            intl = [pax[m][y]["int"] for m in MONTHS]
            fl = [flt[m][y]["tot"] for m in MONTHS]
            for k, src in (("tot", tot), ("int", intl)):
                combined[y][k] = [a + b for a, b in zip(combined[y][k], src)]
            if sum(tot) != pax["TOTAL"][y]["tot"] or sum(fl) != flt["TOTAL"][y]["tot"]:
                raise ValueError(f"{code} {y}: monthly sum != printed TOTAL")
            rec["years"][str(y)] = {"monthly_passengers": dict(zip(MONTHS, tot)),
                                    "monthly_flights": dict(zip(MONTHS, fl)),
                                    "annual_flights": sum(fl), **metrics(tot, intl)}
        out["airports"][code] = rec
    out["combined_4_airports"] = {str(y): metrics(c["tot"], c["int"]) for y, c in combined.items()}

    for (code, y), exp in AGY.items():
        got = (out["combined_4_airports"][str(y)] if code == "ALL"
               else out["airports"][code]["years"][str(y)])
        fields = ["annual_passengers", "international_share_pct", "peak_month",
                  "peak_month_share_pct", "peak_month_passengers", "top3_share_pct", "monthly_gini"]
        for f, e in zip(fields, exp):
            g = got[f]
            ok = (g == e) if isinstance(e, (int, str)) else abs(g - e) <= (0.051 if f.endswith("pct") else 0.00051)
            if not ok:
                out["comparison_with_agy"].append({"airport": code, "year": y, "field": f,
                                                   "agy": e, "reproduced": g})
    text = json.dumps(out, indent=2, ensure_ascii=False)
    if args.json:
        args.json.write_text(text + "\n")
    print(json.dumps({"combined": out["combined_4_airports"],
                      "mismatches_vs_agy": out["comparison_with_agy"]}, indent=2))


if __name__ == "__main__":
    main()
