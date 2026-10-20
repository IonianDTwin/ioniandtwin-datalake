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
- Status: `VERIFIED` (EL62 spatial join complete 2026-10-20)
- Source: EEA WISE Bathing Water (Discomap ArcGIS MapServer layer 3 & Discodata SQL API) - authoritative; proposal also cites CMEMS/EU Tourism Dashboard.
- Online source: `https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2024/MapServer/3` · https://discodata.eea.europa.eu/sql · dashboard export `2024_TourismDashboard_Indicators_Export.csv` (`TOUR_ENV_05`).
- Data access: `API` - ArcGIS REST GeoJSON query (`pull-data02-bathing-water-el62.py`).
- ETL: `VERIFIED` Greece 2024: Excellent 1,677 / 1,729 (96.99 %). **EL62 2024 spatial join:** 173 monitoring points within 3km of EL62 coast, 171 classified, **170 Excellent = 99.42 % of classified (98.27 % of total)**. NUTS3 breakdown: Zakynthos 32/32 (100%), Kefalonia/Ithaki 45/45 (100%), Lefkada 21/21 (100%), Corfu 72/73 (98.63%). 2023 baseline from dashboard was 98.82%. Evidence: `data/manifests/source-verification-2026-10-20.json`, `data/curated/data02-bathing-water-el62-2024.json`.

### Data03 · Clean beach water (reports) (Καθαρό νερό παραλίας)
- Status: `VERIFIED` (EL62 spatial join complete 2026-10-20)
- Source: EEA WISE BWD (derived) + citizen reports (app's own feed).
- Online source: `https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2024/MapServer/3` · Discodata SQL.
- Data access: `API` + internal user reports.
- ETL: `VERIFIED` EL62 2024: 171 / 171 classified waters rated Excellent or Good = **100.0 %** clean waters (zero Poor or Sufficient waters). Evidence: `data/manifests/source-verification-2026-10-20.json`.

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
- Status: `VERIFIED` (approach-buffer scoring implemented 2026-10-20)
- Source: OpenSky Network (free, no-key; D-011 substitute) · FlightRadar24 (paid, fallback).
- Online source: `https://opensky-network.org/api/states/all` (HTTP 200, application/json) · https://www.flightradar24.com/ (paid).
- Data access: `WF/02` - OpenSky anonymous REST (rate-limited, no key). Live endpoint `GET …/api/states/all?lamin=37.0&lomin=19.0&lamax=40.5&lomax=22.0`.
- ETL: `scripts/verification/pull-data06-airport-congestion.py` — filter aircraft states to 25 km buffer around CFU, ZTH, EFL, PVK with altitude $\le 3,000$ m (or on ground); compute score $S = \min(1.0, \text{count} / \text{threshold})$. Emits `data/curated/data06-airport-congestion.json` and `observations-data06-airport-congestion-*.json` / `.csv`. Evidence: `data/manifests/source-verification-2026-10-20.json`.

### Data07 · Port congestion
- Status: `PROPOSAL` (anticipated schedule-based congestion, 2026-10-14; live AIS superseded)
- Source (model): CruiseMapper cruise schedules (one-time read) + Greek National Access Point sailing-traffic export (`scratch/ais-routes/export_sailing_traffic.csv`, Mar–Nov 2025). Superseded live candidates: aisstream.io (crowd-sourced AIS), EMODnet Human Activities (vessel density), MarineTraffic AIS (paid).
- Online source: CruiseMapper `https://www.cruisemapper.com/ports/<slug>?month=<yyyy-mm>` (browser-UA only, no API; one-time read) · Greek NAP sailing-traffic export.
- Production feed (**unverified**): the Corfu Port Authority OLKE (`corfuport.gr`) berth-declaration feed is the intended replacement for the CruiseMapper read — verify its format, update cadence, port/vessel coverage, access terms and whether it carries per-call PAX + arrival/departure before use. Non-Corfu ferry operator timetables are likewise unverified. *(progress §3 "Source verification")*
- Data access: `download` (NAP CSV) + one-time CruiseMapper schedule read (`scratch/cruise-pressure/schedules.json`). No auth.
- ETL: `scripts/verification/compute-data07-anticipated-congestion.py` — aggregate inbound ferry legs by arrival port (month + day-of-week averages) + count planned cruise calls → `S(P,D)=min(1, 0.4·N_ships/B_max + 0.4·(L_cruise+L_ferry_pax)/C_pax + 0.2·L_ferry_veh/C_veh)` → low/medium/high. Outputs `data/curated/scheduled-port-traffic-el62.json` + `observations-data07-anticipated-congestion-*.json` / `.csv`.

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
- Status: `VERIFIED` (2026-10-15, via Eurostat `tour_ce_omn12`; InsideAirbnb superseded)
- Source: Eurostat `tour_ce_omn12` (short-stay accommodation offered via online platforms — EC data-sharing agreement with Airbnb, Booking.com, Expedia, Tripadvisor) ÷ Eurostat `tour_occ_nin2` (conventional nights). Airbnb has no public API; InsideAirbnb has no Ionian Islands coverage.
- Online source: verified endpoint `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_ce_omn12?geo=EL62&indic_to=NGT_SP&c_resid=TOTAL&month=TOTAL&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023&time=2024&time=2025&lang=en` (HTTP 200, application/json, no key); denominator `…/tour_occ_nin2?geo=EL62&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2018&…&time=2025`.
- Data access: `API (scripts/verification/pull-data19-platform-rentals.py)`. No auth.
- ETL: `NGT_SP` (platform guest nights) ÷ (conventional `tour_occ_nin2` nights + platform nights) × 100 → observation `Data19`. `VERIFIED` 2018–2025 share %: **14.50 / 15.88 / 22.08 / 23.02 / 24.02 / 23.50 / 17.65 / 29.80**. 2025 monthly: Jul 2,182,817 · Aug 2,348,265 (Jul+Aug = 52.4 % of annual). FLAG: 2025 platform nights +96 % vs 2024 (likely platform-coverage/onboarding change; re-verify against the next release). Evidence: `data/manifests/source-verification-2026-10-15.json`, `data/curated/data19-platform-rental-share.json`.

## Digital Infrastructure - Ψηφιακή Υποδομή

### Data20 · Internet speed (>100 Mb/s)
- Status: `VERIFIED` (spatial join to GISCO EL62 boundary 2026-10-20)
- Source: Ookla Open Data (free, no key; D-011 substitute) · citizen reports (own app).
- Online source: `https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=fixed/year=2024/quarter=3/2024-07-01_performance_fixed_tiles.zip` (HTTP 200, ~251 MB) and `…/type=mobile/year=2024/quarter=3/2024-07-01_performance_mobile_tiles.zip` (HTTP 200, ~138 MB).
- Data access: `WF/06` - S3 shapefile downloads + `scripts/verification/compute-data20-internet-speed.py` spatial join to Eurostat GISCO NUTS2 EL62 polygon.
- ETL: `VERIFIED` 2024-Q3 performance:
  - **Fixed broadband (EL62):** test-weighted mean download **42.29 Mbps** · upload **9.55 Mbps** · latency **49.6 ms** (2,795 tiles, 41,552 tests, 18,089 devices). Island breakdown: Zakynthos 45.11 Mbps, Corfu 43.70 Mbps, Lefkada 45.91 Mbps, Kefalonia/Ithaki 32.34 Mbps.
  - **Mobile broadband (EL62):** test-weighted mean download **107.48 Mbps** · upload **15.31 Mbps** · latency **59.1 ms** (1,880 tiles, 11,296 tests, 6,248 devices). Island breakdown: Corfu 114.19 Mbps, Lefkada 110.47 Mbps, Zakynthos 101.44 Mbps, Kefalonia/Ithaki 99.02 Mbps.
  - Evidence: `data/manifests/source-verification-2026-10-20.json`, `data/curated/data20-internet-speed.json`.

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
