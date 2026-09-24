# Ingestion Contracts

`VERIFIED` Two contracts are now finalised (Eurostat tourism, EEA bathing water). The template below remains for the remaining sources. No production ingestion runs yet (D-002); these contracts are the reference the future jobs will implement.

## Contract template (per source)

- `source_id` — references `sources/source-registry.md`.
- `endpoint` / `request` — exact method, params, headers.
- `schedule` — ~30-minute cron for asynchronous sources; real-time for mobile reports; annual/monthly for official statistics.
- `auth` — credential reference only (real values in `.env`), or `none`.
- `response_shape` — observed schema notes (from the verification manifest).
- `idempotency` — deduplication key.
- `retention` — raw immutability (checksum + manifest) and retention policy.
- `failure_mode` — recorded as an access constraint, never as "source absent".

---

## Finalised contract — Eurostat tourism statistics

- **source_id**: `Eurostat_tour_occ_nin2` / `tour_occ_arn2` / `tour_cap_nuts2` / `tour_occ_nim` (official tourism statistics).
- **endpoint**: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<dataset>?format=JSON&geo=EL62&time=<years>` (annual NUTS2) and `…/tour_occ_nim?format=JSON&geo=EL&freq=M&…&time=<months>` (monthly country).
- **method**: `GET`; `format=JSON`; no headers, no credentials.
- **schedule**: annual datasets refresh after Eurostat's annual release; monthly after each month's release; polled no more than daily.
- **auth**: none.
- **response_shape**: SDMX 2.1 JSON — `value` map indexed by dimension position; dims `freq, c_resid, unit, nace_r2, geo, time` (annual NUTS2) and `freq, c_resid, unit, nace_r2, geo, time` with `time=YYYY-MM` (monthly). Monthly `time` codes use `YYYY-MM` (not `YYYYM01`).
- **idempotency**: `observation_id = <dataset>:<indicator_id>:<series_label>:<time>`.
- **retention**: raw JSON to `data/samples/` with `sha256`; evidence entry in `data/manifests/source-verification-YYYY-MM-DD.json`.
- **failure_mode**: an HTTP error or empty set (e.g. NUTS2 monthly) is an access constraint, not "source absent".
- **indicators**: Data16/Data26/Data27/Data30 (derived)/Data31/Data32/Data33 (annual NUTS2), Data29 seasonality (monthly country).

## Finalised contract — EEA bathing water (WISE BWD, Discodata SQL)

- **source_id**: `EEA_WISE_BWD_assessment`.
- **endpoint**: `https://discodata.eea.europa.eu/sql` — `GET` with a URL-encoded `query` (T-SQL dialect: `TOP`, not `LIMIT`).
- **method**: `GET`; `query=SELECT quality, COUNT(*) … FROM [WISE_BWD].[latest].[assessment_BathingWaterStatus] WHERE countryCode='EL' AND season=<year> GROUP BY quality`.
- **schedule**: seasonal — poll after each bathing season's assessment release (annual).
- **auth**: none.
- **response_shape**: `{"results":[{countryCode, bathingWaterIdentifier, specialisedZoneType, season, quality, …}]}`; quality ∈ `1 - Excellent` … `4 - Poor`, `0 - Not classified`.
- **idempotency**: `observation_id = EEA_WISE_BWD:<indicator_id>:<series_label>:<season>`.
- **retention**: raw JSON to `data/samples/` with `sha256`; manifest entry.
- **failure_mode**: empty `results` = no data for that season, not "source absent".
- **indicators**: Data02 (% Excellent), Data03 (clean-beach flag, derived).
- **known limitation**: country-level only in this table; NUTS2 (EL62) attribution needs a spatial join on `bathingWaterIdentifier`.

## Priority contracts (remaining, not finalised)

1. Weather/UV — Open-Meteo `VERIFIED` substitute; OpenWeatherMap/Meteo.gr pending keys/terms.
2. Copernicus CAMS / CMEMS — registration token required.
3. Blue Flag (FEE), EMAS/EU Ecolabel, Natura 2000/CDDA — URLs partially confirmed; export/download URLs to confirm.

## Status

`VERIFIED` Two contracts finalised (Eurostat, EEA). Remaining sources stay `BLOCKER` until their access is confirmed (keys/registration or export URLs).
