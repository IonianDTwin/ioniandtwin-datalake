# data/curated - normalized observations

`DECISION` Clean, schema-aligned observations extracted from the verified pull samples, plus derived indicators and one composite prototype. This is the **publication-ready data file** for IonianDTwin.

## Files

- `observations-2026-10-20.json` / `.csv` - **99 schema-aligned observations** (28 base + 47 derived + 6 dashboard + 18 additional), the current canonical **single source of truth**. Consolidates the 2026-10-03 base/derived/dashboard build with the newly verified series Data06 (airport congestion), Data19 (platform rental share), Data20 (internet speed) and Data02/03 (EL62 bathing water).
- `composite-2026-10-20.json` - one transparent composite prototype (Tourism Pressure Index) with exposed formula, weights, units and polarity.
- `data24-protected-land.json` - the Data24 spatial-join audit (per-site overlap table + result), produced by `scripts/verification/compute-data24-protected-land.py`.
- `scheduled-port-traffic-el62.json` - Data07 master scheduled-timetable dataset (cruise calls + ferry baselines + port model + daily congestion scores), produced by `scripts/verification/compute-data07-anticipated-congestion.py`.
- `observations-data07-anticipated-congestion-2026-10-14.json` / `.csv` - **366 schema-compliant Data07 forecast observations** (one per EL62 port per day, 2026-10-01 → 2026-11-30; `temporal_granularity=forecast`, `spatial_ref.level=transport_node`). Kept separate: it is a forecast series, not an annual snapshot.
- `data19-platform-rental-share.json` - the Data19 audit (per-year platform vs conventional nights, share %, 2025 seasonality), produced by `scripts/verification/pull-data19-platform-rentals.py`.
- `observations-data19-platform-rental-share-2026-10-15.json` / `.csv` - **8 schema-compliant Data19 platform-rental-share observations** (one per year 2018-2025; `annual`, `NUTS2/EL62`, `unit=%`), merged into the master.
- `data06-airport-congestion.json` - the Data06 live approach-buffer audit (per-airport aircraft count, threshold, score), produced by `scripts/verification/pull-data06-airport-congestion.py`.
- `observations-data06-airport-congestion-2026-10-20.json` / `.csv` - **4 schema-compliant Data06 instant observations** (CFU/ZTH/EFL/PVK; `instant`, `transport_node`), merged into the master.
- `data20-internet-speed.json` - the Data20 spatial-join audit (fixed/mobile, regional + NUTS3 island breakdown), produced by `scripts/verification/compute-data20-internet-speed.py`.
- `observations-data20-internet-speed-2024Q3.json` / `.csv` - **4 schema-compliant Data20 observations** (fixed/mobile download & upload; `NUTS2/EL62`), merged into the master.
- `data02-bathing-water-el62-2024.json` - the Data02/03 EL62 spatial-join audit (regional counts + NUTS3 island breakdown), produced by `scripts/verification/pull-data02-bathing-water-el62.py`.
- `observations-data02-bathing-water-2024.json` / `.csv` - **2 schema-compliant EL62 Data02/Data03 observations** (2024; `annual`, `NUTS2/EL62`), merged into the master.

The earlier snapshot `observations-2026-10-03.json`/`.csv` and `composite-2026-10-03.json` are **superseded** by the 2026-10-20 build and retained only for traceability. The older `observations-2026-09-22`, `observations-2026-09-24`, `observations-2026-10-01` snapshots were **removed** (2026-10-02/03): the 09-24 file mislabeled Data29 seasonality as `NUTS2` with a country code (`EL`), which violated D-014; the 10-01 file was superseded by the 10-03 build (adds Data24 protected land %).

## Spatial consistency (D-014)

- `spatial_ref.level` is derived from the geo code: `EL` → `country`, `EL62` → `NUTS2`.
- NUTS 3 (EL621-624) is an internal disaggregation only: it is summed to NUTS2/EL62 and the formula applied before emitting a single regional observation (e.g. Data22 diversity = `1 − HHI` of island night shares).
- No observation is emitted at `NUTS3`; finer-than-NUTS2 levels appear only for operational indicators (`point`, `municipality`, `tourism_zone`, `beach`, `transport_node`, `poi`).

Current level distribution (99 observations): `NUTS2/EL62` (42) · `country/EL` (49) · `point` (4) · `transport_node` (4).

## How it is produced

`scripts/verification/build_dashboard.py` reads the verified samples + manifests, emits base observations, computes derived indicators (formulas recorded in `provenance.request_url`), builds the composite, and merges the standalone verified-series observation files (Data06/19/20/02-03). Regenerate after any pull:

```bash
python3 scripts/verification/build_dashboard.py \
  --manifest data/manifests/source-verification-2026-09-22.json \
  --manifest data/manifests/source-verification-2026-09-24.json \
  --manifest data/manifests/source-verification-2026-10-01.json \
  --manifest data/manifests/source-verification-2026-10-02.json \
  --manifest data/manifests/source-verification-2026-10-03.json
```

The standalone series merged into the master are produced separately (their raw fetches are live/large downloads, not base SDMX samples):

```bash
python3 scripts/verification/pull-data06-airport-congestion.py      # Data06 (OpenSky live)
python3 scripts/verification/pull-data19-platform-rentals.py        # Data19 (Eurostat tour_ce_omn12)
python3 scripts/verification/compute-data20-internet-speed.py       # Data20 (Ookla spatial join)
python3 scripts/verification/pull-data02-bathing-water-el62.py      # Data02/03 (EEA Discomap spatial join)
python3 scripts/verification/compute-data07-anticipated-congestion.py  # Data07 (forecast, separate)
```

## Scope & caveats

- Covers the **verified** no-key sources: Eurostat tourism (Data16/22/26/27/29/31/32/33), EEA bathing water (Data02/03), EEA Natura 2000 protected land (Data24), Open-Meteo weather/UV (Data13/14), OpenSky live aircraft (Data06), Ookla Open Data (Data20), Eurostat platform rentals (Data19), and derived indicators (Data22/24/29/30/32, plus Data02/03 percentages).
- `observed_at` is ISO 8601 with `temporal_granularity` (`annual`/`monthly`/`instant`); `ingested_at` is a UTC instant.
- Official statistics for geo `EL62` (Ionia Nisia, NUTS 2021) and Corfu (Open-Meteo point). Data02 bathing water is published both as a country-level Greece series (1990-2024) and, since 2026-10-20, as an EL62 spatial join for 2024. Data29 seasonality is country-level Greece only (no NUTS2 monthly publication); marked `country/EL`.
- Data20 is a 2024-Q3 quarterly aggregate; the observation schema has no `quarterly` granularity, so it is labeled `monthly` (period `2024-07-01` → `2024-09-30`). Open item: add `quarterly` to `temporal_granularity`.
- Unverified indicators are intentionally absent - no value is invented.
