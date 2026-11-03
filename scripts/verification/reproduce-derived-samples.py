#!/usr/bin/env python3
"""Reproduce the three ad hoc derived sample files under data/samples/.

Written 2026-11-03 to make an ad hoc step (the three files were produced by hand
on 2026-10-01/03, with no producing script retained) reproducible.

LINEAGE (inputs -> outputs)
  1. data/samples/elstat-sto12-{2021..2025}-capacity.xlsx   (ELSTAT table STO12)
       -> data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json
     Method: sheet 'ENG'; find the rows whose column B is 'REGIONAL UNIT OF
     <KERKYRA|ZAKYNTHOS|ITHAKI|KEFALLINIA|LEFKADA>'; the value is the column that
     follows the header 'Number of Bed places' / 'Hotels and similar
     establishments' (column F, index 5, in all five workbooks). Hotels and
     similar establishments only (campsites carry pitches, not bed-places).
  2. data/samples/eurostat-tour_occ_nin3-EL621-624-2021-2025.json (JSON-stat per NUTS3)
       -> data/samples/derived-data22-data25-2021-2025.json
     Method (data22): nights per island (EL621 Zakynthos, EL622 Kerkyra, EL623
     Ithaki+Kefallinia combined, EL624 Lefkada); share_i = nights_i / sum nights
     (4 dp); HHI = sum share_i^2 on unrounded shares (4 dp); diversity = 1 - HHI
     computed from the unrounded HHI (4 dp). data25_bed_distribution is an empty
     object in the existing file (nothing was ever derived); it is reproduced as {}.
  3. nin3 JSON + output of step 1
       -> data/samples/derived-data28-nights-per-hotel-bed-index-2021-2025.json
     Method: occupancy % = 100 * nights / (hotel bed-places * 365), 1 dp; Ithaki and
     Kefallinia bed-places summed to match EL623. Same 365 divisor in leap year 2024.
     CAVEAT: the numerator is nights in ALL establishment types (NACE I551-I553:
     hotels, short-stay/holiday lets, camping), the denominator is HOTEL-AND-SIMILAR
     bed-places only (ELSTAT STO12). It is therefore an upper-bound proxy, not a
     true occupancy rate; where non-hotel supply is large (Lefkada, holiday rentals)
     the value is overstated (Lefkada 2025 = 82.4 %). Treat as an index, not occupancy.

Usage:
  reproduce-derived-samples.py            # same as --check: compare, print OK/DIFF, write nothing
  reproduce-derived-samples.py --check
  reproduce-derived-samples.py --write    # overwrite the three sample files (not run by default)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "data" / "samples"
YEARS = [str(y) for y in range(2021, 2026)]
UNITS = ["KERKYRA", "ZAKYNTHOS", "ITHAKI", "KEFALLINIA", "LEFKADA"]
OUT1 = S / "elstat-sto12-ionian-bedplaces-2021-2025.json"
OUT2 = S / "derived-data22-data25-2021-2025.json"
OUT3 = S / "derived-data28-nights-per-hotel-bed-index-2021-2025.json"
NIN3 = S / "eurostat-tour_occ_nin3-EL621-624-2021-2025.json"
# Output key order as in the existing files.
ISLANDS = [("Zakynthos", "EL621"), ("Kerkyra", "EL622"),
           ("Ithaki_Kefallinia", "EL623"), ("Lefkada", "EL624")]


def build_bedplaces() -> dict:
    import openpyxl  # present in .venv (checked 2026-11-03)
    out = {}
    for y in YEARS:
        wb = openpyxl.load_workbook(S / f"elstat-sto12-{y}-capacity.xlsx", data_only=True)
        ws = wb["ENG"]
        rows = list(ws.iter_rows(values_only=True))
        # locate bed-place column from header row
        col = None
        for r in rows[:10]:
            if r and any(isinstance(c, str) and c.strip() == "Number of Bed places" for c in r):
                col = [i for i, c in enumerate(r) if isinstance(c, str) and c.strip() == "Number of Bed places"][0]
        if col is None:
            raise SystemExit(f"{y}: 'Number of Bed places' header not found")
        found = {}
        for r in rows:
            lab = r[1] if len(r) > 1 else None
            if isinstance(lab, str) and lab.startswith("REGIONAL UNIT OF "):
                name = lab[len("REGIONAL UNIT OF "):].strip()
                if name in UNITS:
                    found[name] = r[col]
        missing = [u for u in UNITS if u not in found]
        if missing:
            raise SystemExit(f"{y}: regional units not found: {missing}")
        out[y] = {u: found[u] for u in UNITS}
    return out


def load_nin3() -> dict:
    w = json.loads(NIN3.read_text(encoding="utf-8"))
    nin = {}
    for geo, d in w.items():
        tix = d["dimension"]["time"]["category"]["index"]
        nin[geo] = {t: d["value"].get(str(i)) for t, i in tix.items()}
    return nin


def build_data22(nin: dict) -> dict:
    d22 = {}
    for y in YEARS:
        nights = {k: nin[g][y] for k, g in ISLANDS}
        tot = sum(nights.values())
        sh = {k: v / tot for k, v in nights.items()}
        hhi = sum(s * s for s in sh.values())
        d22[y] = {"nights": nights,
                  "shares": {k: round(v, 4) for k, v in sh.items()},
                  "HHI": round(hhi, 4),
                  "diversity_1_minus_HHI": round(1 - hhi, 4)}
    return {"data22_tourist_diversity": d22, "data25_bed_distribution": {}}


def build_data28(nin: dict, beds: dict) -> dict:
    out = {}
    for y in YEARS:
        b = beds[y]
        bp = {"Zakynthos": b["ZAKYNTHOS"], "Kerkyra": b["KERKYRA"],
              "Ithaki_Kefallinia": b["ITHAKI"] + b["KEFALLINIA"], "Lefkada": b["LEFKADA"]}
        out[y] = {k: round(100 * nin[g][y] / (bp[k] * 365), 1) for k, g in ISLANDS}
    return out


def diff(path: Path, new: dict) -> int:
    old = json.loads(path.read_text(encoding="utf-8"))
    bad = 0
    def walk(o, n, p):
        nonlocal bad
        if isinstance(n, dict) and isinstance(o, dict):
            for k in sorted(set(o) | set(n)):
                if k not in o or k not in n:
                    print(f"DIFF {path.name} {p}/{k}: missing in {'existing' if k not in o else 'rebuilt'}")
                    bad += 1
                else:
                    walk(o[k], n[k], f"{p}/{k}")
        else:
            ok = o == n
            print(f"{'OK  ' if ok else 'DIFF'} {path.name} {p}: existing={o} rebuilt={n}")
            bad += (not ok)
    walk(old, new, "")
    if not old and not new:  # both empty dict leaf case
        pass
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare only (default)")
    ap.add_argument("--write", action="store_true", help="overwrite the three sample files")
    a = ap.parse_args()
    beds = build_bedplaces()
    nin = load_nin3()
    outs = [(OUT1, beds), (OUT2, build_data22(nin)), (OUT3, build_data28(nin, beds))]
    if a.write:
        for p, d in outs:
            p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
            print("WROTE", p)
        return 0
    bad = sum(diff(p, d) for p, d in outs)
    print(f"SUMMARY: {'ALL OK' if bad == 0 else str(bad) + ' DIFF'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
