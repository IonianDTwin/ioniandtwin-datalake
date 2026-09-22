# IonianDTwin — indicator data index

Data01–Data34 grouped by category, with verified values and links to the sample reports in `data/samples/`.

## Environmental Health & Pollutants — Περιβαλλοντική Υγεία & Ρύποι

### Data01 · Airport CO2 levels (Επίπεδα CO2 αεροδρομίων) — `UNVERIFIED`

- Source: Copernicus CAMS; local IoT stations
- Access: `api` · Auth: `registration / partner`
- Note: Air pollutants (CO2/NO2/PM) around entry gates. CAMS download needs a registration token.

### Data02 · Excellent bathing waters (%) (Άριστα νερά κολύμβησης (%)) — `UNVERIFIED`

- Source: Copernicus CMEMS; EU Tourism Dashboard
- Access: `api` · Auth: `registration / none`

### Data03 · Clean beach water (reports) (Καθαρό νερό παραλίας (Reports)) — `UNVERIFIED`

- Source: Copernicus CMEMS; user reports
- Access: `api / user_reports` · Auth: `registration / app`

### Data04 · Blue Flags (Γαλάζιες Σημαίες) — `UNVERIFIED`

- Source: EU Tourism Dashboard
- Access: `download` · Auth: `none`

### Data05 · EMAS / EU Ecolabel (EMAS / EU Ecolabel) — `UNVERIFIED`

- Source: EU Tourism Dashboard
- Access: `download` · Auth: `none`

## Dynamic Congestion — Δυναμική Συμφόρηση

### Data06 · Airport congestion — `UNVERIFIED`

- Source: MarineTraffic / FlightRadar24
- Access: `api` · Auth: `API key (paid)`

### Data07 · Port congestion — `UNVERIFIED`

- Source: MarineTraffic
- Access: `api` · Auth: `API key (paid)`

### Data08 · Road congestion — `UNVERIFIED`

- Source: Google Maps API
- Access: `api` · Auth: `API key (paid)`

### Data09 · Beach congestion — `UNVERIFIED`

- Source: user reports
- Access: `user_reports` · Auth: `app`

### Data10 · City congestion — `UNVERIFIED`

- Source: Google Maps API; user reports
- Access: `api / user_reports` · Auth: `API key (paid) / app`

## Sustainable Transport — Βιώσιμες Μεταφορές

### Data11 · KTEL (bus) congestion — `UNVERIFIED`

- Source: local transport telematics
- Access: `internal` · Auth: `partner`

### Data12 · Urban transit congestion — `UNVERIFIED`

- Source: local transport telematics
- Access: `internal` · Auth: `partner`

## Climate Adaptation — Κλιματική Προσαρμογή

### Data13 · Weather conditions (temp, rain, …) — `VERIFIED`

- Source: Open-Meteo (substitute); OpenWeatherMap / Meteo.gr (proposal)
- Access: `api` · Auth: `none (Open-Meteo) / API key (OpenWeatherMap)`
  - **air temperature** (°C): `26.5 °C` → [viewer](open-meteo-corfu-forecast-2026-09-22.html) · [md](open-meteo-corfu-forecast-2026-09-22.summary.md)
  - **relative humidity** (%): `57 %` → [viewer](open-meteo-corfu-forecast-2026-09-22.html) · [md](open-meteo-corfu-forecast-2026-09-22.summary.md)
  - **apparent (feels-like) temperature** (°C): `28.8 °C` → [viewer](open-meteo-corfu-forecast-2026-09-22.html) · [md](open-meteo-corfu-forecast-2026-09-22.summary.md)

### Data14 · High UV and protection — `VERIFIED`

- Source: Open-Meteo (substitute); OpenWeatherMap / Meteo.gr (proposal)
- Access: `api` · Auth: `none (Open-Meteo) / API key (OpenWeatherMap)`
  - **max UV index**: `5.9` → [viewer](open-meteo-corfu-forecast-2026-09-22.html) · [md](open-meteo-corfu-forecast-2026-09-22.summary.md)

### Data15 · Air quality / AI indoor-activity proposal — `UNVERIFIED`

- Source: CAMS (air quality); LLM output (indoor suggestion)
- Access: `api / internal` · Auth: `registration / local`
- Note: RISK duplicate label in the proposal: air quality and an AI indoor-activity suggestion. Treat as two concerns.

## Social Pressure & Infrastructure — Κοινωνική Πίεση & Υποδομές

### Data16 · Tourism intensity (nights/residents) — `VERIFIED`

- Source: Eurostat tour_occ_nin2
- Access: `api` · Auth: `none`
  - **nights per 1000 residents**: `2022: 80,912.16 · 2023: 97,705.53` → [viewer](eurostat-tour_occ_nin2-EL62-2022-2023.html) · [md](eurostat-tour_occ_nin2-EL62-2022-2023.summary.md)

### Data17 · Hospital / infrastructure congestion — `UNVERIFIED`

- Source: official announcements; user reports
- Access: `web / user_reports` · Auth: `none / app`

### Data18 · Power / water outage — `UNVERIFIED`

- Source: official announcements; user reports
- Access: `web / user_reports` · Auth: `none / app`

### Data19 · Short-term rental share (Airbnb) — `UNVERIFIED`

- Source: EU Tourism Dashboard; Airbnb
- Access: `api` · Auth: `none / API key`

## Digital Infrastructure — Ψηφιακή Υποδομή

### Data20 · Internet speed (>100 Mb/s) — `UNVERIFIED`

- Source: user reports
- Access: `user_reports` · Auth: `app`

### Data21 · 4G/5G availability — `UNVERIFIED`

- Source: user reports
- Access: `user_reports` · Auth: `app`

## Spatial Sustainability — Χωροταξική Αειφορία

### Data22 · Tourist diversity (zones) — `UNVERIFIED`

- Source: EU Tourism Dashboard maps
- Access: `download` · Auth: `none`

### Data23 · Density of cultural elements — `UNVERIFIED`

- Source: EU Tourism Dashboard maps
- Access: `download` · Auth: `none`

### Data24 · Protected land (%) — `UNVERIFIED`

- Source: EU Tourism Dashboard maps
- Access: `download` · Auth: `none`

### Data25 · Accommodation in high-value areas — `UNVERIFIED`

- Source: EU Tourism Dashboard maps
- Access: `download` · Auth: `none`

## Tourism Performance — Τουριστική Απόδοση

### Data26 · Arrivals & overnight stays — `VERIFIED`

- Source: Eurostat tour_occ_nin2 + tour_occ_arn2
- Access: `api` · Auth: `none`
  - **overnight stays** (nights): `2022: 16,512,634 · 2023: 19,762,799` → [viewer](eurostat-tour_occ_nin2-EL62-2022-2023.html) · [md](eurostat-tour_occ_nin2-EL62-2022-2023.summary.md)
  - **arrivals**: `2022: 2,785,360 · 2023: 3,332,407` → [viewer](eurostat-tour_occ_arn2-EL62-2022-2023.html) · [md](eurostat-tour_occ_arn2-EL62-2022-2023.summary.md)

### Data27 · Tourism capacity (beds) — `VERIFIED`

- Source: Eurostat tour_cap_nuts2
- Access: `api` · Auth: `none`
  - **bed-places**: `2022: 159,790 · 2023: 155,968` → [viewer](eurostat-tour_cap_nuts2-EL62-2022-2023.html) · [md](eurostat-tour_cap_nuts2-EL62-2022-2023.summary.md)

### Data28 · Occupancy rate (%) — `UNVERIFIED`

- Source: social media & booking services
- Access: `api` · Auth: `API key`

### Data29 · Seasonality (%) — `UNVERIFIED`

- Source: Eurostat monthly series (to be identified)
- Access: `api` · Auth: `none`
- Note: Requires a monthly nights/arrivals series; the verified datasets are annual.

### Data30 · Average length of stay — `PROPOSAL`

- Source: Eurostat (derived); booking services
- Access: `api` · Auth: `none / API key`
- Note: Derivable as nights ÷ arrivals from Data26 (≈ 5.9 nights 2022/2023); formula to confirm.

## Density & Typology — Πυκνότητα & Τυπολογία

### Data31 · Tourism density (nights/km²) — `VERIFIED`

- Source: Eurostat tour_occ_nin2
- Access: `api` · Auth: `none`
  - **nights per km²**: `2022: 7,176.29 · 2023: 8,588.79` → [viewer](eurostat-tour_occ_nin2-EL62-2022-2023.html) · [md](eurostat-tour_occ_nin2-EL62-2022-2023.summary.md)

### Data32 · Dominant tourism typology — `PARTIAL`

- Source: Eurostat tour_occ_nin2 (nace_r2 breakdown)
- Access: `api` · Auth: `none`
- Note: Data already pulled. Accommodation-type shares of nights (EL62): hotels (I551) ≈73% (2022) / 70% (2023), short-stay (I552) ≈26% / 30%, camping (I553) <1%. 'Dominant typology' = hotels (ASSUMPTION); the classification rule is not defined in the proposal and must be confirmed before emitting a final value.

### Data33 · Foreign tourist share (%) — `VERIFIED`

- Source: Eurostat tour_occ_nin2
- Access: `api` · Auth: `none`
  - **foreign share** (% of total): `2022: 93.72 · 2023: 93.58` → [viewer](eurostat-tour_occ_nin2-EL62-2022-2023.html) · [md](eurostat-tour_occ_nin2-EL62-2022-2023.summary.md)

## Participation — Συμμετοχικότητα

### Data34 · User feedback — `UNVERIFIED`

- Source: TripAdvisor / Google Reviews API; EU Tourism Dashboard
- Access: `api` · Auth: `API key`
