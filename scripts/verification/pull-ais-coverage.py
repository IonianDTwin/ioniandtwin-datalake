#!/usr/bin/env python3
"""Coverage-aware, multi-source AIS collector for Data07 (port congestion).

Collects live AIS positions over the Ionian Sea and assigns each vessel to the
four monitored port buffers (Corfu, Lefkada, Kefalonia, Zakynthos), then reports
per port:
  * live vessel count,
  * a coverage state (live | none) so that "no receiver" is never mistaken for
    "empty port",
  * a congestion score min(1, count / threshold) — threshold is a PROPOSAL
    constant, and
  * the authoritative EMODnet vessel-density baseline for reference.

Sources:
  * aisstream.io  - live (free WebSocket; AISSTREAM_API_KEY from .env)
  * AISHub        - NOT CONFIGURED (free tier requires AISHUB_API_KEY + NMEA
                    decode; add the key and implement the TCP/NMEA connector to
                    merge a second, complementary receiver network)
  * EMODnet Human Activities - vessel-density baseline (already pulled; embedded)

Read-only, bounded window, retained sample + sha256. Outputs to data/samples/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from websocket import WebSocketTimeoutException, create_connection

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "data" / "samples"

# Whole northern + central Ionian (covers all four ports).
IONIAN_BBOX = [[39.9, 19.4], [37.4, 21.5]]

# Monitored port buffers (research-notes 2026-10-08) + EMODnet baseline.
# emodnet_density is hours/km²/yr (vesseldensity_allavg); null = not yet pulled.
# threshold is the congestion-score denominator (PROPOSAL, to be validated).
PORTS = [
    {"id": "corfu", "name": "Corfu (Kerkyra)", "bbox": [[39.70, 19.85], [39.55, 19.98]],
     "emodnet_density": 352.28, "threshold": 5},
    {"id": "lefkada", "name": "Lefkada", "bbox": [[38.86, 20.68], [38.80, 20.73]],
     "emodnet_density": None, "threshold": 2},
    {"id": "kefalonia", "name": "Argostoli & Sami (Kefalonia)", "bbox": [[38.30, 20.45], [38.15, 20.70]],
     "emodnet_density": 226.97, "threshold": 3},
    {"id": "zakynthos", "name": "Zakynthos", "bbox": [[37.82, 20.88], [37.75, 20.93]],
     "emodnet_density": 169.60, "threshold": 3},
]
DEFAULT_WINDOW = 300


def load_key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("AISSTREAM_API_KEY="):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    raise SystemExit("AISSTREAM_API_KEY not set in .env")


def in_bbox(lat: float, lon: float, bbox: list[list[float]]) -> bool:
    if lat is None or lon is None:
        return False
    (lat_max, lon_min), (lat_min, lon_max) = bbox[0], bbox[1]
    return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max


def source_status() -> dict:
    aishub = "AISHUB_API_KEY" in os.environ or any(
        l.strip().startswith("AISHUB_API_KEY=") for l in
        (ROOT / ".env").read_text(encoding="utf-8").splitlines()
    )
    return {
        "aisstream": {"status": "active", "auth": "AISSTREAM_API_KEY"},
        "aishub": {"status": "configured" if aishub else "not_configured",
                   "note": "free tier; TCP/NMEA feed; NMEA (AIVDM) decoding required"},
        "emodnet": {"status": "baseline",
                    "source": "EMODnet Human Activities WMS vesseldensity_allavg",
                    "unit": "hours per square km per year"},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    key = load_key()
    subscription = {
        "APIKey": key,
        "BoundingBoxes": [IONIAN_BBOX],
        "FilterMessageTypes": ["PositionReport", "ShipStaticData"],
    }
    ws = create_connection("wss://stream.aisstream.io/v0/stream", timeout=30)
    ws.send(json.dumps(subscription))
    print("subscribed", IONIAN_BBOX, "window", args.window, "s", flush=True)

    started = time.time()
    vessels: dict[str, dict] = {}

    def touch(mmsi: str) -> dict:
        mmsi = str(mmsi)
        v = vessels.get(mmsi)
        if v is None:
            v = {"mmsi": mmsi, "last_position": {}, "name": "", "call_sign": None,
                 "position_count": 0}
            vessels[mmsi] = v
        return v

    while time.time() - started < args.window:
        remaining = args.window - (time.time() - started)
        ws.settimeout(max(1.0, min(10.0, remaining)))
        try:
            _, data = ws.recv_data()
        except WebSocketTimeoutException:
            continue
        except Exception as exc:
            print("recv stopped:", exc, flush=True)
            break
        if not data:
            continue
        try:
            msg = json.loads(data.decode("utf-8"))
        except Exception:
            continue
        mtype = msg.get("MessageType")
        meta = msg.get("MetaData") or {}
        mid = meta.get("MMSI")
        body = msg.get("Message") or {}
        if mtype == "PositionReport" and mid is not None:
            pr = body.get("PositionReport") or body
            rec = touch(mid)
            rec["last_position"] = {
                "lat": pr.get("Latitude"), "lon": pr.get("Longitude"),
                "sog_kn": pr.get("Sog"), "cog": pr.get("Cog"),
                "nav_status": pr.get("NavigationalStatus"),
                "valid": pr.get("Valid"),
                "ts_utc": meta.get("time_utc"),
            }
            rec["position_count"] += 1
            rec["name"] = rec["name"] or meta.get("ShipName") or ""
        elif mtype == "ShipStaticData" and mid is not None:
            sd = body.get("ShipStaticData") or body
            rec = touch(mid)
            rec["name"] = rec["name"] or sd.get("Name") or sd.get("ShipName") or ""
            rec["call_sign"] = rec["call_sign"] or sd.get("CallSign")
    ws.close()

    # assign to ports
    port_rows = []
    assigned = set()
    for p in PORTS:
        in_port = []
        for m, v in vessels.items():
            pos = v["last_position"]
            if in_bbox(pos.get("lat"), pos.get("lon"), p["bbox"]):
                in_port.append({"mmsi": m, "name": v["name"],
                                "call_sign": v["call_sign"], **pos})
                assigned.add(m)
        coverage = "live" if in_port else "none"
        count = len(in_port)
        score = round(min(1.0, count / p["threshold"]), 3) if coverage == "live" else None
        port_rows.append({
            "id": p["id"], "name": p["name"], "bbox": p["bbox"],
            "emodnet_density_hours_per_km2_yr": p["emodnet_density"],
            "coverage": coverage,
            "live_vessels": count,
            "vessels": in_port,
            "congestion_score": score,
            "threshold_proposal": p["threshold"],
        })

    unassigned = [{"mmsi": m, "name": v["name"], "call_sign": v["call_sign"],
                   **v["last_position"]}
                  for m, v in vessels.items() if m not in assigned]

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = args.out or (SAMPLES / f"ais-coverage-{ts}.json")
    out = out if out.is_absolute() else (ROOT / out).resolve()
    payload = {
        "source": "aisstream.io (live) + EMODnet (baseline) — coverage-aware",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "window_seconds": round(time.time() - started, 1),
        "bbox": IONIAN_BBOX,
        "sources": source_status(),
        "total_unique_vessels": len(vessels),
        "ports": port_rows,
        "unassigned_vessels": unassigned,
        "note": ("coverage=none means zero AIS reports for that port buffer in the "
                 "window — most likely absent receiver coverage, not an empty port. "
                 "Congestion threshold is a PROPOSAL constant; EMODnet density is the "
                 "authoritative reference for validation."),
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()

    print(json.dumps({
        "sample_path": str(out.relative_to(ROOT)),
        "sha256": digest,
        "total_unique_vessels": len(vessels),
        "ports": [{"id": p["id"], "coverage": p["coverage"],
                   "live_vessels": p["live_vessels"],
                   "score": p["congestion_score"],
                   "emodnet_density": p["emodnet_density_hours_per_km2_yr"]}
                  for p in port_rows],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
