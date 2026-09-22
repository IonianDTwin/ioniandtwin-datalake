# data/curated — normalized observations

`DECISION` Clean, schema-aligned observations extracted from the verified pull samples. This is the **publication-ready data file** for IonianDTwin.

## Files

- `observations-2026-09-22.json` — 16 verified observations, aligned with `schemas/observation-schema.json`. Each record carries `indicator_id` (Data13/14/16/26/27/31/33), `source_id`, `observed_at`, `ingested_at`, `spatial_ref`, `value`, `unit`, and `provenance` (raw checksum + request URL).
- `observations-2026-09-22.csv` — the same data flattened for spreadsheets/human reading.

## How it is produced

`scripts/verification/export_observations.py` reads the source-indicator map and the manifest, then emits one record per matched data point from the samples. Regenerate after any pull:

```bash
python3 scripts/verification/export_observations.py \
  --manifest data/manifests/source-verification-2026-09-22.json
```

## Scope & caveats

- Covers only the **verified** no-key sources pulled on 2026-09-22 (Eurostat tourism, Open-Meteo weather/UV).
- `observed_at` uses the source's own granularity: annual (`2022`, `2023`) for Eurostat, timestamp/date for Open-Meteo.
- Values are official public statistics for geo `EL62` (Ionia Nisia, NUTS 2021) and Corfu (Open-Meteo point). No personal data.
- Unverified indicators (Data01–12, 15, 17–25, 28–30, 34) are intentionally absent — no value is invented.
