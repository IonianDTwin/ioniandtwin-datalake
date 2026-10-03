#!/usr/bin/env python3
"""Pull raw geometries for Data24 (Protected land %) and record checksums.

Data24 = "Poseosto prostatevomenis gis (%)" (protected land %). The documented
ETL is: clip Natura 2000 site polygons to EL62 (Ionian Islands NUTS2), split
terrestrial/marine (done by intersecting with the EL62 land polygon), union
Habitats ∪ Birds, then % = protected land area / EL62 land area.

This script acquires the raw inputs (read-only, no credentials):

1. Eurostat GISCO NUTS 2021 boundary (level 2, EPSG:3035 LAEA) -> full file
   retained in data/raw/, then the EL62 feature extracted to a small subset.
2. EEA ArcGIS REST "Natura2000Sites" MapServer, layers 0 (Habitats) and 1
   (Birds). To avoid any reliance on region coding, it pulls the *superset* of
   every Greek site whose envelope intersects the EL62 envelope (a bounding box
   around the Ionian Islands). A precise polygon clip against EL62 happens in
   compute-data24-protected-land.py; mainland sites that merely fall inside the
   bounding box (e.g. Amvrakikos, Acheloos delta, Pindos) are excluded there.

The protected-land computation is a separate script so acquisition stays
distinct from transform. Outputs (raw, git-ignored): data/raw/<files>,
checksums printed for the manifest.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pyproj

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

GISCO_URL = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_3035_LEVL_2.geojson"
GISCO_FULL = RAW / "gisco-nuts-2021-3035-LEVL_2.geojson"
GISCO_EL62 = RAW / "gisco-nuts-2021-3035-EL62.geojson"

N2K_BASE = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"
N2K_HABITATS = RAW / "eea-natura2000-el62-envelope-habitats-4326.geojson"
N2K_BIRDS = RAW / "eea-natura2000-el62-envelope-birds-4326.geojson"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(url: str, dest: Path, timeout: int = 120, retries: int = 3) -> int:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IonianDTwin-data24/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            dest.write_bytes(data)
            return len(data)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise SystemExit(f"fetch failed after {retries} tries: {url} -> {last}")


def pull_gisco() -> dict:
    if not GISCO_FULL.exists():
        n = fetch(GISCO_URL, GISCO_FULL)
    else:
        n = GISCO_FULL.stat().st_size
    full_digest = sha256(GISCO_FULL)
    fc = json.loads(GISCO_FULL.read_text(encoding="utf-8"))
    el62 = [f for f in fc["features"] if f["properties"].get("NUTS_ID") == "EL62"]
    if len(el62) != 1:
        raise SystemExit(f"expected exactly 1 EL62 feature, got {len(el62)}")
    subset = {"type": "FeatureCollection", "features": el62,
              "crs": fc.get("crs"), "name": "EL62 (Ionia Nisia) NUTS2 2021"}
    GISCO_EL62.write_text(json.dumps(subset, ensure_ascii=False), encoding="utf-8")
    prop = el62[0]["properties"]
    return {
        "url": GISCO_URL,
        "full_bytes": n,
        "full_sha256": full_digest,
        "el62_sha256": sha256(GISCO_EL62),
        "el62_path": str(GISCO_EL62.relative_to(ROOT)),
        "nuts_id": prop.get("NUTS_ID"),
        "nuts_name": prop.get("NAME_LATN"),
        "crs": "EPSG:3035 (LAEA, equal-area)",
    }


def el62_envelope_wgs84() -> list[float]:
    """Return [xmin,ymin,xmax,ymax] of EL62 in WGS84 lon/lat for a spatial query."""
    fc = json.loads(GISCO_EL62.read_text(encoding="utf-8"))
    geom = fc["features"][0]["geometry"]
    transformer = pyproj.Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True)
    if geom["type"] == "MultiPolygon":
        rings = [r for p in geom["coordinates"] for r in p]
    else:
        rings = geom["coordinates"]
    xs, ys = [], []
    for ring in rings:
        for x, y in ring:
            lon, lat = transformer.transform(x, y)
            xs.append(lon)
            ys.append(lat)
    return [min(xs), min(ys), max(xs), max(ys)]


def query_ids(layer: int, envelope: list[float]) -> list[str]:
    xmin, ymin, xmax, ymax = envelope
    params = {
        "where": "MS='GR'",
        "geometry": json.dumps({"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax,
                                "spatialReference": {"wkid": 4326}}),
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "inSR": "4326",
        "outFields": "SITECODE",
        "returnGeometry": "false",
        "f": "json",
    }
    url = f"{N2K_BASE}/{layer}/query?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as r:
        d = json.loads(r.read())
    return sorted(f["attributes"]["SITECODE"] for f in d.get("features", []))


def pull_layer(layer: int, dest: Path, codes: list[str]) -> dict:
    """Pull full geometry for an explicit set of site codes (IN list)."""
    # Batch the IN clause (ArcGIS supports it); keep URL length safe with chunks.
    chunks = [codes[i:i + 50] for i in range(0, len(codes), 50)]
    merged = {"type": "FeatureCollection", "features": []}
    for chunk in chunks:
        inlist = ",".join(f"'{c}'" for c in chunk)
        params = {
            "where": f"MS='GR' AND SITECODE IN ({inlist})",
            "outFields": "SITECODE,SITENAME,Area_ha,Area_km2,MS,SITETYPE",
            "returnGeometry": "true",
            "outSR": "4326",
            "f": "geojson",
        }
        url = f"{N2K_BASE}/{layer}/query?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=180) as r:
            d = json.loads(r.read())
        merged["features"].extend(d.get("features", []))
    dest.write_text(json.dumps(merged, ensure_ascii=False), encoding="utf-8")
    got = sorted(f["properties"]["SITECODE"] for f in merged["features"])
    missing = sorted(set(codes) - set(got))
    return {
        "layer": layer,
        "requested": len(codes),
        "received": len(got),
        "missing": missing,
        "bytes": dest.stat().st_size,
        "sha256": sha256(dest),
        "path": str(dest.relative_to(ROOT)),
        "sitecodes": got,
    }


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report = {"source": "Data24 protected land - raw geometry pull",
              "captured_at_utc": datetime.now(timezone.utc).isoformat()}

    print("pulling GISCO NUTS 2021 level 2 ...", flush=True)
    report["gisco"] = pull_gisco()
    print(json.dumps(report["gisco"], indent=2), flush=True)

    env = el62_envelope_wgs84()
    report["el62_envelope_wgs84"] = [round(v, 6) for v in env]

    report["natura2000"] = []
    for layer, dest in ((0, N2K_HABITATS), (1, N2K_BIRDS)):
        codes = query_ids(layer, env)
        print(f"layer {layer}: {len(codes)} sites intersect EL62 envelope; pulling full geometry ...", flush=True)
        res = pull_layer(layer, dest, codes)
        report["natura2000"].append(res)
        print(json.dumps({k: v for k, v in res.items() if k != "sitecodes"}, indent=2), flush=True)

    out = RAW / f"data24-pull-report-{ts}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nreport -> {out.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
