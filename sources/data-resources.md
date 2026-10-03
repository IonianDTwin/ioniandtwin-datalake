# Data resources - Data01-Data34

`DECISION` One list, one row of truth per indicator: the online source link, the Markdown procedure to follow for data access, and the ETL path. Machine-readable twin: `indicators/source-indicator-map.json`. Pull recipes: `sources/pull-workflow/`. Document extraction: `sources/procedures/`.

Legend - access procedure files:

- `WF/01` = `sources/pull-workflow/01-environmental-health.md` (and so on `WF/02`…`WF/10`)
- `PROC/download-extract.md` = `sources/procedures/download-extract.md` (public webpage/PDF/file)
- `API (script)` = `scripts/verification/pull-*.sh` (direct API pull)
- ETL shared references: `pipelines/ingestion-contracts.md`, `pipelines/quality-rules.md`, `schemas/observation-schema.json`, `scripts/verification/export_observations.py`

Status: `VERIFIED` (pull-tested) · `PARTIAL` (data present / access partially confirmed) · `UNVERIFIED` (source not yet reached) · `PROPOSAL` (derived / not yet a feed).

---

## Environmental Health & Pollutants - Περιβαλλοντική Υγεία & Ρύποι

### Data01 · Airport CO2 levels (Επίπεδα CO2 αεροδρομίων)
- Status: `PARTIAL` (CAMS access verified 2026-10-01; CO2 itself is not a CAMS regional variable)
- Source: Copernicus CAMS (regional air quality) + local IoT stations.
- Online source: https://ads.atmosphere.copernicus.eu/ (token: `CAMS_API_KEY`)
- Data access: `WF/01` + `API (cads-api-client)` - `cams-europe-air-quality-forecasts`, ensemble analysis.
- ETL: CAMS netCDF → extract pollutant at airport POI → observation `Data01`. Note: CAMS regional outputs CO/NO2/PM (µg/m³) at the surface, **not CO2**; CO2 is deferred to CAMS global GHG (coarse) or local IoT sensors. Use NO2/CO as airport-congestion/emissions proxies.

### Data02 · Excellent bathing waters (%) (Άριστα νερά κολύμβησης (%))
- Status: `VERIFIED` (EL62 level via EU Tourism Dashboard)
- Source: EEA WISE Bathing Water (Discodata SQL API) - authoritative; proposal also cites CMEMS/EU Tourism Dashboard.
- Online source: https://discodata.eea.europa.eu/sql · dataset page https://www.eea.europa.eu/data-and-maps/data/bathing-water-directive-status-of-bathing-water (datahub item `c3858959-90da-4c1b-b9ca-492db0e514df`) · dashboard export `2024_TourismDashboard_Indicators_Export.csv` (`TOUR_ENV_05`).
- Data access: `API` - table `[WISE_BWD].[latest].[assessment_BathingWaterStatus]` (quality since 1990).
- ETL: `VERIFIED` Greece 2024: Excellent 1677 / 1729 (96.99 %). **EL62 2023 = 98.82 %** from the dashboard (`TOUR_ENV_05`), which resolves the NUTS2 attribution without a `bathingWaterIdentifier` spatial join.

### Data03 · Clean beach water (reports) (Καθαρό νερό παραλίας)
- Status: `VERIFIED` (derived flag, country level)
- Source: EEA WISE BWD (derived) + citizen reports (app's own feed).
- Online source: https://discodata.eea.europa.eu/sql (reports are the app's own feed).
- Data access: `API` + internal user reports.
- ETL: water-quality class → clean-beach flag. `ASSUMPTION` "clean" = classified as Excellent/Good/Sufficient. Greece 2024: 99.94 % of classified waters meet this. Cross-verify reports vs EEA/CMEMS.

### Data04 · Blue Flags (Γαλάζιες Σημαίες)
- Status: `VERIFIED` (via EU Tourism Dashboard, 2026-10-03)
- Source: Blue Flag programme (FEE); proposal cites EU Tourism Dashboard.
- Online source: https://www.blueflag.global/ (interactive map, no machine-readable list) · dashboard export `2024_TourismDashboard_Indicators_Export.csv` (`TOUR_DES_10`).
- Data access: `download` (dashboard CSV).
- ETL: read the count directly. `VERIFIED` EL62 = **51 Blue Flag sites** (2024).

### Data05 · EMAS / EU Ecolabel (EMAS / EU Ecolabel)
- Status: `VERIFIED` (both registers pull-tested 2026-10-02)
- Source: EMAS register + EU Ecolabel catalogue (European Commission).
- Online source: EMAS register REST `https://webgate.ec.europa.eu/emas2/public/rest/registration/list` (HTTP 200, application/json); EU Ecolabel catalogue CSV `https://publicstorage.data.env.service.ec.europa.eu/ecolabel/exports/most-recent-export.csv` (HTTP 200, text/csv). Both discovered via `green-forum.ec.europa.eu/green-business/emas/emas-register_en` and `green-business.ec.europa.eu/eu-ecolabel_en`.
- Data access: `API` (EMAS REST list) + `download` (EU Ecolabel CSV export). No auth.
- ETL: register → count certified organisations per spatial unit → observation `Data05`.
- Verified values: EMAS 4,523 records / 27 countries, Greece 37, EL62 0; EU Ecolabel 89,298 licences, Greece 450 (tourist-accommodation group Greece 0). Evidence: `data/manifests/source-verification-2026-10-02.json`.

## Dynamic Congestion - Δυναμική Συμφόρηση

### Data06 · Airport congestion
- Status: `PARTIAL` (free live-flight source confirmed 2026-09-26)
- Source: OpenSky Network (free, no-key; D-011 substitute) · FlightRadar24 (paid, fallback).
- Online source: `https://opensky-network.org/api/states/all` (HTTP 200, application/json) · https://www.flightradar24.com/ (paid).
- Data access: `WF/02` - OpenSky anonymous REST (rate-limited, no key). Verified 2026-09-26: `GET …/api/states/all?lamin=37.0&lomin=19.0&lamax=40.5&lomax=22.0` returned live aircraft states over the Ionian Islands (Aegean/Wizz callsigns, positions).
- ETL: aircraft positions → count per airport buffer per window → congestion.

### Data07 · Port congestion
- Status: `PARTIAL` (free AIS candidates identified 2026-09-26)
- Source: aisstream.io (free crowd-sourced AIS WebSocket) · EMODnet Human Activities (free authoritative vessel-density) · MarineTraffic AIS (paid). OpenSky (Data06) covers aircraft only, not vessels.
- Online source: `https://aisstream.io/` (HTTP 200) · `https://emodnet.ec.europa.eu/en/human-activities` (HTTP 200) · https://www.marinetraffic.com/ (paid)
- Data access: `WF/02` - aisstream live stream (public stream, no key) or EMODnet vessel-density download; both free. AISHub remains paid/limited-tier.
- ETL: vessel positions/density → count in port buffer → congestion.

### Data08 · Road congestion
- Status: `UNVERIFIED` (no free live-traffic source; routing-only fallback identified 2026-09-26)
- Source: Google Maps Platform (paid, live traffic) · OpenRouteService (free tier, key - routing, not live congestion).
- Online source: https://mapsplatform.google.com/ (paid) · `https://openrouteservice.org/dev/#/signup` (HTTP 200, free tier ~500 req/day)
- Data access: `WF/02` - ORS free API key for routing/distance; no free live-traffic feed confirmed (TomTom/HERE/Google all paid).
- ETL: travel-time/delay per segment → congestion level (live) or ORS static routing as fallback.

### Data09 · Beach congestion
- Status: `UNVERIFIED`
- Source: citizen reports (own app).
- Online source: internal (mobile app → backend).
- Data access: `WF/02` - internal feed.
- ETL: cross-verify reports vs sensors → congestion flag.

### Data10 · City congestion
- Status: `UNVERIFIED`
- Source: Google Maps + citizen reports.
- Online source: https://mapsplatform.google.com/ (reports internal).
- Data access: `WF/02`.
- ETL: traffic layer + reports → zone congestion.

## Sustainable Transport - Βιώσιμες Μεταφορές

### Data11 · KTEL (bus) congestion
- Status: `UNVERIFIED`
- Source: local transport telematics (KTEL).
- Online source: internal/partner - no public link.
- Data access: `WF/03` - request feed from operator.
- ETL: occupancy/delay per route → congestion.

### Data12 · Urban transit congestion
- Status: `UNVERIFIED`
- Source: local transport telematics.
- Online source: internal/partner.
- Data access: `WF/03`.
- ETL: as Data11.

## Climate Adaptation - Κλιματική Προσαρμογή

### Data13 · Weather conditions (temp, rain, …)
- Status: `VERIFIED` (via Open-Meteo substitute)
- Source: OpenWeatherMap / Meteo.gr (proposal); Open-Meteo (no-key substitute, verified).
- Online source: https://openweathermap.org/ · https://www.meteo.gr/ · verified endpoint: `https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1`
- Data access: `WF/04` + `API (scripts/verification/pull-open-meteo.sh)`.
- ETL: flat JSON `current` block → observation `Data13`; ISO 8601 `observed_at`, point `spatial_ref`.

### Data14 · High UV and protection
- Status: `VERIFIED` (via Open-Meteo substitute)
- Source: OpenWeatherMap / Meteo.gr; Open-Meteo (verified).
- Online source: as Data13 (uses `daily.uv_index_max`).
- Data access: `WF/04` + `API (pull-open-meteo.sh)`.
- ETL: `daily.uv_index_max` → observation `Data14`.

### Data15 · Air quality (Ποιότητα Αέρα)
- Status: `VERIFIED` (CAMS ensemble analysis, 2026-10-01)
- Source: Copernicus CAMS (ambient air quality) + OpenWeatherMap / Meteo.gr.
- Online source: https://ads.atmosphere.copernicus.eu/ (token: `CAMS_API_KEY`)
- Data access: `WF/04` + `API (cads-api-client)` - `cams-europe-air-quality-forecasts`, ensemble, surface.
- ETL: AQ pollutant (NO2/PM10/PM2.5/CO, µg/m³) at a POI → observation `Data15`. `VERIFIED` sample 2026-09-30 (Corfu-airport grid point): NO2 5.80, PM10 7.40, PM2.5 5.51, CO 158.70 µg/m³. `DECISION` D-008 (confirmed): the AI indoor-activity suggestion was removed in the corrected source.

## Social Pressure & Infrastructure - Κοινωνική Πίεση & Υποδομές

### Data16 · Tourism intensity (nights/residents)
- Status: `VERIFIED`
- Source: Eurostat `tour_occ_nin2` (unit `P_THAB`).
- Online source: https://ec.europa.eu/eurostat · verified endpoint: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023`
- Data access: `WF/05` + `API (scripts/verification/pull-eurostat-tourism.sh)`.
- ETL: SDMX JSON → filter `c_resid=TOTAL, unit=P_THAB, nace_r2=I551-I553` → observation `Data16`.

### Data17 · Hospital / infrastructure congestion
- Status: `UNVERIFIED`
- Source: official announcements + citizen reports.
- Online source: internal/official channels (no single public link).
- Data access: `WF/05` - request/observe official feed.
- ETL: announcements/reports → congestion flag.

### Data18 · Power / water outage
- Status: `UNVERIFIED`
- Source: official announcements + citizen reports.
- Online source: internal/official channels.
- Data access: `WF/05`.
- ETL: outage reports → status flag.

### Data19 · Short-term rental share (Airbnb)
- Status: `PARTIAL` (free candidate identified, data path unconfirmed 2026-09-26)
- Source: InsideAirbnb (free scrape-derived listings) · EU Tourism Dashboard; Airbnb has no public API.
- Online source: `https://insideairbnb.com/get-the-data/` (HTTP 200) · `https://data.insideairbnb.com/greece/` (HTTP 200 but `content-length: 0`; Greece region/date keys still to resolve - a guessed Athens key returned HTTP 403).
- Data access: `WF/05` - resolve InsideAirbnb Greece region keys (Ionian Islands coverage TBD) or dashboard export.
- ETL: rental listings share → observation `Data19`.

## Digital Infrastructure - Ψηφιακή Υποδομή

### Data20 · Internet speed (>100 Mb/s)
- Status: `VERIFIED` (pulled 2026-10-01)
- Source: Ookla Open Data (free, no key; D-011 substitute) · citizen reports (own app).
- Online source: `https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=fixed/year=2024/quarter=3/2024-07-01_performance_fixed_tiles.zip` (HTTP 200, ~251 MB) · registry `https://registry.opendata.aws/speedtest-global-performance/`.
- Data access: `WF/06` - S3 shapefile download + geopandas bbox filter to the Ionian Islands.
- ETL: `VERIFIED` 2024-Q3 fixed broadband, Ionian bbox (9,209 tiles): mean **39.1 Mbps** · median **26.8 Mbps** · max 926.6 Mbps (123,119 tests, 47,113 devices).

### Data21 · 4G/5G availability
- Status: `UNVERIFIED`
- Source: citizen reports.
- Online source: internal.
- Data access: `WF/06`.
- ETL: coverage reports → availability flag.

## Spatial Sustainability - Χωροταξική Αειφορία

### Data22 · Tourist diversity (zones)
- Status: `VERIFIED` (derived 2026-10-01; definition **adopted provisional** 2026-10-03: `1 − HHI` of island nights shares)
- Source: Eurostat `tour_occ_nin3` (NUTS3 nights) - the EU Tourism Dashboard is a front-end over the same Eurostat API + GISCO geometry.
- Online source: https://ec.europa.eu/eurostat
- Data access: `WF/07` + `API` - NUTS3 nights for EL621-EL624.
- ETL: `1 − HHI` of island nights shares (Herfindahl-Hirschman Index). `VERIFIED` 2021-2025: diversity **0.636 → 0.651 → 0.632 → 0.631 → 0.640** (Kerkyra ≈48-51 % of nights, Zakynthos ≈30-33 %, Ithaki-Kefallinia ≈9-11 %, Lefkada ≈8-10 %). Open question: spatial spread vs accommodation-type mix vs visitor-origin mix.

### Data23 · Density of cultural elements
- Status: `VERIFIED` (via EU Tourism Dashboard, 2026-10-03)
- Source: EU Tourism Dashboard "Cultural assets density" (`TOUR_DES_14`).
- Online source: https://tourism-dashboard.ec.europa.eu/ · dashboard export `2024_TourismDashboard_Indicators_Export.csv`.
- Data access: `download` (dashboard CSV).
- ETL: read the value directly. `VERIFIED` EL62 = **9.07 cultural assets / 100 km²** (2023).

### Data24 · Protected land (%)
- Status: `VERIFIED` (2026-10-03, spatial join complete)
- Source: EU Tourism Dashboard maps; Natura 2000 / EEA (authoritative) + Eurostat GISCO NUTS 2021 boundary.
- Online source: EEA ArcGIS REST `https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer` (HTTP 200, no key; 3 polygon layers - Habitats, Birds, union). Eurostat GISCO NUTS 2021 `NUTS_RG_01M_2021_3035_LEVL_2.geojson`. CDDA/NatDA services under the same `ProtectedSites` folder also reachable.
- Data access: `API` - ArcGIS REST query (`where=MS='GR' AND SITECODE IN (…)` over the EL62-envelope-intersecting superset, `returnGeometry=true`, `outSR=4326`, `f=geojson`). Boundary: GISCO GeoJSON filtered to `NUTS_ID == EL62`.
- ETL: reproject to EPSG:3035 (LAEA equal-area); intersect each site with the EL62 **land** polygon (this is the terrestrial/marine split - marine sites contribute only their coastal footprint); union Habitats ∪ Birds; `% = union.area ÷ EL62.area × 100`. Script: `scripts/verification/compute-data24-protected-land.py`.
- Result: **EL62 protected land = 386.41 km² of 2,304.87 km² = 16.76 %** (Habitats 220.49 km² · Birds 297.44 km² · union 386.41 km²). EL62 area delta vs published 2,307 km² = −0.09 % (1:1M generalisation).
- Completeness note: the Echinades/Petalas islets (Eurostat GISCO NUTS 2021: EL623 "Ithaki, Kefallinia" ⊂ EL62 "Ionia Nisia") are protected via the GR23-coded Acheloos-delta site (1,608 ha) - a GR22-only filter would miss them, so the envelope-superset + polygon clip is the correct method.
- Evidence: `data/curated/data24-protected-land.json` (per-site audit) + `data/manifests/source-verification-2026-10-03.json`; raw geometry `data/raw/eea-natura2000-el62-envelope-*.geojson`, `data/raw/gisco-nuts-2021-3035-EL62.geojson`.

### Data25 · Accommodation in high-value areas
- Status: `VERIFIED` (2026-10-03 - resolved from the EU Tourism Dashboard)
- Source: EU Tourism Dashboard - "Share of accommodations in areas with high-nature value" (code `TOUR_DES_13`); the proposal's own source.
- Online source: https://tourism-dashboard.ec.europa.eu/ · data.europa.eu dataset `9564824a-7f16-4efa-82fb-d4e176350026` · CSV `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/TOURISM/2024/LATEST/2024_TourismDashboard_Indicators_Export.csv`
- Data access: `WF/07` + download (CSV).
- ETL: no overlay needed - read the value directly. `VERIFIED` EL62 = **43 %** (2023); NUTS3: Zakynthos 59 % · Kerkyra 34 % · Ithaki-Kefallinia 34 % · Lefkada 57 %. Greece = 32 %.
- Flag: the exact operationalisation of "high-nature value" (which areas count) is in the dashboard's methodology - to pin down; the earlier proposed Natura 2000 ∪ coastal default is superseded.
- Evidence: `data/manifests/source-verification-2026-10-03.json`, `data/samples/eutd-tourism-dashboard-2024-ionian.json`.

## Tourism Performance - Τουριστική Απόδοση

### Data26 · Arrivals & overnight stays
- Status: `VERIFIED`
- Source: Eurostat `tour_occ_nin2` (nights) + `tour_occ_arn2` (arrivals).
- Online source: https://ec.europa.eu/eurostat · verified endpoints: `…/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023` and `…/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023`
- Data access: `WF/08` + `API (pull-eurostat-tourism.sh)`.
- ETL: `c_resid=TOTAL, unit=NR, nace_r2=I551-I553` → observations (nights + arrivals).

### Data27 · Tourism capacity (beds)
- Status: `VERIFIED`
- Source: Eurostat `tour_cap_nuts2` (bed-places).
- Online source: https://ec.europa.eu/eurostat · verified endpoint: `…/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023`
- Data access: `WF/08` + `API (pull-eurostat-tourism.sh)`.
- ETL: `accomunit=BEDPL, unit=NR, nace_r2=I551-I553` → observation `Data27`.

### Data28 · Occupancy rate (%)
- Status: `VERIFIED` (via EU Tourism Dashboard, 2026-10-03)
- Source: EU Tourism Dashboard "Occupancy rate" (`TOUR_DES_04`) - Eurostat underlying.
- Online source: https://tourism-dashboard.ec.europa.eu/ · dashboard export `2024_TourismDashboard_Indicators_Export.csv`.
- Data access: `download` (dashboard CSV).
- ETL: read the value directly. `VERIFIED` EL62 = **65.4 % net occupancy** (2023). Note: this is the standard *net* rate (nights ÷ beds×open-days); the earlier gross derivation (nights ÷ beds×365 ≈ 28-36 %) is superseded.

### Data29 · Seasonality (%)
- Status: `VERIFIED` (via EU Tourism Dashboard, 2026-10-03)
- Source: EU Tourism Dashboard "Tourism seasonality" (`TOUR_SOE_02`) - Eurostat underlying.
- Online source: https://tourism-dashboard.ec.europa.eu/ · dashboard export `2024_TourismDashboard_Indicators_Export.csv`.
- Data access: `download` (dashboard CSV).
- ETL: read the value directly. `VERIFIED` EL62 = **71.08 % peak-season share** (2023). Flag: exact month window (Jun-Sep vs Jul-Aug) to be confirmed from the dashboard methodology. Supersedes the country-level peak-month proxy (21.53 %).

### Data30 · Average length of stay
- Status: `VERIFIED` (formula **confirmed** 2026-10-03: `nights ÷ arrivals`)
- Source: derived from Eurostat Data26 (nights ÷ arrivals); booking services as secondary.
- Online source: https://ec.europa.eu/eurostat
- Data access: `WF/08` - derive from Data26.
- ETL: `nights ÷ arrivals` (5.93 in 2022 → 5.58 in 2025) → observation `Data30`.

## Density & Typology - Πυκνότητα & Τυπολογία

### Data31 · Tourism density (nights/km²)
- Status: `VERIFIED`
- Source: Eurostat `tour_occ_nin2` (unit `P_KM2`).
- Online source: https://ec.europa.eu/eurostat · verified endpoint: `…/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023`
- Data access: `WF/09` + `API (pull-eurostat-tourism.sh)`.
- ETL: `c_resid=TOTAL, unit=P_KM2, nace_r2=I551-I553` → observation `Data31`.

### Data32 · Dominant tourism typology
- Status: `VERIFIED` (rule **adopted provisional** 2026-10-03: dominant = highest nights share → hotels)
- Source: Eurostat `tour_occ_nin2` (`nace_r2` breakdown) - **data already pulled**.
- Online source: https://ec.europa.eu/eurostat · endpoint as Data31.
- Data access: `WF/09` - no new pull needed; the classification rule is adopted.
- ETL: `nace_r2` shares (hotels ≈73%/70%, short-stay ≈26%/30%, camping <1%) → dominant type (hotels). Open question: nights vs bed-places vs arrivals basis.

### Data33 · Foreign tourist share (%)
- Status: `VERIFIED`
- Source: Eurostat `tour_occ_nin2` (`c_resid=FOR`, unit `PC_TOT`).
- Online source: https://ec.europa.eu/eurostat · endpoint as Data31.
- Data access: `WF/09` + `API (pull-eurostat-tourism.sh)`.
- ETL: `c_resid=FOR, unit=PC_TOT, nace_r2=I551-I553` → observation `Data33`.

## Participation - Συμμετοχικότητα

### Data34 · User feedback
- Status: `UNVERIFIED`
- Source: TripAdvisor / Google Reviews (paid, privacy-sensitive) + EU Tourism Dashboard.
- Online source: https://www.tripadvisor.com/ (reviews via API/platform).
- Data access: `WF/10` - feasibility track; citizen reports are the app's own feed.
- ETL: sentiment (local-first LLM) over reviews/reports → satisfaction indicator.
