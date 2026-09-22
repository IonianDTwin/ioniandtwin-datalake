# Source Verification Matrix

`VERIFIED` Verification state updated after live pull tests on 2026-09-22T11:27Z. Evidence: `data/manifests/source-verification-2026-09-22.json`.

## Status legend

- `UNVERIFIED` — listed but not tested.
- `APP-DECLARED` — the deployed frontend names the source and access route (not pull-tested).
- `VERIFIED` — pull-tested with recorded evidence (status, content-type, checksum).
- `PARTIAL` — accessible but schema/terms not fully established (e.g. platform reachable, data download gated).
- `INACCESSIBLE` — tested and blocked (recorded error), e.g. missing credentials.
- `DEPRECATED` / `HYPOTHETICAL` — retired or speculative.

## Matrix

| Source | Provider | Access | Auth | Status | Evidence |
|---|---|---|---|---|---|
| Eurostat `tour_occ_nin2` (nights, NUTS2) | Eurostat/EC | SDMX 2.1 REST API | none | **VERIFIED** | HTTP 200; manifest 2026-09-22 |
| Eurostat `tour_occ_arn2` (arrivals, NUTS2) | Eurostat/EC | SDMX 2.1 REST API | none | **VERIFIED** | HTTP 200; manifest 2026-09-22 |
| Eurostat `tour_cap_nuts2` (bed-places, NUTS2) | Eurostat/EC | SDMX 2.1 REST API | none | **VERIFIED** | HTTP 200; manifest 2026-09-22 |
| Open-Meteo (weather + UV) | Open-Meteo | HTTPS API | none | **VERIFIED** | HTTP 200; `PROPOSAL` substitute |
| OpenWeatherMap | OpenWeatherMap | HTTPS API | API key | **INACCESSIBLE** | HTTP 401 (needs key) |
| Copernicus CDSE catalogue | EU | HTTPS OData | none (catalogue) | **PARTIAL** | HTTP 200; download gated by token |
| GSTC Destination Criteria v2.0 | GSTC | PDF download | none | **VERIFIED** | HTTP 200; 18-page PDF; sha256 recorded |
| Copernicus CAMS | ECMWF/EU | API — CAMS Regional | registration | APP-DECLARED | app bundle 2026-09-21 |
| Copernicus CMEMS | EU | Copernicus Marine Data Store | registration | APP-DECLARED | app bundle |
| Copernicus Sentinel-1/2 | EU | Copernicus Data Space | registration | APP-DECLARED | app bundle |
| EU Tourism Dashboard | Eurostat/EC | Eurostat / CSV | none | APP-DECLARED | Eurostat API now `VERIFIED` (same backend) |
| PeopleFlows | Ionian University | peopleflows.di.ionio.gr | unknown | APP-DECLARED | app bundle |
| Google Maps Platform | Google | API | API key (paid) | APP-DECLARED | app bundle |
| MarineTraffic | MarineTraffic | API | API key (paid) | APP-DECLARED | app bundle |
| FlightRadar24 | FlightRadar24 | API | API key (paid) | APP-DECLARED | app bundle |
| Citizen Reports | IonianDTwin (own) | Mobile app → backend | app | APP-DECLARED | app bundle |
| Indoor IoT stations (10) | IonianDTwin (own) | MQTT / LoRaWAN → cloud | partner | APP-DECLARED | app bundle |
| Meteo.gr | EMY | web/API | unknown | UNVERIFIED (proposal-only) | — |
| Fraport | Fraport Greece | web/data | unknown | UNVERIFIED (proposal-only) | — |
| Local transport telematics | KTEL/urban | internal | partner | UNVERIFIED (proposal-only) | — |
| Airbnb | Airbnb | API | API key | UNVERIFIED (proposal-only) | — |
| TripAdvisor / Google Reviews | respective | API | API key | UNVERIFIED (proposal-only) | — |

## Verified sample values (EL62 = Ionia Nisia)

- Nights spent: 2022 = 16,512,634 · 2023 = 19,762,799
- Arrivals: 2022 = 2,785,360 · 2023 = 3,332,407
- Bed-places: 2022 = 159,790 · 2023 = 155,968
- Tourism intensity (nights/1000 residents): 2022 = 80,912.16 · 2023 = 97,705.53
- Tourism density (nights/km²): 2022 = 7,176.29 · 2023 = 8,588.79
- Foreign tourist share: 2022 = 93.72 % · 2023 = 93.58 %

## Application inspection evidence (carried forward)

- `GET /` → 200, `text/html`, 1,552,985 bytes, sha256 `445f8f176cb8fc7d175a0769848a29063eb69ccc897ad599875dc5c56e2d1806`.
- `GET /robots.txt` → 404.
- Accessed 2026-09-21T12:32Z. Full report in `docs/validation/application-inspection-report.md`.

## Status

`VERIFIED` Official tourism statistics and a weather/UV substitute now pull-tested. `BLOCKER` Credential-gated sources (OpenWeatherMap, CAMS/CMEMS download, Google Maps, MarineTraffic, FlightRadar24, Airbnb, review platforms) remain unverified pending keys/registration.
