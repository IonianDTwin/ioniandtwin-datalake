#!/usr/bin/env python3
"""Compute Data24 (Protected land %) via spatial join and verify the result.

Method (documented ETL, decisions D-014/D-0xx-consistent):
  1. EL62 (Ionian Islands NUTS2) land polygon from Eurostat GISCO NUTS 2021
     (EPSG:3035, equal-area LAEA).
  2. Natura 2000 sites (Habitats + Birds) pulled as the envelope-intersecting
     superset (see pull-data24-protected-land.py), reprojected to EPSG:3035.
  3. Intersect each site with the EL62 polygon -> the portion inside the
     islands' land. Because EL62 is a land polygon, this is the terrestrial
     (non-marine) protected area within the region.
  4. Union Habitats ∪ Birds (dissolve overlaps) -> protected land geometry.
  5. % = area(protected land) / area(EL62) * 100.

Verification built in:
  - EL62 land area is cross-checked against the published ~2,307 km² figure.
  - Every site's EL62-overlap is reported, so the completeness claim (no
    non-GR22 site contributes meaningful land) is auditable.
  - A small tolerance/buffer(0) pass cleans invalid ring self-intersections.

Output: data/curated/data24-protected-land-2026-10-03.json (full audit) +
a compact summary printed to stdout for the manifest/observation.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform, unary_union
from shapely.validation import make_valid

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
CURATED = ROOT / "data" / "curated"

EL62_PATH = RAW / "gisco-nuts-2021-3035-EL62.geojson"
HABITATS_PATH = RAW / "eea-natura2000-el62-envelope-habitats-4326.geojson"
BIRDS_PATH = RAW / "eea-natura2000-el62-envelope-birds-4326.geojson"

PUBLISHED_EL62_KM2 = 2307.0  # known Ionian Islands land area (km2)


def load_feature(geom):
    g = shape(geom)
    if not g.is_valid:
        g = make_valid(g)
    return g.buffer(0)


def to_3035(geom):
    proj = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True).transform
    return transform(proj, geom)


def load_el62() -> tuple:
    fc = json.loads(EL62_PATH.read_text(encoding="utf-8"))
    g = load_feature(fc["features"][0]["geometry"])
    return g


def load_sites(path: Path) -> list[dict]:
    fc = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for f in fc["features"]:
        p = f["properties"]
        g = load_feature(f["geometry"])
        out.append({
            "sitecode": p.get("SITECODE"),
            "sitename": p.get("SITENAME"),
            "area_ha": p.get("Area_ha"),
            "geom_4326": g,
        })
    return out


def main() -> None:
    el62 = load_el62()
    el62_km2 = el62.area / 1e6
    el62_ha = el62.area / 1e4

    audit = []
    for directive, path in (("Habitats", HABITATS_PATH), ("Birds", BIRDS_PATH)):
        for s in load_sites(path):
            g3035 = to_3035(s["geom_4326"])
            g3035 = g3035.buffer(0) if not g3035.is_valid else g3035
            inter = g3035.intersection(el62)
            overlap_ha = inter.area / 1e4 if not inter.is_empty else 0.0
            audit.append({
                "directive": directive,
                "sitecode": s["sitecode"],
                "sitename": s["sitename"],
                "full_area_ha": s["area_ha"],
                "within_el62_ha": round(overlap_ha, 3),
                "is_gr22": s["sitecode"].startswith("GR22"),
            })

    # Completeness: any non-GR22 site with meaningful land overlap?
    nongr22_overlap = [a for a in audit if not a["is_gr22"] and a["within_el62_ha"] > 1.0]

    # Union per directive then overall.
    habitats_union = unary_union([
        to_3035(s["geom_4326"]).intersection(el62)
        for s in load_sites(HABITATS_PATH)
    ]).buffer(0)
    birds_union = unary_union([
        to_3035(s["geom_4326"]).intersection(el62)
        for s in load_sites(BIRDS_PATH)
    ]).buffer(0)
    combined = unary_union([habitats_union, birds_union]).buffer(0)

    res = {
        "computed_at_utc": datetime.now(timezone.utc).isoformat(),
        "indicator_id": "Data24",
        "indicator_name": "Protected land (%)",
        "spatial_ref": {"level": "NUTS2", "code": "EL62"},
        "el62_land_km2": round(el62_km2, 2),
        "el62_land_ha": round(el62_ha, 2),
        "published_el62_km2": PUBLISHED_EL62_KM2,
        "el62_area_delta_pct": round((el62_km2 - PUBLISHED_EL62_KM2) / PUBLISHED_EL62_KM2 * 100, 3),
        "habitats_protected_land_ha": round(habitats_union.area / 1e4, 2),
        "birds_protected_land_ha": round(birds_union.area / 1e4, 2),
        "combined_protected_land_ha": round(combined.area / 1e4, 2),
        "combined_protected_land_km2": round(combined.area / 1e6, 2),
        "protected_land_pct": round(combined.area / 1e4 / el62_ha * 100, 4),
        "nongr22_sites_with_land_overlap": nongr22_overlap,
        "audit": audit,
    }

    out = CURATED / "data24-protected-land.json"
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {k: v for k, v in res.items() if k != "audit"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\naudit -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
