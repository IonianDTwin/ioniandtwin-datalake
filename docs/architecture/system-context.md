# System Context

`PROPOSAL` Context-level view of IonianDTwin. No implementation exists yet.

```text
External sources                      IonianDTwin                           Consumers
──────────────────────               ────────────────────                  ─────────────
Copernicus CAMS / CMEMS ──┐
EU Tourism Dashboard ─────┤        ┌───────────────────┐                 Institutional users
OpenWeatherMap / Meteo.gr ┤  read  │  Ingestion (30min) │                 (Web Dashboard)
Google Maps / MarineTraffic├──────▶│  Data Lake → ETL   │── indicators ─▶ Businesses (API GW)
FlightRadar24 / Fraport ──┘        │  Data Warehouse    │── forecasts ─▶ Residents/Visitors
Local transport telematics          │  ML / anomaly det. │── alerts    ─▶ (Mobile App)
TripAdvisor / Google Reviews        │  Local LLM         │── Open Data ─▶ Academia
Mobile app reports ─────────────────▶└───────────────────┘
```

## Trust boundaries (initial)

See `SECURITY_PRIVACY_ETHICS.md` for the six trust boundaries to review.

## Key external actors

- **Copernicus CAMS / CMEMS** — air quality, marine / sea-surface indicators.
- **EU Tourism Dashboard (Eurostat)** — tourism statistics at NUTS 2.
- **OpenWeatherMap / Meteo.gr** — weather and UV.
- **Google Maps, MarineTraffic, FlightRadar24, Fraport** — mobility / congestion.
- **Local transport telematics** — bus / urban transit occupancy.
- **TripAdvisor / Google Reviews** — sentiment for visitor satisfaction.
- **Citizens / visitors** — participatory reports via the mobile app.

`RISK` All external actors are candidate sources; availability, terms, and schemas are unverified.
