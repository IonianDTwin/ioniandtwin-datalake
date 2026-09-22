# API Sources

`VERIFIED` The following API endpoints have passed bounded, read-only pull tests (2026-09-22). Full evidence in `docs/validation/api-verification-report.md` and `data/manifests/source-verification-2026-09-22.json`.

## Verified (no credentials)

| Source | Endpoint (template) | Auth | Feeds |
|---|---|---|---|
| Eurostat — nights (NUTS2) | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023` | none | Data16, 26, 29, 31, 33 |
| Eurostat — arrivals (NUTS2) | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023` | none | Data26 |
| Eurostat — capacity (NUTS2) | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023` | none | Data27 |
| Open-Meteo — weather + UV | `https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1` | none | Data13, 14 (substitute) |
| Copernicus CDSE catalogue | `https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$top=1&$format=json` | none (catalogue only) | Data01–03 (platform reachability) |

## Inaccessible without credentials (tested)

| Source | Likely access | Auth | Evidence |
|---|---|---|---|
| OpenWeatherMap | HTTPS API | API key | `VERIFIED` HTTP 401 with an invalid test key — a valid key is required |
| Copernicus CAMS / CMEMS data download | HTTPS API / ADS | registration token | catalogue reachable; download not tested (token required) |

## Unverified (proposal-only or paid)

| Source | Likely access | Auth | Notes |
|---|---|---|---|
| Meteo.gr | web/API | unknown | not pull-tested |
| Google Maps (Routes/Directions/Traffic) | HTTPS API | API key, paid | cost & ToS unverified |
| MarineTraffic | HTTPS API | API key, paid | ToS unverified |
| FlightRadar24 | HTTPS API | API key, paid | ToS unverified |
| TripAdvisor / Google Reviews | HTTPS API | API key | privacy-sensitive |
| Airbnb | API | API key | ToS unverified |

## Verification rules

- Read-only, bounded requests only.
- Record URL, method, params, status, content-type, checksum, evidence path.
- A failure is recorded as an access constraint, never as "source does not exist".

## Status

`VERIFIED` First no-key sources pull-tested. `BLOCKER` Credential-gated sources remain unverified until keys/registration are provided in the untracked `.env`.
