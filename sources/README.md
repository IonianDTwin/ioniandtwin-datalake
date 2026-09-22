# Sources — index

`DECISION` This directory records every candidate data source, its verification state, and the per-indicator pull recipes. Start here, then drill into the file you need.

## Read order

1. `data-resources.md` — **Data01–Data34 resource list**: online link + access procedure + ETL per indicator.
2. `source-registry.md` — the reconciled source inventory (proposal + deployed app).
3. `source-verification-matrix.md` — one row per source with live verification status.
4. `api-sources.md` — verified and gated API endpoints.
5. `pdf-and-document-sources.md` — verified and candidate downloadable documents.
6. `application-endpoints.md` — what the deployed web app exposes.
7. `pull-workflow/` — the agentic pull recipes, one per indicator section.
8. `procedures/` — download-and-extract procedures for non-API sources.

## Verified links (2026-09-22)

- **Eurostat — nights (NUTS2, EL62 = Ionia Nisia):** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023`
- **Eurostat — arrivals (NUTS2):** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023`
- **Eurostat — capacity/bed-places (NUTS2):** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023`
- **Open-Meteo — weather + UV (no-key substitute):** `https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1`
- **Copernicus CDSE catalogue:** `https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$top=1&$format=json`
- **GSTC Destination Criteria v2.0 PDF:** `https://www.gstc.org/wp-content/uploads/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`

Evidence and checksums: `data/manifests/source-verification-2026-09-22.json` · `docs/validation/api-verification-report.md` · `docs/validation/pdf-verification-report.md`.

## Status

`VERIFIED` four no-key sources and one PDF. `BLOCKER` credential-gated sources (OpenWeatherMap, CAMS/CMEMS download, Google Maps, MarineTraffic, FlightRadar24, Airbnb, review platforms) remain unverified pending keys/registration.
