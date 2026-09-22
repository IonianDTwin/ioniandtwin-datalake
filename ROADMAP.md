# ROADMAP — IonianDTwin

`DECISION` Follow a thin, reproducible vertical slice before any full Digital Twin implementation. Ordered priority from the technical proposal:

1. `VERIFIED` Create the isolated workstation and Markdown knowledge base. **Done.**
2. Extract and normalise the proposed indicators. **Partially done** — catalogue written from the proposal; metadata/schema normalisation pending.
3. Create the source registry and verification matrix. **Scaffolded** — `sources/`; content from proposal written; verification pending.
4. Inspect the two project web applications safely. **Done** (`docs/validation/application-inspection-report.md`).
5. Verify safe public/read-only data access routes. **Partially done** (`docs/validation/api-verification-report.md`) — Eurostat, Open-Meteo, Copernicus CDSE catalogue verified; credential-gated sources remain.
6. Start with weather/UV, one official tourism-statistics source, and one environmental source where verification permits. **Done** — Eurostat tourism + Open-Meteo weather/UV verified; Copernicus catalogue reachable (download gated).
7. Define the normalized observation schema and data-quality checks. **Scaffolded** — `schemas/observation-schema.json`, `pipelines/quality-rules.md`.
8. Produce a simple dashboard-ready API/data response and a transparent composite-indicator prototype. **Pending.**
9. Expand only after data contracts and provenance are stable.

## Deferred (do not start yet)

`DECISION` Production-scale forecasting, RAG/vector infrastructure, Kafka, public alerts, mobile-app integration, and sensitive data integrations are deferred until source access, data contracts, legal constraints, security requirements, and data-quality checks are verified.

`DECISION` Google Maps, FlightRadar24, MarineTraffic, Airbnb, review platforms, telecom, hospital, utility, and business-partner data are separate feasibility tracks — their availability, cost, terms of use, licensing, privacy, technical access, and operational reliability must be independently verified.

## Related files

- `sources/data-resources.md` — Data01–Data34 resource list (link + access procedure + ETL per indicator).
- `sources/source-registry.md`, `sources/source-verification-matrix.md` — source inventory and verification state.
- `sources/pull-workflow/` — per-indicator-section pull recipes; `sources/procedures/` — document extraction.
- `docs/validation/api-verification-report.md`, `docs/validation/pdf-verification-report.md` — pull/document evidence.
