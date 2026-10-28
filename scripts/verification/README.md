# Verification & Dataset Build Scripts

`DECISION` Reproducible, public, read-only, bounded pull tests and dataset builders. Raw pulls land in `data/raw/` (untracked, shared across indicators) or `data/samples/` (small tracked baseline samples), provenance is recorded in `data/manifests/`, per-indicator self-describing JSONs + Markdown dictionaries are built in `data/indicators/data01..data34/`, and the master roll-up is built in `data/curated/`.

## Core Build & Verification Commands

### 1. Build & Verify All 34 Per-Indicator Folders (`data/indicators/data01..data34`)
Generates `extracted-summary.json` (with `_meta.feature_dictionary`), `observations.json`, and `README.md` for every indicator `Data01`–`Data34`, and executes two-tier verification (strict schema + domain bounds + `D-014` spatial consistency):

```bash
python3 scripts/verification/build_indicator_folders.py
```

### 2. Build Master Observations & Composite Roll-up (`data/curated/`)
Merges base, derived, dashboard, and standalone verified series into `data/curated/observations-<date>.json` / `.csv` and `composite-<date>.json`:

```bash
python3 scripts/verification/build_dashboard.py \
  --manifest data/manifests/source-verification-2026-09-22.json \
  --manifest data/manifests/source-verification-2026-09-24.json \
  --manifest data/manifests/source-verification-2026-10-01.json \
  --manifest data/manifests/source-verification-2026-10-02.json \
  --manifest data/manifests/source-verification-2026-10-03.json
```

### 3. Render Master Progress HTML (`docs/data-preparation-progress.html`)
Renders `docs/data-preparation-progress.md` to a standalone GitHub-styled HTML report:

```bash
python3 scripts/verification/render_progress_html.py
```

## Individual Indicator Pull & Compute Scripts

- `pull-data02-bathing-water-el62.py` — EEA Discomap 2024 Greece bathing-water GeoJSON pull + 3 km coastal spatial join to GISCO `EL62` (`Data02`, `Data03`).
- `pull-data06-airport-congestion.py` — OpenSky Network live state-vector pull + 25 km approach-buffer scoring across `CFU`, `ZTH`, `EFL`, `PVK` (`Data06`).
- `compute-data07-anticipated-congestion.py` — Anticipated port-congestion model fusing CruiseMapper calls with Greek NAP ferry baselines (`Data07`, `PROPOSAL`).
- `pull-data19-platform-rentals.py` — Eurostat `tour_ce_omn12` + `tour_occ_nin2` pull and platform share calculation for `EL62` 2018–2025 (`Data19`).
- `compute-data20-internet-speed.py` — Ookla Open Data 2024-Q3 fixed & mobile tile spatial join to GISCO `EL62` (`Data20`).
- `pull-data24-protected-land.py` & `compute-data24-protected-land.py` & `viz-data24-protected-land.py` — EEA Natura 2000 Habitats & Birds spatial clip to GISCO `EL62` land polygon (`Data24`).
- `pull-eurostat-tourism.sh`, `pull-open-meteo.sh`, `pull-gstc-pdf.sh` — Initial vertical-slice shell pullers (`Data13`, `Data14`, `Data16`, `Data26`, `Data27`, `Data31`, `Data33`).
