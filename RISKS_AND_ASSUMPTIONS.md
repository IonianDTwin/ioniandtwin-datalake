# RISKS AND ASSUMPTIONS — IonianDTwin

## Risks

- `DECISION` (confirmed 2026-09-24, D-007) **Data35** — the GSTC A5 & A6 mapping's "Data 24, 35" is a transcription error for **Data34** (user feedback). User confirmed "35" → "34"; no new indicator invented.
- `DECISION` (confirmed 2026-09-24, D-008) **Duplicate Data15** — Data15 = "Ποιότητα Αέρα" (Air quality). The corrected source removed the second entry, "Πρόταση AI για εσωτερικές δραστηριότητες". Scope overlap with Data01 (airport CO2 vs ambient air quality) noted, not an error.
- `RISK` **Source availability and licensing unverified.** Copernicus CAMS/CMEMS, EU Tourism Dashboard, OpenWeatherMap/Meteo.gr, Google Maps, MarineTraffic, FlightRadar24, TripAdvisor/Google Reviews, and local transport telematics are all candidate sources whose access, terms of use, cost, and schema are unknown until tested.
- `RISK` **Third-party data feasibility.** Google Maps, FlightRadar24, MarineTraffic, Airbnb, review platforms, telecom, hospital, utility, and business-partner data may be paid, licensed, or privacy-sensitive; each is a separate feasibility track.
- `RISK` **Privacy of participatory data.** Citizen reports, reviews, exact locations, inferred mobility, contact data, and free text are potentially sensitive; GDPR-oriented governance required before any production ingestion.
- `RISK` **Unverified data driving decisions.** Unverified data must not trigger public alerts, automated enforcement, or policy recommendations.

## Assumptions

- `ASSUMPTION` The technical proposal is a requirements baseline, not proof of operational sources, APIs, licenses, or data-access routes.
- `ASSUMPTION` (D-011) The proposal's source column is a **suggestion**; free/no-cost alternatives are preferred and are expected to cover the majority of Data01–Data34 before any paid API is considered.
- `ASSUMPTION` The two `.plesk.page` web applications are reachable and publicly inspectable — verified by the application inspection (`docs/validation/application-inspection-report.md`).
- `ASSUMPTION` Eurostat tourism statistics, EEA bathing water (Discodata), and Open-Meteo weather/UV are the verified first sources; the remaining candidates are untested or credential-gated.
- `ASSUMPTION` ISO 8601 timestamps with explicit time zones will be used for observations; this is a convention decision, not yet enforced by any pipeline.
