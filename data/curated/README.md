# data/curated - normalized observations

`DECISION` Clean, schema-aligned observations extracted from the verified pull samples, plus derived indicators and one composite prototype. This is the **publication-ready data file** for IonianDTwin.

## Files

- `observations-2026-10-03.json` / `.csv` - **81 schema-aligned observations** (28 base + 47 derived + 6 dashboard-sourced), the current canonical dataset.
- `composite-2026-10-03.json` - one transparent composite prototype (Tourism Pressure Index) with exposed formula, weights, units and polarity.
- `data24-protected-land.json` - the Data24 spatial-join audit (per-site overlap table + result), produced by `scripts/verification/compute-data24-protected-land.py`.

Earlier snapshots (`observations-2026-09-22`, `observations-2026-09-24`, `observations-2026-10-01`) were **removed** (2026-10-02/03): the 09-24 file mislabeled Data29 seasonality as `NUTS2` with a country code (`EL`), which violated D-014; the 10-01 file was superseded by the 10-03 build (adds Data24 protected land %).

## Spatial consistency (D-014)

- `spatial_ref.level` is derived from the geo code: `EL` → `country`, `EL62` → `NUTS2`.
- NUTS 3 (EL621-624) is an internal disaggregation only: it is summed to NUTS2/EL62 and the formula applied before emitting a single regional observation (e.g. Data22 diversity = `1 − HHI` of island night shares).
- No observation is emitted at `NUTS3`; finer-than-NUTS2 levels appear only for operational indicators (`point`, `municipality`, `tourism_zone`, `beach`, `transport_node`, `poi`).

Current level distribution: `NUTS2/EL62` (22) · `country/EL` (15) · `point` (4).

## How it is produced

`scripts/verification/build_dashboard.py` reads the verified samples + manifests, emits base observations, computes derived indicators (formulas recorded in `provenance.request_url`), and builds the composite. Regenerate after any pull:

```bash
python3 scripts/verification/build_dashboard.py \
  --manifest data/manifests/source-verification-2026-09-22.json \
  --manifest data/manifests/source-verification-2026-09-24.json \
  --manifest data/manifests/source-verification-2026-10-01.json \
  --manifest data/manifests/source-verification-2026-10-02.json \
  --manifest data/manifests/source-verification-2026-10-03.json
```

## Scope & caveats

- Covers the **verified** no-key sources: Eurostat tourism (Data16/22/26/27/29/31/32/33), EEA bathing water (Data02/03), EEA Natura 2000 protected land (Data24), Open-Meteo weather/UV (Data13/14), and derived indicators (Data22/24/29/30/32, plus Data02/03 percentages).
- `observed_at` is ISO 8601 with `temporal_granularity` (`annual`/`monthly`/`instant`); `ingested_at` is a UTC instant.
- Official statistics for geo `EL62` (Ionia Nisia, NUTS 2021) and Corfu (Open-Meteo point). Bathing water and Data29 seasonality are **country-level Greece** (no NUTS2 publication); noted in the data and marked `country/EL`.
- Unverified indicators are intentionally absent - no value is invented.
