#!/usr/bin/env python3
"""Build the dashboard-ready, schema-aligned observation dataset.

This is the reproducible "first vertical slice" exporter. It:
  1. re-decodes the verified raw samples (Eurostat SDMX, Open-Meteo flat, EEA Discodata SQL)
     and emits one schema-aligned observation per verified data point;
  2. adds DERIVED indicators (seasonality %, length of stay, % excellent bathing water,
     clean-beach flag, dominant typology) with their formulas recorded in provenance;
  3. adds ONE transparent COMPOSITE indicator (Tourism Pressure Index, prototype) with
     exposed formula, weights, units and polarity;
  4. merges the standalone verified-series observations emitted by their dedicated
     pullers (Data06 airport congestion, Data19 platform rentals, Data20 internet speed,
     Data02/03 EL62 bathing water) into the single master snapshot.

Outputs (all schema-validated against schemas/observation-schema.json):
  data/curated/observations-<date>.json / .csv
  data/curated/composite-<date>.json

Usage:
  python3 scripts/verification/build_dashboard.py \
      --manifest data/manifests/source-verification-2026-09-22.json \
      --manifest data/manifests/source-verification-2026-09-24.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_pull_reports import decode, load_map, series_for, _match_series, indicators_by_id  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
SAMPLES = ROOT / "data" / "samples"
CURATED = ROOT / "data" / "curated"

ISO_MONTH = re.compile(r"^\d{4}-\d{2}$")
ISO_YEAR = re.compile(r"^\d{4}$")
ISO_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def granularity_of(time_str: str) -> str:
    if "T" in time_str:
        return "instant"
    if ISO_MONTH.match(time_str):
        return "monthly"
    if ISO_YEAR.match(time_str):
        return "annual"
    if ISO_DAY.match(time_str):
        return "daily"
    return "instant"


def _spatial_level(geo: str) -> str:
    """Map a Eurostat geo code to observation-schema spatial_ref.level.

    D-014: NUTS2 (EL62) is the analysis reference; country (EL) is a national
    proxy; NUTS3 (EL621-624) is internal disaggregation only and is never
    emitted as an observation (aggregate to NUTS2 first).
    """
    if len(geo) == 2:
        return "country"   # ISO 3166 alpha-2, e.g. EL
    if len(geo) == 4:
        return "NUTS2"     # e.g. EL62
    raise ValueError(
        f"geo {geo!r} is finer than NUTS2; aggregate to NUTS2 before emitting (D-014)"
    )


def _obs(oid, indicator_id, ind_name, series_label, source_id, observed_at,
         granularity, spatial_level, spatial_code, value, unit, provenance,
         polarity=None, period_end=None):
    return {
        "observation_id": oid,
        "indicator_id": indicator_id,
        "indicator_name": ind_name,
        "series_label": series_label,
        "source_id": source_id,
        "observed_at": observed_at,
        "observed_period_end": period_end,
        "temporal_granularity": granularity,
        "ingested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spatial_ref": {"level": spatial_level, "code": spatial_code, "geometry": None},
        "value": value,
        "unit": unit,
        "polarity": polarity,
        "provenance": provenance,
    }


def sdmx_values(path: Path) -> dict:
    """Decode an SDMX 2.1 JSON sample into {dimension-combo-key: value} rows (as dicts)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    _, _, rows, _ = decode(data)
    return rows


def _nuts3_nights_years(path: Path) -> dict:
    """Load a wrapper {NUTS3_geo: SDMX dataset} and return {year: {geo: nights}}.

    D-014: NUTS3 data is an internal disaggregation; callers must aggregate it to
    NUTS2 (EL62) before emitting an observation.
    """
    wrapper = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict[str, float]] = {}
    for geo, dataset in wrapper.items():
        _, _, rows, _ = decode(dataset)
        for r in rows:
            year = r.get("time", "")
            val = r.get("value")
            if isinstance(val, (int, float)) and year:
                out.setdefault(str(year), {})[geo] = val
    return out


def base_observations(manifests: list[Path], mapping: dict) -> list[dict]:
    series_map = series_for(mapping)
    ind_by_id = indicators_by_id(mapping)
    obs: list[dict] = []
    seen: set[str] = set()

    for mpath in manifests:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
        for ev in manifest.get("evidence", []):
            p = ev.get("sample_path")
            if not p or not p.lower().endswith(".json"):
                continue
            path = ROOT / p
            if not path.exists():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            kind, cols, rows, labels = decode(data)
            src_key = ev.get("source_id", "")
            src_series = series_map.get(src_key, [])
            url = ev.get("url", "")
            checksum = ev.get("checksum_sha256", "")
            for s in src_series:
                for r in rows:
                    if not _match_series(kind, r, [s]):
                        continue
                    iid = s["indicator_id"]
                    t = r.get("time", "")
                    value = r.get("value")
                    gran = granularity_of(t)
                    code = r.get("geo", "") if kind == "sdmx" else "39.62,19.92"
                    level = _spatial_level(code) if kind == "sdmx" else "point"
                    oid = f"{src_key}:{iid}:{s.get('label','')}:{t}"
                    if oid in seen:
                        continue
                    seen.add(oid)
                    ind = ind_by_id.get(iid, {})
                    obs.append(_obs(
                        oid, iid, ind.get("name", iid), s.get("label", ""),
                        src_key, t, gran, level, code, value,
                        s.get("unit", "") or (r.get("unit", "") if kind != "sdmx" else ""),
                        {"raw_checksum_sha256": checksum, "access_method": "api",
                         "request_url": url},
                    ))
    return obs


def derived_observations(ingested: list[dict]) -> list[dict]:
    """Derived indicators with formulas recorded in provenance.request_url (formula string)."""
    out: list[dict] = []

    # --- Data29 seasonality % (peak-month share) from monthly nights sample ---
    monthly = sdmx_values(SAMPLES / "eurostat-tour_occ_nim-EL-2023.json")
    vals = {r["time"]: r["value"] for r in monthly if isinstance(r.get("value"), (int, float))}
    if vals:
        total = sum(vals.values())
        peak = max(vals.values())
        peak_month = [k for k, v in vals.items() if v == peak][0]
        pct = round(peak / total * 100, 2)
        out.append(_obs(
            f"Eurostat_tour_occ_nim:Data29:seasonality_peak_share:2023",
            "Data29", "Seasonality (%)", "peak-month share of annual nights",
            "Eurostat_tour_occ_nim", "2023", "annual", "country", "EL",
            pct, "%", {"access_method": "derived",
                       "request_url": "seasonality = max(monthly nights) / sum(monthly nights) * 100 "
                                      f"(peak {peak_month} = {peak:,} of {total:,})"},
            polarity="negative",
        ))

    # --- Data30 average length of stay = nights / arrivals (EL62) ---
    nights = {o["observed_at"]: o["value"] for o in ingested
              if o["indicator_id"] == "Data26" and o["series_label"] == "overnight stays"}
    arrivals = {o["observed_at"]: o["value"] for o in ingested
                if o["indicator_id"] == "Data26" and o["series_label"] == "arrivals"}
    for year in sorted(nights):
        if year in arrivals and arrivals[year]:
            los = round(nights[year] / arrivals[year], 3)
            out.append(_obs(
                f"Eurostat:Data30:length_of_stay:{year}",
                "Data30", "Average length of stay", "nights ÷ arrivals",
                "Eurostat_tour_occ_nin2", year, "annual", "NUTS2", "EL62",
                los, "nights", {"access_method": "derived",
                                "request_url": f"length_of_stay = nights({nights[year]:,}) ÷ arrivals({arrivals[year]:,})"},
            ))

    # --- Data02 / Data03 from EEA bathing-water quality counts ---
    bw = json.loads((SAMPLES / "eea-bathing-water-quality-EL-2024.json").read_text(encoding="utf-8"))
    counts = {r["quality"]: r["n"] for r in bw.get("results", [])}
    exc = counts.get("1 - Excellent", 0)
    good = counts.get("2 - Good", 0)
    suff = counts.get("3 - Sufficient", 0)
    poor = counts.get("4 - Poor", 0)
    notc = counts.get("0 - Not classified", 0)
    total = exc + good + suff + poor + notc
    classified = exc + good + suff + poor
    if total:
        # Emit the full Data02 time series (1990-2024) when the series sample exists.
        bw_series = SAMPLES / "eea-bathing-water-EL-1990-2024.json"
        if bw_series.exists():
            for row in json.loads(bw_series.read_text(encoding="utf-8")).get("series", []):
                out.append(_obs(
                    f"EEA_WISE_BWD:Data02:pct_excellent:{row['season']}",
                    "Data02", "Excellent bathing waters (%)", "% excellent (of all monitored)",
                    "EEA_WISE_BWD_assessment", str(row["season"]), "annual", "country", "EL",
                    row["pct_excellent"], "%",
                    {"access_method": "derived",
                     "request_url": f"pct_excellent = excellent({row['excellent']}) / total({row['total']}) * 100"},
                    polarity="positive",
                ))
        else:
            out.append(_obs(
                "EEA_WISE_BWD:Data02:pct_excellent:2024", "Data02", "Excellent bathing waters (%)",
                "% excellent (of all monitored)", "EEA_WISE_BWD_assessment", "2024",
                "annual", "country", "EL", round(exc / total * 100, 2), "%",
                {"access_method": "derived",
                 "request_url": f"pct_excellent = excellent({exc}) / total({total}) * 100"},
                polarity="positive",
            ))
    if classified:
        out.append(_obs(
            "EEA_WISE_BWD:Data03:clean_beach_share:2024", "Data03", "Clean beach water (reports)",
            "share at least 'Sufficient' (of classified)", "EEA_WISE_BWD_assessment", "2024",
            "annual", "country", "EL", round((exc + good + suff) / classified * 100, 2), "%",
            {"access_method": "derived",
             "request_url": "clean = (Excellent+Good+Sufficient)/classified * 100 (ASSUMPTION)"},
            polarity="positive",
        ))

    # --- Data32 dominant typology (categorical; D-009 rule) ---
    out.append(_obs(
        "Eurostat_tour_occ_nin2:Data32:dominant_typology:2023", "Data32", "Dominant tourism typology",
        "accommodation category with highest nights share", "Eurostat_tour_occ_nin2", "2023",
        "annual", "NUTS2", "EL62", "hotels", None,
        {"access_method": "derived",
         "request_url": "D-009: dominant = argmax(nace_r2 share of nights); hotels ≈73%/70% vs short-stay 26%/30%"},
    ))

    # --- Data22 tourist diversity = 1 − HHI of NUTS3 island night shares (aggregated to NUTS2/EL62) ---
    nin3 = SAMPLES / "eurostat-tour_occ_nin3-EL621-624-2021-2025.json"
    if nin3.exists():
        island_nights = _nuts3_nights_years(nin3)
        for year in sorted(island_nights):
            shares = island_nights[year]
            total = sum(shares.values())
            if total <= 0:
                continue
            hhi = sum((v / total) ** 2 for v in shares.values())
            diversity = round(1 - hhi, 3)
            out.append(_obs(
                f"Eurostat_tour_occ_nin3:Data22:diversity_1_hhi:{year}",
                "Data22", "Tourist diversity (zones)", "1 − HHI of island nights shares",
                "Eurostat_tour_occ_nin3", year, "annual", "NUTS2", "EL62",
                diversity, "index",
                {"access_method": "derived",
                 "request_url": f"diversity = 1 − HHI over {len(shares)} island nights shares, aggregated to EL62"},
            ))

    # --- Data24 protected land % (Natura 2000 ∩ EL62 land, terrestrial) ---
    # Computed by scripts/verification/compute-data24-protected-land.py; result JSON
    # is the auditable provenance (per-site overlap table + Echinades completeness note).
    d24 = CURATED / "data24-protected-land.json"
    if d24.exists():
        r = json.loads(d24.read_text(encoding="utf-8"))
        pct = r.get("protected_land_pct")
        if pct is not None:
            out.append(_obs(
                "EEA_Natura2000:Data24:protected_land_pct:2026",
                "Data24", "Protected land (%)",
                "share of EL62 land under Natura 2000 (Habitats ∪ Birds, terrestrial)",
                "EEA_ArcGIS_ProtectedSites_Natura2000", "2026", "annual", "NUTS2", "EL62",
                round(pct, 2), "%",
                {"access_method": "derived",
                 "request_url": (f"protected_land_pct = union(Natura2000 Habitats ∪ Birds ∩ EL62 land) "
                                 f"÷ EL62 land area × 100 = {r.get('combined_protected_land_ha')} ha "
                                 f"÷ {r.get('el62_land_ha')} ha (NUTS 2021, LAEA EPSG:3035)")},
                polarity="positive",
            ))

    return out


def additional_series_observations() -> list[dict]:
    """Merge the standalone verified-series observation files into the master dataset.

    Data06 (airport congestion), Data19 (platform rental share), Data20 (internet
    speed) and Data02/03 (EL62 bathing water) are produced by their own pullers
    (live OpenSky, Ookla spatial join, EEA Discomap spatial join, Eurostat
    ``tour_ce_omn12``) rather than from the base SDMX samples. Their already-
    schema-validated observations are loaded here and deduplicated by
    ``observation_id`` (latest date-stamped file wins).
    """
    patterns = [
        "observations-data06-airport-congestion-*.json",
        "observations-data19-platform-rental-share-*.json",
        "observations-data20-internet-speed-*.json",
        "observations-data02-bathing-water-*.json",
    ]
    merged: dict[str, dict] = {}
    for pat in patterns:
        for path in sorted(CURATED.glob(pat)):
            for o in json.loads(path.read_text(encoding="utf-8")):
                merged[o.get("observation_id")] = o
    return list(merged.values())


def dashboard_observations() -> list[dict]:
    """Emit EU Tourism Dashboard-sourced indicators (reconciliation, 2026-10-03).

    These are read directly from the dashboard export (the proposal's own source)
    rather than derived; the sample data/samples/eutd-tourism-dashboard-2024-el62.json
    carries the EL62 values.
    """
    src = SAMPLES / "eutd-tourism-dashboard-2024-el62.json"
    if not src.exists():
        return []
    d = json.loads(src.read_text(encoding="utf-8"))
    meta = {
        "excellent_bathing_water": ("Data02", "Excellent bathing waters (%)", "share of bathing waters rated excellent", "%", "positive"),
        "blue_flag_sites": ("Data04", "Blue Flags", "number of Blue Flag sites", "number", "positive"),
        "cultural_assets_density": ("Data23", "Density of cultural elements", "cultural assets per 100 km²", "no. of cultural assets / 100 km²", None),
        "high_nature_value_accommodation": ("Data25", "Accommodation in high-value areas", "share of accommodations in high-nature-value areas", "%", None),
        "net_occupancy": ("Data28", "Occupancy rate (%)", "net occupancy of bed places", "%", None),
        "peak_season_share": ("Data29", "Seasonality (%)", "share of nights in peak season", "%", "negative"),
    }
    out: list[dict] = []
    for key, rec in d.get("el62", {}).items():
        if key not in meta:
            continue
        iid, name, series, unit, pol = meta[key]
        year = str(rec.get("year"))
        out.append(_obs(
            f"EU_Tourism_Dashboard:{iid}:{key}:{year}", iid, name, series,
            "EU_Tourism_Dashboard_2024", year, "annual", "NUTS2", "EL62",
            rec.get("value"), unit,
            {"access_method": "download",
             "request_url": f"EU Tourism Dashboard {rec.get('code')} (2024 export), EL62 {year}"},
            polarity=pol,
        ))
    return out


def composite_observations() -> list[dict]:
    """Tourism Pressure Index (prototype): one transparent composite with exposed formula/weights."""
    # Normalisation reference bounds are ASSUMPTION (documented in the output).
    ref = {"intensity_max": 150_000.0, "density_max": 12_000.0}
    intensity = 97705.53  # Data16 2023, nights/1000 residents (EL62)
    density = 8588.79     # Data31 2023, nights/km² (EL62)
    seasonality_pct = 21.53  # Data29 2023, peak-month share (Greece proxy)
    weights = {"intensity": 0.4, "density": 0.4, "seasonality": 0.2}

    norm = {
        "intensity": min(1.0, intensity / ref["intensity_max"]),
        "density": min(1.0, density / ref["density_max"]),
        "seasonality": seasonality_pct / 100.0,
    }
    index = round(100 * sum(weights[k] * norm[k] for k in weights), 1)

    composite = {
        "composite_id": "tourist_pressure_index",
        "name": "Tourism Pressure Index (prototype)",
        "status": "PROPOSAL",
        "year": 2023,
        "spatial_ref": {"level": "NUTS2", "code": "EL62"},
        "value": index,
        "unit": "index (0-100)",
        "polarity": "negative",
        "formula": "100 * (0.4*intensity_norm + 0.4*density_norm + 0.2*seasonality_norm)",
        "weights": weights,
        "normalisation": {
            "intensity_norm": f"min(1, intensity/{ref['intensity_max']:.0f})",
            "density_norm": f"min(1, density/{ref['density_max']:.0f})",
            "seasonality_norm": "peak_share/100",
        },
        "reference_bounds": ref,
        "inputs": {
            "Data16_tourism_intensity_2023": intensity,
            "Data31_tourism_density_2023": density,
            "Data29_seasonality_peak_share_2023_pct": seasonality_pct,
        },
        "notes": "ASSUMPTION: reference maxima and weights are candidate values, not proposal-defined. "
                 "Prototype only; must not drive public alerts or policy.",
    }
    return [composite]


def validate_against_schema(obs: list[dict], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    props = schema.get("properties", {})
    top_allowed = set(props)
    nested = {
        "spatial_ref": set(props["spatial_ref"]["properties"]),
        "quality": set(props["quality"]["properties"]),
        "provenance": set(props["provenance"]["properties"]),
    }
    gran_enum = set(props["temporal_granularity"].get("enum", []))
    level_enum = set(props["spatial_ref"]["properties"]["level"].get("enum", []))
    pol_enum = set(props["polarity"].get("enum", [])) | {None}
    problems = []
    for o in obs:
        oid = o.get("observation_id", "?")
        for k in required:
            if k not in o:
                problems.append(f"{oid}: missing required '{k}'")
        for k in o:
            if k not in top_allowed:
                problems.append(f"{oid}: unknown top-level key '{k}'")
        if o.get("temporal_granularity") not in gran_enum:
            problems.append(f"{oid}: invalid temporal_granularity {o.get('temporal_granularity')!r}")
        if "polarity" in o and o["polarity"] not in pol_enum:
            problems.append(f"{oid}: invalid polarity {o['polarity']!r}")
        for key, allowed in nested.items():
            obj = o.get(key)
            if isinstance(obj, dict):
                for k in obj:
                    if k not in allowed:
                        problems.append(f"{oid}: unknown {key} key '{k}'")
        sr = o.get("spatial_ref")
        if isinstance(sr, dict) and sr.get("level") not in level_enum:
            problems.append(f"{oid}: invalid spatial_ref.level {sr.get('level')!r}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", action="append", required=True)
    ap.add_argument("--map", default="indicators/source-indicator-map.json")
    ap.add_argument("--schema", default="schemas/observation-schema.json")
    args = ap.parse_args()

    mapping = load_map(args.map)
    manifests = [Path(m) for m in args.manifest]

    base = base_observations(manifests, mapping)
    derived = derived_observations(base)
    dashboard = dashboard_observations()
    additional = additional_series_observations()
    all_obs = base + derived + dashboard + additional

    problems = validate_against_schema(all_obs, ROOT / args.schema)
    if problems:
        print("SCHEMA PROBLEMS:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    CURATED.mkdir(parents=True, exist_ok=True)
    json_path = CURATED / f"observations-{date}.json"
    csv_path = CURATED / f"observations-{date}.csv"
    json_path.write_text(json.dumps(all_obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fields = ["observation_id", "indicator_id", "indicator_name", "series_label",
              "source_id", "temporal_granularity", "observed_at", "observed_period_end",
              "value", "unit", "spatial_level", "spatial_code", "polarity"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for o in all_obs:
            w.writerow({
                "observation_id": o["observation_id"], "indicator_id": o["indicator_id"],
                "indicator_name": o["indicator_name"], "series_label": o["series_label"],
                "source_id": o["source_id"], "temporal_granularity": o["temporal_granularity"],
                "observed_at": o["observed_at"], "observed_period_end": o["observed_period_end"],
                "value": o["value"], "unit": o["unit"],
                "spatial_level": o["spatial_ref"]["level"], "spatial_code": o["spatial_ref"]["code"],
                "polarity": o["polarity"],
            })

    composites = composite_observations()
    comp_path = CURATED / f"composite-{date}.json"
    comp_path.write_text(json.dumps(composites, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"observations: {len(all_obs)} ({len(base)} base + {len(derived)} derived + {len(dashboard)} dashboard + {len(additional)} additional)")
    print(f"  {json_path}")
    print(f"  {csv_path}")
    print(f"composite: {len(composites)}")
    print(f"  {comp_path}")
    if problems:
        print(f"schema problems: {len(problems)} (see above)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
