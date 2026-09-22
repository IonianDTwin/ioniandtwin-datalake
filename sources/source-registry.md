# Source Registry

`PROPOSAL` Candidate sources from the technical proposal, reconciled with the **deployed application's declared source registry**.

`VERIFIED` As of 2026-09-22, four no-key sources have passed live pull tests and one PDF has been downloaded: Eurostat tourism datasets (`tour_occ_nin2`, `tour_occ_arn2`, `tour_cap_nuts2`), Open-Meteo weather/UV (no-key substitute), Copernicus CDSE catalogue (platform reachability), and the GSTC Destination Criteria v2.0 PDF. See `source-verification-matrix.md`, `api-sources.md`, `pdf-and-document-sources.md`, and `docs/validation/api-verification-report.md`.

## Two evidence tiers

- `VERIFIED (app-declared)` — the live dashboard frontend names this source and its access route; this proves the project *references* it, not that backend integration is operational.
- `PROPOSAL (proposal-only)` — named in the technical proposal but **not** present in the deployed app's source list.

## Sources declared by the deployed application

| Source | Provider | Access (declared) | Feeds | Priority |
|---|---|---|---|---|
| Atmosphere data | Copernicus CAMS | API — CAMS Regional | air pollutants (PM2.5, coastal) | environmental (high) |
| Marine data | Copernicus CMEMS | Copernicus Marine Data Store | Chl-a, sea-surface, turbidity, slope | environmental (high) |
| Sentinel imagery | Copernicus Sentinel-1 (SAR) / Sentinel-2 (optical) | Copernicus Data Space | habitat, EO composite, land | environmental (high) |
| Meteorological data | OpenWeather | API | weather, UV | weather/UV (high) |
| EU Tourism Dashboard | Eurostat | Eurostat / CSV | tourism statistics, expenditure, employment | official tourism stats (high) |
| PeopleFlows | Ionian University | peopleflows.di.ionio.gr | pedestrian/visitor mobility flows | mobility |
| Traffic data | Google Maps Platform | API | road traffic | mobility |
| Maritime AIS data | MarineTraffic | API | vessel positions, ferries, cruise | mobility |
| Air Arrivals | FlightRadar24 | API | aviation flows | mobility |
| Citizen Reports | IonianDTwin (own) | Mobile app → backend | condition reports, photos, accessibility | participatory |
| Indoor collection stations (10) | IonianDTwin (own) | Local systems → cloud (MQTT / LoRaWAN) | indoor environmental sensors | environmental |

## Proposal-only candidates (absent from deployed app)

| Source | Note |
|---|---|
| Meteo.gr | `PROPOSAL`; not in the deployed app's list (OpenWeather is used instead) |
| Fraport | `PROPOSAL`; not in the deployed app |
| Local transport telematics (KTEL/urban) | `PROPOSAL`; not in the deployed app |
| Airbnb (short-term rentals) | `PROPOSAL`; not in the deployed app |
| TripAdvisor / Google Reviews | `PROPOSAL`; not in the deployed app (sentiment uses "Citizen Reports" instead) |

## Not data sources (excluded)

- OpenRouter / Opencode — LLM fallback APIs, not data sources.
- AirLLM / QWEN — local model runtimes.
- Copernicus CDSE / Marine Data Store — data-access platforms, not sources themselves.

## Status

`VERIFIED` Application source list extracted. `VERIFIED` First no-key sources (Eurostat, Open-Meteo, Copernicus CDSE catalogue) pull-tested; GSTC PDF downloaded. `BLOCKER` Credential-gated sources (OpenWeatherMap, CAMS/CMEMS download, Google Maps, MarineTraffic, FlightRadar24, Airbnb, review platforms) remain unverified — see `source-verification-matrix.md`.
