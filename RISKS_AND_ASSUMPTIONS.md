# RISKS AND ASSUMPTIONS — IonianDTwin

## Risks

- `RISK` **Data35** — the GSTC mapping for A5 & A6 references "Data 24, 35", but the indicator catalogue ends at Data34. `BLOCKER` for requirements clarification. Do not invent or remap Data35.
- `RISK` **Duplicate Data15** — the Climate Adaptation category lists both "Data 15. Ποιότητα Αέρα" and "Data 15. Πρόταση AI για εσωτερικές δραστηριότητες". Also "Ποιότητα Αέρα" (air quality) overlaps the Environmental Health category's air-quality scope. `BLOCKER` for a clean normalized catalogue.
- `RISK` **Source availability and licensing unverified.** Copernicus CAMS/CMEMS, EU Tourism Dashboard, OpenWeatherMap/Meteo.gr, Google Maps, MarineTraffic, FlightRadar24, TripAdvisor/Google Reviews, and local transport telematics are all candidate sources whose access, terms of use, cost, and schema are unknown until tested.
- `RISK` **Third-party data feasibility.** Google Maps, FlightRadar24, MarineTraffic, Airbnb, review platforms, telecom, hospital, utility, and business-partner data may be paid, licensed, or privacy-sensitive; each is a separate feasibility track.
- `RISK` **Privacy of participatory data.** Citizen reports, reviews, exact locations, inferred mobility, contact data, and free text are potentially sensitive; GDPR-oriented governance required before any production ingestion.
- `RISK` **Unverified data driving decisions.** Unverified data must not trigger public alerts, automated enforcement, or policy recommendations.

## Assumptions

- `ASSUMPTION` The technical proposal is a requirements baseline, not proof of operational sources, APIs, licenses, or data-access routes.
- `ASSUMPTION` The two `.plesk.page` web applications are reachable and publicly inspectable — verified by the application inspection (`docs/validation/application-inspection-report.md`).
- `ASSUMPTION` Weather/UV (OpenWeatherMap / Meteo.gr), EU Tourism Dashboard, and Copernicus are the highest-priority first sources; none has been pull-tested yet.
- `ASSUMPTION` ISO 8601 timestamps with explicit time zones will be used for observations; this is a convention decision, not yet enforced by any pipeline.
