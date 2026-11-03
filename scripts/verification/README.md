# Verification & Dataset Build Scripts

`DECISION` Reproducible, public, read-only, bounded pull tests and dataset builders. Raw pulls land in `data/raw/` (untracked, shared across indicators) or `data/samples/` (small tracked baseline samples), provenance is recorded in `data/manifests/`, per-indicator self-describing JSONs + Markdown dictionaries are built in `data/indicators/data01..data34/`, and the master roll-up is built in `data/curated/`.

## Core Build & Verification Commands

### 1. Build & Verify All 34 Per-Indicator Folders (`data/indicators/data01..data34`)
Generates `raw-source-description.json`, `refined-data.json` and `README.md` for every indicator `Data01`–`Data34`, then verifies the result by re-reading it from disk. Requires `jsonschema` (`pip install -e '.[verify]'`).

```bash
python3 scripts/verification/build_indicator_folders.py           # build, then check
python3 scripts/verification/build_indicator_folders.py --check   # check only, writes nothing
```

The check:
- recomputes the sha256 of every raw file and requires it in the cited manifest;
- validates every observation against `schemas/observation-schema.json` with `jsonschema`;
- requires each folder's observations to equal `data/curated/observations-2026-11-03.json` (Data07: its own snapshot);
- checks percentage and score bounds.

A build stops if a raw file no longer matches the hash pinned in the script.

### 1b. Reproduce ad hoc intermediate files (check mode by default)

```bash
python3 scripts/verification/extract-cams-summary.py          # CAMS zip -> cams-ionian-20260930-summary.json (Data01, Data15)
python3 scripts/verification/reproduce-derived-samples.py     # ELSTAT STO12 xlsx -> bed-places JSON; nin3 -> derived Data22 / Data28 files
```

Both compare a fresh rebuild with the existing file and write only with `--write`.

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
