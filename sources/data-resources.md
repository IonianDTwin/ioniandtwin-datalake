# Data resources — Data01–Data34

`DECISION` One list, one row of truth per indicator: the online source link, the Markdown procedure to follow for data access, and the ETL path. Machine-readable twin: `indicators/source-indicator-map.json`. Pull recipes: `sources/pull-workflow/`. Document extraction: `sources/procedures/`.

Legend — access procedure files:

- `WF/01` = `sources/pull-workflow/01-environmental-health.md` (and so on `WF/02`…`WF/10`)
- `PROC/download-extract.md` = `sources/procedures/download-extract.md` (public webpage/PDF/file)
- `API (script)` = `scripts/verification/pull-*.sh` (direct API pull)
- ETL shared references: `pipelines/ingestion-contracts.md`, `pipelines/quality-rules.md`, `schemas/observation-schema.json`, `scripts/verification/export_observations.py`

Status: `VERIFIED` (pull-tested) · `PARTIAL` (data present / access partially confirmed) · `UNVERIFIED` (source not yet reached) · `PROPOSAL` (derived / not yet a feed).

---

## Environmental Health & Pollutants — Περιβαλλοντική Υγεία & Ρύποι

### Data01 · Airport CO2 levels (Επίπεδα CO2 αεροδρομίων)
- Status: `UNVERIFIED`
- Source: Copernicus CAMS (regional air quality) + local IoT stations.
- Online source: https://atmosphere.copernicus.eu/
- Data access: `WF/01` — CAMS requires a registration token; IoT is internal.
- ETL: CAMS netCDF/GRIB → extract value at airport POI → observation `Data01` (CO2/NO2/PM).

### Data02 · Excellent bathing waters (%) (Άριστα νερά κολύμβησης (%))
- Status: `VERIFIED` (country level)
- Source: EEA WISE Bathing Water (Discodata SQL API) — authoritative; proposal also cites CMEMS/EU Tourism Dashboard.
- Online source: https://discodata.eea.europa.eu/sql · dataset page https://www.eea.europa.eu/data-and-maps/data/bathing-water-directive-status-of-bathing-water (datahub item `c3858959-90da-4c1b-b9ca-492db0e514df`)
- Data access: `API` — table `[WISE_BWD].[latest].[assessment_BathingWaterStatus]` (quality since 1990).
- ETL: `SELECT quality, COUNT(*) ... WHERE countryCode='EL' AND season=<year>` → % Excellent. `VERIFIED` Greece 2024: Excellent 1677 / total 1729 (96.99 % of total; 99.00 % of classified).

### Data03 · Clean beach water (reports) (Καθαρό νερό παραλίας)
- Status: `VERIFIED` (derived flag, country level)
- Source: EEA WISE BWD (derived) + citizen reports (app's own feed).
- Online source: https://discodata.eea.europa.eu/sql (reports are the app's own feed).
- Data access: `API` + internal user reports.
- ETL: water-quality class → clean-beach flag. `ASSUMPTION` "clean" = classified as Excellent/Good/Sufficient. Greece 2024: 99.94 % of classified waters meet this. Cross-verify reports vs EEA/CMEMS.

### Data04 · Blue Flags (Γαλάζιες Σημαίες)
- Status: `PARTIAL`
- Source: Blue Flag programme (FEE); proposal cites EU Tourism Dashboard.
- Online source: https://www.blueflag.global/ (confirmed HTTP 200, 2026-09-24).
- Data access: `PROC/download-extract.md` — the global site is an interactive map (Squarespace); no clean machine-readable CSV/list of certified sites is exposed from `blueflag.global` navigation. National-operator pages carry per-country lists. Recorded as an access constraint (no export confirmed), not "source does not exist".
- ETL: list → count certified sites per spatial unit → observation `Data04`.

### Data05 · EMAS / EU Ecolabel (EMAS / EU Ecolabel)
- Status: `PARTIAL` (register URL confirmed)
- Source: EMAS register + EU Ecolabel catalogue (European Commission).
- Online source: EMAS register `https://green-forum.ec.europa.eu/green-business/emas/emas-register_en` (confirmed HTTP 200, 2026-09-24); EU Ecolabel catalogue `https://green-business.ec.europa.eu/eu-ecolabel_en`.
- Data access: `PROC/download-extract.md` — download/export the register/catalogue (the register page exposes a search UI; the export/download URL to confirm on next pass).
- ETL: register → count certified organisations per spatial unit → observation `Data05`.

## Dynamic Congestion — Δυναμική Συμφόρηση

### Data06 · Airport congestion
- Status: `PARTIAL` (free live-flight source confirmed 2026-09-26)
- Source: OpenSky Network (free, no-key; D-011 substitute) · FlightRadar24 (paid, fallback).
- Online source: `https://opensky-network.org/api/states/all` (HTTP 200, application/json) · https://www.flightradar24.com/ (paid).
- Data access: `WF/02` — OpenSky anonymous REST (rate-limited, no key). Verified 2026-09-26: `GET …/api/states/all?lamin=37.0&lomin=19.0&lamax=40.5&lomax=22.0` returned live aircraft states over the Ionian Islands (Aegean/Wizz callsigns, positions).
- ETL: aircraft positions → count per airport buffer per window → congestion.

### Data07 · Port congestion
- Status: `PARTIAL` (free AIS candidates identified 2026-09-26)
- Source: aisstream.io (free crowd-sourced AIS WebSocket) · EMODnet Human Activities (free authoritative vessel-density) · MarineTraffic AIS (paid). OpenSky (Data06) covers aircraft only, not vessels.
- Online source: `https://aisstream.io/` (HTTP 200) · `https://emodnet.ec.europa.eu/en/human-activities` (HTTP 200) · https://www.marinetraffic.com/ (paid)
- Data access: `WF/02` — aisstream live stream (public stream, no key) or EMODnet vessel-density download; both free. AISHub remains paid/limited-tier.
- ETL: vessel positions/density → count in port buffer → congestion.

### Data08 · Road congestion
- Status: `UNVERIFIED` (no free live-traffic source; routing-only fallback identified 2026-09-26)
- Source: Google Maps Platform (paid, live traffic) · OpenRouteService (free tier, key — routing, not live congestion).
- Online source: https://mapsplatform.google.com/ (paid) · `https://openrouteservice.org/dev/#/signup` (HTTP 200, free tier ~500 req/day)
- Data access: `WF/02` — ORS free API key for routing/distance; no free live-traffic feed confirmed (TomTom/HERE/Google all paid).
- ETL: travel-time/delay per segment → congestion level (live) or ORS static routing as fallback.

### Data09 · Beach congestion
- Status: `UNVERIFIED`
- Source: citizen reports (own app).
- Online source: internal (mobile app → backend).
- Data access: `WF/02` — internal feed.
- ETL: cross-verify reports vs sensors → congestion flag.

### Data10 · City congestion
- Status: `UNVERIFIED`
- Source: Google Maps + citizen reports.
- Online source: https://mapsplatform.google.com/ (reports internal).
- Data access: `WF/02`.
- ETL: traffic layer + reports → zone congestion.

## Sustainable Transport — Βιώσιμες Μεταφορές

### Data11 · KTEL (bus) congestion
- Status: `UNVERIFIED`
- Source: local transport telematics (KTEL).
- Online source: internal/partner — no public link.
- Data access: `WF/03` — request feed from operator.
- ETL: occupancy/delay per route → congestion.

### Data12 · Urban transit congestion
- Status: `UNVERIFIED`
- Source: local transport telematics.
- Online source: internal/partner.
- Data access: `WF/03`.
- ETL: as Data11.

## Climate Adaptation — Κλιματική Προσαρμογή

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
- Status: `UNVERIFIED` (credential-gated: CAMS token / weather key)
- Source: Copernicus CAMS (ambient air quality) + OpenWeatherMap / Meteo.gr.
- Online source: https://atmosphere.copernicus.eu/
- Data access: `WF/04` (CAMS, registration token).
- ETL: AQ pollutant value (NO2/PM/CO2) at a POI → observation `Data15`. `DECISION` D-008 (confirmed): the AI indoor-activity suggestion was removed in the corrected source.

## Social Pressure & Infrastructure — Κοινωνική Πίεση & Υποδομές

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
- Data access: `WF/05` — request/observe official feed.
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
- Online source: `https://insideairbnb.com/get-the-data/` (HTTP 200) · `https://data.insideairbnb.com/greece/` (HTTP 200 but `content-length: 0`; Greece region/date keys still to resolve — a guessed Athens key returned HTTP 403).
- Data access: `WF/05` — resolve InsideAirbnb Greece region keys (Ionian Islands coverage TBD) or dashboard export.
- ETL: rental listings share → observation `Data19`.

## Digital Infrastructure — Ψηφιακή Υποδομή

### Data20 · Internet speed (>100 Mb/s)
- Status: `PARTIAL` (free source confirmed 2026-09-26)
- Source: Ookla Open Data (free, no key; D-011 substitute) · citizen reports (own app).
- Online source: `https://ookla-open-data.s3.amazonaws.com/shapefiles/performance/type=fixed/year=2024/quarter=3/2024-07-01_performance_fixed_tiles.zip` (HTTP 200, application/zip) · registry `https://registry.opendata.aws/speedtest-global-performance/`.
- Data access: `WF/06` — direct S3 shapefile download (fixed broadband tiles, quarterly, free).
- ETL: speed tile → aggregate per spatial unit → observation `Data20`.

### Data21 · 4G/5G availability
- Status: `UNVERIFIED`
- Source: citizen reports.
- Online source: internal.
- Data access: `WF/06`.
- ETL: coverage reports → availability flag.

## Spatial Sustainability — Χωροταξική Αειφορία

### Data22 · Tourist diversity (zones)
- Status: `UNVERIFIED`
- Source: EU Tourism Dashboard (maps).
- Online source: https://tourism-dashboard.ec.europa.eu/
- Data access: `WF/07` + `PROC/download-extract.md` (export map/table).
- ETL: zone classification → diversity observation with `spatial_ref`.

### Data23 · Density of cultural elements
- Status: `UNVERIFIED`
- Source: EU Tourism Dashboard maps.
- Online source: https://tourism-dashboard.ec.europa.eu/
- Data access: `WF/07` + `PROC/download-extract.md`.
- ETL: cultural-POI density per zone.

### Data24 · Protected land (%)
- Status: `PARTIAL` (dataset URLs confirmed)
- Source: EU Tourism Dashboard maps; Natura 2000 / EEA (authoritative).
- Online source: Natura 2000 EEA datahub item `https://www.eea.europa.eu/en/datahub/datahubitem-view/6fc8ad2d-195d-40f4-bdec-576e7d1268e4` (HTTP 200); CDDA "Nationally designated areas" `https://www.eea.europa.eu/en/datahub/datahubitem-view/f60cec02-6494-4d08-b12d-17a37012cb28` (HTTP 200). Both expose a GeoNetwork record via `https://sdi.eea.europa.eu/catalogue/datahub/api/records/<uuid>`.
- Data access: `WF/07` + `PROC/download-extract.md` (CDDA / Natura 2000); the file download (GeoPackage/Shapefile) is behind the SDI download link — to confirm on the next pass.
- ETL: protected-area geometry → % per spatial unit.

### Data25 · Accommodation in high-value areas
- Status: `UNVERIFIED`
- Source: EU Tourism Dashboard maps.
- Online source: https://tourism-dashboard.ec.europa.eu/
- Data access: `WF/07` + `PROC/download-extract.md`.
- ETL: accommodation density in high-value zones.

## Tourism Performance — Τουριστική Απόδοση

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
- Status: `PARTIAL` (free source candidate reachable 2026-09-26)
- Source: ELSTAT (Greek statistics, free) · booking/social services (paid, ToS-gated).
- Online source: ELSTAT occupancy publication `https://www.statistics.gr/en/statistics/-/publication/STO12/` (HTTP 200) · no public booking API.
- Data access: `WF/08` — confirm the ELSTAT occupancy dataset/export; fallback: derive occupancy = nights/bed-places from Data26/27.
- ETL: occupancy = stays/capacity (ELSTAT table or Eurostat-derived).

### Data29 · Seasonality (%)
- Status: `PARTIAL`
- Source: Eurostat monthly nights (`tour_occ_nim`) — country level only.
- Online source: https://ec.europa.eu/eurostat · verified endpoint (country level, monthly): `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&geo=EL&freq=M&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2023-01..2023-12`
- Data access: `WF/08` + `API (pull-eurostat-tourism.sh)` — NUTS2 monthly (`geo=EL62`) returns an empty set; use country-level Greece as the documented proxy.
- ETL: monthly distribution → peak-month share → seasonality %. `VERIFIED` 2023 (Greece): total 147,209,821 nights · peak Aug 31,687,354 (21.53 %) · Jul+Aug 41.54 % · Jun–Sep 71.95 %.

### Data30 · Average length of stay
- Status: `PROPOSAL`
- Source: derived from Eurostat Data26 (nights ÷ arrivals); booking services as secondary.
- Online source: https://ec.europa.eu/eurostat
- Data access: `WF/08` — derive from Data26.
- ETL: `nights ÷ arrivals` (≈5.9 nights 2022/2023) → observation `Data30` once the formula is confirmed.

## Density & Typology — Πυκνότητα & Τυπολογία

### Data31 · Tourism density (nights/km²)
- Status: `VERIFIED`
- Source: Eurostat `tour_occ_nin2` (unit `P_KM2`).
- Online source: https://ec.europa.eu/eurostat · verified endpoint: `…/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023`
- Data access: `WF/09` + `API (pull-eurostat-tourism.sh)`.
- ETL: `c_resid=TOTAL, unit=P_KM2, nace_r2=I551-I553` → observation `Data31`.

### Data32 · Dominant tourism typology
- Status: `PARTIAL`
- Source: Eurostat `tour_occ_nin2` (`nace_r2` breakdown) — **data already pulled**.
- Online source: https://ec.europa.eu/eurostat · endpoint as Data31.
- Data access: `WF/09` — no new pull needed; define the classification rule.
- ETL: `nace_r2` shares (hotels ≈73%/70%, short-stay ≈26%/30%, camping <1%) → dominant type (hotels, `ASSUMPTION`).

### Data33 · Foreign tourist share (%)
- Status: `VERIFIED`
- Source: Eurostat `tour_occ_nin2` (`c_resid=FOR`, unit `PC_TOT`).
- Online source: https://ec.europa.eu/eurostat · endpoint as Data31.
- Data access: `WF/09` + `API (pull-eurostat-tourism.sh)`.
- ETL: `c_resid=FOR, unit=PC_TOT, nace_r2=I551-I553` → observation `Data33`.

## Participation — Συμμετοχικότητα

### Data34 · User feedback
- Status: `UNVERIFIED`
- Source: TripAdvisor / Google Reviews (paid, privacy-sensitive) + EU Tourism Dashboard.
- Online source: https://www.tripadvisor.com/ (reviews via API/platform).
- Data access: `WF/10` — feasibility track; citizen reports are the app's own feed.
- ETL: sentiment (local-first LLM) over reviews/reports → satisfaction indicator.
