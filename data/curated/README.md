# data/curated — Master Observation & Composite Roll-ups

`DECISION` This directory holds the **master consolidated dataset** across all verified indicators, plus standalone series inputs merged by `scripts/verification/build_dashboard.py`. Per-indicator raw source descriptions (`raw-source-description.json`), self-describing refined JSONs (`refined-data.json`), and sidecar guides (`README.md`) now live in `data/indicators/data01-<slug>/` … `data34-<slug>/`.

## Canonical Master Files

- `observations-2026-10-20.json` / `.csv` — **99 schema-aligned observations** (28 base + 47 derived + 6 dashboard + 18 additional), the canonical **single source of truth** across all 23 `VERIFIED` indicators.
- `composite-2026-10-20.json` — transparent composite prototype (`Tourism Pressure Index`) with exposed formula, weights, units, and polarity.
- `observations-data07-anticipated-congestion-2026-10-14.json` / `.csv` — **366 schema-compliant `Data07` forecast observations** (one per EL62 port per day, `2026-10-01` → `2026-11-30`; `temporal_granularity=forecast`, `spatial_ref.level=transport_node`). Kept separate from the annual/instant master snapshot because it is a 61-day forward schedule projection (`PROPOSAL`).

## Producer Audit & Series Inputs (also mirrored with `_meta` in `data/indicators/`)

- `data02-bathing-water-el62-2024.json` & `observations-data02-bathing-water-2024.json`/`.csv` (`Data02` & `Data03` EL62 2024 spatial join)
- `data06-airport-congestion.json` & `observations-data06-airport-congestion-2026-10-20.json`/`.csv` (`Data06` OpenSky live approach buffers)
- `scheduled-port-traffic-el62.json` (`Data07` anticipated port congestion timetable)
- `data19-platform-rental-share.json` & `observations-data19-platform-rental-share-2026-10-15.json`/`.csv` (`Data19` Eurostat `tour_ce_omn12` share)
- `data20-internet-speed.json` & `observations-data20-internet-speed-2024Q3.json`/`.csv` (`Data20` Ookla 2024-Q3 spatial join)
- `data24-protected-land.json` & `data24-protected-land.geojson` (`Data24` Natura 2000 ∩ EL62 land spatial join)

## Regeneration & Verification Commands

```bash
# 1. Rebuild master observations & composite roll-up
python3 scripts/verification/build_dashboard.py \
  --manifest data/manifests/source-verification-2026-09-22.json \
  --manifest data/manifests/source-verification-2026-09-24.json \
  --manifest data/manifests/source-verification-2026-10-01.json \
  --manifest data/manifests/source-verification-2026-10-02.json \
  --manifest data/manifests/source-verification-2026-10-03.json

# 2. Rebuild & verify all 34 per-indicator folders (data/indicators/data01..data34)
python3 scripts/verification/build_indicator_folders.py
```
