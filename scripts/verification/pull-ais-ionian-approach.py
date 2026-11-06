#!/usr/bin/env python3
"""Bounded AIS coverage test for ships approaching the Ionian Islands (Data07 hours-ahead layer).

Reads AISSTREAM_API_KEY from .env (never printed). Subscribes to aisstream.io for the
Ionian bounding box (37.0-40.5N, 19.0-22.0E) for a short window and records position
reports plus ship static data (type, destination, ETA). Read-only, bounded.

Usage: python3 -P scripts/verification/pull-ais-ionian-approach.py [--seconds 180]
Output: data/raw/aisstream-ionian-approach-<UTC>.json (data/raw is git-ignored)
Status: PROPOSAL (feasibility only).
"""
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from websocket import WebSocketTimeoutException, create_connection

ROOT = Path(__file__).resolve().parents[2]
BBOX = [[37.0, 19.0], [40.5, 22.0]]


def load_key():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("AISSTREAM_API_KEY="):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    raise SystemExit("AISSTREAM_API_KEY not set in .env")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=180)
    a = ap.parse_args()
    ws = create_connection("wss://stream.aisstream.io/v0/stream", timeout=10)
    ws.send(json.dumps({"APIKey": load_key(), "BoundingBoxes": [BBOX],
                        "FilterMessageTypes": ["PositionReport", "ShipStaticData"]}))
    start = time.time()
    pos, static, n = {}, {}, 0
    while time.time() - start < min(a.seconds, 600):
        try:
            msg = json.loads(ws.recv())
        except WebSocketTimeoutException:
            continue
        n += 1
        meta = msg.get("MetaData", {})
        mmsi = meta.get("MMSI")
        if msg.get("MessageType") == "PositionReport":
            pos[mmsi] = {"lat": meta.get("latitude"), "lon": meta.get("longitude"),
                         "sog": msg["Message"]["PositionReport"].get("Sog"), "name": meta.get("ShipName", "").strip()}
        elif msg.get("MessageType") == "ShipStaticData":
            s = msg["Message"]["ShipStaticData"]
            static[mmsi] = {"name": s.get("Name", "").strip(), "type": s.get("Type"),
                            "destination": s.get("Destination", "").strip(), "eta": s.get("Eta"),
                            "dimension": s.get("Dimension")}
    ws.close()
    elapsed = round(time.time() - start)
    # AIS ship type 60-69 = passenger vessels
    passenger = {m: v for m, v in static.items() if isinstance(v.get("type"), int) and 60 <= v["type"] <= 69}
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / f"data/raw/aisstream-ionian-approach-{ts}.json"
    out.write_text(json.dumps({"source": "aisstream.io (live AIS WebSocket)", "bbox": BBOX,
                               "window_seconds": elapsed, "messages": n,
                               "positions": pos, "static": static}, indent=1))
    print("window_s", elapsed, "messages", n, "vessels_with_position", len(pos), "with_static", len(static))
    print("passenger_vessels_static", len(passenger))
    for m, v in sorted(passenger.items(), key=lambda kv: -(sum((kv[1].get("dimension") or {}).get(k, 0) for k in ("A", "B")))):
        d = v.get("dimension") or {}
        print("  ", v["name"], "len", d.get("A", 0) + d.get("B", 0), "dest", v["destination"], "eta", v["eta"])
    print("wrote", out.relative_to(ROOT), out.stat().st_size, "sha256", hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
