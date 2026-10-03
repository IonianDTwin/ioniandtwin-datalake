#!/usr/bin/env python3
"""Pull a bounded live AIS sample for Data07 (port congestion) from aisstream.io.

Reads AISSTREAM_API_KEY from .env (untracked, never committed). Subscribes to a
bounding box around Corfu port, captures PositionReports for a short window, and
reports the unique vessels observed. Read-only, bounded, retained sample + checksum.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from websocket import WebSocketTimeoutException, create_connection

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "data" / "samples"

# Corfu port + harbor approaches
BBOX = [[39.55, 19.85], [39.70, 19.98]]
WINDOW_SECS = 90


def load_key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("AISSTREAM_API_KEY="):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    raise SystemExit("AISSTREAM_API_KEY not set in .env")


def main() -> None:
    key = load_key()
    url = "wss://stream.aisstream.io/v0/stream"
    subscription = {
        "APIKey": key,
        "BoundingBoxes": [BBOX],
        "FilterMessageTypes": ["PositionReport"],
    }

    ws = create_connection(url, timeout=30)
    ws.send(json.dumps(subscription))
    print("subscribed bbox", BBOX, flush=True)

    started = time.time()
    mmsi: set[str] = set()
    names: dict[str, str] = {}
    frames: list = []
    positions: list = []

    while time.time() - started < WINDOW_SECS:
        remaining = WINDOW_SECS - (time.time() - started)
        ws.settimeout(max(1.0, min(10.0, remaining)))
        try:
            _, data = ws.recv_data()
        except WebSocketTimeoutException:
            continue
        except Exception:
            break
        if not data:
            continue
        try:
            msg = json.loads(data.decode("utf-8"))
        except Exception:
            continue
        frames.append(msg)
        mtype = msg.get("MessageType")
        meta = msg.get("MetaData") or {}
        mid = meta.get("MMSI")
        if mtype == "PositionReport" and mid is not None:
            s = str(mid)
            mmsi.add(s)
            names.setdefault(s, meta.get("ShipName") or "")
            body = msg.get("Message") or {}
            pr = body.get("PositionReport") or body
            lat = pr.get("Latitude")
            lon = pr.get("Longitude")
            positions.append(
                {
                    "mmsi": mid,
                    "name": meta.get("ShipName"),
                    "lat": lat if lat is not None else meta.get("latitude"),
                    "lon": lon if lon is not None else meta.get("longitude"),
                    "sog_kn": pr.get("Sog"),
                    "cog": pr.get("Cog"),
                }
            )
    ws.close()

    elapsed = round(time.time() - started, 1)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = SAMPLES / f"aisstream-corfu-positionreports-{ts}.json"
    payload = {
        "source": "aisstream.io (live AIS WebSocket)",
        "bbox": BBOX,
        "window_seconds": elapsed,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "unique_vessels": len(mmsi),
        "vessels": [{"mmsi": m, "name": names.get(m, "")} for m in sorted(mmsi)],
        "sample_positions": positions[:20],
        "frame_count": len(frames),
        "raw_frames": frames,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()

    print(
        json.dumps(
            {
                "bbox": BBOX,
                "window_seconds": elapsed,
                "unique_vessels": len(mmsi),
                "vessels": [{"mmsi": m, "name": names.get(m, "")} for m in sorted(mmsi)],
                "frame_count": len(frames),
                "sample_path": str(out.relative_to(ROOT)),
                "sha256": digest,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
