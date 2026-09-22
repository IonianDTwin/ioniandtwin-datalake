# Indicator Catalogue — Data01–Data34

`VERIFIED` This catalogue is transcribed from the technical proposal (`Παράρτημα - Συνοδευτικό Πρότασης με Τεχνικές Λεπτομέρειες.docx`). Field names and descriptions are the proposal's own; units, formulas, polarity, and exact schemas are **not** specified in the proposal and are marked `ASSUMPTION` or left blank rather than invented.

## Normalised fields

Each indicator will carry at minimum: `indicator_id`, `name`, `category`, `strategic_pillar`, `description`, `formula`, `unit`, `polarity`, `spatial_level`, `temporal_resolution`, `source_ids`, `GSTC_mapping`, `owner`, `status`, `notes`. Machine-readable metadata lives in `indicator-metadata.yaml`.

## Catalogue

### Environmental Health & Pollutants (`Περιβαλλοντική Υγεία & Ρύποι`)

| ID | Name (EN) | Name (EL) | Source candidates |
|---|---|---|---|
| Data01 | Airport CO2 levels | Επίπεδα CO2 αεροδρομίων | Copernicus CAMS, local IoT stations |
| Data02 | Excellent bathing waters (%) | Άριστα νερά κολύμβησης (%) | Copernicus CMEMS, EU Tourism Dashboard |
| Data03 | Clean beach water (reports) | Καθαρό νερό παραλίας (Reports) | Copernicus CMEMS, user reports |
| Data04 | Blue Flags | Γαλάζιες Σημαίες | EU Tourism Dashboard |
| Data05 | EMAS / EU Ecolabel | EMAS / EU Ecolabel | EU Tourism Dashboard |

### Dynamic Congestion (Real-time) (`Δυναμική Συμφόρηση`)

| ID | Name | Source candidates |
|---|---|---|
| Data06 | Airport congestion | MarineTraffic / FlightRadar24 |
| Data07 | Port congestion | MarineTraffic |
| Data08 | Road congestion | Google Maps API |
| Data09 | Beach congestion | User reports |
| Data10 | City congestion | Google Maps API, user reports |

### Sustainable Transport (`Βιώσιμες Μεταφορές`)

| ID | Name | Source candidates |
|---|---|---|
| Data11 | KTEL (bus) congestion | Local transport telematics |
| Data12 | Urban transit congestion | Local transport telematics |

### Climate Adaptation (`Κλιματική Προσαρμογή`)

| ID | Name | Source candidates |
|---|---|---|
| Data13 | Weather conditions (temp, rain, …) | OpenWeatherMap, Meteo.gr |
| Data14 | High UV and protection | OpenWeatherMap, Meteo.gr |
| Data15 | Air quality — `RISK` duplicate label | (see note) |
| Data15 | AI proposal for indoor activities — `RISK` duplicate label | (LLM output, not an external source) |

### Social Pressure & Infrastructure (`Κοινωνική Πίεση & Υποδομές`)

| ID | Name | Source candidates |
|---|---|---|
| Data16 | Tourism intensity (nights/residents) | EU Tourism Dashboard |
| Data17 | Hospital / infrastructure congestion | official outage announcements, user reports |
| Data18 | Power / water outage | official announcements, user reports |
| Data19 | Short-term rental share (Airbnb) | EU Tourism Dashboard, Airbnb (feasibility track) |

### Digital Infrastructure (`Ψηφιακή Υποδομή`)

| ID | Name | Source candidates |
|---|---|---|
| Data20 | Internet speed (>100 Mb/s) | User reports |
| Data21 | 4G/5G availability | User reports |

### Spatial Sustainability (`Χωροταξική Αειφορία`)

| ID | Name | Source candidates |
|---|---|---|
| Data22 | Tourist diversity (zones) | EU Tourism Dashboard maps |
| Data23 | Density of cultural elements | EU Tourism Dashboard maps |
| Data24 | Protected land (%) | EU Tourism Dashboard maps |
| Data25 | Accommodation in high-value areas | EU Tourism Dashboard maps |

### Tourism Performance (`Τουριστική Απόδοση`)

| ID | Name | Source candidates |
|---|---|---|
| Data26 | Arrivals & overnight stays | EU Tourism Dashboard |
| Data27 | Tourism capacity (beds) | EU Tourism Dashboard |
| Data28 | Occupancy rate (%) | Social media & booking services |
| Data29 | Seasonality (%) | EU Tourism Dashboard |
| Data30 | Average length of stay | EU Tourism Dashboard, booking services |

### Density & Typology (`Πυκνότητα & Τυπολογία`)

| ID | Name | Source candidates |
|---|---|---|
| Data31 | Tourism density (nights/km²) | EU Tourism Dashboard |
| Data32 | Dominant tourism typology | EU Tourism Dashboard |
| Data33 | Foreign tourist share (%) | EU Tourism Dashboard |

### Participation (`Συμμετοχικότητα`)

| ID | Name | Source candidates |
|---|---|---|
| Data34 | User feedback | TripAdvisor / Google Reviews API, EU Tourism Dashboard |

## GSTC v2.0 mapping (from proposal)

| GSTC criterion | Title | Mapped Data |
|---|---|---|
| A2 | Strategy & Action Plan | 7, 10, 19, 22, 27, 32, 33 |
| A3 | Monitoring & Reporting | 1, 6, 9, 12, 26, 27, 28, 29 |
| A5 & A6 | Resident & Visitor Engagement | 24, **35** |
| A8 | Volume & Pressure Management | 1, 2, 3, 4, 5, 6, 8, 9, 10, 16, 21, 22, 31 |
| A10 & A11 | Climate Adaptation & Crises | 13, 14, 15, 16, 17, 23, 34 |
| B1 | Economic Contribution | 30, 31, 32 |
| B7 | Safety & Health | 16, 17, 18, 23, 24 |
| B8 | Access for All & Digital Infrastructure | 20, 21, 25, 26 |
| Γ1 & Γ6 | Cultural Protection & Management | 11, 15, 20, 23 |
| Δ1 & Δ3 | Natural Heritage Protection | 5, 13, 19 |
| Δ4 | Environmental Signage | 18 |
| Δ7 | Water Quality | 13, 14, 15 |
| Δ10 | Climate Change Mitigation | 12 |
| Δ11 | Low-impact Transport | 11, 12, 21, 22 |

## Known inconsistencies (do not resolve silently)

- `BLOCKER` **Data35** appears in GSTC A5 & A6 mapping but the catalogue ends at Data34.
- `RISK` **Duplicate Data15** in Climate Adaptation: "Ποιότητα Αέρα" (air quality) and "Πρόταση AI για εσωτερικές δραστηριότητες" (AI indoor-activity suggestion). The latter is an LLM output, not an external data source.
- `RISK` "Air quality" appears both as Data01 (airport CO2) under Environmental Health and as Data15 under Climate Adaptation — possible overlap.
