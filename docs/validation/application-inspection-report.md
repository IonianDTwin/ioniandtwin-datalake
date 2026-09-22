# Application Inspection Report

`VERIFIED` Inspection performed 2026-09-21T12:32Z (bounded, read-only, public requests).

## Targets

- `https://bold-matsumoto.213-158-90-162.plesk.page/#/indicators`
- `https://bold-matsumoto.213-158-90-162.plesk.page/#/resources/data-sources`

## Result

`VERIFIED` Both URLs resolve to a single public single-page application (SPA) served at the site root; the `#/…` fragments are client-side routes and are not separate server documents.

Evidence:

- Host resolves to `213.158.90.162`.
- `GET /robots.txt` → `404` (no robots.txt present).
- `GET /` → `200`, `content-type: text/html`, `content-length: 1552985`, `last-modified: Fri, 18 Sep 2026 15:52:09 GMT`.
- Retrieved document sha256 `445f8f176cb8fc7d175a0769848a29063eb69ccc897ad599875dc5c56e2d1806` (1552985 bytes).

## What the application is

`VERIFIED` IonianDTwin — a geospatial Digital Twin web dashboard (React + Leaflet + CARTO basemap, bilingual Greek/English). Document metadata: "IonianDTwin is a geospatial Digital Twin that continuously measures the sustainability of the Ionian Islands: ecosystems, water, energy, waste, biodiversity and cultural heritage. EU co-funded under the Ionian Islands 2021–2027 programme."

`VERIFIED` Project identifiers visible in the bundle: CORDIS project `101287315`, `OPS 6061866`, programme `Ionian Islands 2021–2027`, region `NUTS-2 · Ionian Islands`, beneficiary `Ionian University · ELKE-IP`.

## Useful content extracted (metadata-level only)

### Source registry (actual, deployed)

The bundle embeds the project's real data-source registry (name, type, what it provides, access route):

- Atmosphere data — Copernicus CAMS — `API — CAMS Regional`
- Marine data — Copernicus CMEMS — `Copernicus Marine Data Store`
- Sentinel imagery — Sentinel-1 (SAR) / Sentinel-2 (optical) — `Copernicus Data Space`
- Meteorological data — OpenWeather — `API`
- Traffic data — Google Maps Platform — `API`
- Maritime AIS data — MarineTraffic — `API`
- Air Arrivals — FlightRadar24 — `API`
- EU Tourism Dashboard — Eurostat — `Eurostat / CSV`
- PeopleFlows — mobility research — `peopleflows.di.ionio.gr`
- Citizen Reports — crowdsourced — `Mobile app → backend`
- Indoor collection stations (10) — IoT (MQTT / LoRaWAN) — `Local systems → cloud`

### Architecture

`VERIFIED` Named layers and technology: Data Collection / Sensor Layer ("ten indoor collection stations"), MQTT broker, LoRaWAN server, REST / API connectors, Copernicus CDSE.

### Map feature layers (POIs the twin models)

`VERIFIED` Beach Occupancy, Cruise & Ferries, Ferry Flow/Terminal, Marina Mooring, Port Terminal, Canal Transit, Caretta Habitat, Marine Habitat, Chl-a/Seawater, Slope & Turbidity, PM2.5/Coastal, Coastal Noise & UV, Air Arrivals, Aviation, Old Fortress Flow, Desalination Unit, Power Substation, Solar Array.

### GSTC alignment

`VERIFIED` GSTC Destination Criteria structured as four bilingual pillars (A–D), Pillar D = Environmental Sustainability ("air quality, water resources, marine environment, waste management and Natura habitat protection").

### References (citations)

`VERIFIED` Academic/press citations in the bundle: Springer (2025) `doi.org/10.1007/s40558-025-00338-y`, Research Square (2026) `doi.org/10.21203/rs.3.rs-9982997/v1`, arXiv (2026) `doi.org/10.48550/arxiv.2603.00079`, MDPI (2025) `mdpi.com/2673-4060/6/4/148`, plus press (`India Outbound`, `Travel and Tour World`) and standards (`GSTC-Destination-Criteria-v2.0-2022.pdf`, W3C WCAG).

## Caveats

- `RISK` The dashboard shows **simulated demo values** (e.g. "Twin synchronised · 12 s ago", "Sustainability index · good", AQI "41/100", "118%", "R² 0.38"). These are UI placeholders, **not** verified live data.
- `RISK` Source names/access routes are what the frontend declares; this proves the app *references* them, not that each backend integration is operational. Live pull tests are still required (see `docs/validation/api-verification-report.md`).
- `RISK` No credentials, API keys, or secret material were found; none are recorded here.

## Next diagnostic step

Run bounded, read-only pull tests against the declared access routes (Copernicus CDSE/CAMS/CMEMS, OpenWeather, Eurostat CSV), starting with weather/UV — see `docs/validation/api-verification-report.md`.
