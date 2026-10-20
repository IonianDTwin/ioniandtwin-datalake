#!/usr/bin/env python3
"""Compute Data07 — Anticipated Port Congestion — for the Ionian Islands (EL62).

This is the durable implementation of the research specification in
``daily/2026-10-15/research-notes.md``. It replaces the live-AIS prototype and the
``scratch/cruise-pressure/build-cruise-pressure.py`` one-off with a schedule-based
**anticipated** congestion model: instead of counting vessels currently inside a
port buffer (a live snapshot with zero forecasting ability), it aggregates
**planned cruise calls** and the **empirical ferry throughput baseline** into a
forward-looking daily congestion score per monitored port.

Inputs
------
* ``scratch/cruise-pressure/schedules.json`` — one-time CruiseMapper schedule read
  (Oct–Nov 2026 cruise calls). ``ASSUMPTION``: a source sample, not a production
  feed; a port-authority (OLKE) declaration feed should replace it in production.
* ``scratch/ais-routes/export_sailing_traffic.csv`` — Greek National Access Point
  sailing-traffic export (Mar–Nov 2025, 184,436 leg rows). This is the empirical
  ferry baseline: for each monitored port we sum every leg whose ``arrivalport``
  is an EL62 island port and normalise by operating days, optionally by calendar
  month and day-of-week (the ``PAX̄_route(f, month, day_of_week)`` term in the spec).

Model (research-notes §4A)
--------------------------
For port ``P`` and forecast date ``D``::

    N_ships(P,D)   = number of cruise calls on D
    L_cruise(P,D)  = N_ships * cruise_pax_default          (ASSUMPTION: per-call PAX)
    L_ferry_pax(P,D) = ferry baseline passengers arriving at P on (month, dow)
    L_ferry_veh(P,D) = ferry baseline vehicles arriving at P on (month, dow)

    S(P,D) = min(1.0,
                 w_berth * N_ships/B_max
               + w_pax   * (L_cruise + L_ferry_pax)/C_pax
               + w_veh   * L_ferry_veh/C_veh)

Levels: low (S < 0.50), medium (0.50 ≤ S < 0.85), high (S ≥ 0.85).

All capacities (``B_max``, ``C_pax``, ``C_veh``), the weights, and the per-call
cruise PAX are ``PROPOSAL``/``ASSUMPTION`` defaults (the proposal names the
indicator but no formula); they are recorded in the emitted dataset and must not
drive public alerts or policy until the author confirms them.

Outputs (under ``data/curated/``)
---------------------------------
* ``scheduled-port-traffic-el62.json`` — master scheduled-timetable dataset:
  cruise calls + ferry baselines + port model + daily scores (audit artefact).
* ``observations-data07-anticipated-congestion-<date>.json`` / ``.csv`` —
  schema-compliant observations (one per port per forecast day).

Usage
-----
    python3 scripts/verification/compute-data07-anticipated-congestion.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CURATED = ROOT / "data" / "curated"

# ---------------------------------------------------------------------------
# Port model (EL62). Capacities are ASSUMPTION (no proposal numbers exist);
# berth capacities follow research-notes §4A. csv_codes map Greek NAP port
# codes to the monitored island port; Igoumenitsa/Kyllini/Patras are mainland
# gateways and are intentionally absent (not EL62).
# ---------------------------------------------------------------------------
PORTS: dict[str, dict] = {
    "corfu": {
        "name": "Corfu (Kerkyra)", "berth_capacity": 5,
        "pax_capacity": 12_000, "veh_capacity": 1_800,
        "csv_codes": ("CFU", "LFK"),
    },
    "kefalonia": {
        "name": "Kefalonia (Argostoli)", "berth_capacity": 3,
        "pax_capacity": 7_000, "veh_capacity": 900,
        "csv_codes": ("PKE", "SAI", "FIS"),
    },
    "zakynthos": {
        "name": "Zakynthos", "berth_capacity": 3,
        "pax_capacity": 7_000, "veh_capacity": 900,
        "csv_codes": ("ZTH",),
    },
    "lefkada": {
        "name": "Lefkada", "berth_capacity": 2,
        "pax_capacity": 3_000, "veh_capacity": 400,
        "csv_codes": ("VSS", "LEV"),
    },
    "paxos": {
        "name": "Paxos", "berth_capacity": 1,
        "pax_capacity": 1_500, "veh_capacity": 200,
        "csv_codes": ("PAX",),
    },
    "ithaki": {
        "name": "Ithaki", "berth_capacity": 1,
        "pax_capacity": 1_500, "veh_capacity": 200,
        "csv_codes": ("PIS",),
    },
}

WEIGHTS = {"berth": 0.4, "pax": 0.4, "veh": 0.2}          # PROPOSAL (research-notes default)
CRUISE_PAX_DEFAULT = 2_500                                 # ASSUMPTION (mid-range 2,000–5,500)
LEVEL_BANDS = ((0.0, 0.50, "low"), (0.50, 0.85, "medium"), (0.85, 1.01, "high"))

# Research-notes §3 corridor cross-check (routecode → (description, EL62 port)).
# Used only for the audit section of the curated dataset; the model itself uses
# the complete per-port arrival aggregation, not this subset.
CORRIDORS = [
    ("IGOCFU", "Igoumenitsa → Corfu town", "corfu"),
    ("IGOLFK", "Igoumenitsa → Lefkimmi (south Corfu)", "corfu"),
    ("KYLZTH", "Kyllini → Zakynthos", "zakynthos"),
    ("KYLPKE", "Kyllini → Poros (Kefalonia)", "kefalonia"),
    ("GPASAIPIS", "Patras → Sami (Kefalonia) → Pisaetos (Ithaki)", "kefalonia+ithaki"),
    ("VSSFIS", "Vasiliki (Lefkada) → Fiskardo (Kefalonia)", "kefalonia"),
    ("FISVSS", "Fiskardo (Kefalonia) → Vasiliki (Lefkada)", "lefkada"),
    ("CFUPAX", "Corfu → Paxos (foot passengers)", "paxos"),
    ("IGOPAX", "Igoumenitsa → Paxos", "paxos"),
    ("LFKPAX", "Lefkimmi → Paxos (foot passengers)", "paxos"),
]

SCHEMA_PATH = ROOT / "schemas" / "observation-schema.json"

# Excluded EL62 micro-ports (present in the CSV but outside the 6-port model):
# OTH (Othonoi), ERK (Ereikousa), MTR (Mathraki) — Diapontia islets; MGN (Meganisi).
EXCLUDED_CODES = {"OTH", "ERK", "MTR", "MGN"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def level_of(score: float) -> str:
    for lo, hi, label in LEVEL_BANDS:
        if lo <= score < hi:
            return label
    return "high"


def load_cruise_schedules(path: Path) -> dict:
    sched = json.loads(path.read_text(encoding="utf-8"))
    by_port: dict[str, list[dict]] = defaultdict(list)
    for p in sched.get("ports", []):
        by_port[p["id"]] = p.get("calls", [])
    return {"captured_at_utc": sched.get("captured_at_utc"),
            "source": sched.get("source"), "ports": dict(by_port)}


def load_ferry_baselines(path: Path) -> dict:
    """Aggregate inbound ferry traffic per monitored port.

    For every CSV leg, the ``arrivalport`` is the island port the passengers/
    vehicles disembark into; we aggregate by (port, month, day-of-week) with
    distinct-date denominators, plus (port, month) and (port) rollups as fallback.

    Returns:
        {"by_port": {port: {"pax_per_day", "veh_per_day", "operating_days",
                            "total_pax", "total_veh"}},
         "by_month_dow": {port: {(month, dow): {pax, veh, dates}}},
         "by_month": {port: {month: {pax, veh, dates}}}}
    """
    code_to_port = {}
    for pid, cfg in PORTS.items():
        for c in cfg["csv_codes"]:
            code_to_port[c] = pid

    month_dow: dict[str, dict] = defaultdict(lambda: defaultdict(
        lambda: {"pax": 0, "veh": 0, "dates": set()}))
    month: dict[str, dict] = defaultdict(lambda: defaultdict(
        lambda: {"pax": 0, "veh": 0, "dates": set()}))
    total: dict[str, dict] = defaultdict(lambda: {"pax": 0, "veh": 0, "dates": set()})

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["arrivalport"]
            pid = code_to_port.get(code)
            if pid is None:
                continue  # mainland gateway or excluded micro-port
            d = row["date"]  # ISO, e.g. 2025-03-17
            if not d:
                continue
            try:
                pax = int(row["passengercount"] or 0)
                veh = int(row["vehiclecount"] or 0)
            except ValueError:
                continue
            month_no = int(d[5:7])
            dow = date.fromisoformat(d).weekday()  # Mon=0..Sun=6
            md = month_dow[pid][(month_no, dow)]
            mo = month[pid][month_no]
            tt = total[pid]
            for bucket in (md, mo, tt):
                bucket["pax"] += pax
                bucket["veh"] += veh
                bucket["dates"].add(d)

    by_month_dow = {
        pid: {k: {"pax": v["pax"], "veh": v["veh"], "days": len(v["dates"])}
              for k, v in cells.items()}
        for pid, cells in month_dow.items()
    }
    by_month = {
        pid: {k: {"pax": v["pax"], "veh": v["veh"], "days": len(v["dates"])}
              for k, v in cells.items()}
        for pid, cells in month.items()
    }
    by_port = {}
    for pid, v in total.items():
        days = len(v["dates"])
        by_port[pid] = {
            "total_pax": v["pax"], "total_veh": v["veh"], "operating_days": days,
            "pax_per_day": round(v["pax"] / days, 1) if days else 0.0,
            "veh_per_day": round(v["veh"] / days, 1) if days else 0.0,
        }
    return {"by_port": by_port, "by_month_dow": by_month_dow, "by_month": by_month}


def ferry_load_for(pid: str, d: date, baselines: dict) -> tuple[float, float]:
    """Return (pax, veh) daily ferry load for port ``pid`` on date ``d``.

    Prefers (month, day-of-week) average, then month average, then overall.
    """
    md = baselines["by_month_dow"].get(pid, {}).get((d.month, d.weekday()))
    if md and md["days"]:
        return round(md["pax"] / md["days"], 1), round(md["veh"] / md["days"], 1)
    mo = baselines["by_month"].get(pid, {}).get(d.month)
    if mo and mo["days"]:
        return round(mo["pax"] / mo["days"], 1), round(mo["veh"] / mo["days"], 1)
    bp = baselines["by_port"].get(pid, {})
    return bp.get("pax_per_day", 0.0), bp.get("veh_per_day", 0.0)


def score_port(pid: str, n_ships: int, ferry_pax: float, ferry_veh: float) -> dict:
    cfg = PORTS[pid]
    cruise_pax = n_ships * CRUISE_PAX_DEFAULT
    total_pax = cruise_pax + ferry_pax
    s = min(
        1.0,
        WEIGHTS["berth"] * n_ships / cfg["berth_capacity"]
        + WEIGHTS["pax"] * total_pax / cfg["pax_capacity"]
        + WEIGHTS["veh"] * ferry_veh / cfg["veh_capacity"],
    )
    return {
        "ships": n_ships,
        "cruise_pax": cruise_pax,
        "ferry_pax": round(ferry_pax, 1),
        "ferry_veh": round(ferry_veh, 1),
        "total_pax": round(total_pax, 1),
        "score": round(s, 3),
        "level": level_of(round(s, 3)),
    }


def corridor_audit(path: Path) -> list[dict]:
    """Cross-check table for the research-notes §3 corridor baselines."""
    cells: dict[str, dict] = {rc: {"pax": 0, "veh": 0, "dates": set(), "desc": dsc, "port": port}
                             for rc, dsc, port in CORRIDORS}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rc = row["routecode"]
            if rc not in cells:
                continue
            c = cells[rc]
            try:
                c["pax"] += int(row["passengercount"] or 0)
                c["veh"] += int(row["vehiclecount"] or 0)
            except ValueError:
                continue
            c["dates"].add(row["date"])
    out = []
    for rc, dsc, port in CORRIDORS:
        c = cells[rc]
        days = len(c["dates"])
        out.append({
            "routecode": rc, "corridor": dsc, "port": port,
            "total_pax": c["pax"], "total_veh": c["veh"], "operating_days": days,
            "pax_per_day": round(c["pax"] / days, 1) if days else 0.0,
            "veh_per_day": round(c["veh"] / days, 1) if days else 0.0,
        })
    return out


def _obs(oid, source_id, series_label, observed_at, spatial_code, value, method_url, sched_sha):
    return {
        "observation_id": oid,
        "indicator_id": "Data07",
        "indicator_name": "Port congestion",
        "series_label": series_label,
        "source_id": source_id,
        "observed_at": observed_at,
        "observed_period_end": None,
        "temporal_granularity": "forecast",
        "ingested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spatial_ref": {"level": "transport_node", "code": spatial_code, "geometry": None},
        "value": value,
        "unit": "index (0-1)",
        "polarity": "negative",
        "provenance": {
            "raw_checksum_sha256": sched_sha,
            "raw_manifest": "source-verification-2026-10-14",
            "access_method": "derived",
            "request_url": method_url,
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
    ap.add_argument("--schedules", type=Path,
                    default=ROOT / "scratch" / "cruise-pressure" / "schedules.json")
    ap.add_argument("--ferry", type=Path,
                    default=ROOT / "scratch" / "ais-routes" / "export_sailing_traffic.csv")
    ap.add_argument("--start", type=date.fromisoformat, default=None,
                    help="forecast start (default: min cruise date)")
    ap.add_argument("--end", type=date.fromisoformat, default=None,
                    help="forecast end (default: max cruise date)")
    ap.add_argument("--out-dir", type=Path, default=CURATED)
    ap.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    ap.add_argument("--run-date", default=None, help="override output-file date stamp")
    args = ap.parse_args()

    for p in (args.schedules, args.ferry):
        if not p.exists():
            print(f"error: input not found: {p}", file=sys.stderr)
            return 2

    cruise = load_cruise_schedules(args.schedules)
    ferries = load_ferry_baselines(args.ferry)
    sched_sha = sha256(args.schedules)
    ferry_sha = sha256(args.ferry)

    def method_url(pid: str) -> str:
        cfg = PORTS[pid]
        return (f"S(P,D)=min(1,{WEIGHTS['berth']}*N_ships/{cfg['berth_capacity']}"
                f"+{WEIGHTS['pax']}*(L_cruise+L_ferry_pax)/{cfg['pax_capacity']}"
                f"+{WEIGHTS['veh']}*L_ferry_veh/{cfg['veh_capacity']}); "
                f"cruise_pax={CRUISE_PAX_DEFAULT}/call; inputs CruiseMapper schedules "
                f"(sha256 {sched_sha[:16]}…) + Greek NAP sailing traffic (sha256 {ferry_sha[:16]}…)")

    # Cruise call index: cruise-port-id -> {date: [calls]}
    cruise_by_date: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for pid, calls in cruise["ports"].items():
        for c in calls:
            if c.get("date"):
                cruise_by_date[pid][c["date"]].append(c)

    all_dates = sorted({c["date"] for calls in cruise["ports"].values()
                        for c in calls if c.get("date")})
    start = args.start or date.fromisoformat(all_dates[0])
    end = args.end or date.fromisoformat(all_dates[-1])

    # Cruise port ids in the schedule file map 1:1 onto our EL62 port ids except
    # for the mainland gateway "igoumenitsa", which is excluded from EL62.
    excluded_cruise = {
        pid: len(calls) for pid, calls in cruise["ports"].items() if pid not in PORTS
    }

    daily_scores: list[dict] = []
    observations: list[dict] = []
    run_date = args.run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    d = start
    while d <= end:
        iso = d.isoformat()
        for pid, cfg in PORTS.items():
            calls_today = cruise_by_date.get(pid, {}).get(iso, [])
            n_ships = len(calls_today)
            f_pax, f_veh = ferry_load_for(pid, d, ferries)
            res = score_port(pid, n_ships, f_pax, f_veh)
            res["port"] = pid
            res["port_name"] = cfg["name"]
            res["date"] = iso
            daily_scores.append(res)
            observations.append(_obs(
                f"CruiseMapper_schedules:Data07:{pid}:{iso}",
                "CruiseMapper_schedules",
                f"anticipated congestion score ({cfg['name']})",
                iso, pid, res["score"], method_url(pid), sched_sha,
            ))
        d = date.fromordinal(d.toordinal() + 1)

    # Curated master-timetable dataset
    dataset = {
        "title": "Scheduled port traffic (EL62) — master timetable for Data07 anticipated congestion",
        "indicator_id": "Data07",
        "status": "PROPOSAL",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": ("S(P,D) = min(1, w_berth*N_ships/B_max + w_pax*(L_cruise+L_ferry_pax)/C_pax "
                   "+ w_veh*L_ferry_veh/C_veh); level low<0.50, medium<0.85, high>=0.85 "
                   "(research-notes 2026-10-15 §4)."),
        "sources": [
            {"source_id": "CruiseMapper_schedules", "path": str(args.schedules),
             "sha256": sched_sha, "captured_at_utc": cruise["captured_at_utc"],
             "note": cruise["source"] + ". One-time bounded read; NOT a production feed "
                     "(substitute the OLKE port-authority declaration feed)."},
            {"source_id": "GreekNAP_sailing_traffic", "path": str(args.ferry),
             "sha256": ferry_sha,
             "note": "Greek National Access Point sailing-traffic export, Mar–Nov 2025 "
                     "(empirical ferry baseline)."},
        ],
        "assumptions": {
            "weights": WEIGHTS,
            "cruise_pax_default_per_call": CRUISE_PAX_DEFAULT,
            "capacities": {pid: {"berth": cfg["berth_capacity"],
                                 "pax_per_day": cfg["pax_capacity"],
                                 "veh_per_day": cfg["veh_capacity"]}
                           for pid, cfg in PORTS.items()},
            "note": ("B_max from research-notes §4A; C_pax/C_veh and cruise PAX are ASSUMPTION "
                     "(no proposal numbers). Ferry load = inbound arrivals at the island port, "
                     "averaged by (month, day-of-week) with month→overall fallback."),
        },
        "forecast_window": {"start": start.isoformat(), "end": end.isoformat(),
                            "days": (end - start).days + 1},
        "ports": [],
        "excluded_ports": [{"id": pid, "calls": n} for pid, n in excluded_cruise.items()],
        "ferry_baselines": {pid: ferries["by_port"].get(pid, {}) for pid in PORTS},
        "ferry_corridor_crosscheck": corridor_audit(args.ferry),
        "daily_scores": daily_scores,
    }
    for pid, cfg in PORTS.items():
        calls = cruise["ports"].get(pid, [])
        dataset["ports"].append({
            "id": pid, "name": cfg["name"], "berth_capacity": cfg["berth_capacity"],
            "pax_capacity": cfg["pax_capacity"], "veh_capacity": cfg["veh_capacity"],
            "total_cruise_calls": len(calls),
            "cruise_calls": calls,
        })

    args.out_dir.mkdir(parents=True, exist_ok=True)
    master_path = args.out_dir / "scheduled-port-traffic-el62.json"
    obs_json = args.out_dir / f"observations-data07-anticipated-congestion-{run_date}.json"
    obs_csv = args.out_dir / f"observations-data07-anticipated-congestion-{run_date}.csv"

    master_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n",
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
                "observation_id": o["observation_id"], "indicator_id": o["indicator_id"],
                "indicator_name": o["indicator_name"], "series_label": o["series_label"],
                "source_id": o["source_id"], "temporal_granularity": o["temporal_granularity"],
                "observed_at": o["observed_at"], "observed_period_end": o["observed_period_end"],
                "value": o["value"], "unit": o["unit"],
                "spatial_level": o["spatial_ref"]["level"],
                "spatial_code": o["spatial_ref"]["code"], "polarity": o["polarity"],
            })

    problems = validate_against_schema(observations, args.schema)

    # Summary
    print("=== Data07 anticipated port congestion (EL62) ===")
    print(f"forecast window: {start} → {end} ({(end - start).days + 1} days)")
    print("ferry baseline (inbound arrivals, Mar–Nov 2025):")
    for pid in PORTS:
        bp = ferries["by_port"].get(pid, {})
        print(f"  {pid:10s} {bp.get('pax_per_day', 0):7.1f} pax/day  "
              f"{bp.get('veh_per_day', 0):7.1f} veh/day  "
              f"({bp.get('operating_days', 0)} op days)")
    if excluded_cruise:
        print("excluded (mainland, not EL62): " +
              ", ".join(f"{k}={v} calls" for k, v in excluded_cruise.items()))
    by_level = defaultdict(int)
    peak = {}
    for r in daily_scores:
        by_level[r["level"]] += 1
        cur = peak.setdefault(r["port"], r)
        if r["score"] > cur["score"]:
            peak[r["port"]] = r
    print(f"daily observations: {len(daily_scores)}  "
          f"(low={by_level['low']}, medium={by_level['medium']}, high={by_level['high']})")
    print("peak day per port:")
    for pid in PORTS:
        r = peak.get(pid)
        if r:
            print(f"  {pid:10s} {r['date']}  ships={r['ships']}  score={r['score']} ({r['level']})")
    print(f"wrote {master_path.relative_to(ROOT)}")
    print(f"wrote {obs_json.relative_to(ROOT)}")
    print(f"wrote {obs_csv.relative_to(ROOT)}")
    if problems:
        print(f"SCHEMA PROBLEMS ({len(problems)}):", file=sys.stderr)
        for p in problems[:20]:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"observations schema-valid: {len(observations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
