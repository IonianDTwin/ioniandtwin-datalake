# Pull Workflow — 04 Climate Adaptation

**Category:** Climate Adaptation — `Κλιματική Προσαρμογή`
**Indicators:** Data13–Data15
**Pillar:** Environment

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data13 | Weather conditions (temp, rain, …) | OpenWeatherMap / Meteo.gr | api | API key / unknown | Open-Meteo `VERIFIED` (substitute) |
| Data14 | High UV and protection | OpenWeatherMap / Meteo.gr | api | API key / unknown | Open-Meteo `VERIFIED` (substitute) |
| Data15 | Air quality | CAMS / OpenWeatherMap / Meteo.gr | api | registration / key | UNVERIFIED (credential-gated) |

## Pull process

### Data13 / Data14 — Weather & UV

`VERIFIED` A no-key weather/UV endpoint is pull-tested (Open-Meteo), used as an interim substitute because OpenWeatherMap requires an API key and Meteo.gr is untested.

1. **Request** (Open-Meteo, no key):
   ```bash
   curl -sS "https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1"
   ```
   Reproducible script: `scripts/verification/pull-open-meteo.sh`.
2. **Store raw / manifest** — sample in `data/samples/open-meteo-corfu-forecast-2026-09-22.json`; checksum in `data/manifests/source-verification-2026-09-22.json`.
3. **Transform** — `current.temperature_2m` etc. → `Data13`; `daily.uv_index_max` → `Data14`.
4. **OpenWeatherMap** — `VERIFIED` HTTP 401 without a key. Add `OPENWEATHERMAP_API_KEY` to `.env` to use the proposal's named source.
5. **Meteo.gr** — `UNVERIFIED`; locate the official endpoint/terms before use.

### Data15 — Air quality

`DECISION` D-008 (confirmed 2026-09-24). Data15 = ambient air quality (Ποιότητα Αέρα). The corrected source removed the second "Data 15" — the AI indoor-activity suggestion — entirely; it survives only as prose (LLM visitor guidance), not as an indicator.

1. **Air quality** — pull from CAMS (registration token required) or local IoT; same recipe as Data01 (ambient NO2/PM/CO2 at a POI).
2. **AI indoor-activity proposal** — an LLM output derived from weather/UV/air-quality; not a source, not numbered.

## Notes & blockers

- `DECISION` Open-Meteo is a `PROPOSAL` substitute, not the proposal's named source; re-confirm before production.
- `BLOCKER` OpenWeatherMap needs a key; CAMS data download needs a registration token.
- `DECISION` D-008 (confirmed): Data15 is a single indicator (air quality); the AI indoor-activity item is an LLM feature, not a source.
