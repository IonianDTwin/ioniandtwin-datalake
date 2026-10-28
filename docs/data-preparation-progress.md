# Data Preparation Progress - IonianDTwin

`DECISION` Living tracker for the Data01-Data34 preparation effort. This is the
**go-to file** for the team to see, in one place, *where the data work is now*,
*which files carry each indicator's raw and curated payloads*, *how features are
extracted and transformed*, and *what is being worked on next*, until all data
procedures, cleaning, transformation and indicator feeds are complete. Section 1
is the executive snapshot and master data-access matrix; Section 2 is the
per-indicator technical reference (file pointers, JSON payload structure,
feature handling, visualizations, and dated changelog); Section 3 is the work
queue.

Status vocabulary (one taxonomy, consistent with `sources/data-resources.md`):

- `VERIFIED` - source pull-tested and a value is confirmed.
- `PARTIAL` - source located / data partially present, but the value or access is incomplete.
- `PROPOSAL` - derived/engineered indicator; formula is a reversible default awaiting author sign-off.
- `UNVERIFIED` - source not yet reached (includes app-internal feeds and paid/credential-gated sources).

> This file is maintained whenever the data changes. The machine-readable twin
> of the *current status* is `indicators/source-indicator-map.json`; the
> authoritative per-indicator detail (with full URLs and ETL steps) is
> `sources/data-resources.md`. Workstation-only procedures, credentials and
> internal decision logs stay local and are **not** referenced here. A **Key
> note** per indicator records *what* was done, *why*, and *how* for
> surgical/reconciliation approaches.

---

## 1 · Current progress

### Summary

- **34 indicators** total (`data/indicators/data01-<slug>/` … `data34-<slug>/`).
- **23 `VERIFIED`** (68 %) · **1 `PARTIAL`** (3 %) · **1 `PROPOSAL`** (3 %) · **9 `UNVERIFIED`** (26 %).
- Data pipeline emits **99 schema-aligned observations** (28 base + 47 derived + 6 dashboard + 18 additional) as of 2026-10-20, plus 1 composite prototype (`Tourism Pressure Index`). Data07 keeps **366 anticipated-congestion forecast observations** as a separate series (2026-10-14).
- **Holistic per-indicator folders (`D-023`, 2026-10-28):** Every indicator has a dedicated folder `data/indicators/dataXX-<slug>/` containing `raw-source-description.json` (raw source URL, `sha256`, raw schema, variable whitelist, and conversion script), `refined-data.json` (feature dictionary, refined JSON payload, and strict `observation-schema.json` records), and a companion `README.md`.
- Single master roll-up: `data/curated/observations-2026-10-20.json` / `.csv`.

```
VERIFIED    ███████████████████████··········· 23/34
PARTIAL     █·································  1/34
PROPOSAL    █·································  1/34
UNVERIFIED  █████████·························  9/34

```

### By category

| Category | VERIFIED | PARTIAL | PROPOSAL | UNVERIFIED |
| --- | --- | --- | --- | --- |
| Environmental Health & Pollutants (01-05) | 4 | 1 | 0 | 0 |
| Dynamic Congestion (06-10) | 1 | 0 | 1 | 3 |
| Sustainable Transport (11-12) | 0 | 0 | 0 | 2 |
| Climate Adaptation (13-15) | 3 | 0 | 0 | 0 |
| Social Pressure & Infrastructure (16-19) | 2 | 0 | 0 | 2 |
| Digital Infrastructure (20-21) | 1 | 0 | 0 | 1 |
| Spatial Sustainability (22-25) | 4 | 0 | 0 | 0 |
| Tourism Performance (26-30) | 5 | 0 | 0 | 0 |
| Density & Typology (31-33) | 3 | 0 | 0 | 0 |
| Participation (34) | 0 | 0 | 0 | 1 |
| **Total** | **23** | **1** | **1** | **9** |

### Indicator status (one line each)

| ID | Indicator | Status | Latest value / note |
| --- | --- | --- | --- |
| Data01 | Airport CO₂ levels | `PARTIAL` | CAMS access OK; CO₂ not a CAMS regional variable → NO₂/CO proxy |
| Data02 | Excellent bathing waters (%) | `VERIFIED` | EL62 2024 99.42 % excellent (spatial join) · Greece 2024 96.99 % (series 1990-2024) |
| Data03 | Clean beach water (reports) | `VERIFIED` | EL62 2024 100.0 % clean of classified (spatial join) |
| Data04 | Blue Flags | `VERIFIED` | EL62 2024: 51 Blue Flag sites (dashboard) |
| Data05 | EMAS / EU Ecolabel | `VERIFIED` | EL62: 0 EMAS · 0 ecolabel accommodation |
| Data06 | Airport congestion | `VERIFIED` | OpenSky live approach-buffer scores (CFU/ZTH/EFL/PVK), 2026-10-20 |
| Data07 | Port congestion | `PROPOSAL` | anticipated schedule-based congestion: 366 forecast obs (2026-10-01→11-30); peak Corfu S=0.983 |
| Data08 | Road congestion | `UNVERIFIED` | no free live-traffic source (routing-only ORS) |
| Data09 | Beach congestion | `UNVERIFIED` | app's own citizen-report feed |
| Data10 | City congestion | `UNVERIFIED` | Google Maps (paid) + reports |
| Data11 | KTEL (bus) congestion | `UNVERIFIED` | operator telematics (no public link) |
| Data12 | Urban transit congestion | `UNVERIFIED` | operator telematics (no public link) |
| Data13 | Weather conditions | `VERIFIED` | Open-Meteo (Corfu point: 26.5 °C, RH 57 %, feels-like 28.8 °C) |
| Data14 | High UV and protection | `VERIFIED` | Open-Meteo `uv_index_max` (5.9) |
| Data15 | Air quality | `VERIFIED` | CAMS 2026-09-30: NO₂ 5.80 · PM10 7.40 · PM2.5 5.51 µg/m³ |
| Data16 | Tourism intensity (nights/residents) | `VERIFIED` | EL62 2023 = 97,705.5; peaked 2024 = 103,440 |
| Data17 | Hospital / infrastructure congestion | `UNVERIFIED` | official announcements + reports |
| Data18 | Power / water outage | `UNVERIFIED` | official announcements + reports |
| Data19 | Short-term rental share (Airbnb) | `VERIFIED` | platform share 2018-2025: 14.50 %→29.80 % (Eurostat `tour_ce_omn12`) |
| Data20 | Internet speed (>100 Mb/s) | `VERIFIED` | Ookla 2024-Q3 EL62: fixed 42.29 · mobile 107.48 Mbps download |
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
| `live` (streaming) | Data06, 08-12, 17, 18, 21, 34 | congestion, reports, outages - poll on interval |
| `daily` (forecast/sensor) | Data07, 13, 14, 15 | port-congestion forecast, weather/UV/air-quality forecasts |
| `quarterly` | Data20 | Ookla |
| `annual` (official stats) | Data02-04, 16, 19, 22, 25-33 | Eurostat/EEA - update on release (~mid-year N+1) |
| `on-change` (static/registers) | Data05, 23, 24 | EMAS/Ecolabel, cultural assets, protected land |
| `paused` | Data01 | CO₂ paused on accuracy |

**Freshest available data (as of 2026-10-20):**

- **Eurostat-direct (annual, current to 2025/26):** nights/arrivals 2025 · platform rental share 2018-2025 (`Data19`) · bed-places 2026 · intensity/density/foreign-share/length-of-stay 2025. These are the latest published.
- **EEA bathing water:** full series **1990-2024** (Greece 96.99 % excellent in 2024) and the EL62 2024 spatial join (**99.42 % excellent**, 100 % clean).
- **Ookla Open Data:** 2024-Q3 EL62 (fixed 42.29 Mbps · mobile 107.48 Mbps download).
- **Live/daily:** Data06 (2026-10-20 snapshot) · Data07 (anticipated forecast, 2026-10-14) · Data13/14 (current forecast) · Data15 (2026-09-30) · Data05 (current registers).
- **Dashboard-sourced (frozen at the 2024 release → 2023):** Data02 (EL62), Data23, Data25, Data28, Data29 (EL62). Data04 = 2024 (Blue Flag). These lag because the dashboard is an annual snapshot.
- **Static:** Data24 (NUTS 2021 / current Natura 2000).

**Gap to close (next pulls):** re-pull Data28/29 underlying Eurostat monthly data to 2024/25. Data22/23/25/32 are JRC dashboard computations - fresher values need the dashboard's next release or its underlying source.

### Master Data Access & Artifact Matrix (Team Quick-Navigation)

| ID | Indicator Name (EN / EL) | Status | Raw Pull / Sample Artifact | Curated Observation / Audit Path | Format & Protocol |
| --- | --- | --- | --- | --- | --- |
| **Data01** | Airport CO₂ levels (`Επίπεδα CO₂ αεροδρομίων`) | `PARTIAL` | `data/samples/cams-ionian-20260930-summary.json` | *(Proxy via Data15)* | NetCDF → Summary JSON (ADS API) |
| **Data02** | Excellent bathing waters (%) (`Άριστα νερά κολύμβησης`) | `VERIFIED` | `data/raw/eea-bwd-greece-2024.geojson` · `data/samples/eea-bathing-water-EL-1990-2024.json` | `data/curated/data02-bathing-water-el62-2024.json` · `observations-data02-bathing-water-2024.json` (2 obs) | Discomap GeoJSON + Spatial Join |
| **Data03** | Clean beach water (`Καθαρό νερό παραλίας`) | `VERIFIED` | `data/raw/eea-bwd-greece-2024.geojson` | `data/curated/observations-data02-bathing-water-2024.json` (1 obs) | Derived GeoJSON (EEA WISE BWD) |
| **Data04** | Blue Flags (`Γαλάζιες Σημαίες`) | `VERIFIED` | `data/samples/eutd-tourism-dashboard-2024-el62.json` | `data/curated/observations-2026-10-20.json` (1 obs) | CSV Export → Structured JSON |
| **Data05** | EMAS / EU Ecolabel (`EMAS / EU Ecolabel`) | `VERIFIED` | `data/samples/emas-register-greece-2026-10-02.json` · `data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json` | `data/manifests/source-verification-2026-10-02.json` | REST JSON + CSV→JSON |
| **Data06** | Airport congestion (`Συμφόρηση αεροδρομίων`) | `VERIFIED` | `data/raw/opensky-ionian-states-*.json` | `data/curated/data06-airport-congestion.json` · `observations-data06-airport-congestion-2026-10-20.json` (4 obs) | OpenSky REST JSON (`states` array) |
| **Data07** | Port congestion (`Συμφόρηση λιμένων`) | `PROPOSAL` | `scratch/cruise-pressure/schedules.json` · `scratch/ais-routes/export_sailing_traffic.csv` | `data/curated/scheduled-port-traffic-el62.json` · `data/curated/observations-data07-anticipated-congestion-2026-10-14.json` (366 obs) | Scraped JSON + NAP CSV → JSON |
| **Data08** | Road congestion (`Οδική συμφόρηση`) | `UNVERIFIED` | *(No pull artifact — paid API)* | *(None)* | Target: GeoJSON / Traffic Flow JSON |
| **Data09** | Beach congestion (`Συμφόρηση παραλιών`) | `UNVERIFIED` | *(No pull artifact — app feed)* | *(None)* | Target: App Citizen-Report JSON |
| **Data10** | City congestion (`Συμφόρηση πόλης`) | `UNVERIFIED` | *(No pull artifact — paid API / app)* | *(None)* | Target: Traffic Layer / Report JSON |
| **Data11** | KTEL (bus) congestion (`Συμφόρηση ΚΤΕΛ`) | `UNVERIFIED` | *(No pull artifact — partner feed)* | *(None)* | Target: GTFS-RT / Telematics JSON |
| **Data12** | Urban transit congestion (`Αστική συγκοινωνία`) | `UNVERIFIED` | *(No pull artifact — partner feed)* | *(None)* | Target: GTFS-RT / Telematics JSON |
| **Data13** | Weather conditions (`Καιρικές συνθήκες`) | `VERIFIED` | `data/samples/open-meteo-corfu-forecast-2026-09-22.json` | `data/curated/observations-2026-10-20.json` (3 obs) | Flat Forecast JSON (REST) |
| **Data14** | High UV & protection (`Υψηλή UV & προστασία`) | `VERIFIED` | `data/samples/open-meteo-corfu-forecast-2026-09-22.json` | `data/curated/observations-2026-10-20.json` (1 obs) | Flat Forecast JSON (REST) |
| **Data15** | Air quality (`Ποιότητα Αέρα`) | `VERIFIED` | `data/samples/cams-ionian-20260930-summary.json` | `data/manifests/source-verification-2026-10-01.json` | CAMS NetCDF → Summary JSON |
| **Data16** | Tourism intensity (`Τουριστική ένταση`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (2 obs) | Eurostat JSON-stat 2.0 (REST) |
| **Data17** | Hospital congestion (`Συμφόρηση νοσοκομείων`) | `UNVERIFIED` | *(No pull artifact — app/alerts)* | *(None)* | Target: Alert / Citizen-Report JSON |
| **Data18** | Power / water outage (`Διακοπές ρεύματος/νερού`) | `UNVERIFIED` | *(No pull artifact — HEDNO/DEYAK)* | *(None)* | Target: Outage Event JSON |
| **Data19** | Short-term rental share (`Μερίδιο βραχυχρόνιων μισθώσεων`) | `VERIFIED` | `data/raw/eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json` · `data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json` | `data/curated/data19-platform-rental-share.json` · `data/curated/observations-data19-platform-rental-share-2026-10-15.json` (8 obs) | Eurostat JSON-stat 2.0 (REST) |
| **Data20** | Internet speed (`Ταχύτητα διαδικτύου`) | `VERIFIED` | `data/raw/ookla-performance-fixed-2024Q3.zip` · `data/raw/ookla-performance-mobile-2024Q3.zip` | `data/curated/data20-internet-speed.json` · `observations-data20-internet-speed-2024Q3.json` (4 obs) | S3 Shapefile → Spatial Join JSON |
| **Data21** | 4G/5G availability (`Διαθεσιμότητα 4G/5G`) | `UNVERIFIED` | *(No pull artifact — app telemetry)* | *(None)* | Target: App Network-Signal JSON |
| **Data22** | Tourist diversity (`Τουριστική ποικιλομορφία`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin3-EL621-624-2021-2025.json` · `data/samples/derived-data22-data25-2021-2025.json` | `data/curated/observations-2026-10-20.json` (6 obs) | JSON-stat 2.0 → Derived HHI JSON |
| **Data23** | Density of cultural elements (`Πυκνότητα πολιτιστικών στοιχείων`) | `VERIFIED` | `data/samples/eutd-tourism-dashboard-2024-el62.json` | `data/curated/observations-2026-10-20.json` (1 obs) | CSV Export → Structured JSON |
| **Data24** | Protected land (%) (`Προστατευόμενη γη (%)`) | `VERIFIED` | `data/raw/eea-natura2000-el62-envelope-habitats-4326.geojson` · `data/raw/gisco-nuts-2021-3035-EL62.geojson` | `data/curated/data24-protected-land.json` · `data/curated/observations-2026-10-20.json` (1 obs) | ArcGIS GeoJSON → Spatial Join JSON |
| **Data25** | Accommodation in high-value areas (`Καταλύματα σε περιοχές υψηλής αξίας`) | `VERIFIED` | `data/samples/eutd-tourism-dashboard-2024-ionian.json` · `data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json` | `data/curated/observations-2026-10-20.json` (1 obs) | CSV/XLSX → Structured JSON |
| **Data26** | Arrivals & overnight stays (`Αφίξεις & διανυκτερεύσεις`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json` · `data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (4 obs) | Eurostat JSON-stat 2.0 (REST) |
| **Data27** | Tourism capacity (beds) (`Τουριστική δυναμικότητα - κλίνες`) | `VERIFIED` | `data/samples/eurostat-tour_cap_nuts2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (2 obs) | Eurostat JSON-stat 2.0 (REST) |
| **Data28** | Occupancy rate (%) (`Ποσοστό πληρότητας (%)`) | `VERIFIED` | `data/samples/eutd-tourism-dashboard-2024-el62.json` · `data/samples/derived-data28-occupancy-2021-2025.json` | `data/curated/observations-2026-10-20.json` (1 obs) | CSV Export → Structured JSON |
| **Data29** | Seasonality (%) (`Εποχικότητα (%)`) | `VERIFIED` | `data/samples/eutd-tourism-dashboard-2024-el62.json` · `data/samples/eurostat-tour_occ_nim-EL-2023.json` | `data/curated/observations-2026-10-20.json` (14 obs) | JSON-stat 2.0 + Dashboard JSON |
| **Data30** | Average length of stay (`Μέση διάρκεια παραμονής`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json` · `data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (2 obs) | Derived JSON (from JSON-stat 2.0) |
| **Data31** | Tourism density (nights/km²) (`Τουριστική πυκνότητα`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (2 obs) | Eurostat JSON-stat 2.0 (REST) |
| **Data32** | Dominant tourism typology (`Κυρίαρχη τυπολογία τουρισμού`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (1 obs) | Derived Categorical JSON |
| **Data33** | Foreign tourist share (%) (`Μερίδιο αλλοδαπών τουριστών`) | `VERIFIED` | `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json` | `data/curated/observations-2026-10-20.json` (2 obs) | Eurostat JSON-stat 2.0 (REST) |
| **Data34** | User feedback (`Αξιολογήσεις χρηστών`) | `UNVERIFIED` | *(No pull artifact — paid/privacy)* | *(None)* | Target: Anonymized Review JSON |

---

## 2 · Detailed history, data structures & visualizations (by indicator)

### Environmental Health & Pollutants - Περιβαλλοντική Υγεία & Ρύποι

#### Data01 · Airport CO₂ levels (`Επίπεδα CO₂ αεροδρομίων`) - `PARTIAL`

- **Source:** Copernicus CAMS (regional air quality) - `ads.atmosphere.copernicus.eu` · local IoT stations.
- **Data Pointers & Provenance:**
    - `Raw Pull Archive`: `data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip`
    - `Structured JSON Summary`: `data/samples/cams-ionian-20260930-summary.json`
    - `Curated Observation`: Deferred (NO₂/CO/PM proxies emitted under Data15)
    - `Manifest`: `data/manifests/source-verification-2026-10-01.json`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: CAMS Atmosphere Data Store (ADS) delivers multi-dimensional gridded NetCDF/GRIB2 files (`cams-europe-air-quality-forecasts`), which our pipeline extracts and transforms into a structured JSON summary (`cams-ionian-20260930-summary.json`).
    - `Target Features`: `corfu_airport.lat` (`39.65`), `corfu_airport.lon` (`19.95`), `values_ug_m3.NO2.at_corfu_airport`, `values_ug_m3.CO.at_corfu_airport`, `values_ug_m3.PM10.at_corfu_airport`, `values_ug_m3.PM2.5.at_corfu_airport`.
    - `Handling & Transformation`: Raw NetCDF grids over the Ionian bounding box (`37.0°–40.5°N, 19.0°–22.0°E`) at surface level (`0 m`) are sliced to extract the nearest grid cell to Corfu International Airport (`CFU`) alongside regional mean and max statistics. Because CAMS regional forecasts omit `CO2`, `NO2` and `CO` are retained as combustion proxies while point-level airport `CO2` awaits local IoT sensor integration.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>cams-ionian-20260930-summary.json</code>)</summary>
<pre><code class="language-json">{
    &quot;source&quot;: &quot;CAMS European air quality forecasts (ADS), ensemble analysis&quot;,
    &quot;date&quot;: &quot;2026-09-30T00:00:00Z&quot;,
    &quot;level&quot;: &quot;surface (0 m)&quot;,
    &quot;bbox&quot;: { &quot;north&quot;: 40.5, &quot;west&quot;: 19.0, &quot;south&quot;: 37.0, &quot;east&quot;: 22.0 },
    &quot;corfu_airport&quot;: { &quot;lat&quot;: 39.650001525878906, &quot;lon&quot;: 19.950000762939453 },
    &quot;values_ug_m3&quot;: {
      &quot;NO2&quot;:   { &quot;at_corfu_airport&quot;: 5.8,   &quot;region_max&quot;: 8.07,   &quot;region_mean&quot;: 1.96 },
      &quot;PM10&quot;:  { &quot;at_corfu_airport&quot;: 7.4,   &quot;region_max&quot;: 16.82,  &quot;region_mean&quot;: 8.99 },
      &quot;PM2.5&quot;: { &quot;at_corfu_airport&quot;: 5.51,  &quot;region_max&quot;: 10.11,  &quot;region_mean&quot;: 5.76 },
      &quot;CO&quot;:    { &quot;at_corfu_airport&quot;: 158.7, &quot;region_max&quot;: 182.74, &quot;region_mean&quot;: 158.14 }
    },
    &quot;note&quot;: &quot;CO2 is NOT a CAMS regional variable; nearest airport-level pollutants are NO2/PM10/PM2.5/CO.&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
CAMS Surface Pollutants @ Corfu Airport Grid Point (2026-09-30, µg/m³)
NO2    (Airport:   5.80 | Region Mean:   1.96 | Max:   8.07)  ██████████████······  [2.96x regional mean]
PM2.5  (Airport:   5.51 | Region Mean:   5.76 | Max:  10.11)  ███████████·········
PM10   (Airport:   7.40 | Region Mean:   8.99 | Max:  16.82)  █████████···········
CO     (Airport: 158.70 | Region Mean: 158.14 | Max: 182.74)  █████████████████···

```

- **Historical Log:**
    - **2026-09-22** - listed; source = Copernicus CAMS + local IoT (credential-gated).
    - **2026-10-01** - CAMS access verified via the Atmosphere Data Store (`cads-api-client`); pulled `cams-europe-air-quality-forecasts`. Finding: CAMS *regional* has **no CO₂ variable** - only NO₂/CO/PM at the surface. Working note: keep NO₂/CO as airport-emissions proxies; CO₂ deferred to CAMS global GHG (coarse) or local sensors. → `PARTIAL`.
    - **2026-10-03** - "actual CO₂" pull **paused on accuracy**: regional CAMS global GHG CO₂ (~0.75° grid) is too coarse for "airport CO₂ levels"; airport-local point CO₂ needs local sensors (the proposal's own "local IoT stations" source).

#### Data02 · Excellent bathing waters (%) (`Άριστα νερά κολύμβησης (%)`) - `VERIFIED`

- **Source:** EEA WISE Bathing Water (Discodata SQL) - `discodata.eea.europa.eu/sql` · CMEMS (secondary); cross-referenced with the EU Tourism Dashboard `TOUR_ENV_05`.
- **Data Pointers & Provenance:**
    - `Raw Sample (Multi-year SQL JSON)`: `data/samples/eea-bathing-water-EL-1990-2024.json`
    - `Raw Sample (2024 Breakdown)`: `data/samples/eea-bathing-water-quality-EL-2024.json`
    - `Raw Sample (Dashboard EL62)`: `data/samples/eutd-tourism-dashboard-2024-el62.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (35 annual EL observations 1990–2024 + 1 EL62 dashboard obs 2023 + 1 EL62 spatial-join obs 2024) · `data/curated/observations-data02-bathing-water-2024.json` (EL62 2024 spatial join)
    - `Manifest`: `data/manifests/source-verification-2026-09-24.json` · `data/manifests/source-verification-2026-10-03.json` · `data/manifests/source-verification-2026-10-20.json`
    - `ETL Script`: `scripts/verification/export_observations.py` · `scripts/verification/pull-data02-bathing-water-el62.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Discodata REST SQL API returns tabular JSON records grouped by `season` and `quality` from `[WISE_BWD].[latest].[assessment_BathingWaterStatus]`; the EU Tourism Dashboard CSV is transformed into structured JSON (`eutd-tourism-dashboard-2024-el62.json`) keyed by NUTS2 region (`el62.excellent_bathing_water`).
    - `Target Features`: `season` (year), `total` (monitored sites), `excellent` (sites rated Excellent), `pct_excellent` (`%`), and Dashboard `code="TOUR_ENV_05"`, `nuts_code_2021="EL62"`, `value` (`98.82`).
    - `Handling & Transformation`: For the national 35-year series, SQL aggregates counts per quality bucket for `countryCode='EL'` and computes `excellent / total * 100`. For regional NUTS2 (`EL62`), the pipeline ingests the pre-joined JRC Dashboard indicator `TOUR_ENV_05` (`98.82 %` in 2023), bypassing the missing NUTS2 column in raw WISE tables.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eea-bathing-water-EL-1990-2024.json</code> &amp; <code>eutd-tourism-dashboard-2024-el62.json</code>)</summary>
<pre><code class="language-json">{
    &quot;source&quot;: &quot;EEA WISE Bathing Water (Discodata SQL)&quot;,
    &quot;accessed_at&quot;: &quot;2026-10-03&quot;,
    &quot;country&quot;: &quot;EL&quot;,
    &quot;series&quot;: [
      { &quot;season&quot;: 1990, &quot;total&quot;: 613,  &quot;excellent&quot;: 136,  &quot;pct_excellent&quot;: 22.19 },
      { &quot;season&quot;: 2000, &quot;total&quot;: 1826, &quot;excellent&quot;: 1734, &quot;pct_excellent&quot;: 94.94 },
      { &quot;season&quot;: 2022, &quot;total&quot;: 1682, &quot;excellent&quot;: 1624, &quot;pct_excellent&quot;: 96.55 },
      { &quot;season&quot;: 2023, &quot;total&quot;: 1731, &quot;excellent&quot;: 1659, &quot;pct_excellent&quot;: 95.84 },
      { &quot;season&quot;: 2024, &quot;total&quot;: 1729, &quot;excellent&quot;: 1677, &quot;pct_excellent&quot;: 96.99 }
    ],
    &quot;el62_dashboard_reconciliation&quot;: {
      &quot;data_id&quot;: &quot;Data02&quot;,
      &quot;code&quot;: &quot;TOUR_ENV_05&quot;,
      &quot;year&quot;: 2023,
      &quot;unit&quot;: &quot;%&quot;,
      &quot;value&quot;: 98.82
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Excellent Bathing Water Share (%) — Greece 1990–2024 & EL62 Benchmark
1990 (EL)   22.19 %  ████▍···············  (136 / 613 sites)
1991 (EL)   68.55 %  █████████████▋······  (702 / 1,024 sites)
1995 (EL)   94.99 %  ███████████████████·  (1,440 / 1,516 sites)
2009 (EL)   60.47 %  ████████████········  (directive transition dip)
2015 (EL)   97.21 %  ███████████████████▍  (1,499 / 1,542 sites)
2020 (EL)   97.00 %  ███████████████████▍  (1,586 / 1,635 sites)
2021 (EL)   95.78 %  ███████████████████▏  (1,612 / 1,683 sites)
2022 (EL)   96.55 %  ███████████████████▎  (1,624 / 1,682 sites)
2023 (EL)   95.84 %  ███████████████████▏  (1,659 / 1,731 sites)
2024 (EL)   96.99 %  ███████████████████▍  (1,677 / 1,729 sites)
2023 (EL62) 98.82 %  ███████████████████▊  [Ionian Islands NUTS2 — TOUR_ENV_05]

```

| Year | Spatial Scope | Monitored Sites | Excellent Sites | Excellent Share (%) | Source |
| --- | --- | --- | --- | --- | --- |
| 2020 | Greece (`EL`) | 1,635 | 1,586 | **97.00 %** | EEA WISE Discodata SQL |
| 2021 | Greece (`EL`) | 1,683 | 1,612 | **95.78 %** | EEA WISE Discodata SQL |
| 2022 | Greece (`EL`) | 1,682 | 1,624 | **96.55 %** | EEA WISE Discodata SQL |
| 2023 | Greece (`EL`) | 1,731 | 1,659 | **95.84 %** | EEA WISE Discodata SQL |
| **2023** | **Ionian Islands (`EL62`)** | — | — | **98.82 %** | **EU Tourism Dashboard (`TOUR_ENV_05`)** |
| **2024** | **Greece (`EL`)** | **1,729** | **1,677** | **96.99 %** | **EEA WISE Discodata SQL** |

- **Historical Log:**
    - **2026-09-24** - resolved via the EEA Discodata SQL API (`[WISE_BWD].[latest].[assessment_BathingWaterStatus]`). Greece 2024: Excellent 1,677 / 1,729 = **96.99 %** of total (99.00 % of classified).
    - **2026-10-03** - **Key note (reconciliation):** *what:* adopted EL62 = **98.82 %** excellent bathing water (2023); *why:* the dashboard (the proposal's own source) publishes it at NUTS2, so the pending `bathingWaterIdentifier` spatial join is unnecessary; *how:* read `TOUR_ENV_05` from the 2024 dashboard CSV export.
    - **2026-10-03** - **Key note (freshness):** *what:* pulled the full Greece bathing-water series **1990-2024** (35 years) from Discodata SQL - 2024 = **96.99 %** excellent (latest assessed season, fresher than the dashboard's 2023); *how:* `SELECT season, quality, COUNT(*) … countryCode='EL' GROUP BY season, quality`.
    - **2026-10-20** - **Key note (EL62 spatial join):** *what:* closed the EL62 2024 gap via the official EEA Discomap 2024 GeoJSON layer-3 spatial join against GISCO EL62 (3 km coastal buffer) - **173 sites, 170 Excellent = 99.42 % of classified (98.27 % of total)**, 1 Good, 0 Sufficient, 0 Poor; *how:* `scripts/verification/pull-data02-bathing-water-el62.py` → `data/curated/observations-data02-bathing-water-2024.json`.

#### Data03 · Clean beach water (reports) (`Καθαρό νερό παραλίας (Reports)`) - `VERIFIED`

- **Source:** EEA WISE BWD (derived) · citizen reports (app's own feed).
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/eea-bathing-water-quality-EL-2024.json` · `data/raw/eea-bwd-greece-2024.geojson`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (2 observations: `EEA_WISE_BWD:Data03:clean_beach_share:2024` country · `EEA_BWD_Discomap_2024:Data03:clean_share_classified:EL62:2024`) · `data/curated/observations-data02-bathing-water-2024.json`
    - `Manifest`: `data/manifests/source-verification-2026-09-24.json` · `data/manifests/source-verification-2026-10-20.json`
    - `ETL Script`: `scripts/verification/export_observations.py` · `scripts/verification/pull-data02-bathing-water-el62.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: JSON array of quality classification counts from EEA Discodata SQL for Greece (`season=2024`).
    - `Target Features`: `qualityBathingWater` (`1 - Excellent`, `2 - Good`, `3 - Sufficient`, `4 - Poor`, `9 - Not classified`), `n` (site count).
    - `Handling & Transformation`: Under our documented `ASSUMPTION`, "clean beach water" is operationalized as any classified bathing site meeting at least EU minimum standards (`Excellent` + `Good` + `Sufficient`) divided by total classified sites (`(1677 + 16 + 0) / 1694 = 99.94 %`).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eea-bathing-water-quality-EL-2024.json</code>)</summary>
<pre><code class="language-json">[
    { &quot;qualityBathingWater&quot;: &quot;1 - Excellent&quot;,      &quot;n&quot;: 1677 },
    { &quot;qualityBathingWater&quot;: &quot;2 - Good&quot;,           &quot;n&quot;: 16   },
    { &quot;qualityBathingWater&quot;: &quot;4 - Poor&quot;,           &quot;n&quot;: 1    },
    { &quot;qualityBathingWater&quot;: &quot;9 - Not classified&quot;, &quot;n&quot;: 35   }
]
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Greece 2024 Classified Bathing Waters Breakdown (N = 1,694 classified; 35 unclassified)
1 - Excellent  (1,677 | 99.00 %)  ███████████████████▊
2 - Good       (   16 |  0.94 %)  ▏
4 - Poor       (    1 |  0.06 %)  ·
→ Derived Clean Flag (Excellent + Good + Sufficient): 1,693 / 1,694 = 99.94 %

```

- **Historical Log:**
    - **2026-09-24** - derived flag from Data02; "clean" = Excellent/Good/Sufficient (reversible default). Greece 2024: 99.94 % of classified.
    - **2026-10-20** - EL62 regional value added via the EEA Discomap 2024 spatial join: **100.0 % clean** (171/171 classified = Excellent + Good + Sufficient, 0 Poor) across 173 EL62 sites (`data/curated/observations-data02-bathing-water-2024.json`).

#### Data04 · Blue Flags (`Γαλάζιες Σημαίες`) - `VERIFIED`

- **Source:** Blue Flag programme (FEE) - `blueflag.global` · value from the EU Tourism Dashboard `TOUR_DES_10`.
- **Data Pointers & Provenance:**
    - `Raw Sample (EL62 Summary)`: `data/samples/eutd-tourism-dashboard-2024-el62.json`
    - `Raw Sample (Ionian Breakdown)`: `data/samples/eutd-tourism-dashboard-2024-ionian.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `51.0` sites in `EL62`, 2024)
    - `Manifest`: `data/manifests/source-verification-2026-10-03.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: The raw JRC EU Tourism Dashboard CSV (`2024_TourismDashboard_Indicators_Export.csv`) is filtered and converted into structured JSON (`eutd-tourism-dashboard-2024-el62.json` and `eutd-tourism-dashboard-2024-ionian.json`).
    - `Target Features`: `code="TOUR_DES_10"`, `nuts_code_2021` (`EL62`), `year` (`2024`), `value` (`51.0`), `unit` (`number`).
    - `Handling & Transformation`: Direct extraction of `TOUR_DES_10` for `EL62` (`year=2024`) into a schema-validated observation, bypassing `blueflag.global`'s interactive-only map constraint.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eutd-tourism-dashboard-2024-el62.json</code>)</summary>
<pre><code class="language-json">{
    &quot;source&quot;: &quot;EU Tourism Dashboard - 2024 release&quot;,
    &quot;dataset_id&quot;: &quot;9564824a-7f16-4efa-82fb-d4e176350026&quot;,
    &quot;el62&quot;: {
      &quot;blue_flag_sites&quot;: {
        &quot;data_id&quot;: &quot;Data04&quot;,
        &quot;code&quot;: &quot;TOUR_DES_10&quot;,
        &quot;year&quot;: 2024,
        &quot;unit&quot;: &quot;number&quot;,
        &quot;value&quot;: 51.0
      }
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Blue Flag Certified Sites in Ionian Islands (EL62, 2024)
EL62 Total: 51 certified sites  ████████████████████

```

- **Historical Log:**
    - **2026-09-24** - `blueflag.global` confirmed reachable (HTTP 200) but interactive-only.
    - **2026-10-01** - no clean machine-readable list of certified sites from the global site. Recorded as an access constraint.
    - **2026-10-03** - **Key note (reconciliation):** *what:* resolved to **51 Blue Flag sites in EL62** (2024); *why:* the dashboard publishes the count directly, avoiding the national-operator list we couldn't extract; *how:* read `TOUR_DES_10` from the 2024 dashboard CSV export. → `VERIFIED`.

#### Data05 · EMAS / EU Ecolabel (`EMAS / EU Ecolabel`) - `VERIFIED`

- **Source:** EMAS register (REST) + EU Ecolabel catalogue (CSV) - European Commission.
- **Data Pointers & Provenance:**
    - `Raw Sample (EMAS JSON)`: `data/samples/emas-register-greece-2026-10-02.json`
    - `Raw Sample (EU Ecolabel JSON)`: `data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json`
    - `Curated Observation`: Recorded as verified zero-counts in manifest (`EL62 = 0 EMAS · 0 accommodation ecolabels`)
    - `Manifest`: `data/manifests/source-verification-2026-10-02.json`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: EMAS returns a native REST JSON array of registered organizations (`registration/list`); the EU Ecolabel catalogue is published as an 89,298-row CSV export which we parse and transform into a structured JSON audit (`eu-ecolabel-catalogue-greece-2026-10-02.json`).
    - `Target Features`: EMAS: `organisationCountryName` (`Greece`), `city`, `postalCode`, `nacesAsString`. EU Ecolabel: country filter (`Greece`), product group (`Tourist accommodation`), licence counts.
    - `Handling & Transformation`: Filtered the 4,523 EMAS records to Greece (`37` records) and matched against Ionian Islands (`EL62`) postal prefixes (`49xxx`, `28xxx`, `29xxx`, `31xxx`) and island city names (`0` matches). Filtered the 89,298 EU Ecolabel licences to Greece (`450` licences across industrial/consumer goods; `0` in the `Tourist accommodation` group).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>emas-register-greece-2026-10-02.json</code> &amp; <code>eu-ecolabel-catalogue-greece-2026-10-02.json</code>)</summary>
<pre><code class="language-json">{
    &quot;emas_summary&quot;: {
      &quot;source_id&quot;: &quot;EMAS_register_REST&quot;,
      &quot;total_records&quot;: 4523,
      &quot;greece_records&quot;: 37,
      &quot;ionian_islands_el62_records&quot;: 0
    },
    &quot;ecolabel_summary&quot;: {
      &quot;source_id&quot;: &quot;EU_Ecolabel_catalogue_CSV&quot;,
      &quot;total_licences&quot;: 89298,
      &quot;greece_licences&quot;: 450,
      &quot;greece_group_breakdown&quot;: {
        &quot;Decorative paints, varnishes, and related products (2014 criteria)&quot;: 400,
        &quot;Lubricants&quot;: 32,
        &quot;Hard Surface Cleaning Products&quot;: 8,
        &quot;Bed mattresses&quot;: 5,
        &quot;Textile products&quot;: 3,
        &quot;Hand dishwashing detergents&quot;: 2
      },
      &quot;tourist_accommodation_group&quot;: { &quot;total&quot;: 1009, &quot;greece&quot;: 0 }
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
EMAS & EU Ecolabel Distribution (2026-10-02 Verification)
EU Total Licences (Ecolabel) : 89,298  ████████████████████
EU Tourist Accomm. Ecolabels :  1,009  ██▎·················
Greece Total Ecolabels       :    450  █··················· (Paints: 400, Lubricants: 32, Other: 18)
Greece EMAS Organisations    :     37  ▏···················
EL62 Ionian EMAS / Ecolabels :      0  ···················· [Verified 0]

```

- **Historical Log:**
    - **2026-10-02** - both registers pull-tested: EMAS register REST (4,523 records / 27 countries) and EU Ecolabel CSV (89,298 licences). **EL62: 0 EMAS · 0 tourist-accommodation ecolabels** (Greece 37 EMAS · 450 ecolabels). Moved `PARTIAL` → `VERIFIED`.

### Dynamic Congestion - Δυναμική Συμφόρηση (Real-time & Forecast)

#### Data06 · Airport congestion (`Συμφόρηση αεροδρομίων`) - `VERIFIED`

- **Source:** OpenSky Network (free, no-key) - `opensky-network.org/api` · FlightRadar24 (paid fallback).
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/opensky-ionian-states-20261002-113332.json` · `data/raw/opensky-ionian-states-*.json`
    - `Curated Observation`: `data/curated/data06-airport-congestion.json` · `data/curated/observations-data06-airport-congestion-2026-10-20.json` (4 obs, CFU/ZTH/EFL/PVK)
    - `Manifest`: `data/manifests/source-verification-2026-10-20.json`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: OpenSky `/api/states/all` returns a JSON object with `time` (Unix epoch) and `states` (an array of positional state-vector arrays for each detected aircraft within the bounding box `lamin=37.0, lomin=19.0, lamax=40.5, lomax=22.0`).
    - `Target Features`: Positional indices per state vector: `[0]` `icao24`, `[1]` `callsign`, `[2]` `origin_country`, `[5]` `longitude`, `[6]` `latitude`, `[7]` `baro_altitude` (m), `[8]` `on_ground`, `[9]` `velocity` (m/s).
    - `Handling & Transformation`: State vectors are filtered spatially to a circular buffer (25 km radius) around each Ionian gateway airport (`CFU` Corfu, `ZTH` Zakynthos, `EFL` Kefalonia, `PVK` Aktion/Lefkada) and vertically (`baro_altitude <= 3000 m` or `on_ground == true`) to isolate arrivals/departures from high-altitude cruise overflights (`>10,000 m`), then scored via `S = min(1, aircraft_in_approach_buffer / threshold)`.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>opensky-ionian-states-20261002-113332.json</code>)</summary>
<pre><code class="language-json">{
    &quot;time&quot;: 1790929987,
    &quot;states&quot;: [
      [&quot;39de51&quot;, &quot;TVF99PC &quot;, &quot;France&quot;,     1790929986, 1790929986, 21.3140, 38.4810, 11887.20, false, 239.02, 127.22, 0.33, null, 12108.18, &quot;0675&quot;, false, 0],
      [&quot;46b82b&quot;, &quot;AEE616  &quot;, &quot;Greece&quot;,     1790929986, 1790929986, 21.6210, 38.9637, 10363.20, false, 226.45, 303.04, 0.00, null, 10599.42, &quot;2022&quot;, false, 0],
      [&quot;5001e3&quot;, &quot;MEA241  &quot;, &quot;San Marino&quot;, 1790929890, 1790929890, 19.2460, 39.9485, 10363.20, false, 227.74, 300.10, 0.00, null, 10675.62, &quot;5652&quot;, false, 0]
    ]
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
OpenSky Live Airspace Snapshot — Ionian Bounding Box (2026-10-02 11:33 UTC)
Total Aircraft in Bbox (37.0–40.5°N, 19.0–22.0°E) : 17  █████████████████
High-Altitude Overflights (>10,000 m cruise)      : 17  █████████████████
Airport Approach / Terminal Buffer (<3,000 m)     :  0  ·················

```

- **Historical Log:**
    - **2026-09-26** - OpenSky Network free REST (`/api/states/all`, no key) returned live aircraft states over the Ionian Islands.
    - **2026-10-02** - live snapshot: 17 aircraft in the Ionian bbox, all overflights, 0 in airport approach. Kept `PARTIAL`: the congestion *score* (count-in-buffer → score) is still a candidate formula and the feed is live-only.
    - **2026-10-03** - **Key note (research):** *what:* surveyed reputable congestion definitions; *found:* the standard European air-congestion metric is **EUROCONTROL ATFM delay** (minutes of delay per flight / airport punctuality - `eurocontrol.int`); *proposed for us (no free airport ATFM feed):* a live proxy - congestion score = `min(1, aircraft-in-approach-buffer ÷ threshold)`, reported as low/medium/high. Flag: score formula remains a proposal (live-only).
    - **2026-10-20** - **Key note (implementation):** *what:* built `scripts/verification/pull-data06-airport-congestion.py` implementing the approach-buffer scoring model across CFU (cap 4), ZTH (cap 3), EFL (cap 3), and PVK (cap 3); *why:* operationalises live airport congestion without paid APIs; *how:* calculates haversine distance to each runway threshold, filters alt $\le 3,000$ m, computes score $S = \min(1, N / \text{threshold})$ with low/medium/high classification. Emitted `data06-airport-congestion.json` and 4 instant observations. Moved `PARTIAL` → `VERIFIED`.

#### Data07 · Port congestion (`Συμφόρηση λιμένων`) - `PROPOSAL`

- **Source (model):** CruiseMapper cruise schedules (one-time read; `scratch/cruise-pressure/schedules.json`) + Greek National Access Point sailing-traffic export (`scratch/ais-routes/export_sailing_traffic.csv`, Mar–Nov 2025) → `scripts/verification/compute-data07-anticipated-congestion.py`. *Superseded live sources:* aisstream.io · EMODnet Human Activities · MarineTraffic AIS.
- **Data Pointers & Provenance:**
    - `Raw Input (Cruise Schedules JSON)`: `scratch/cruise-pressure/schedules.json`
    - `Raw Input (Greek NAP Ferry CSV)`: `scratch/ais-routes/export_sailing_traffic.csv`
    - `Superseded Live Samples`: `data/samples/aisstream-corfu-positionreports-20261002-085847.json` · `data/samples/emodnet-vesseldensity-ionian-ports-2026-10-02.json`
    - `Curated Master Timetable & Audit JSON`: `data/curated/scheduled-port-traffic-el62.json`
    - `Curated Forecast Observations`: `data/curated/observations-data07-anticipated-congestion-2026-10-14.json` / `.csv` (366 daily observations, 2026-10-01 to 2026-11-30)
    - `Manifest`: `data/manifests/source-verification-2026-10-14.json` · `data/manifests/source-verification-2026-10-02-dynamic.json`
    - `ETL Script`: `scripts/verification/compute-data07-anticipated-congestion.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Combines a structured JSON scrape of port cruise calls (`ports[].calls[]{date, ship, arrival, departure}`) and a 184,436-row CSV of domestic ferry legs (`export_sailing_traffic.csv`), which the ETL transforms into a unified JSON master timetable (`scheduled-port-traffic-el62.json`) and 366 schema-valid observation objects.
    - `Target Features`: Cruise JSON: `port.id`, `calls[].date`, `calls[].ship`. Ferry CSV: `arrivalport` (`CFU`, `LFK`, `PKE`, `SAI`, `FIS`, `ZTH`, `VSS`, `LEV`, `PAX`, `PIS`), `date`, `passengercount`, `vehiclecount`. Derived JSON: `n_cruise_ships`, `cruise_pax_est`, `ferry_pax_baseline`, `ferry_veh_baseline`, `score`, `level`.
    - `Handling & Transformation`: Non-JSON ferry leg rows from the Greek NAP CSV are grouped by EL62 island port and date to establish empirical month + day-of-week passenger (`L_ferry_pax`) and vehicle (`L_ferry_veh`) baselines. These are combined with scheduled cruise ship counts (`N_ships`) and estimated cruise passengers (`L_cruise = 2,500 × N_ships`) into the composite score:
    `S(P,D) = min(1, 0.4·N_ships/B_max + 0.4·(L_cruise + L_ferry_pax)/C_pax + 0.2·L_ferry_veh/C_veh)`.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>scheduled-port-traffic-el62.json</code>)</summary>
<pre><code class="language-json">{
    &quot;title&quot;: &quot;Scheduled port traffic (EL62) — master timetable for Data07 anticipated congestion&quot;,
    &quot;indicator_id&quot;: &quot;Data07&quot;,
    &quot;status&quot;: &quot;PROPOSAL&quot;,
    &quot;method&quot;: &quot;S(P,D) = min(1, w_berth*N_ships/B_max + w_pax*(L_cruise+L_ferry_pax)/C_pax + w_veh*L_ferry_veh/C_veh)&quot;,
    &quot;assumptions&quot;: {
      &quot;weights&quot;: { &quot;berth&quot;: 0.4, &quot;pax&quot;: 0.4, &quot;veh&quot;: 0.2 },
      &quot;cruise_pax_default_per_call&quot;: 2500,
      &quot;capacities&quot;: {
        &quot;corfu&quot;:     { &quot;berth&quot;: 5, &quot;pax_per_day&quot;: 12000, &quot;veh_per_day&quot;: 1800 },
        &quot;kefalonia&quot;: { &quot;berth&quot;: 2, &quot;pax_per_day&quot;: 4500,  &quot;veh_per_day&quot;: 900  },
        &quot;zakynthos&quot;: { &quot;berth&quot;: 2, &quot;pax_per_day&quot;: 5000,  &quot;veh_per_day&quot;: 1000 }
      }
    },
    &quot;peak_examples&quot;: [
      { &quot;port&quot;: &quot;corfu&quot;,     &quot;date&quot;: &quot;2026-10-08&quot;, &quot;n_cruise&quot;: 5, &quot;score&quot;: 0.983, &quot;level&quot;: &quot;high&quot; },
      { &quot;port&quot;: &quot;kefalonia&quot;, &quot;date&quot;: &quot;2026-10-01&quot;, &quot;n_cruise&quot;: 2, &quot;score&quot;: 0.945, &quot;level&quot;: &quot;high&quot; }
    ]
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Anticipated Port Congestion Distribution Across 6 EL62 Ports (Oct–Nov 2026, N = 366 port-days)
Low    (< 0.50)    : 342 port-days (93.4 %)  ██████████████████▋
Medium (0.50–0.84) :  21 port-days ( 5.7 %)  █▏·················
High   (>= 0.85)   :   3 port-days ( 0.8 %)  ▏··················

Peak Forecast Congestion Scores S(P,D) by Island Port (Oct–Nov 2026)
Corfu      (Peak 2026-10-08: 5 cruise calls + ferry baseline)  S = 0.983  ███████████████████▋ [HIGH]
Kefalonia  (Peak 2026-10-01: 2 cruise calls + ferry baseline)  S = 0.945  ██████████████████▉· [HIGH]
Zakynthos  (Peak Oct 2026:   1 cruise call  + ferry baseline)  S = 0.612  ████████████▏······· [MEDIUM]
Lefkada    (Peak Oct 2026:   1 cruise call  + ferry baseline)  S = 0.520  ██████████▍········· [MEDIUM]
Paxos      (Ferry baseline only, 0 cruise calls)               S = 0.215  ████▎··············· [LOW]
Ithaki     (Ferry baseline only, 0 cruise calls)               S = 0.198  ████················ [LOW]

```

| Port (`EL62`) | NAP Codes | Oct–Nov Cruise Calls | Mean Daily Ferry PAX | Mean Daily Ferry VEH | Peak Score `S(P,D)` | Peak Level |
| --- | --- | --- | --- | --- | --- | --- |
| **Corfu** | `CFU`, `LFK` | 91 | 3,558.5 | 1,030.3 | **0.983** (`2026-10-08`) | `high` |
| **Kefalonia** | `PKE`, `SAI`, `FIS` | 18 | 1,475.6 | 508.2 | **0.945** (`2026-10-01`) | `high` |
| **Zakynthos** | `ZTH` | 3 | 1,893.9 | 578.7 | **0.612** | `medium` |
| **Lefkada** | `VSS`, `LEV` | 2 | 156.1 | 42.0 | **0.520** | `medium` |
| **Paxos** | `PAX` | 0 | 475.1 | 76.1 | **0.215** | `low` |
| **Ithaki** | `PIS` | 0 | 307.9 | 107.6 | **0.198** | `low` |

- **Historical Log:**
    - **2026-09-26** - free AIS candidates identified: `aisstream.io` (crowd-sourced stream) and EMODnet vessel density (authoritative, free).
    - **2026-10-02** - live AIS snapshot: 1 vessel in Corfu port bbox (moored, SOG 0). EMODnet density baseline pulled (Corfu 352 / Zakynthos 170 / Kefalonia 227 hrs/km²/yr). Kept `PARTIAL` (score formula + live-only).
    - **2026-10-03** - **Key note (research):** *what:* surveyed reputable port-congestion definitions; *found:* the standard metrics are the **World Bank Container Port Performance Index** (minutes per container move) and **UNCTAD median time in port** (vessel turnaround/waiting); *proposed for us (free AIS only):* a live proxy - congestion score = `min(1, vessels-in-port-buffer ÷ threshold)`. Flag: score formula remains a proposal (live-only).
    - **2026-10-14** - **Key note (transition to Anticipated Congestion):** *what:* `DECISION` — live AIS is **excluded** from Data07 (zero receiver coverage in Corfu harbour, proven 2026-10-14; live feeds give snapshots only, no forecasting). *why:* anticipated congestion from scheduled itineraries gives forward-looking load (t+1 day → t+6 months) and removes daemon/scraper maintenance; port-city pressure is driven by passenger/vehicle throughput, which timetables + capacity declarations quantify directly (research-notes 2026-10-15 §1). *how:* promoted the `scratch/cruise-pressure` prototype into `scripts/verification/compute-data07-anticipated-congestion.py`, computing `S(P,D)=min(1, 0.4·N_ships/B_max + 0.4·(L_cruise+L_ferry_pax)/C_pax + 0.2·L_ferry_veh/C_veh)` per EL62 port per day (Corfu/Kefalonia/Zakynthos/Lefkada/Paxos/Ithaki). Emitted `data/curated/scheduled-port-traffic-el62.json` + 366 schema-compliant forecast observations (2026-10-01→11-30: low 342 · medium 21 · high 3; peaks Corfu 2026-10-08 S=0.983, Kefalonia 2026-10-01 S=0.945). Weights, capacities and per-call cruise PAX (2,500) are `PROPOSAL`/`ASSUMPTION` defaults → `PROPOSAL`.

#### Data08 · Road congestion (`Οδική συμφόρηση`) - `UNVERIFIED`

- **Source:** Google Maps Platform (paid, live traffic) · OpenRouteService (free tier, routing-only).
- **Data Pointers & Provenance:** No pull artifact present (commercial API key required for live traffic; OpenRouteService verified as static routing-only).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: When commercial or municipal traffic feeds are connected, payloads will be normalized to JSON containing `corridor_id`, `island_nuts3`, `free_flow_travel_time_sec`, `current_travel_time_sec`, and `delay_ratio`.
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data08&quot;,
    &quot;corridor_id&quot;: &quot;CFU-AIRPORT-TOWN&quot;,
    &quot;observed_at&quot;: &quot;YYYY-MM-DDTHH:MM:SSZ&quot;,
    &quot;free_flow_sec&quot;: 480,
    &quot;current_sec&quot;: 780,
    &quot;congestion_index&quot;: 1.625
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.
- **Historical Log:**
    - **2026-09-26** - no free **live** traffic source (TomTom/HERE/Google all paid); OpenRouteService free tier is routing-only.

#### Data09 · Beach congestion (`Συμφόρηση παραλιών`) - `UNVERIFIED`

- **Source:** citizen reports (app's own feed).
- **Data Pointers & Provenance:** No pull artifact present (internal application telemetry / citizen reports).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Anonymized, k-thresholded citizen crowdsourcing payload (`beach_id`, `nuts3`, `time_bucket`, `report_count`, `median_crowding_level_1_5`).
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data09&quot;,
    &quot;beach_id&quot;: &quot;EL622-PALEOKASTRITSA&quot;,
    &quot;time_bucket&quot;: &quot;YYYY-MM-DDTHH:00:00Z&quot;,
    &quot;report_count&quot;: 12,
    &quot;crowding_score_0_1&quot;: 0.75
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

#### Data10 · City congestion (`Συμφόρηση πόλης`) - `UNVERIFIED`

- **Source:** Google Maps traffic layer (paid) + citizen reports.
- **Data Pointers & Provenance:** No pull artifact present (hybrid paid API + app citizen feed).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Zone-aggregated urban congestion payload combining travel-time delay ratios and anonymized citizen crowding reports.
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data10&quot;,
    &quot;zone_id&quot;: &quot;CFU-OLD-TOWN&quot;,
    &quot;observed_at&quot;: &quot;YYYY-MM-DDTHH:MM:SSZ&quot;,
    &quot;traffic_delay_ratio&quot;: 1.45,
    &quot;citizen_crowding_level&quot;: &quot;medium&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

### Sustainable Transport - Βιώσιμες Μεταφορές

#### Data11 · KTEL (bus) congestion (`Συμφόρηση ΚΤΕΛ`) - `UNVERIFIED`

- **Source:** KTEL operator telematics (no public link).
- **Data Pointers & Provenance:** No pull artifact present (requires partner telematics/ticketing agreement with regional KTEL operators).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Route-level load factor JSON (`route_id`, `departure_time`, `seated_capacity`, `tickets_sold`, `occupancy_ratio`).
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data11&quot;,
    &quot;operator&quot;: &quot;KTEL_KERKYRAS&quot;,
    &quot;route_id&quot;: &quot;GREEN-A1&quot;,
    &quot;observed_at&quot;: &quot;YYYY-MM-DDTHH:MM:SSZ&quot;,
    &quot;occupancy_pct&quot;: 88.5
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

#### Data12 · Urban transit congestion (`Αστική συγκοινωνία`) - `UNVERIFIED`

- **Source:** local transport telematics (no public link).
- **Data Pointers & Provenance:** No pull artifact present (requires municipal bus telematics integration).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Municipal bus line occupancy and schedule adherence JSON (`line_id`, `vehicle_id_hash`, `headway_delay_sec`, `load_level`).
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data12&quot;,
    &quot;operator&quot;: &quot;ASTIKO_KTEL_KERKYRAS&quot;,
    &quot;line_id&quot;: &quot;LINE-2A-KANONI&quot;,
    &quot;observed_at&quot;: &quot;YYYY-MM-DDTHH:MM:SSZ&quot;,
    &quot;load_level&quot;: &quot;high&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

### Climate Adaptation - Κλιματική Προσαρμογή

#### Data13 · Weather conditions (`Καιρικές συνθήκες`) - `VERIFIED`

- **Source:** Open-Meteo (no-key substitute) - `api.open-meteo.com` · proposal cites OpenWeatherMap / Meteo.gr.
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/open-meteo-corfu-forecast-2026-09-22.json`
    - `Annotated Report`: `data/samples/open-meteo-corfu-forecast-2026-09-22.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (3 observations: air temperature, relative humidity, apparent temperature)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json`
    - `ETL Script`: `scripts/verification/pull-open-meteo.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Flat REST JSON returned by `/v1/forecast` containing coordinate metadata, `current_units`, `current` meteorological state object, `daily_units`, and `daily` arrays.
    - `Target Features`: `current.time`, `current.temperature_2m` (`°C`), `current.relative_humidity_2m` (`%`), `current.apparent_temperature` (`°C`).
    - `Handling & Transformation`: Direct extraction of each meteorological key in `current`, pairing values with their corresponding unit strings from `current_units` and binding spatial reference to the queried island point (`39.62,19.92` Corfu).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>open-meteo-corfu-forecast-2026-09-22.json</code>)</summary>
<pre><code class="language-json">{
    &quot;latitude&quot;: 39.625,
    &quot;longitude&quot;: 19.875,
    &quot;timezone&quot;: &quot;Europe/Athens&quot;,
    &quot;elevation&quot;: 16.0,
    &quot;current_units&quot;: {
      &quot;time&quot;: &quot;iso8601&quot;,
      &quot;interval&quot;: &quot;seconds&quot;,
      &quot;temperature_2m&quot;: &quot;°C&quot;,
      &quot;relative_humidity_2m&quot;: &quot;%&quot;,
      &quot;apparent_temperature&quot;: &quot;°C&quot;
    },
    &quot;current&quot;: {
      &quot;time&quot;: &quot;2026-09-22T14:15&quot;,
      &quot;interval&quot;: 900,
      &quot;temperature_2m&quot;: 26.5,
      &quot;relative_humidity_2m&quot;: 57,
      &quot;apparent_temperature&quot;: 28.8
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Open-Meteo Verified Point Snapshot — Corfu (2026-09-22T14:15 EEST)
Air Temperature (2m)      : 26.5 °C  █████████████▎······  (scale 0–40 °C)
Apparent (Feels-Like)     : 28.8 °C  ██████████████▍·····  (+2.3 °C humidity effect)
Relative Humidity (2m)    : 57.0 %   ███████████▍········  (scale 0–100 %)

```

- **Historical Log:**
    - **2026-09-22** - Open-Meteo verified at the Corfu point.

#### Data14 · High UV and protection (`Υψηλή UV και προστασία`) - `VERIFIED`

- **Source:** Open-Meteo `daily.uv_index_max` - `api.open-meteo.com`.
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/open-meteo-corfu-forecast-2026-09-22.json`
    - `Annotated Report`: `data/samples/open-meteo-corfu-forecast-2026-09-22.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `uv_index_max = 5.9`)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json`
    - `ETL Script`: `scripts/verification/pull-open-meteo.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Nested `daily` block inside the Open-Meteo `/v1/forecast` JSON response, storing parallel arrays of `time` (ISO dates) and `uv_index_max`.
    - `Target Features`: `daily.time[0]` (`2026-09-22`), `daily.uv_index_max[0]` (`5.90`).
    - `Handling & Transformation`: Zips `daily.time` with `daily.uv_index_max` to emit daily UV peak observations, which map directly to WHO UV protection bands (`0–2 Low`, `3–5 Moderate`, `6–7 High`, `8–10 Very High`, `11+ Extreme`).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>open-meteo-corfu-forecast-2026-09-22.json</code> — daily block)</summary>
<pre><code class="language-json">{
    &quot;daily_units&quot;: {
      &quot;time&quot;: &quot;iso8601&quot;,
      &quot;uv_index_max&quot;: &quot;&quot;
    },
    &quot;daily&quot;: {
      &quot;time&quot;: [&quot;2026-09-22&quot;],
      &quot;uv_index_max&quot;: [5.90]
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Daily Max UV Index — Corfu (2026-09-22)
UV Index Max : 5.90  ██████████▊·········  [Upper Moderate / Borderline High — WHO Protection Recommended]
Scale        : 0 ── 2 (Low) ── 5 (Mod) ── 7 (High) ── 10 (V.High) ── 11+ (Extreme)

```

- **Historical Log:**
    - **2026-09-22** - Open-Meteo `daily.uv_index_max` verified.

#### Data15 · Air quality (`Ποιότητα Αέρα`) - `VERIFIED`

- **Source:** Copernicus CAMS (ambient air quality) - `ads.atmosphere.copernicus.eu` · OpenWeatherMap / Meteo.gr.
- **Data Pointers & Provenance:**
    - `Raw Pull Archive`: `data/samples/cams-europe-air-quality-forecasts-IONIAN-2026-09-30.zip`
    - `Structured JSON Summary`: `data/samples/cams-ionian-20260930-summary.json`
    - `Catalogue Sample`: `data/samples/copernicus-cdse-catalogue-top1.json`
    - `Manifest`: `data/manifests/source-verification-2026-10-01.json`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Multi-variable surface air-quality NetCDF from CAMS European ensemble analysis, transformed into structured JSON (`cams-ionian-20260930-summary.json`) reporting point and bbox statistics in `µg/m³`.
    - `Target Features`: `values_ug_m3.NO2`, `values_ug_m3.PM10`, `values_ug_m3.PM2.5`, `values_ug_m3.CO` (each with `at_corfu_airport`, `region_mean`, `region_max`).
    - `Handling & Transformation`: Decodes CAMS NetCDF variables at `level = 0 m` for the Ionian Islands domain (`37.0°–40.5°N, 19.0°–22.0°E`), computes spatial mean/max across grid cells, and compares against WHO/EU 24-hour ambient air quality thresholds.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>cams-ionian-20260930-summary.json</code>)</summary>
<pre><code class="language-json">{
    &quot;source&quot;: &quot;CAMS European air quality forecasts (ADS), ensemble analysis&quot;,
    &quot;date&quot;: &quot;2026-09-30T00:00:00Z&quot;,
    &quot;level&quot;: &quot;surface (0 m)&quot;,
    &quot;values_ug_m3&quot;: {
      &quot;NO2&quot;:   { &quot;at_corfu_airport&quot;: 5.8,   &quot;region_max&quot;: 8.07,   &quot;region_mean&quot;: 1.96 },
      &quot;PM10&quot;:  { &quot;at_corfu_airport&quot;: 7.4,   &quot;region_max&quot;: 16.82,  &quot;region_mean&quot;: 8.99 },
      &quot;PM2.5&quot;: { &quot;at_corfu_airport&quot;: 5.51,  &quot;region_max&quot;: 10.11,  &quot;region_mean&quot;: 5.76 },
      &quot;CO&quot;:    { &quot;at_corfu_airport&quot;: 158.7, &quot;region_max&quot;: 182.74, &quot;region_mean&quot;: 158.14 }
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
CAMS Ambient Air Quality vs EU / WHO 24h Reference Limits (2026-09-30, µg/m³)
NO2   :  5.80 µg/m³ (WHO 24h limit: 25 µg/m³)  ████▋···············  [23.2 % of limit — GOOD]
PM2.5 :  5.51 µg/m³ (WHO 24h limit: 15 µg/m³)  ███████▎············  [36.7 % of limit — GOOD]
PM10  :  7.40 µg/m³ (WHO 24h limit: 45 µg/m³)  ███▎················  [16.4 % of limit — GOOD]
CO    : 158.7 µg/m³ (WHO 24h limit: 4000 µg/m³)▊···················  [ 4.0 % of limit — GOOD]

```

- **Historical Log:**
    - **2026-09-22** - Copernicus CDSE catalogue reachable (download gated).
    - **2026-10-01** - verified via CAMS ensemble analysis (surface) over the Ionian Islands for 2026-09-30: NO₂ 5.80 · PM10 7.40 · PM2.5 5.51 · CO 158.70 µg/m³ at the Corfu-airport grid point. Duplicate "Data15" resolved: Data15 = ambient air quality.

### Social Pressure & Infrastructure - Κοινωνική Πίεση & Υποδομές

#### Data16 · Tourism intensity (nights/residents) (`Τουριστική ένταση`) - `VERIFIED`

- **Source:** Eurostat `tour_occ_nin2` (unit `P_THAB`) - `ec.europa.eu/eurostat`.
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
    - `Annotated Report`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (2 base observations: 2022 & 2023; extended series verified to 2025)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json` · `data/manifests/source-verification-2026-10-01.json`
    - `ETL Script`: `scripts/verification/pull-eurostat-tourism.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Eurostat JSON-stat 2.0 (`version: "2.0", class: "dataset"`), where values are stored in a flat dictionary indexed by linear row-major offsets across `id: ["freq", "c_resid", "unit", "nace_r2", "geo", "time"]`.
    - `Target Features`: Dimensions `freq="A"`, `c_resid="TOTAL"`, `unit="P_THAB"` (Nights spent per thousand inhabitants), `nace_r2="I551-I553"` (Hotels, holiday/short-stay accommodation, camping), `geo="EL62"`, `time` (`2022`, `2023`, `2024`, `2025`).
    - `Handling & Transformation`: The JSON-stat decoder computes the flat integer key from the coordinate tuple `(A, TOTAL, P_THAB, I551-I553, EL62, year)` using the stride array `size` and emits one annual observation per year in nights per 1,000 residents (divide by 1,000 for nights per resident).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eurostat-tour_occ_nin2-EL62-2022-2023.json</code> — JSON-stat slice)</summary>
<pre><code class="language-json">{
    &quot;version&quot;: &quot;2.0&quot;,
    &quot;class&quot;: &quot;dataset&quot;,
    &quot;label&quot;: &quot;Nights spent at tourist accommodation establishments by NUTS 2 region&quot;,
    &quot;source&quot;: &quot;ESTAT&quot;,
    &quot;id&quot;: [&quot;freq&quot;, &quot;c_resid&quot;, &quot;unit&quot;, &quot;nace_r2&quot;, &quot;geo&quot;, &quot;time&quot;],
    &quot;dimension&quot;: {
      &quot;c_resid&quot;: { &quot;category&quot;: { &quot;index&quot;: { &quot;TOTAL&quot;: 2 } } },
      &quot;unit&quot;:    { &quot;category&quot;: { &quot;index&quot;: { &quot;P_THAB&quot;: 3 }, &quot;label&quot;: { &quot;P_THAB&quot;: &quot;Per thousand inhabitants&quot; } } },
      &quot;nace_r2&quot;: { &quot;category&quot;: { &quot;index&quot;: { &quot;I551-I553&quot;: 0 } } },
      &quot;geo&quot;:     { &quot;category&quot;: { &quot;index&quot;: { &quot;EL62&quot;: 0 } } },
      &quot;time&quot;:    { &quot;category&quot;: { &quot;index&quot;: { &quot;2022&quot;: 0, &quot;2023&quot;: 1 } } }
    },
    &quot;decoded_slice&quot;: [
      { &quot;geo&quot;: &quot;EL62&quot;, &quot;unit&quot;: &quot;P_THAB&quot;, &quot;nace_r2&quot;: &quot;I551-I553&quot;, &quot;time&quot;: &quot;2022&quot;, &quot;value&quot;: 80912.16 },
      { &quot;geo&quot;: &quot;EL62&quot;, &quot;unit&quot;: &quot;P_THAB&quot;, &quot;nace_r2&quot;: &quot;I551-I553&quot;, &quot;time&quot;: &quot;2023&quot;, &quot;value&quot;: 97705.53 }
    ]
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Tourism Intensity in EL62 (Nights per 1,000 Residents, Eurostat tour_occ_nin2)
2022 :  80,912.2  ███████████████▋····  (~80.9 nights / resident)
2023 :  97,705.5  ██████████████████▉·  (~97.7 nights / resident)
2024 : 103,440.0  ████████████████████  (~103.4 nights / resident — Peak, #2 in EU)

```

| Year | Spatial Scope | Nights per 1,000 Residents (`P_THAB`) | Nights per Resident | YoY Change |
| --- | --- | --- | --- | --- |
| **2022** | `NUTS2 / EL62` | **80,912.16** | 80.91 | — |
| **2023** | `NUTS2 / EL62` | **97,705.53** | 97.71 | +20.75 % |
| **2024** | `NUTS2 / EL62` | **103,440.00** | 103.44 | +5.87 % |

- **Historical Log:**
    - **2026-09-22** - Eurostat `tour_occ_nin2` verified.
    - **2026-10-01** - extended to 2025; reconciled the Kathimerini figure (103,440 nights/1,000 = Eurostat 2024 Ionian intensity).

#### Data17 · Hospital / infrastructure congestion (`Συμφόρηση νοσοκομείων / υποδομών`) - `UNVERIFIED`

- **Source:** official announcements + citizen reports.
- **Data Pointers & Provenance:** No pull artifact present (requires civil-protection / regional health authority feed or citizen report ingestion).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Facility pressure event JSON (`facility_id`, `island_nuts3`, `alert_level`, `wait_time_band`, `source_type`).
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data17&quot;,
    &quot;facility_id&quot;: &quot;GEN-HOSP-CORFU&quot;,
    &quot;observed_at&quot;: &quot;YYYY-MM-DDTHH:MM:SSZ&quot;,
    &quot;pressure_level&quot;: &quot;elevated&quot;,
    &quot;report_source&quot;: &quot;citizen_verified&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

#### Data18 · Power / water outage (`Διακοπές ρεύματος / νερού`) - `UNVERIFIED`

- **Source:** official announcements (HEDNO / ΔΕΔΔΗΕ, municipal water utilities ΔΕΥΑ) + citizen reports.
- **Data Pointers & Provenance:** No pull artifact present.
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Utility outage event JSON (`utility_type` `["power", "water"]`, `municipality_code`, `start_utc`, `estimated_restoration_utc`, `affected_reports`).
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data18&quot;,
    &quot;utility_type&quot;: &quot;water&quot;,
    &quot;municipality&quot;: &quot;EL622-CORFU-CENTRAL&quot;,
    &quot;start_utc&quot;: &quot;YYYY-MM-DDTHH:MM:SSZ&quot;,
    &quot;status&quot;: &quot;active_outage&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

#### Data19 · Short-term rental share (Airbnb) (`Μερίδιο βραχυχρόνιων μισθώσεων`) - `VERIFIED`

- **Source:** Eurostat `tour_ce_omn12` (short-stay accommodation offered via online platforms — the EC data-sharing agreement with Airbnb, Booking.com, Expedia, Tripadvisor) ÷ Eurostat `tour_occ_nin2` (conventional nights). Airbnb has no public API; InsideAirbnb has no Ionian Islands coverage.
- **Data Pointers & Provenance:**
    - `Raw Pull (Platform Nights Annual 2018–2025)`: `data/raw/eurostat-tour_ce_omn12-el62-ngtsp-annual-2018-2025.json`
    - `Raw Pull (Platform Nights 2025 Monthly)`: `data/raw/eurostat-tour_ce_omn12-el62-ngtsp-2025-monthly.json`
    - `Raw Pull (Conventional Nights 2018–2025)`: `data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json`
    - `Curated Audit JSON`: `data/curated/data19-platform-rental-share.json`
    - `Curated Observations`: `data/curated/observations-data19-platform-rental-share-2026-10-15.json` / `.csv` (8 annual observations, 2018–2025)
    - `Manifest`: `data/manifests/source-verification-2026-10-15.json`
    - `ETL Script`: `scripts/verification/pull-data19-platform-rentals.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Two Eurostat JSON-stat 2.0 datasets (`tour_ce_omn12` and `tour_occ_nin2`), parsed by `pull-data19-platform-rentals.py` into a structured audit JSON (`data19-platform-rental-share.json`) containing the 2018–2025 annual series and 2025 monthly seasonality profile.
    - `Target Features`: `tour_ce_omn12`: `indic_to="NGT_SP"` (guest nights spent), `c_resid="TOTAL"`, `month="TOTAL"` (and `M01..M12`), `geo="EL62"`, `time="2018..2025"`. `tour_occ_nin2`: `unit="NR"`, `nace_r2="I551-I553"`, `c_resid="TOTAL"`, `geo="EL62"`, `time="2018..2025"`.
    - `Handling & Transformation`: Decodes annual platform guest nights (`NGT_SP_platform`) and conventional establishment nights (`NGT_conventional`) for each year `Y ∈ [2018..2025]`, then computes the share of total regional accommodation volume:
    `Data19(Y) = NGT_SP_platform(EL62, Y) / (NGT_conventional(EL62, Y) + NGT_SP_platform(EL62, Y)) × 100`.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>data/curated/data19-platform-rental-share.json</code>)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data19&quot;,
    &quot;indicator_name&quot;: &quot;Short-term rental share (Airbnb)&quot;,
    &quot;status&quot;: &quot;VERIFIED&quot;,
    &quot;spatial_ref&quot;: { &quot;level&quot;: &quot;NUTS2&quot;, &quot;code&quot;: &quot;EL62&quot; },
    &quot;method&quot;: &quot;Data19(Y) = NGT_SP_platform(EL62,Y) / (NGT_conventional(EL62,Y) + NGT_SP_platform(EL62,Y)) * 100&quot;,
    &quot;series&quot;: [
      { &quot;year&quot;: &quot;2018&quot;, &quot;platform_nights&quot;: 3055815, &quot;conventional_nights&quot;: 18016737, &quot;total_tourism_nights&quot;: 21072552, &quot;share_pct&quot;: 14.50 },
      { &quot;year&quot;: &quot;2019&quot;, &quot;platform_nights&quot;: 3389027, &quot;conventional_nights&quot;: 17954520, &quot;total_tourism_nights&quot;: 21343547, &quot;share_pct&quot;: 15.88 },
      { &quot;year&quot;: &quot;2020&quot;, &quot;platform_nights&quot;: 1274758, &quot;conventional_nights&quot;: 4498381,  &quot;total_tourism_nights&quot;: 5773139,  &quot;share_pct&quot;: 22.08 },
      { &quot;year&quot;: &quot;2021&quot;, &quot;platform_nights&quot;: 2768197, &quot;conventional_nights&quot;: 9257610,  &quot;total_tourism_nights&quot;: 12025807, &quot;share_pct&quot;: 23.02 },
      { &quot;year&quot;: &quot;2022&quot;, &quot;platform_nights&quot;: 5220869, &quot;conventional_nights&quot;: 16512634, &quot;total_tourism_nights&quot;: 21733503, &quot;share_pct&quot;: 24.02 },
      { &quot;year&quot;: &quot;2023&quot;, &quot;platform_nights&quot;: 6069273, &quot;conventional_nights&quot;: 19762799, &quot;total_tourism_nights&quot;: 25832072, &quot;share_pct&quot;: 23.50 },
      { &quot;year&quot;: &quot;2024&quot;, &quot;platform_nights&quot;: 4400084, &quot;conventional_nights&quot;: 20524700, &quot;total_tourism_nights&quot;: 24924784, &quot;share_pct&quot;: 17.65 },
      { &quot;year&quot;: &quot;2025&quot;, &quot;platform_nights&quot;: 8644420, &quot;conventional_nights&quot;: 20363829, &quot;total_tourism_nights&quot;: 29008249, &quot;share_pct&quot;: 29.80 }
    ]
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Short-Term Rental (Platform) Share of Total Tourism Nights in EL62 (2018–2025)
2018 : 14.50 %  █████████▋··········  (3.06M platform / 21.07M total nights)
2019 : 15.88 %  ██████████▌·········  (3.39M platform / 21.34M total nights)
2020 : 22.08 %  ██████████████▊·····  (1.27M platform /  5.77M total nights — COVID resilience)
2021 : 23.02 %  ███████████████▎····  (2.77M platform / 12.03M total nights)
2022 : 24.02 %  ████████████████····  (5.22M platform / 21.73M total nights)
2023 : 23.50 %  ███████████████▋····  (6.07M platform / 25.83M total nights)
2024 : 17.65 %  ███████████▊········  (4.40M platform / 24.92M total nights)
2025 : 29.80 %  ████████████████████  (8.64M platform / 29.01M total nights — *Flag: +96% step)

2025 Monthly Platform Seasonality Profile in EL62 (Total = 8,644,420 nights; Jul+Aug = 52.4 %)
Jan (M01) :     8,342  ·
Feb (M02) :    11,511  ·
Mar (M03) :    23,938  ▏
Apr (M04) :   266,962  ██▎
May (M05) :   534,823  ████▌
Jun (M06) : 1,445,193  ████████████▎
Jul (M07) : 2,182,817  ██████████████████▌
Aug (M08) : 2,348,265  ████████████████████
Sep (M09) : 1,367,852  ███████████▋
Oct (M10) :   419,047  ███▌
Nov (M11) :    18,824  ▏
Dec (M12) :    16,846  ▏

```

| Year | Platform Nights (`tour_ce_omn12`) | Conventional Nights (`tour_occ_nin2`) | Total Tourism Nights | Platform Share (`Data19`) |
| --- | --- | --- | --- | --- |
| **2018** | 3,055,815 | 18,016,737 | 21,072,552 | **14.50 %** |
| **2019** | 3,389,027 | 17,954,520 | 21,343,547 | **15.88 %** |
| **2020** | 1,274,758 | 4,498,381 | 5,773,139 | **22.08 %** |
| **2021** | 2,768,197 | 9,257,610 | 12,025,807 | **23.02 %** |
| **2022** | 5,220,869 | 16,512,634 | 21,733,503 | **24.02 %** |
| **2023** | 6,069,273 | 19,762,799 | 25,832,072 | **23.50 %** |
| **2024** | 4,400,084 | 20,524,700 | 24,924,784 | **17.65 %** |
| **2025** | 8,644,420 | 20,363,829 | 29,008,249 | **29.80 %** *(flagged)* |

- **Historical Log:**
    - **2026-09-26** - InsideAirbnb identified as free candidate (`insideairbnb.com/get-the-data/` HTTP 200); Greece region/date keys unresolved (guessed Athens key → 403).
    - **2026-10-15** - **Key note (source resolution):** *what:* InsideAirbnb is non-viable for EL62 (zero Ionian Islands coverage — Greece is Athens/Crete only; the guessed Athens key returned HTTP 403); *why:* replaced it with the official Eurostat platform dataset `tour_ce_omn12` (`NGT_SP`, `c_resid=TOTAL`, NUTS2/EL62), published under the EC agreement with the four major platforms; *how:* `scripts/verification/pull-data19-platform-rentals.py` computes Data19(Y) = platform nights ÷ (conventional nights + platform nights) × 100 against `tour_occ_nin2`. **Result (share %): 14.50 (2018) → 15.88 (2019) → 22.08 (2020) → 23.02 (2021) → 24.02 (2022) → 23.50 (2023) → 17.65 (2024) → 29.80 (2025)**. 2025 monthly: Jul 2,182,817 · Aug 2,348,265 (Jul+Aug = 52.4 % of annual). → `VERIFIED`.
    - **2026-10-15** - **Flag (2025 step change):** platform nights 8,644,420 (2025) vs 4,400,084 (2024) = **+96 %** — likely a platform-coverage/onboarding change in the EC agreement rather than true market growth; treat the 2025 share (29.80 %) cautiously and re-verify against the next Eurostat release. Evidence: `data/manifests/source-verification-2026-10-15.json`, `data/curated/data19-platform-rental-share.json`.

### Digital Infrastructure - Ψηφιακή Υποδομή

#### Data20 · Internet speed (>100 Mb/s) (`Ταχύτητα διαδικτύου`) - `VERIFIED`

- **Source:** Ookla Open Data (free, no key) - `registry.opendata.aws/speedtest-global-performance` · EU Tourism Dashboard (`TOUR_DIG_05`) · citizen reports.
- **Data Pointers & Provenance:**
    - `Raw Pull Archive (S3 Shapefile)`: `data/raw/ookla-performance-fixed-2024Q3.zip` · `data/raw/ookla-performance-mobile-2024Q3.zip`
    - `Structured JSON Summary`: `data/samples/ookla-ionian-2024Q3-summary.json`
    - `Curated Audit`: `data/curated/data20-internet-speed.json`
    - `Curated Observation`: `data/curated/observations-data20-internet-speed-2024Q3.json` (4 obs: fixed/mobile download & upload, EL62)
    - `Dashboard Reconciliation Sample`: `data/samples/eutd-tourism-dashboard-2024-ionian.json`
    - `Manifest`: `data/manifests/source-verification-2026-10-01.json` · `data/manifests/source-verification-2026-10-20.json`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Ookla distributes quarterly global slippy-map tile shapefiles (`2024-07-01_performance_fixed_tiles.zip`). Our pipeline spatially clips the shapefile to the Ionian Islands bounding box and transforms the aggregated statistics into a clean JSON summary (`ookla-ionian-2024Q3-summary.json`).
    - `Target Features`: `avg_d_kbps` (converted to Mbps: `avg_download_Mbps_mean`, `avg_download_Mbps_median`, `avg_download_Mbps_max`), `tests` (count of speed tests), `devices` (unique devices), `tiles` (spatial tiles in bbox).
    - `Handling & Transformation`: Spatial bounding-box filter (`lon 19.0–22.0, lat 37.0–40.5`) via `geopandas` isolates 9,209 fixed-broadband tiles (123,119 tests across 47,113 devices), converting `avg_d_kbps / 1000.0` to compute regional mean (`39.1 Mbps`), median (`26.8 Mbps`), and peak (`926.6 Mbps`).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>ookla-ionian-2024Q3-summary.json</code>)</summary>
<pre><code class="language-json">{
    &quot;source&quot;: &quot;Ookla Open Data — fixed broadband performance tiles&quot;,
    &quot;period&quot;: &quot;2024 Q3 (2024-07-01)&quot;,
    &quot;spatial&quot;: &quot;Ionian Islands bbox (lon 19–22, lat 37–40.5)&quot;,
    &quot;tiles&quot;: 9209,
    &quot;avg_download_Mbps_mean&quot;: 39.1,
    &quot;avg_download_Mbps_median&quot;: 26.8,
    &quot;avg_download_Mbps_max&quot;: 926.6,
    &quot;tests&quot;: 123119,
    &quot;devices&quot;: 47113,
    &quot;zip_sha256&quot;: &quot;00b610cfcbc8d58ae4856fdbe2f69ebdd06df2b27ab6dd79452ce092df39de8e&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Ookla Fixed Broadband Speeds — Ionian Islands Bbox (2024-Q3, 9,209 tiles / 123,119 tests)
Median Download Speed :  26.8 Mbps  █████▍··············  (vs 100 Mbps target)
Mean Download Speed   :  39.1 Mbps  ███████▊············  (vs 100 Mbps target)
Target Threshold      : 100.0 Mbps  ████████████████████  [Benchmark]
Max Tile Speed        : 926.6 Mbps  [Fiber/FTTH localized peak]
Dashboard TOUR_DIG_05 :  39.67 %    (EL62 2023 share metric)

```

- **Historical Log:**
    - **2026-09-26** - Ookla Open Data identified (free S3 shapefile).
    - **2026-10-01** - pulled 2024-Q3 fixed broadband over the Ionian bbox: **mean 39.1 Mbps** · median 26.8 · max 926.6 (123,119 tests).
    - **2026-10-03** - **Flag (reconciliation):** the dashboard's "Internet speed at tourism destinations" (`TOUR_DIG_05`) = **39.67 %** (EL62 2023) - a *share* metric, not the Mbps mean we measured via Ookla. The exact "% of what" needs the dashboard methodology; keep Ookla Mbps for now and note the definitions differ.
    - **2026-10-20** - **Key note (EL62 spatial join):** *what:* superseded the loose bbox mean with a GISCO EL62 clip (`compute-data20-internet-speed.py`) - fixed **42.29 Mbps** download / 9.55 upload / 49.6 ms (2,795 tiles, 41,552 tests, 18,089 devices) and mobile **107.48 Mbps** download / 15.31 upload / 59.1 ms (1,880 tiles, 11,296 tests, 6,248 devices); *how:* test-weighted average over tiles intersecting the EL62 polygon. Emitted `observations-data20-internet-speed-2024Q3.json` (4 obs).

#### Data21 · 4G/5G availability (`Διαθεσιμότητα 4G/5G`) - `UNVERIFIED`

- **Source:** citizen reports (app's own feed).
- **Data Pointers & Provenance:** No pull artifact present (mobile application network-telemetry / user report feed).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Geohash-binned cellular connectivity report (`geohash_6`, `network_generation` `["5G", "4G", "3G", "no_service"]`, `sample_count`, `coverage_4g5g_pct`).
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data21&quot;,
    &quot;geohash&quot;: &quot;sqx9pe&quot;,
    &quot;island_nuts3&quot;: &quot;EL622&quot;,
    &quot;observed_at&quot;: &quot;YYYY-MM-DD&quot;,
    &quot;coverage_4g5g_pct&quot;: 91.2
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

### Spatial Sustainability - Χωροταξική Αειφορία

#### Data22 · Tourist diversity (zones) (`Τουριστική ποικιλομορφία (ζώνες)`) - `VERIFIED`

- **Source:** Eurostat `tour_occ_nin3` (NUTS3 nights) - `ec.europa.eu/eurostat` · EU Tourism Dashboard (front-end over the same data).
- **Definition (adopted, provisional):** `1 − HHI` of the four NUTS3 island night shares, aggregated to NUTS2/EL62. **Basis:** Herfindahl-Hirschman Index (standard concentration measure).
- **Open question:** does "diversity" mean spatial spread across islands (adopted), accommodation-type mix (`nace_r2`), or visitor-origin mix (`c_resid`)?
- **Data Pointers & Provenance:**
    - `Raw Sample (Eurostat NUTS3 Nights)`: `data/samples/eurostat-tour_occ_nin3-EL621-624-2021-2025.json`
    - `Derived Audit JSON`: `data/samples/derived-data22-data25-2021-2025.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (6 annual observations, 2020–2025)
    - `Manifest`: `data/manifests/source-verification-2026-10-01.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Eurostat JSON-stat 2.0 (`tour_occ_nin3`) covering the four NUTS3 regions of `EL62` (`EL621` Zakynthos, `EL622` Kerkyra, `EL623` Ithaki-Kefallinia, `EL624` Lefkada), decoded into `derived-data22-data25-2021-2025.json`.
    - `Target Features`: `geo` (`EL621`, `EL622`, `EL623`, `EL624`), `time` (`2020..2025`), `c_resid="TOTAL"`, `unit="NR"`, `nace_r2="I551-I553"`, and derived fields `shares`, `HHI`, `diversity_1_minus_HHI`.
    - `Handling & Transformation`: For each year, computes each island's share of total regional nights `s_i = nights_i / sum(nights)`, sums squared shares `HHI = sum(s_i^2)`, and computes `Diversity = 1 - HHI` (where `0` = single-island monopoly and `0.75` = equal 4-way split).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>derived-data22-data25-2021-2025.json</code>)</summary>
<pre><code class="language-json">{
    &quot;data22_tourist_diversity&quot;: {
      &quot;2021&quot;: {
        &quot;nights&quot;: { &quot;Zakynthos&quot;: 3093879, &quot;Kerkyra&quot;: 4495736, &quot;Ithaki_Kefallinia&quot;: 850030, &quot;Lefkada&quot;: 817965 },
        &quot;shares&quot;: { &quot;Zakynthos&quot;: 0.3342,  &quot;Kerkyra&quot;: 0.4856,  &quot;Ithaki_Kefallinia&quot;: 0.0918, &quot;Lefkada&quot;: 0.0884 },
        &quot;HHI&quot;: 0.3638,
        &quot;diversity_1_minus_HHI&quot;: 0.6362
      },
      &quot;2022&quot;: {
        &quot;nights&quot;: { &quot;Zakynthos&quot;: 5138655, &quot;Kerkyra&quot;: 7918650, &quot;Ithaki_Kefallinia&quot;: 1763599, &quot;Lefkada&quot;: 1691730 },
        &quot;shares&quot;: { &quot;Zakynthos&quot;: 0.3112,  &quot;Kerkyra&quot;: 0.4796,  &quot;Ithaki_Kefallinia&quot;: 0.1068,  &quot;Lefkada&quot;: 0.1025 },
        &quot;HHI&quot;: 0.3488,
        &quot;diversity_1_minus_HHI&quot;: 0.6512
      }
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Spatial Tourist Diversity Index (1 − HHI across 4 NUTS3 Island Zones, Theoretical Max = 0.750)
2020 : 0.663  █████████████████▋··
2021 : 0.636  █████████████████···
2022 : 0.651  █████████████████▍··
2023 : 0.632  ████████████████▉···
2024 : 0.631  ████████████████▊···
2025 : 0.640  █████████████████··

NUTS3 Island Share of EL62 Overnight Stays (2022 Baseline)
Kerkyra (EL622)           : 47.96 %  █████████▌··········  (7,918,650 nights)
Zakynthos (EL621)         : 31.12 %  ██████▏·············  (5,138,655 nights)
Ithaki-Kefallinia (EL623) : 10.68 %  ██▏·················  (1,763,599 nights)
Lefkada (EL624)           : 10.25 %  ██··················  (1,691,730 nights)

```

| Year | Kerkyra (`EL622`) | Zakynthos (`EL621`) | Ithaki-Kefallinia (`EL623`) | Lefkada (`EL624`) | `HHI` | Diversity (`1 − HHI`) |
| --- | --- | --- | --- | --- | --- | --- |
| **2020** | — | — | — | — | 0.3370 | **0.663** |
| **2021** | 48.56 % | 33.42 % | 9.18 % | 8.84 % | 0.3638 | **0.636** |
| **2022** | 47.96 % | 31.12 % | 10.68 % | 10.25 % | 0.3488 | **0.651** |
| **2023** | ~50.1 % | ~30.8 % | ~9.8 % | ~9.3 % | 0.3680 | **0.632** |
| **2024** | ~50.3 % | ~30.7 % | ~9.7 % | ~9.3 % | 0.3690 | **0.631** |
| **2025** | ~49.2 % | ~31.0 % | ~10.1 % | ~9.7 % | 0.3600 | **0.640** |

- **Historical Log:**
    - **2026-10-01** - derived `1 − HHI` over NUTS3 island night shares (0.636 / 0.651 / 0.632 / 0.631 / 0.640 for 2021→2025), aggregated to NUTS2/EL62.
    - **2026-10-03** - definition adopted as the working default (provisional); open question logged for the author.
    - **2026-10-03** - **Flag (reconciliation):** the dashboard's "Tourism diversity" (`TOUR_SOE_04`) reads **0 (index)** for EL62 and all its islands - a *different concept* whose definition is not yet confirmed (and Greece reads 0 across the board, suggesting a data/definition gap). Do **not** swap our spatial `1 − HHI` (which matches the proposal's "diversity (zones)") for the dashboard value without understanding it.

#### Data23 · Density of cultural elements (`Πυκνότητα πολιτιστικών στοιχείων`) - `VERIFIED`

- **Source:** EU Tourism Dashboard "Cultural assets density" (`TOUR_DES_14`) - `tourism-dashboard.ec.europa.eu`.
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/eutd-tourism-dashboard-2024-el62.json` · `data/samples/eutd-tourism-dashboard-2024-ionian.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `9.073` cultural assets / 100 km² in `EL62`, 2023)
    - `Manifest`: `data/manifests/source-verification-2026-10-03.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: JRC EU Tourism Dashboard CSV export converted to structured JSON (`eutd-tourism-dashboard-2024-el62.json`).
    - `Target Features`: `code="TOUR_DES_14"`, `nuts_code_2021="EL62"`, `year=2023`, `value=9.073`, `unit="no. of cultural assets / 100 km²"`.
    - `Handling & Transformation`: Reads the JRC-computed cultural POI density for `EL62`, normalizing the HTML superscript tag (`100km<sup>2</sup>` → `100 km²`).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eutd-tourism-dashboard-2024-el62.json</code>)</summary>
<pre><code class="language-json">{
    &quot;cultural_assets_density&quot;: {
      &quot;data_id&quot;: &quot;Data23&quot;,
      &quot;code&quot;: &quot;TOUR_DES_14&quot;,
      &quot;year&quot;: 2023,
      &quot;unit&quot;: &quot;no. of cultural assets / 100km&lt;sup&gt;2&lt;/sup&gt;&quot;,
      &quot;value&quot;: 9.073
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Cultural Assets Density (TOUR_DES_14, 2023)
Ionian Islands (EL62) : 9.073 assets / 100 km²  ██████████████████▏  (~209 mapped cultural assets across 2,305 km²)

```

- **Historical Log:**
    - **2026-10-03** - **Key note (reconciliation):** *what:* resolved to **9.07 cultural assets / 100 km²** (EL62, 2023); *why:* the dashboard (the proposal's own source) already publishes "cultural asset intensity", so no separate POI survey was needed; *how:* read `TOUR_DES_14` from the 2024 dashboard CSV export. → `VERIFIED`.

#### Data24 · Protected land (%) (`Προστατευόμενη γη (%)`) - `VERIFIED`

- **Source:** EEA Natura 2000 - `bio.discomap.eea.europa.eu` · Eurostat GISCO NUTS 2021 boundary - `gisco-services.ec.europa.eu`.
- **Data Pointers & Provenance:**
    - `Raw Boundary GeoJSON`: `data/raw/gisco-nuts-2021-3035-EL62.geojson`
    - `Raw Natura 2000 GeoJSONs`: `data/raw/eea-natura2000-el62-envelope-habitats-4326.geojson` · `data/raw/eea-natura2000-el62-envelope-birds-4326.geojson`
    - `Initial REST Summary`: `data/samples/eea-natura2000-gr22-summary-2026-10-02.json`
    - `Curated Spatial Join Audit JSON`: `data/curated/data24-protected-land.json` · `data/curated/data24-protected-land.geojson`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `16.76 %` in `EL62`)
    - `Visual Map Artifact`: `data/samples/data24-protected-land-map-2026-10-03.png`
    - `Manifest`: `data/manifests/source-verification-2026-10-03.json`
    - `ETL & Viz Scripts`: `scripts/verification/pull-data24-protected-land.py` · `scripts/verification/compute-data24-protected-land.py` · `scripts/verification/viz-data24-protected-land.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Three GeoJSON `FeatureCollection` datasets (GISCO `EL62` land polygon in equal-area `EPSG:3035`, plus EEA ArcGIS MapServer layer `0` Habitats and layer `1` Birds polygons in `EPSG:4326`), processed into the audit JSON `data24-protected-land.json`.
    - `Target Features`: GISCO: `properties.NUTS_ID == "EL62"`, `geometry` (53 island polygon parts). Natura 2000: `properties.SITECODE`, `properties.SITENAME`, `properties.SITETYPE`, `geometry`. Derived JSON: `el62_land_ha`, `habitats_protected_land_ha`, `birds_protected_land_ha`, `combined_protected_land_ha`, `protected_land_pct`.
    - `Handling & Transformation`: Reprojects all Natura 2000 site geometries (34 Habitats + 25 Birds sites intersecting the `EL62` envelope, capturing cross-regional sites like `GR2310001` Acheloos delta covering the Echinades islets) into `EPSG:3035` LAEA Europe, intersects each site with the `EL62` terrestrial land polygon to strip marine areas, computes `unary_union(Habitats ∪ Birds)` to eliminate double-counting where SPA and SAC sites overlap, and divides by total `EL62` land area (`38,640.51 ha / 230,486.97 ha = 16.76 %`).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>data/curated/data24-protected-land.json</code>)</summary>
<pre><code class="language-json">{
    &quot;computed_at_utc&quot;: &quot;2026-10-03T09:37:56.371570+00:00&quot;,
    &quot;indicator_id&quot;: &quot;Data24&quot;,
    &quot;indicator_name&quot;: &quot;Protected land (%)&quot;,
    &quot;spatial_ref&quot;: { &quot;level&quot;: &quot;NUTS2&quot;, &quot;code&quot;: &quot;EL62&quot; },
    &quot;el62_land_km2&quot;: 2304.87,
    &quot;el62_land_ha&quot;: 230486.97,
    &quot;published_el62_km2&quot;: 2307.0,
    &quot;el62_area_delta_pct&quot;: -0.092,
    &quot;habitats_protected_land_ha&quot;: 22049.2,
    &quot;birds_protected_land_ha&quot;: 29744.22,
    &quot;combined_protected_land_ha&quot;: 38640.51,
    &quot;combined_protected_land_km2&quot;: 386.41,
    &quot;protected_land_pct&quot;: 16.7647
}
</code></pre>
</details>
- **Visualizations & Data Findings:**
    - **Rendered Map Artifact:** `data/samples/data24-protected-land-map-2026-10-03.png`

```
EL62 Terrestrial Protected Area Breakdown (EPSG:3035 Equal-Area Spatial Join)
Total EL62 Land Area (GISCO 2021)     : 230,487.0 ha (100.00 %)  ████████████████████
Habitats Directive Terrestrial (SCI)  :  22,049.2 ha (  9.57 %)  █▉··················
Birds Directive Terrestrial (SPA)     :  29,744.2 ha ( 12.90 %)  ██▌·················
Combined Union (Habitats ∪ Birds)     :  38,640.5 ha ( 16.76 %)  ███▍················  [VERIFIED: 16.76 %]
EU Tourism Dashboard Cross-Check      :  TOUR_DES_12 ( 16.57 %)  ███▎················  (Δ = +0.19 pp)

```

| Spatial Layer / Metric | Area (Hectares) | Area (km²) | Share of `EL62` Land (%) | Notes |
| --- | --- | --- | --- | --- |
| **`EL62` Land Polygon (`EPSG:3035`)** | 230,486.97 ha | 2,304.87 km² | 100.00 % | Matches published 2,307 km² (-0.09 %) |
| **Habitats Directive (`pSCI/SCI/SAC`)** | 22,049.20 ha | 220.49 km² | 9.57 % | Clipped to terrestrial land |
| **Birds Directive (`SPA`)** | 29,744.22 ha | 297.44 km² | 12.90 % | Clipped to terrestrial land |
| **Combined Union (`Habitats ∪ Birds`)** | **38,640.51 ha** | **386.41 km²** | **16.76 %** | De-duplicated overlap (13,152.9 ha shared) |
| **Dashboard Benchmark (`TOUR_DES_12`)** | — | — | **16.57 %** | Independent JRC check within 0.19 pp |

- **Historical Log:**
    - **2026-09-24** - EEA CDDA/Natura 2000 document URLs confirmed (datahub + GeoNetwork).
    - **2026-10-02** - machine-readable source located: EEA ArcGIS REST `Natura2000Sites` MapServer (no key); GR22 = 18 Habitats + 8 Birds sites. Value left pending (needed clip + terrestrial/marine split + union).
    - **2026-10-03** - **spatial join complete**: Natura 2000 Habitats ∪ Birds clipped to the EL62 land polygon (GISCO NUTS 2021, EPSG:3035), terrestrial/marine split via land-polygon intersection, union dissolved → **16.76 %** (386.41 / 2,304.87 km²). Completeness finding: the Echinades/Petalas islets (GISCO NUTS3 EL623 "Ithaki, Kefallinia") are protected via a GR23-coded Acheloos-delta site (1,608 ha) - a GR22-only filter would under-count. → `VERIFIED`.
    - **2026-10-03** - cross-check: EU Tourism Dashboard "Share of protected/designated land" (`TOUR_DES_12`) = **16.57 %** for EL62, within 0.2 pp of our independent spatial join (16.76 %).

#### Data25 · Accommodation in high-value areas (`Καταλύματα σε περιοχές υψηλής αξίας`) - `VERIFIED`

- **Source:** EU Tourism Dashboard - "Share of accommodations in areas with high-nature value" (code `TOUR_DES_13`) - `tourism-dashboard.ec.europa.eu` · data.europa.eu dataset `9564824a-7f16-4efa-82fb-d4e176350026`.
- **Definition (adopted):** the proposal's own source (EU Tourism Dashboard) already publishes this indicator - no overlay needed. **Value:** EL62 = **43 %** (2023); per-island: Zakynthos 59 % · Kerkyra 34 % · Ithaki-Kefallinia 34 % · Lefkada 57 %.
- **Data Pointers & Provenance:**
    - `Raw Sample (EL62 Summary)`: `data/samples/eutd-tourism-dashboard-2024-el62.json`
    - `Raw Sample (Ionian NUTS3 Breakdown)`: `data/samples/eutd-tourism-dashboard-2024-ionian.json`
    - `Supplementary Capacity Sample (ELSTAT)`: `data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `43.0 %` in `EL62`, 2023)
    - `Manifest`: `data/manifests/source-verification-2026-10-03.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: JRC EU Tourism Dashboard CSV export converted to structured JSON (`eutd-tourism-dashboard-2024-el62.json` and `eutd-tourism-dashboard-2024-ionian.json`); supplementary ELSTAT `.xlsx` capacity workbooks (`elstat-sto12-2021..2025-capacity.xlsx`) converted to `elstat-sto12-ionian-bedplaces-2021-2025.json`.
    - `Target Features`: `code="TOUR_DES_13"`, `nuts_code_2021` (`EL62`, `EL621`, `EL622`, `EL623`, `EL624`), `year=2023`, `value` (`43.0 %` for `EL62`), `unit="%"`.
    - `Handling & Transformation`: Direct extraction of `TOUR_DES_13` at `NUTS2/EL62` for the authoritative curated observation, retaining the `NUTS3` island breakdown (`EL621`–`EL624`) for internal disaggregation.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eutd-tourism-dashboard-2024-el62.json</code> &amp; NUTS3 breakdown)</summary>
<pre><code class="language-json">{
    &quot;high_nature_value_accommodation&quot;: {
      &quot;data_id&quot;: &quot;Data25&quot;,
      &quot;code&quot;: &quot;TOUR_DES_13&quot;,
      &quot;year&quot;: 2023,
      &quot;unit&quot;: &quot;%&quot;,
      &quot;value_el62&quot;: 43.0,
      &quot;nuts3_breakdown&quot;: {
        &quot;EL621_Zakynthos&quot;: 59.0,
        &quot;EL624_Lefkada&quot;: 57.0,
        &quot;EL622_Kerkyra&quot;: 34.0,
        &quot;EL623_Ithaki_Kefallinia&quot;: 34.0
      },
      &quot;country_benchmark_EL&quot;: 32.0
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Share of Accommodations in High-Nature-Value Areas (TOUR_DES_13, 2023)
Zakynthos (EL621)         : 59.0 %  ███████████▊········
Lefkada (EL624)           : 57.0 %  ███████████▍········
Ionian Islands (EL62)     : 43.0 %  ████████▌···········  [Regional NUTS2 Value]
Kerkyra (EL622)           : 34.0 %  ██████▊·············
Ithaki-Kefallinia (EL623) : 34.0 %  ██████▊·············
Greece National (EL)      : 32.0 %  ██████▍·············

```

- **Historical Log:**
    - **Key note (reconciliation):** *what:* adopted the dashboard's "Share of accommodations in areas with high-nature value" (43 %, EL62 2023); *why:* the proposal's own source already publishes it, so building a Natura-2000-∪-coastal overlay was unnecessary (and that overlay definition was my earlier guess); *how:* pulled the 2024 dashboard CSV export and read `TOUR_DES_13`.
    - **Flag / open question:** the exact operationalisation of "high-nature value" (which areas count) is defined in the dashboard's methodology - to be pinned down; my earlier proposed default (Natura 2000 ∪ coastal buffer) is **superseded** by the dashboard definition.
    - **2026-10-01** - ELSTAT bed-places pulled as a partial path (104,108 → 109,565) but lacked the spatial distribution.
    - **2026-10-03** - resolved directly from the EU Tourism Dashboard (43 %, EL62 2023, + NUTS3 breakdown). → `VERIFIED`.

### Tourism Performance - Τουριστική Απόδοση

#### Data26 · Arrivals & overnight stays (`Αφίξεις & διανυκτερεύσεις`) - `VERIFIED`

- **Source:** Eurostat `tour_occ_nin2` (nights) + `tour_occ_arn2` (arrivals) - `ec.europa.eu/eurostat`.
- **Data Pointers & Provenance:**
    - `Raw Sample (Nights 2022–2023)`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
    - `Raw Sample (Arrivals 2022–2023)`: `data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json`
    - `Raw Pull (Nights 2018–2025)`: `data/raw/eurostat-tour_occ_nin2-el62-nr-annual-2018-2025.json`
    - `Annotated Reports`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.summary.md` · `data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.summary.md`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (4 base observations: nights & arrivals for 2022–2023; full 2018–2025 nights audited in `data/curated/data19-platform-rental-share.json`)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json` · `data/manifests/source-verification-2026-10-15.json`
    - `ETL Script`: `scripts/verification/pull-eurostat-tourism.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Two Eurostat JSON-stat 2.0 datasets (`tour_occ_nin2` for overnight stays and `tour_occ_arn2` for arrivals at tourist accommodation establishments).
    - `Target Features`: `freq="A"`, `c_resid="TOTAL"` (plus `FOR` foreign / `DOM` domestic), `unit="NR"` (Number), `nace_r2="I551-I553"` (total tourist accommodation), `geo="EL62"`, `time="2018..2025"`.
    - `Handling & Transformation`: Decodes multi-dimensional JSON-stat indices to extract headline `TOTAL` / `NR` / `I551-I553` series for `EL62` overnight stays and arrivals, retaining the `nace_r2` (`I551` hotels, `I552` holiday/short-stay, `I553` camping) and `c_resid` (`FOR`, `DOM`) breakdowns for downstream indicators (`Data30`, `Data32`, `Data33`).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eurostat-tour_occ_nin2-EL62-2022-2023.json</code> &amp; <code>arn2</code> decoded slices)</summary>
<pre><code class="language-json">{
    &quot;dataset_nights&quot;: &quot;tour_occ_nin2&quot;,
    &quot;dataset_arrivals&quot;: &quot;tour_occ_arn2&quot;,
    &quot;geo&quot;: &quot;EL62&quot;,
    &quot;nace_r2&quot;: &quot;I551-I553&quot;,
    &quot;c_resid&quot;: &quot;TOTAL&quot;,
    &quot;unit&quot;: &quot;NR&quot;,
    &quot;decoded_series&quot;: [
      { &quot;year&quot;: &quot;2018&quot;, &quot;overnight_stays&quot;: 18016737, &quot;arrivals&quot;: null    },
      { &quot;year&quot;: &quot;2019&quot;, &quot;overnight_stays&quot;: 17954520, &quot;arrivals&quot;: null    },
      { &quot;year&quot;: &quot;2020&quot;, &quot;overnight_stays&quot;: 4498381,  &quot;arrivals&quot;: null    },
      { &quot;year&quot;: &quot;2021&quot;, &quot;overnight_stays&quot;: 9257610,  &quot;arrivals&quot;: null    },
      { &quot;year&quot;: &quot;2022&quot;, &quot;overnight_stays&quot;: 16512634, &quot;arrivals&quot;: 2785360 },
      { &quot;year&quot;: &quot;2023&quot;, &quot;overnight_stays&quot;: 19762799, &quot;arrivals&quot;: 3332407 },
      { &quot;year&quot;: &quot;2024&quot;, &quot;overnight_stays&quot;: 20524700, &quot;arrivals&quot;: null    },
      { &quot;year&quot;: &quot;2025&quot;, &quot;overnight_stays&quot;: 20363829, &quot;arrivals&quot;: 3649432 }
    ]
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Conventional Overnight Stays in EL62 (Eurostat tour_occ_nin2, 2018–2025)
2018 : 18,016,737  █████████████████▌··
2019 : 17,954,520  █████████████████▌··
2020 :  4,498,381  ████▍···············  (COVID-19 trough)
2021 :  9,257,610  █████████···········
2022 : 16,512,634  ████████████████····  (Arrivals: 2,785,360)
2023 : 19,762,799  ███████████████████▎  (Arrivals: 3,332,407)
2024 : 20,524,700  ████████████████████  [All-time conventional peak]
2025 : 20,363,829  ███████████████████▊

```

| Year | Overnight Stays (`tour_occ_nin2`) | Arrivals (`tour_occ_arn2`) | Foreign Nights (`FOR`) | Domestic Nights (`DOM`) |
| --- | --- | --- | --- | --- |
| **2018** | 18,016,737 | — | — | — |
| **2019** | 17,954,520 | — | — | — |
| **2020** | 4,498,381 | — | — | — |
| **2021** | 9,257,610 | — | — | — |
| **2022** | **16,512,634** | **2,785,360** | 15,475,156 (93.72 %) | 1,037,478 (6.28 %) |
| **2023** | **19,762,799** | **3,332,407** | 18,493,790 (93.58 %) | 1,269,009 (6.42 %) |
| **2024** | **20,524,700** | — | — | — |
| **2025** | **20,363,829** | ~3,649,432 | — | — |

- **Historical Log:**
    - **2026-09-22** - Eurostat `tour_occ_nin2` + `tour_occ_arn2` verified (EL62).
    - **2026-10-01** - series extended to 2025 (nights/arrivals) and 2026 (bed-places).

#### Data27 · Tourism capacity (beds) (`Τουριστική δυναμικότητα (κλίνες)`) - `VERIFIED`

- **Source:** Eurostat `tour_cap_nuts2` (bed-places) - `ec.europa.eu/eurostat` · supplementary ELSTAT `STO12` regional capacity tables.
- **Data Pointers & Provenance:**
    - `Raw Sample (Eurostat NUTS2)`: `data/samples/eurostat-tour_cap_nuts2-EL62-2022-2023.json`
    - `Annotated Report`: `data/samples/eurostat-tour_cap_nuts2-EL62-2022-2023.summary.md` · `.html`
    - `Supplementary Sample (ELSTAT NUTS3)`: `data/samples/elstat-sto12-ionian-bedplaces-2021-2025.json` · `data/samples/elstat-sto12-2021..2025-capacity.xlsx`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (2 observations: `159,790` in 2022, `155,968` in 2023)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json` · `data/manifests/source-verification-2026-10-01.json`
    - `ETL Script`: `scripts/verification/pull-eurostat-tourism.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Eurostat JSON-stat 2.0 (`tour_cap_nuts2`) with dimensions `["freq", "accomunit", "unit", "nace_r2", "geo", "time"]`; plus ELSTAT `.xlsx` workbooks converted into structured JSON (`elstat-sto12-ionian-bedplaces-2021-2025.json`) for island-level hotel bed breakdowns.
    - `Target Features`: `accomunit="BEDPL"` (Bed-places), `unit="NR"`, `nace_r2="I551-I553"` (and `I551`, `I552`, `I553`), `geo="EL62"`, `time="2022, 2023"`.
    - `Handling & Transformation`: Extracts `accomunit=BEDPL` and `unit=NR` for `I551-I553` in `EL62` (`159,790` bed-places in 2022; `155,968` in 2023). Because Eurostat `tour_cap_nuts3` returns 0 rows for Greece, island-level hotel bed capacity (`104,108` → `109,565` across 2021–2025) is parsed from ELSTAT `STO12` Excel tables into JSON.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eurostat-tour_cap_nuts2-EL62-2022-2023.json</code> &amp; <code>elstat-sto12-ionian-bedplaces-2021-2025.json</code>)</summary>
<pre><code class="language-json">{
    &quot;eurostat_tour_cap_nuts2_EL62&quot;: {
      &quot;2022&quot;: { &quot;I551_I553_total_beds&quot;: 159790, &quot;I551_hotels&quot;: 106653, &quot;I552_short_stay&quot;: 47944, &quot;I553_camping&quot;: 5193, &quot;establishments&quot;: 4853 },
      &quot;2023&quot;: { &quot;I551_I553_total_beds&quot;: 155968, &quot;I551_hotels&quot;: 107952, &quot;I552_short_stay&quot;: 44734, &quot;I553_camping&quot;: 3282, &quot;establishments&quot;: 4527 }
    },
    &quot;elstat_sto12_hotels_by_island_2025&quot;: {
      &quot;KERKYRA&quot;: 51413,
      &quot;ZAKYNTHOS&quot;: 39625,
      &quot;KEFALLINIA&quot;: 12041,
      &quot;LEFKADA&quot;: 6221,
      &quot;ITHAKI&quot;: 265
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
EL62 Total Tourist Accommodation Bed-Places by NACE Category (Eurostat tour_cap_nuts2, 2023: 155,968 beds)
Hotels & Similar (I551)         : 107,952 beds (69.21 %)  █████████████▊······
Holiday & Short-Stay (I552)     :  44,734 beds (28.68 %)  █████▋··············
Camping Grounds (I553)          :   3,282 beds ( 2.10 %)  ▍···················

ELSTAT Hotel Bed-Places by Island Regional Unit (2021 → 2025)
Kerkyra     : 49,444 (2021) → 51,413 (2025) [+3.98 %]  ████████████████████
Zakynthos   : 36,696 (2021) → 39,625 (2025) [+7.98 %]  ███████████████▍····
Kefallinia  : 11,449 (2021) → 12,041 (2025) [+5.17 %]  ████▋···············
Lefkada     :  5,954 (2021) →  6,221 (2025) [+4.48 %]  ██▍·················
Ithaki      :    265 (2021) →    265 (2025) [ 0.00 %]  ▏···················

```

- **Historical Log:**
    - **2026-09-22** - Eurostat `tour_cap_nuts2` (EL62) verified.

#### Data28 · Occupancy rate (%) (`Ποσοστό πληρότητας (%)`) - `VERIFIED`

- **Source:** EU Tourism Dashboard "Occupancy rate" (`TOUR_DES_04`) - `tourism-dashboard.ec.europa.eu` · Eurostat (underlying).
- **Data Pointers & Provenance:**
    - `Raw Sample (Dashboard Net Occupancy)`: `data/samples/eutd-tourism-dashboard-2024-el62.json` · `data/samples/eutd-tourism-dashboard-2024-ionian.json`
    - `Superseded Sample (Gross Proxy)`: `data/samples/derived-data28-occupancy-2021-2025.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `65.4 %` net occupancy in `EL62`, 2023)
    - `Manifest`: `data/manifests/source-verification-2026-10-03.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Structured JSON extracted from the JRC EU Tourism Dashboard CSV export (`eutd-tourism-dashboard-2024-el62.json`).
    - `Target Features`: `code="TOUR_DES_04"`, `nuts_code_2021="EL62"`, `year=2023`, `value=65.4`, `unit="%"`.
    - `Handling & Transformation`: Adopts the official JRC/Eurostat **net** bed-place occupancy rate (`65.4 %` during active operating months), superseding our earlier gross annualized calculation (`nights / (beds × 365) ≈ 34.7 %`) which penalized seasonal winter closures.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eutd-tourism-dashboard-2024-el62.json</code>)</summary>
<pre><code class="language-json">{
    &quot;net_occupancy&quot;: {
      &quot;data_id&quot;: &quot;Data28&quot;,
      &quot;code&quot;: &quot;TOUR_DES_04&quot;,
      &quot;year&quot;: 2023,
      &quot;unit&quot;: &quot;%&quot;,
      &quot;value&quot;: 65.4
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
EL62 Bed-Place Occupancy Rate Comparison (2023)
Official Net Occupancy (TOUR_DES_04, open-days denominator) : 65.40 %  █████████████·······  [VERIFIED]
Superseded Gross Proxy (nights ÷ [beds × 365 days])         : 34.72 %  ██████▉·············  [Superseded]

```

- **Historical Log:**
    - **2026-10-01** - earlier attempt: derived occupancy = nights ÷ (beds × 365) ≈ 28-36 % (a *gross* rate; wrong for a seasonal destination).
    - **2026-10-03** - **Key note (reconciliation):** *what:* adopted **65.4 % net occupancy** (EL62, 2023); *why:* the dashboard's occupancy is the standard *net* rate (nights ÷ beds×open-days), not our gross ÷365 which understated a highly seasonal region; *how:* read `TOUR_DES_04` from the 2024 dashboard CSV export. Our gross derivation is superseded. → `VERIFIED`.

#### Data29 · Seasonality (%) (`Εποχικότητα (%)`) - `VERIFIED`

- **Source:** EU Tourism Dashboard "Tourism seasonality" (`TOUR_SOE_02`) - `tourism-dashboard.ec.europa.eu` · Eurostat `tour_occ_nim` (monthly country curve).
- **Data Pointers & Provenance:**
    - `Raw Sample (EL62 Dashboard)`: `data/samples/eutd-tourism-dashboard-2024-el62.json`
    - `Raw Sample (National Monthly Curve)`: `data/samples/eurostat-tour_occ_nim-EL-2023.json`
    - `Annotated Report`: `data/samples/eurostat-tour_occ_nim-EL-2023.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (14 observations: 1 `EL62` peak-season share `71.08 %`, 1 `EL` peak-month share `21.53 %`, and 12 monthly `EL` values `2023-01`..`2023-12`)
    - `Manifest`: `data/manifests/source-verification-2026-09-24.json` · `data/manifests/source-verification-2026-10-03.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Dashboard JSON (`TOUR_SOE_02` for `EL62`) paired with Eurostat JSON-stat 2.0 (`tour_occ_nim`, `freq="M"`, `geo="EL"`, `time="2023-01..2023-12"`).
    - `Target Features`: `TOUR_SOE_02.value` (`71.08 %` for `EL62`), and `tour_occ_nim` monthly `value["0".."11"]` (`c_resid="TOTAL"`, `unit="NR"`, `nace_r2="I551-I553"`).
    - `Handling & Transformation`: Adopts `71.08 %` from `TOUR_SOE_02` as the headline `NUTS2/EL62` peak-season share, while retaining the 12-month `tour_occ_nim` curve (`147,209,821` total Greece nights in 2023; Jun–Sep = `71.95 %`; Aug peak = `21.53 %`) to visualize the annual bell curve.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eutd-tourism-dashboard-2024-el62.json</code> &amp; <code>eurostat-tour_occ_nim-EL-2023.json</code>)</summary>
<pre><code class="language-json">{
    &quot;el62_peak_season_share&quot;: {
      &quot;data_id&quot;: &quot;Data29&quot;,
      &quot;code&quot;: &quot;TOUR_SOE_02&quot;,
      &quot;year&quot;: 2023,
      &quot;unit&quot;: &quot;%&quot;,
      &quot;value&quot;: 71.08
    },
    &quot;el_monthly_nights_2023&quot;: {
      &quot;2023-01&quot;: 1591829,  &quot;2023-02&quot;: 1603094,  &quot;2023-03&quot;: 2450684,  &quot;2023-04&quot;: 6491390,
      &quot;2023-05&quot;: 14349293, &quot;2023-06&quot;: 22554193, &quot;2023-07&quot;: 29461403, &quot;2023-08&quot;: 31687354,
      &quot;2023-09&quot;: 22215646, &quot;2023-10&quot;: 10467410, &quot;2023-11&quot;: 2201951,  &quot;2023-12&quot;: 2135574
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Monthly Overnight Stays Distribution (Eurostat tour_occ_nim 2023; EL62 Peak-Season Share = 71.08 %)
2023-01 (Jan) :  1,591,829 ( 1.08 %)  █···················
2023-02 (Feb) :  1,603,094 ( 1.09 %)  █···················
2023-03 (Mar) :  2,450,684 ( 1.66 %)  █▌··················
2023-04 (Apr) :  6,491,390 ( 4.41 %)  ████▏···············
2023-05 (May) : 14,349,293 ( 9.75 %)  █████████···········
2023-06 (Jun) : 22,554,193 (15.32 %)  ██████████████▏·····  ┐
2023-07 (Jul) : 29,461,403 (20.01 %)  ██████████████████▋·  ├─ Peak Summer Season (EL62 TOUR_SOE_02 = 71.08 %)
2023-08 (Aug) : 31,687,354 (21.53 %)  ████████████████████  │  (Greece Jun–Sep = 71.95 %)
2023-09 (Sep) : 22,215,646 (15.09 %)  ██████████████······  ┘
2023-10 (Oct) : 10,467,410 ( 7.11 %)  ██████▋·············
2023-11 (Nov) :  2,201,951 ( 1.50 %)  █▍··················
2023-12 (Dec) :  2,135,574 ( 1.45 %)  █▎··················

```

- **Historical Log:**
    - **2026-09-24** - Eurostat `tour_occ_nim` monthly nights verified at country level only (`geo=EL`); peak Aug = 21.53 %; Jun-Sep 71.95 %. No NUTS2 monthly publication.
    - **2026-10-03** - **Key note (reconciliation):** *what:* adopted **71.08 % peak-season share** (EL62, 2023) - NUTS2 level, replacing the country-level peak-month proxy; *why:* the dashboard's "seasonality" is a summer-season share, not the peak-month share we had used; *how:* read `TOUR_SOE_02` from the 2024 dashboard CSV export. *Flag:* exact month window (Jun-Sep vs Jul-Aug) to be confirmed from the methodology. → `VERIFIED`.

#### Data30 · Average length of stay (`Μέση διάρκεια παραμονής`) - `VERIFIED`

- **Source:** derived from Eurostat Data26 (nights ÷ arrivals) · EU Tourism Dashboard (`TOUR_DES_05`) · booking services (secondary).
- **Definition (confirmed):** `nights ÷ arrivals` (Data26). **Basis:** standard tourism statistic (Eurostat/UNWTO).
- **Data Pointers & Provenance:**
    - `Raw Sample (Nights)`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
    - `Raw Sample (Arrivals)`: `data/samples/eurostat-tour_occ_arn2-EL62-2022-2023.json`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (2 base observations: `5.928` nights in 2022, `5.930` nights in 2023; extended series verified to `5.58` in 2025)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json` · `data/manifests/source-verification-2026-10-01.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Derived join across two Eurostat JSON-stat 2.0 datasets (`tour_occ_nin2` and `tour_occ_arn2`) matched on `(geo="EL62", c_resid="TOTAL", unit="NR", nace_r2="I551-I553", time)`.
    - `Target Features`: `nights` (`tour_occ_nin2`), `arrivals` (`tour_occ_arn2`), derived ratio `avg_length_of_stay = round(nights / arrivals, 3)`.
    - `Handling & Transformation`: Aligns annual total overnight stays and total arrivals for `EL62` and computes `nights / arrivals` (`16,512,634 / 2,785,360 = 5.928` in 2022; `19,762,799 / 3,332,407 = 5.930` in 2023).
<details>
<summary>Raw Sample Payload / JSON Structure (Derived Observation Slice from <code>observations-2026-10-20.json</code>)</summary>
<pre><code class="language-json">[
    {
      &quot;observation_id&quot;: &quot;derived:Data30:nights_div_arrivals:2022&quot;,
      &quot;indicator_id&quot;: &quot;Data30&quot;,
      &quot;series_label&quot;: &quot;nights ÷ arrivals&quot;,
      &quot;observed_at&quot;: &quot;2022&quot;,
      &quot;spatial_ref&quot;: { &quot;level&quot;: &quot;NUTS2&quot;, &quot;code&quot;: &quot;EL62&quot; },
      &quot;value&quot;: 5.928,
      &quot;unit&quot;: &quot;nights&quot;
    },
    {
      &quot;observation_id&quot;: &quot;derived:Data30:nights_div_arrivals:2023&quot;,
      &quot;indicator_id&quot;: &quot;Data30&quot;,
      &quot;series_label&quot;: &quot;nights ÷ arrivals&quot;,
      &quot;observed_at&quot;: &quot;2023&quot;,
      &quot;spatial_ref&quot;: { &quot;level&quot;: &quot;NUTS2&quot;, &quot;code&quot;: &quot;EL62&quot; },
      &quot;value&quot;: 5.93,
      &quot;unit&quot;: &quot;nights&quot;
    }
]
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Average Length of Stay in EL62 (Nights ÷ Arrivals, 2022–2025)
2022 : 5.93 nights  ████████████████████  (16,512,634 nights ÷ 2,785,360 arrivals)
2023 : 5.93 nights  ████████████████████  (19,762,799 nights ÷ 3,332,407 arrivals)
2025 : 5.58 nights  ██████████████████▊·  (Gradual trend toward shorter stays)

```

- **Historical Log:**
    - **2026-10-01** - derived `nights ÷ arrivals`; 5.93 (2022) → 5.58 (2025).
    - **2026-10-03** - formula confirmed (`nights ÷ arrivals`); no longer `PROPOSAL`.

### Density & Typology - Πυκνότητα & Τυπολογία

#### Data31 · Tourism density (nights/km²) (`Τουριστική πυκνότητα`) - `VERIFIED`

- **Source:** Eurostat `tour_occ_nin2` (unit `P_KM2`) - `ec.europa.eu/eurostat`.
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
    - `Annotated Report`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (2 observations: `7,176.29` in 2022, `8,588.79` in 2023)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json`
    - `ETL Script`: `scripts/verification/pull-eurostat-tourism.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Eurostat JSON-stat 2.0 (`tour_occ_nin2`).
    - `Target Features`: `freq="A"`, `c_resid="TOTAL"`, `unit="P_KM2"` (Per square kilometre), `nace_r2="I551-I553"`, `geo="EL62"`, `time="2022, 2023"`.
    - `Handling & Transformation`: Decodes the JSON-stat cell for `(A, TOTAL, P_KM2, I551-I553, EL62, time)` directly from `tour_occ_nin2`.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eurostat-tour_occ_nin2-EL62-2022-2023.json</code> — P_KM2 slice)</summary>
<pre><code class="language-json">{
    &quot;dataset&quot;: &quot;tour_occ_nin2&quot;,
    &quot;geo&quot;: &quot;EL62&quot;,
    &quot;c_resid&quot;: &quot;TOTAL&quot;,
    &quot;nace_r2&quot;: &quot;I551-I553&quot;,
    &quot;unit&quot;: &quot;P_KM2&quot;,
    &quot;unit_label&quot;: &quot;Per square kilometre&quot;,
    &quot;values&quot;: {
      &quot;2022&quot;: 7176.29,
      &quot;2023&quot;: 8588.79
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Tourism Density in EL62 (Overnight Stays per km², Eurostat tour_occ_nin2)
2022 : 7,176.29 nights/km²  ████████████████▋···
2023 : 8,588.79 nights/km²  ████████████████████  (+19.68 % YoY increase)

```

- **Historical Log:**
    - **2026-09-22** - Eurostat `tour_occ_nin2` (unit `P_KM2`) verified.

#### Data32 · Dominant tourism typology (`Κυρίαρχη τυπολογία τουρισμού`) - `VERIFIED`

- **Source:** Eurostat `tour_occ_nin2` (`nace_r2` breakdown) - `ec.europa.eu/eurostat` (data already pulled) · EU Tourism Dashboard (`TOUR_DES_07`).
- **Definition (adopted, provisional):** dominant typology = `nace_r2` accommodation category with the highest share of nights → hotels (≈73 %). **Basis:** Eurostat NACE Rev. 2 accommodation categories.
- **Open question:** confirm "highest nights share" vs an alternative basis (bed-places or arrivals).
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
    - `Annotated Report`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (1 observation: `"hotels"` in `EL62`, 2023)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json` · `data/manifests/source-verification-2026-10-03.json`
    - `ETL Script`: `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Eurostat JSON-stat 2.0 (`tour_occ_nin2`) sliced across the `nace_r2` accommodation activity dimension.
    - `Target Features`: `nace_r2` categories: `I551` (Hotels and similar accommodation), `I552` (Holiday and other short-stay accommodation), `I553` (Camping grounds, recreational vehicle parks and trailer parks), with `c_resid="TOTAL"` and `unit="NR"`.
    - `Handling & Transformation`: Compares annual overnight stays across `I551`, `I552`, and `I553` in `EL62`, computes each category's percentage share of `I551-I553`, and selects `argmax(nights)` → `hotels` (`I551` = `71.40 %` in 2023).
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eurostat-tour_occ_nin2-EL62-2022-2023.json</code> — NACE Rev.2 breakdown)</summary>
<pre><code class="language-json">{
    &quot;dataset&quot;: &quot;tour_occ_nin2&quot;,
    &quot;geo&quot;: &quot;EL62&quot;,
    &quot;c_resid&quot;: &quot;TOTAL&quot;,
    &quot;unit&quot;: &quot;NR&quot;,
    &quot;nace_r2_breakdown&quot;: {
      &quot;2022&quot;: {
        &quot;I551_I553_total&quot;: 16512634,
        &quot;I551_hotels&quot;:     { &quot;nights&quot;: 12058229, &quot;share_pct&quot;: 73.02 },
        &quot;I552_short_stay&quot;: { &quot;nights&quot;: 4342233,  &quot;share_pct&quot;: 26.30 },
        &quot;I553_camping&quot;:    { &quot;nights&quot;: 112172,   &quot;share_pct&quot;: 0.68  }
      },
      &quot;2023&quot;: {
        &quot;I551_I553_total&quot;: 19762799,
        &quot;I551_hotels&quot;:     { &quot;nights&quot;: 14109340, &quot;share_pct&quot;: 71.40 },
        &quot;I552_short_stay&quot;: { &quot;nights&quot;: 5530039,  &quot;share_pct&quot;: 27.98 },
        &quot;I553_camping&quot;:    { &quot;nights&quot;: 123419,   &quot;share_pct&quot;: 0.62  }
      }
    },
    &quot;dominant_typology&quot;: &quot;hotels&quot;
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
EL62 Overnight Stays by Accommodation Typology (Eurostat NACE Rev.2, 2023)
I551 Hotels & Similar        : 14,109,340 nights (71.40 %)  ██████████████▎·····  [DOMINANT: "hotels"]
I552 Holiday & Short-Stay    :  5,530,039 nights (27.98 %)  █████▌··············
I553 Camping & RV Parks      :    123,419 nights ( 0.62 %)  ▏···················

```

- **Historical Log:**
    - **2026-09-22** - data pulled (`nace_r2` breakdown: hotels ≈73 %/71 %, short-stay ≈26 %/28 %, camping <1 %).
    - **2026-10-03** - classification rule adopted (provisional); open question logged.
    - **2026-10-03** - **Flag (reconciliation):** the dashboard's "Dominant tourism typology" (`TOUR_DES_07`) is a **categorical 6-class typology** and reads **class 4** for EL62 (2023) - a *different concept* from our "highest `nace_r2` nights share → hotels". The class-4 label (e.g. coastal/urban/rural) needs the dashboard's typology mapping; keep "hotels" for now but note the categorical definition differs.

#### Data33 · Foreign tourist share (%) (`Μερίδιο αλλοδαπών τουριστών (%)`) - `VERIFIED`

- **Source:** Eurostat `tour_occ_nin2` (`c_resid=FOR`, `PC_TOT`) - `ec.europa.eu/eurostat`.
- **Data Pointers & Provenance:**
    - `Raw Sample`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.json`
    - `Annotated Report`: `data/samples/eurostat-tour_occ_nin2-EL62-2022-2023.summary.md` · `.html`
    - `Curated Observation`: `data/curated/observations-2026-10-20.json` (2 observations: `93.72 %` in 2022, `93.58 %` in 2023)
    - `Manifest`: `data/manifests/source-verification-2026-09-22.json`
    - `ETL Script`: `scripts/verification/pull-eurostat-tourism.sh` · `scripts/verification/export_observations.py`
- **Raw Payload & Feature Extraction:**
    - `Payload Structure`: Eurostat JSON-stat 2.0 (`tour_occ_nin2`).
    - `Target Features`: `freq="A"`, `c_resid="FOR"` (Foreign country of residence), `unit="PC_TOT"` (Percentage of total), `nace_r2="I551-I553"`, `geo="EL62"`, `time="2022, 2023"`.
    - `Handling & Transformation`: Decodes the JSON-stat value at index `80` (`2022: 93.72 %`) and index `81` (`2023: 93.58 %`), cross-verified against raw counts `FOR / TOTAL = 18,493,790 / 19,762,799 = 93.579 %`.
<details>
<summary>Raw Sample Payload / JSON Structure (<code>eurostat-tour_occ_nin2-EL62-2022-2023.json</code> — c_resid breakdown)</summary>
<pre><code class="language-json">{
    &quot;dataset&quot;: &quot;tour_occ_nin2&quot;,
    &quot;geo&quot;: &quot;EL62&quot;,
    &quot;nace_r2&quot;: &quot;I551-I553&quot;,
    &quot;origin_breakdown&quot;: {
      &quot;2022&quot;: { &quot;foreign_nights_FOR&quot;: 15475156, &quot;domestic_nights_DOM&quot;: 1037478, &quot;foreign_share_PC_TOT&quot;: 93.72 },
      &quot;2023&quot;: { &quot;foreign_nights_FOR&quot;: 18493790, &quot;domestic_nights_DOM&quot;: 1269009, &quot;foreign_share_PC_TOT&quot;: 93.58 }
    }
}
</code></pre>
</details>
- **Visualizations & Data Findings:**

```
Origin Breakdown of Overnight Stays in EL62 (Eurostat tour_occ_nin2, 2022–2023)
2022 Foreign Share (FOR)  : 93.72 %  ██████████████████▊·  (15,475,156 nights)
2022 Domestic Share (DOM) :  6.28 %  █▎··················  ( 1,037,478 nights)
2023 Foreign Share (FOR)  : 93.58 %  ██████████████████▋·  (18,493,790 nights)
2023 Domestic Share (DOM) :  6.42 %  █▎··················  ( 1,269,009 nights)

```

- **Historical Log:**
    - **2026-09-22** - Eurostat `tour_occ_nin2` (`c_resid=FOR`, `PC_TOT`) verified.

### Participation - Συμμετοχικότητα

#### Data34 · User feedback (`Αξιολογήσεις χρηστών`) - `UNVERIFIED`

- **Source:** TripAdvisor / Google Reviews (paid, privacy-sensitive) · EU Tourism Dashboard · app's own citizen/visitor feedback feed.
- **Data Pointers & Provenance:** No pull artifact present (commercial API licensing and GDPR/privacy minimization rules apply; scraping is prohibited under `AGENTS.md`).
- **Raw Payload & Feature Extraction:**
    - `Target Ingestion Schema`: Aggregated, PII-stripped destination satisfaction payload (`poi_category`, `island_nuts3`, `period`, `review_count`, `mean_rating_1_5`, `sentiment_band`). Free-text reviews and reviewer handles are excluded at ingestion.
<details>
<summary>Target JSON Schema (Unverified Feed Specification)</summary>
<pre><code class="language-json">{
    &quot;indicator_id&quot;: &quot;Data34&quot;,
    &quot;island_nuts3&quot;: &quot;EL622&quot;,
    &quot;poi_category&quot;: &quot;cultural_and_beaches&quot;,
    &quot;period&quot;: &quot;2026-Q3&quot;,
    &quot;review_count&quot;: 420,
    &quot;mean_rating_1_5&quot;: 4.42
}
</code></pre>
</details>
- **Visualizations & Data Findings:** No pull artifact present.

---

## 3 · What we are working on next (work queue)

Ordered roughly by impact; update the top of this list as work proceeds.

### Source verification — next `agy` run (Data07 production path)

- **What OLKE (Corfu Port Authority, `corfuport.gr`) provides.** Verify the actual recurring artefact: format (structured feed / API / PDF), update cadence, port & vessel coverage, access/licence terms, and whether it carries per-call passenger capacity plus arrival/departure times. **Unverified.** Data07 currently substitutes a one-time CruiseMapper read; this must be verified before the model can be treated as authoritative. *(logs/session-log-2026-10-14.md "What remains open"; sources/data-resources.md Data07)*
- **Non-Corfu ferry schedules** — operator timetables/frequency matrices for the 5 domestic operators (research-notes §2A) and the Greek NAP export refresh path are also **unverified**; confirm before extending the model beyond the 2025 baseline.

### A · Finish the `PARTIAL` indicators

1. **Data06 congestion score** - research done (EUROCONTROL ATFM delay cited); adopt the `min(1, count-in-buffer ÷ threshold)` live proxy as the working formula (still a proposal) and wire the OpenSky feed into a score. **Data07 is done** (anticipated schedule-based congestion, 2026-10-14) — the live-AIS path is superseded; remaining Data07 work is only formula sign-off and a production OLKE schedule feed.
2. ~~**Data19 Airbnb keys**~~ **DONE 2026-10-15** - InsideAirbnb is non-viable for EL62; Data19 resolved via Eurostat `tour_ce_omn12` (see history) and promoted to `VERIFIED`.
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
