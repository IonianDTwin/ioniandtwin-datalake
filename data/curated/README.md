# data/curated — normalized observations

`DECISION` Clean, schema-aligned observations extracted from the verified pull samples, plus derived indicators and one composite prototype. This is the **publication-ready data file** for IonianDTwin.

## Files

- `observations-2026-09-24.json` / `.csv` — 34 schema-aligned observations (28 base + 6 derived): Eurostat tourism (Data16/26/27/29/31/32/33), Open-Meteo weather/UV (Data13/14), EEA bathing water (Data02/03), derived length-of-stay (Data30) and seasonality (Data29).
- `observations-2026-09-22.json` / `.csv` — the earlier 16-observation snapshot (kept for history).
- `composite-2026-09-24.json` — one transparent composite prototype (Tourism Pressure Index) with exposed formula, weights, units and polarity.

## How it is produced

`scripts/verification/build_dashboard.py` reads the verified samples + manifests, emits base observations, computes derived indicators (formulas recorded in `provenance.request_url`), and builds the composite. Regenerate after any pull:

```bash
python3 scripts/verification/build_dashboard.py \
  --manifest data/manifests/source-verification-2026-09-22.json \
  --manifest data/manifests/source-verification-2026-09-24.json
```

## Scope & caveats

- Covers only the **verified** no-key sources (Eurostat tourism, EEA bathing water, Open-Meteo weather/UV).
- `observed_at` is ISO 8601 with `temporal_granularity` (`annual`/`monthly`/`instant`); `ingested_at` is a UTC instant.
- Official statistics for geo `EL62` (Ionia Nisia, NUTS 2021) and Corfu (Open-Meteo point). Bathing water and Data29 seasonality are **country-level Greece** (no NUTS2 publication); noted in the data.
- Unverified indicators are intentionally absent — no value is invented.
