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
- Status: `UNVERIFIED`
- Source: Copernicus CMEMS + EU Tourism Dashboard (proposal); authoritative bathing-water status = EEA.
- Online source: https://marine.copernicus.eu/ · https://tourism-dashboard.ec.europa.eu/ · https://www.eea.europa.eu/
- Data access: `WF/01` (CMEMS, registration) or `PROC/download-extract.md` (EEA bathing-water status report/data).
- ETL: status table/PDF → count "% excellent" per spatial unit → observation `Data02`.

### Data03 · Clean beach water (reports) (Καθαρό νερό παραλίας)
- Status: `UNVERIFIED`
- Source: Copernicus CMEMS + citizen reports.
- Online source: https://marine.copernicus.eu/ (reports are the app's own feed).
- Data access: `WF/01` (CMEMS) + internal user reports.
- ETL: water-quality class → clean-beach flag; cross-verify reports vs CMEMS/IoT.

### Data04 · Blue Flags (Γαλάζιες Σημαίες)
- Status: `UNVERIFIED`
- Source: Blue Flag programme (FEE); proposal cites EU Tourism Dashboard.
- Online source: https://www.blueflag.global/
- Data access: `PROC/download-extract.md` — locate/export the certified-sites list (interactive page; no clean CSV confirmed).
- ETL: list → count certified sites per spatial unit → observation `Data04`.

### Data05 · EMAS / EU Ecolabel (EMAS / EU Ecolabel)
- Status: `UNVERIFIED`
- Source: EMAS register + EU Ecolabel catalogue (European Commission).
- Online source: https://green-business.ec.europa.eu/eco-management-and-audit-scheme-emas_en · https://green-business.ec.europa.eu/eu-ecolabel_en
- Data access: `PROC/download-extract.md` — download/export the register/catalogue.
- ETL: register → count certified organisations per spatial unit → observation `Data05`.

## Dynamic Congestion — Δυναμική Συμφόρηση

### Data06 · Airport congestion
- Status: `UNVERIFIED`
- Source: MarineTraffic / FlightRadar24 (paid APIs).
- Online source: https://www.marinetraffic.com/ · https://www.flightradar24.com/
- Data access: `WF/02` — paid API key + ToS verification (feasibility track).
- ETL: arrivals/flight positions → count per airport buffer per window → congestion.

### Data07 · Port congestion
- Status: `UNVERIFIED`
- Source: MarineTraffic AIS.
- Online source: https://www.marinetraffic.com/
- Data access: `WF/02` — paid API.
- ETL: vessel positions → count in port buffer → congestion.

### Data08 · Road congestion
- Status: `UNVERIFIED`
- Source: Google Maps Platform.
- Online source: https://mapsplatform.google.com/
- Data access: `WF/02` — paid API.
- ETL: travel-time/delay per segment → congestion level.

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

### Data15 · Air quality / AI indoor-activity proposal
- Status: `UNVERIFIED` (duplicate label — treat as two concerns)
- Source: CAMS (air quality) + local LLM output (indoor suggestion).
- Online source: https://atmosphere.copernicus.eu/ (indoor suggestion is generated locally, not a source).
- Data access: `WF/04` (CAMS) + local-first LLM.
- ETL: air quality as Data01; indoor suggestion is an LLM output, not a pull.

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
- Status: `UNVERIFIED`
- Source: EU Tourism Dashboard; Airbnb (feasibility).
- Online source: https://tourism-dashboard.ec.europa.eu/ · https://www.airbnb.com/ (no public data API).
- Data access: `WF/05` — dashboard export or Airbnb partner API (feasibility track).
- ETL: rental listings share → observation `Data19`.

## Digital Infrastructure — Ψηφιακή Υποδομή

### Data20 · Internet speed (>100 Mb/s)
- Status: `UNVERIFIED`
- Source: citizen reports (own app).
- Online source: internal (mobile app).
- Data access: `WF/06` — internal feed.
- ETL: speed reports → aggregate per spatial unit.

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
- Status: `UNVERIFIED`
- Source: EU Tourism Dashboard maps; Natura 2000 / EEA (authoritative).
- Online source: https://natura2000.eea.europa.eu/ · https://www.eea.europa.eu/
- Data access: `WF/07` + `PROC/download-extract.md` (CDDA / Natura 2000).
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
- Status: `UNVERIFIED`
- Source: booking/social services (paid, ToS-gated).
- Online source: no public data API (booking platforms).
- Data access: `WF/08` — feasibility track; no public pull.
- ETL: occupancy = stays/capacity (or platform feed once authorized).

### Data29 · Seasonality (%)
- Status: `UNVERIFIED`
- Source: Eurostat monthly nights (`tour_occ_nim`).
- Online source: https://ec.europa.eu/eurostat · verified endpoint (country level): `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&geo=EL&time=2023`
- Data access: `WF/08` + extend `pull-eurostat-tourism.sh` (NUTS2 monthly not published — use EL or annual distribution).
- ETL: monthly distribution → peak-month share → seasonality %.

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
