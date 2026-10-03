# Data Preparation Progress - IonianDTwin

`DECISION` Living tracker for the Data01-Data34 preparation effort. This is the
**go-to file** for the team to see, in one place, *where the data work is now* and
*what is being worked on next*, until all data procedures, cleaning, transformation
and indicator feeds are complete. Section 1 is a clean snapshot; Section 2 is the
dated, per-indicator record - including each indicator's **source** - of what
changed and when; Section 3 is the work queue.

Status vocabulary (one taxonomy, consistent with `sources/data-resources.md`):

- `VERIFIED` - source pull-tested and a value is confirmed.
- `PARTIAL` - source located / data partially present, but the value or access is incomplete.
- `PROPOSAL` - derived/engineered indicator; formula is a reversible default awaiting author sign-off.
- `UNVERIFIED` - source not yet reached (includes app-internal feeds and paid/credential-gated sources).

> This file is maintained by hand whenever the data changes. The
> machine-readable twin of the *current status* is `indicators/source-indicator-map.json`;
> the authoritative per-indicator detail (with full URLs and ETL steps) is
> `sources/data-resources.md`. Workstation-only procedures, credentials and internal
> decision logs stay local and are **not** referenced here. A **Key note** per indicator
> records *what* was done, *why*, and *how* for surgical/reconciliation approaches.

---

## 1 · Current progress

### Summary

- **34 indicators** total.
- **21 `VERIFIED`** (62 %) · **4 `PARTIAL`** (12 %) · **0 `PROPOSAL`** (0 %) · **9 `UNVERIFIED`** (26 %).
- Data pipeline emits **81 schema-aligned observations** (28 base + 47 derived + 6 dashboard) as of 2026-10-03, plus 1 composite prototype (`Tourism Pressure Index`).
- Single source of truth: `data/curated/observations-2026-10-03.json` / `.csv`.

```
VERIFIED    █████████████████████··········· 21/34
PARTIAL     ████·····························  4/34
PROPOSAL    ···································  0/34
UNVERIFIED  █████████························  9/34
```

### By category

| Category | VERIFIED | PARTIAL | PROPOSAL | UNVERIFIED |
| --- | --- | --- | --- | --- |
| Environmental Health & Pollutants (01-05) | 4 | 1 | 0 | 0 |
| Dynamic Congestion (06-10) | 0 | 2 | 0 | 3 |
| Sustainable Transport (11-12) | 0 | 0 | 0 | 2 |
| Climate Adaptation (13-15) | 3 | 0 | 0 | 0 |
| Social Pressure & Infrastructure (16-19) | 1 | 1 | 0 | 2 |
| Digital Infrastructure (20-21) | 1 | 0 | 0 | 1 |
| Spatial Sustainability (22-25) | 4 | 0 | 0 | 0 |
| Tourism Performance (26-30) | 5 | 0 | 0 | 0 |
| Density & Typology (31-33) | 3 | 0 | 0 | 0 |
| Participation (34) | 0 | 0 | 0 | 1 |
| **Total** | **21** | **4** | **0** | **9** |

### Indicator status (one line each)

| ID | Indicator | Status | Latest value / note |
| --- | --- | --- | --- |
| Data01 | Airport CO₂ levels | `PARTIAL` | CAMS access OK; CO₂ not a CAMS regional variable → NO₂/CO proxy |
| Data02 | Excellent bathing waters (%) | `VERIFIED` | EL62 2023 98.82 % · Greece 2024 96.99 % (series 1990-2024) |
| Data03 | Clean beach water (reports) | `VERIFIED` | derived flag; 99.94 % of classified (country level) |
| Data04 | Blue Flags | `VERIFIED` | EL62 2024: 51 Blue Flag sites (dashboard) |
| Data05 | EMAS / EU Ecolabel | `VERIFIED` | EL62: 0 EMAS · 0 ecolabel accommodation |
| Data06 | Airport congestion | `PARTIAL` | OpenSky live snapshot (17 aircraft); score formula TBD |
| Data07 | Port congestion | `PARTIAL` | aisstream/EMODnet live snapshot (1 vessel); score formula TBD |
| Data08 | Road congestion | `UNVERIFIED` | no free live-traffic source (routing-only ORS) |
| Data09 | Beach congestion | `UNVERIFIED` | app's own citizen-report feed |
| Data10 | City congestion | `UNVERIFIED` | Google Maps (paid) + reports |
| Data11 | KTEL (bus) congestion | `UNVERIFIED` | operator telematics (no public link) |
| Data12 | Urban transit congestion | `UNVERIFIED` | operator telematics (no public link) |
| Data13 | Weather conditions | `VERIFIED` | Open-Meteo (Corfu point) |
| Data14 | High UV and protection | `VERIFIED` | Open-Meteo `uv_index_max` |
| Data15 | Air quality | `VERIFIED` | CAMS 2026-09-30: NO₂ 5.80 · PM10 7.40 · PM2.5 5.51 µg/m³ |
| Data16 | Tourism intensity (nights/residents) | `VERIFIED` | EL62 2023 = 97,705.5; peaked 2024 = 103,440 |
| Data17 | Hospital / infrastructure congestion | `UNVERIFIED` | official announcements + reports |
| Data18 | Power / water outage | `UNVERIFIED` | official announcements + reports |
| Data19 | Short-term rental share (Airbnb) | `PARTIAL` | InsideAirbnb Greece keys 403; unresolved |
| Data20 | Internet speed (>100 Mb/s) | `VERIFIED` | Ookla 2024-Q3: mean 39.1 Mbps (Ionian bbox) |
| Data21 | 4G/5G availability | `UNVERIFIED` | app's own citizen-report feed |
| Data22 | Tourist diversity (zones) | `VERIFIED` | 1−HHI 0.636→0.640 (2021-25); definition adopted (provisional) |
| Data23 | Density of cultural elements | `VERIFIED` | EL62 2023: 9.07 cultural assets / 100 km² (dashboard) |
| Data24 | Protected land (%) | `VERIFIED` | EL62 = 16.76 % (386.41 / 2,304.87 km²) |
| Data25 | Accommodation in high-value areas | `VERIFIED` | share of accommodations in high-nature-value areas: EL62 = 43 % (2023) |
| Data26 | Arrivals & overnight stays | `VERIFIED` | nights 2023 = 19,762,799; arrivals 3,332,407 |
| Data27 | Tourism capacity (beds) | `VERIFIED` | EL62 beds 2023 = 155,968 |
| Data28 | Occupancy rate (%) | `VERIFIED` | EL62 2023: 65.4 % net occupancy (dashboard) |
| Data29 | Seasonality (%) | `VERIFIED` | EL62 2023: 71.08 % peak-season share (dashboard) |
| Data30 | Average length of stay | `VERIFIED` | nights ÷ arrivals: 5.93 → 5.58 (confirmed) |
| Data31 | Tourism density (nights/km²) | `VERIFIED` | EL62 2023 = 8,588.79 |
| Data32 | Dominant tourism typology | `VERIFIED` | dominant = highest nights share → hotels (adopted) |
| Data33 | Foreign tourist share (%) | `VERIFIED` | EL62 2023 = 93.58 % |
| Data34 | User feedback | `UNVERIFIED` | TripAdvisor/Google (paid, privacy-sensitive) |

### Refresh cadence & data vintage

Expected refresh cadence per indicator (recorded as `cadence` in `indicators/source-indicator-map.json`):

| Cadence | Indicators | Notes |
| --- | --- | --- |
| `live` (streaming) | Data06-12, 17, 18, 21, 34 | congestion, reports, outages - poll on interval |
| `daily` (forecast/sensor) | Data13, 14, 15 | weather/UV/air-quality forecasts |
| `quarterly` | Data19, 20 | Airbnb snapshots, Ookla |
| `annual` (official stats) | Data02-04, 16, 22, 25-33 | Eurostat/EEA - update on release (~mid-year N+1) |
| `on-change` (static/registers) | Data05, 23, 24 | EMAS/Ecolabel, cultural assets, protected land |
| `paused` | Data01 | CO₂ paused on accuracy |

**Freshest available data (as of 2026-10-03):**

- **Eurostat-direct (annual, current to 2025/26):** nights/arrivals 2025 · bed-places 2026 · intensity/density/foreign-share/length-of-stay 2025. These are the latest published.
- **EEA bathing water:** full series **1990-2024** (Greece 96.99 % excellent in 2024) - the latest assessed season.
- **Live/daily:** Data06/07 (2026-10-02 snapshots) · Data13/14 (current forecast) · Data15 (2026-09-30) · Data05 (current registers).
- **Dashboard-sourced (frozen at the 2024 release → 2023):** Data02 (EL62), Data23, Data25, Data28, Data29 (EL62). Data04 = 2024 (Blue Flag). These lag because the dashboard is an annual snapshot.
- **Static:** Data24 (NUTS 2021 / current Natura 2000).

**Gap to close (next pulls):** re-pull Data02 at EL62 for 2024 (spatial join on bathing-water coordinates), and Data28/29 underlying Eurostat to reach 2024/25. Data22/23/25/32 are JRC dashboard computations - fresher values need the dashboard's next release or its underlying source.

---

## 2 · Detailed history & sources (by indicator)

### Environmental Health & Pollutants - Περιβαλλοντική Υγεία & Ρύποι

- **Data01 · Airport CO₂ levels** - `PARTIAL`
  - **Source:** Copernicus CAMS (regional air quality) - `ads.atmosphere.copernicus.eu` · local IoT stations.
  - **2026-09-22** - listed; source = Copernicus CAMS + local IoT (credential-gated).
  - **2026-10-01** - CAMS access verified via the Atmosphere Data Store (`cads-api-client`); pulled `cams-europe-air-quality-forecasts`. Finding: CAMS *regional* has **no CO₂ variable** - only NO₂/CO/PM at the surface. Working note: keep NO₂/CO as airport-emissions proxies; CO₂ deferred to CAMS global GHG (coarse) or local sensors. → `PARTIAL`.
  - **2026-10-03** - "actual CO₂" pull **paused on accuracy**: regional CAMS global GHG CO₂ (~0.75° grid) is too coarse for "airport CO₂ levels"; airport-local point CO₂ needs local sensors (the proposal's own "local IoT stations" source).

- **Data02 · Excellent bathing waters (%)** - `VERIFIED`
  - **Source:** EEA WISE Bathing Water (Discodata SQL) - `discodata.eea.europa.eu/sql` · CMEMS (secondary); cross-referenced with the EU Tourism Dashboard `TOUR_ENV_05`.
  - **2026-09-24** - resolved via the EEA Discodata SQL API (`[WISE_BWD].[latest].[assessment_BathingWaterStatus]`). Greece 2024: Excellent 1,677 / 1,729 = **96.99 %** of total (99.00 % of classified).
  - **2026-10-03** - **Key note (reconciliation):** *what:* adopted EL62 = **98.82 %** excellent bathing water (2023); *why:* the dashboard (the proposal's own source) publishes it at NUTS2, so the pending `bathingWaterIdentifier` spatial join is unnecessary; *how:* read `TOUR_ENV_05` from the 2024 dashboard CSV export.
  - **2026-10-03** - **Key note (freshness):** *what:* pulled the full Greece bathing-water series **1990-2024** (35 years) from Discodata SQL - 2024 = **96.99 %** excellent (latest assessed season, fresher than the dashboard's 2023); *how:* `SELECT season, quality, COUNT(*) … countryCode='EL' GROUP BY season, quality`. *Gap:* EL62 for 2024 still needs a `bathingWaterIdentifier` → coordinates spatial join (deferred).

- **Data03 · Clean beach water (reports)** - `VERIFIED`
  - **Source:** EEA WISE BWD (derived) · citizen reports (app's own feed).
  - **2026-09-24** - derived flag from Data02; "clean" = Excellent/Good/Sufficient (reversible default). Greece 2024: 99.94 % of classified.

- **Data04 · Blue Flags** - `VERIFIED`
  - **Source:** Blue Flag programme (FEE) - `blueflag.global` · value from the EU Tourism Dashboard `TOUR_DES_10`.
  - **2026-09-24** - `blueflag.global` confirmed reachable (HTTP 200) but interactive-only.
  - **2026-10-01** - no clean machine-readable list of certified sites from the global site. Recorded as an access constraint.
  - **2026-10-03** - **Key note (reconciliation):** *what:* resolved to **51 Blue Flag sites in EL62** (2024); *why:* the dashboard publishes the count directly, avoiding the national-operator list we couldn't extract; *how:* read `TOUR_DES_10` from the 2024 dashboard CSV export. → `VERIFIED`.

- **Data05 · EMAS / EU Ecolabel** - `VERIFIED`
  - **Source:** EMAS register (REST) + EU Ecolabel catalogue (CSV) - European Commission.
  - **2026-10-02** - both registers pull-tested: EMAS register REST (4,523 records / 27 countries) and EU Ecolabel CSV (89,298 licences). **EL62: 0 EMAS · 0 tourist-accommodation ecolabels** (Greece 37 EMAS · 450 ecolabels). Moved `PARTIAL` → `VERIFIED`.

### Dynamic Congestion - Δυναμική Συμφόρηση (Real-time)

- **Data06 · Airport congestion** - `PARTIAL`
  - **Source:** OpenSky Network (free, no-key) - `opensky-network.org/api` · FlightRadar24 (paid fallback).
  - **2026-09-26** - OpenSky Network free REST (`/api/states/all`, no key) returned live aircraft states over the Ionian Islands.
  - **2026-10-02** - live snapshot: 17 aircraft in the Ionian bbox, all overflights, 0 in airport approach. Kept `PARTIAL`: the congestion *score* (count-in-buffer → score) is still a candidate formula and the feed is live-only.
  - **2026-10-03** - **Key note (research):** *what:* surveyed reputable congestion definitions; *found:* the standard European air-congestion metric is **EUROCONTROL ATFM delay** (minutes of delay per flight / airport punctuality - `eurocontrol.int`); *proposed for us (no free airport ATFM feed):* a live proxy - congestion score = `min(1, aircraft-in-approach-buffer ÷ threshold)`, reported as low/medium/high. Flag: score formula remains a proposal (live-only).

- **Data07 · Port congestion** - `PARTIAL`
  - **Source:** aisstream.io · EMODnet Human Activities - `emodnet.ec.europa.eu` · MarineTraffic AIS (paid).
  - **2026-09-26** - free AIS candidates identified: `aisstream.io` (crowd-sourced stream) and EMODnet vessel density (authoritative, free).
  - **2026-10-02** - live AIS snapshot: 1 vessel in Corfu port bbox (moored, SOG 0). EMODnet density baseline pulled (Corfu 352 / Zakynthos 170 / Kefalonia 227 hrs/km²/yr). Kept `PARTIAL` (score formula + live-only).
  - **2026-10-03** - **Key note (research):** *what:* surveyed reputable port-congestion definitions; *found:* the standard metrics are the **World Bank Container Port Performance Index** (minutes per container move) and **UNCTAD median time in port** (vessel turnaround/waiting); *proposed for us (free AIS only):* a live proxy - congestion score = `min(1, vessels-in-port-buffer ÷ threshold)`. Flag: score formula remains a proposal (live-only).

- **Data08 · Road congestion** - `UNVERIFIED`
  - **Source:** Google Maps Platform (paid, live traffic) · OpenRouteService (free tier, routing-only).
  - **2026-09-26** - no free **live** traffic source (TomTom/HERE/Google all paid); OpenRouteService free tier is routing-only.

- **Data09 · Beach congestion** - `UNVERIFIED`
  - **Source:** citizen reports (app's own feed).
- **Data10 · City congestion** - `UNVERIFIED`
  - **Source:** Google Maps traffic layer (paid) + citizen reports.

### Sustainable Transport - Βιώσιμες Μεταφορές

- **Data11 · KTEL (bus) congestion** - `UNVERIFIED`
  - **Source:** KTEL operator telematics (no public link).
- **Data12 · Urban transit congestion** - `UNVERIFIED`
  - **Source:** local transport telematics (no public link).

### Climate Adaptation - Κλιματική Προσαρμογή

- **Data13 · Weather conditions** - `VERIFIED`
  - **Source:** Open-Meteo (no-key substitute) - `api.open-meteo.com` · proposal cites OpenWeatherMap / Meteo.gr.
  - **2026-09-22** - Open-Meteo verified at the Corfu point.

- **Data14 · High UV and protection** - `VERIFIED`
  - **Source:** Open-Meteo `daily.uv_index_max` - `api.open-meteo.com`.
  - **2026-09-22** - Open-Meteo `daily.uv_index_max` verified.

- **Data15 · Air quality** - `VERIFIED`
  - **Source:** Copernicus CAMS (ambient air quality) - `ads.atmosphere.copernicus.eu` · OpenWeatherMap / Meteo.gr.
  - **2026-09-22** - Copernicus CDSE catalogue reachable (download gated).
  - **2026-10-01** - verified via CAMS ensemble analysis (surface) over the Ionian Islands for 2026-09-30: NO₂ 5.80 · PM10 7.40 · PM2.5 5.51 · CO 158.70 µg/m³ at the Corfu-airport grid point. Duplicate "Data15" resolved: Data15 = ambient air quality.

### Social Pressure & Infrastructure - Κοινωνική Πίεση & Υποδομές

- **Data16 · Tourism intensity (nights/residents)** - `VERIFIED`
  - **Source:** Eurostat `tour_occ_nin2` (unit `P_THAB`) - `ec.europa.eu/eurostat`.
  - **2026-09-22** - Eurostat `tour_occ_nin2` verified.
  - **2026-10-01** - extended to 2025; reconciled the Kathimerini figure (103,440 nights/1,000 = Eurostat 2024 Ionian intensity).

- **Data17 · Hospital / infrastructure congestion** - `UNVERIFIED`
  - **Source:** official announcements + citizen reports.
- **Data18 · Power / water outage** - `UNVERIFIED`
  - **Source:** official announcements + citizen reports.

- **Data19 · Short-term rental share (Airbnb)** - `PARTIAL`
  - **Source:** InsideAirbnb (free scrape-derived listings) - `insideairbnb.com` · EU Tourism Dashboard (Airbnb has no public API).
  - **2026-09-26** - InsideAirbnb identified as free candidate (`insideairbnb.com/get-the-data/` HTTP 200); Greece region/date keys unresolved (guessed Athens key → 403).

### Digital Infrastructure - Ψηφιακή Υποδομή

- **Data20 · Internet speed (>100 Mb/s)** - `VERIFIED`
  - **Source:** Ookla Open Data (free, no key) - `registry.opendata.aws/speedtest-global-performance` · citizen reports.
  - **2026-09-26** - Ookla Open Data identified (free S3 shapefile).
  - **2026-10-01** - pulled 2024-Q3 fixed broadband over the Ionian bbox: **mean 39.1 Mbps** · median 26.8 · max 926.6 (123,119 tests).
  - **2026-10-03** - **Flag (reconciliation):** the dashboard's "Internet speed at tourism destinations" (`TOUR_DIG_05`) = **39.67 %** (EL62 2023) - a *share* metric, not the Mbps mean we measured via Ookla. The exact "% of what" needs the dashboard methodology; keep Ookla Mbps for now and note the definitions differ.

- **Data21 · 4G/5G availability** - `UNVERIFIED`
  - **Source:** citizen reports (app's own feed).

### Spatial Sustainability - Χωροταξική Αειφορία

- **Data22 · Tourist diversity (zones)** - `VERIFIED`
  - **Source:** Eurostat `tour_occ_nin3` (NUTS3 nights) - `ec.europa.eu/eurostat` · EU Tourism Dashboard (front-end over the same data).
  - **Definition (adopted, provisional):** `1 − HHI` of the four NUTS3 island night shares, aggregated to NUTS2/EL62. **Basis:** Herfindahl-Hirschman Index (standard concentration measure).
  - **Open question:** does "diversity" mean spatial spread across islands (adopted), accommodation-type mix (`nace_r2`), or visitor-origin mix (`c_resid`)?
  - **2026-10-01** - derived `1 − HHI` over NUTS3 island night shares (0.636 / 0.651 / 0.632 / 0.631 / 0.640 for 2021→2025), aggregated to NUTS2/EL62.
  - **2026-10-03** - definition adopted as the working default (provisional); open question logged for the author.
  - **2026-10-03** - **Flag (reconciliation):** the dashboard's "Tourism diversity" (`TOUR_SOE_04`) reads **0 (index)** for EL62 and all its islands - a *different concept* whose definition is not yet confirmed (and Greece reads 0 across the board, suggesting a data/definition gap). Do **not** swap our spatial `1 − HHI` (which matches the proposal's "diversity (zones)") for the dashboard value without understanding it.

- **Data23 · Density of cultural elements** - `VERIFIED`
  - **Source:** EU Tourism Dashboard "Cultural assets density" (`TOUR_DES_14`) - `tourism-dashboard.ec.europa.eu`.
  - **2026-10-03** - **Key note (reconciliation):** *what:* resolved to **9.07 cultural assets / 100 km²** (EL62, 2023); *why:* the dashboard (the proposal's own source) already publishes "cultural asset intensity", so no separate POI survey was needed; *how:* read `TOUR_DES_14` from the 2024 dashboard CSV export. → `VERIFIED`.

- **Data24 · Protected land (%)** - `VERIFIED`
  - **Source:** EEA Natura 2000 - `bio.discomap.eea.europa.eu` · Eurostat GISCO NUTS 2021 boundary - `gisco-services.ec.europa.eu`.
  - **2026-09-24** - EEA CDDA/Natura 2000 document URLs confirmed (datahub + GeoNetwork).
  - **2026-10-02** - machine-readable source located: EEA ArcGIS REST `Natura2000Sites` MapServer (no key); GR22 = 18 Habitats + 8 Birds sites. Value left pending (needed clip + terrestrial/marine split + union).
  - **2026-10-03** - **spatial join complete**: Natura 2000 Habitats ∪ Birds clipped to the EL62 land polygon (GISCO NUTS 2021, EPSG:3035), terrestrial/marine split via land-polygon intersection, union dissolved → **16.76 %** (386.41 / 2,304.87 km²). Completeness finding: the Echinades/Petalas islets (GISCO NUTS3 EL623 "Ithaki, Kefallinia") are protected via a GR23-coded Acheloos-delta site (1,608 ha) - a GR22-only filter would under-count. → `VERIFIED`.
  - **2026-10-03** - cross-check: EU Tourism Dashboard "Share of protected/designated land" (`TOUR_DES_12`) = **16.57 %** for EL62, within 0.2 pp of our independent spatial join (16.76 %).

- **Data25 · Accommodation in high-value areas** - `VERIFIED`
  - **Source:** EU Tourism Dashboard - "Share of accommodations in areas with high-nature value" (code `TOUR_DES_13`) - `tourism-dashboard.ec.europa.eu` · data.europa.eu dataset `9564824a-7f16-4efa-82fb-d4e176350026`.
  - **Definition (adopted):** the proposal's own source (EU Tourism Dashboard) already publishes this indicator - no overlay needed. **Value:** EL62 = **43 %** (2023); per-island: Zakynthos 59 % · Kerkyra 34 % · Ithaki-Kefallinia 34 % · Lefkada 57 %.
  - **Key note (reconciliation):** *what:* adopted the dashboard's "Share of accommodations in areas with high-nature value" (43 %, EL62 2023); *why:* the proposal's own source already publishes it, so building a Natura-2000-∪-coastal overlay was unnecessary (and that overlay definition was my earlier guess); *how:* pulled the 2024 dashboard CSV export and read `TOUR_DES_13`.
  - **Flag / open question:** the exact operationalisation of "high-nature value" (which areas count) is defined in the dashboard's methodology - to be pinned down; my earlier proposed default (Natura 2000 ∪ coastal buffer) is **superseded** by the dashboard definition.
  - **2026-10-01** - ELSTAT bed-places pulled as a partial path (104,108 → 109,565) but lacked the spatial distribution.
  - **2026-10-03** - resolved directly from the EU Tourism Dashboard (43 %, EL62 2023, + NUTS3 breakdown). → `VERIFIED`.

### Tourism Performance - Τουριστική Απόδοση

- **Data26 · Arrivals & overnight stays** - `VERIFIED`
  - **Source:** Eurostat `tour_occ_nin2` (nights) + `tour_occ_arn2` (arrivals) - `ec.europa.eu/eurostat`.
  - **2026-09-22** - Eurostat `tour_occ_nin2` + `tour_occ_arn2` verified (EL62).
  - **2026-10-01** - series extended to 2025 (nights/arrivals) and 2026 (bed-places).

- **Data27 · Tourism capacity (beds)** - `VERIFIED`
  - **Source:** Eurostat `tour_cap_nuts2` (bed-places) - `ec.europa.eu/eurostat`.
  - **2026-09-22** - Eurostat `tour_cap_nuts2` (EL62) verified.

- **Data28 · Occupancy rate (%)** - `VERIFIED`
  - **Source:** EU Tourism Dashboard "Occupancy rate" (`TOUR_DES_04`) - `tourism-dashboard.ec.europa.eu` · Eurostat (underlying).
  - **2026-10-01** - earlier attempt: derived occupancy = nights ÷ (beds × 365) ≈ 28-36 % (a *gross* rate; wrong for a seasonal destination).
  - **2026-10-03** - **Key note (reconciliation):** *what:* adopted **65.4 % net occupancy** (EL62, 2023); *why:* the dashboard's occupancy is the standard *net* rate (nights ÷ beds×open-days), not our gross ÷365 which understated a highly seasonal region; *how:* read `TOUR_DES_04` from the 2024 dashboard CSV export. Our gross derivation is superseded. → `VERIFIED`.

- **Data29 · Seasonality (%)** - `VERIFIED`
  - **Source:** EU Tourism Dashboard "Tourism seasonality" (`TOUR_SOE_02`) - `tourism-dashboard.ec.europa.eu` · Eurostat (underlying).
  - **2026-09-24** - Eurostat `tour_occ_nim` monthly nights verified at country level only (`geo=EL`); peak Aug = 21.53 %; Jun-Sep 71.95 %. No NUTS2 monthly publication.
  - **2026-10-03** - **Key note (reconciliation):** *what:* adopted **71.08 % peak-season share** (EL62, 2023) - NUTS2 level, replacing the country-level peak-month proxy; *why:* the dashboard's "seasonality" is a summer-season share, not the peak-month share we had used; *how:* read `TOUR_SOE_02` from the 2024 dashboard CSV export. *Flag:* exact month window (Jun-Sep vs Jul-Aug) to be confirmed from the methodology. → `VERIFIED`.

- **Data30 · Average length of stay** - `VERIFIED`
  - **Source:** derived from Eurostat Data26 (nights ÷ arrivals) · booking services (secondary).
  - **Definition (confirmed):** `nights ÷ arrivals` (Data26). **Basis:** standard tourism statistic (Eurostat/UNWTO).
  - **2026-10-01** - derived `nights ÷ arrivals`; 5.93 (2022) → 5.58 (2025).
  - **2026-10-03** - formula confirmed (`nights ÷ arrivals`); no longer `PROPOSAL`.

### Density & Typology - Πυκνότητα & Τυπολογία

- **Data31 · Tourism density (nights/km²)** - `VERIFIED`
  - **Source:** Eurostat `tour_occ_nin2` (unit `P_KM2`) - `ec.europa.eu/eurostat`.
  - **2026-09-22** - Eurostat `tour_occ_nin2` (unit `P_KM2`) verified.
- **Data32 · Dominant tourism typology** - `VERIFIED`
  - **Source:** Eurostat `tour_occ_nin2` (`nace_r2` breakdown) - `ec.europa.eu/eurostat` (data already pulled).
  - **Definition (adopted, provisional):** dominant typology = `nace_r2` accommodation category with the highest share of nights → hotels (≈73 %). **Basis:** Eurostat NACE Rev. 2 accommodation categories.
  - **Open question:** confirm "highest nights share" vs an alternative basis (bed-places or arrivals).
  - **2026-09-22** - data pulled (`nace_r2` breakdown: hotels ≈73 %/70 %, short-stay ≈26 %/30 %, camping <1 %).
  - **2026-10-03** - classification rule adopted (provisional); open question logged.
  - **2026-10-03** - **Flag (reconciliation):** the dashboard's "Dominant tourism typology" (`TOUR_DES_07`) is a **categorical 6-class typology** and reads **class 4** for EL62 (2023) - a *different concept* from our "highest `nace_r2` nights share → hotels". The class-4 label (e.g. coastal/urban/rural) needs the dashboard's typology mapping; keep "hotels" for now but note the categorical definition differs.
- **Data33 · Foreign tourist share (%)** - `VERIFIED`
  - **Source:** Eurostat `tour_occ_nin2` (`c_resid=FOR`, `PC_TOT`) - `ec.europa.eu/eurostat`.
  - **2026-09-22** - Eurostat `tour_occ_nin2` (`c_resid=FOR`, `PC_TOT`) verified.

### Participation - Συμμετοχικότητα

- **Data34 · User feedback** - `UNVERIFIED`
  - **Source:** TripAdvisor / Google Reviews (paid, privacy-sensitive) · EU Tourism Dashboard.

---

## 3 · What we are working on next (work queue)

Ordered roughly by impact; update the top of this list as work proceeds.

### A · Finish the `PARTIAL` indicators

1. **Data06 & Data07 congestion score** - research done (EUROCONTROL ATFM delay · World Bank CPPI · UNCTAD time-in-port cited); adopt the `min(1, count-in-buffer ÷ threshold)` live proxy as the working formula (still a proposal) and wire the OpenSky/AIS feeds into a score.
2. **Data19 Airbnb keys** - resolve InsideAirbnb Greece region/date keys.
3. **Data24 follow-up (optional tightening)** - the spatial join is `VERIFIED`; optionally re-run with a higher-resolution land mask if sub-1 % precision is wanted.

### B · Unblock the `UNVERIFIED` indicators

- **App-internal feeds (design work, not external pulls):** Data09 (beach), Data10 (city, partly), Data17 (hospital), Data18 (outage), Data21 (4G/5G), Data34 (feedback). These come from the mobile app / citizen reports - their ingestion path needs designing, not a data-source search.
- **Paid / gated (free alternatives exhausted first):** Data08 (road congestion - Google/TomTom/HERE), Data10 (city traffic), Data34 (reviews).
- **Operator feeds (request access):** Data11 (KTEL bus), Data12 (urban transit).

### C · `PROPOSAL` sign-off

- **Composite Tourism Pressure Index** - confirm the provisional weights (0.4/0.4/0.2) and reference bounds.

### D · Open definition questions & reconciliation flags (optional revisit)

- **Data22** - dashboard "Tourism diversity" reads 0 for EL62 (different concept / possible Greece gap); keep our spatial `1 − HHI` (matches the proposal's "diversity (zones)") until the dashboard definition is understood.
- **Data25** - "high-nature value areas": dashboard operationalisation to be pinned down.
- **Data32** - dashboard "Dominant tourism typology" is a categorical 6-class typology (EL62 = class 4); class label + mapping to be confirmed; keep "hotels" for now.
- **Data20** - dashboard "Internet speed" is a share (%) = 39.67 %, not our Ookla Mbps mean; "% of what" to be confirmed.
- **Data29** - seasonality exact month window (Jun-Sep vs Jul-Aug) to be confirmed from the methodology.

### E · Paused

- **Data01 CO₂** - paused on accuracy: regional CAMS global GHG CO₂ (~0.75°) is too coarse for "airport CO₂"; airport-local point CO₂ needs local sensors.

### F · Cross-cutting data work

- Check the **EU Tourism Dashboard export** before building any spatial/tourism indicator from scratch - it is the proposal's own source and provides ready-made values at NUTS2/NUTS3.
- Keep `data/curated/observations-<date>.json` / `.csv` the single source of truth; retire superseded dated snapshots after each build.
- Apply the spatial-reference rule (NUTS2/EL62 is the analysis level; NUTS3 = internal disaggregation only) to every new route.
- Record every new pull in `data/manifests/` with URL + status + checksum + sample path.

---

## Appendix - requirement-consistency fixes (not indicators)

- **2026-09-24** - "Data 35" in the GSTC A5 & A6 mapping is a transcription error → **Data34**. No new indicator invented.
- **2026-09-24** - duplicate Data15 removed - Data15 = air quality (the "AI indoor-activity" entry removed).
- **2026-10-02** - spatial reference = NUTS2 **EL62**; NUTS3 is internal disaggregation only; fixed a 12-observation mislabeling bug in the curated data.
