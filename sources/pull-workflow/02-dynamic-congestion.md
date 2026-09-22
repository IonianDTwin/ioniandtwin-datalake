# Pull Workflow — 02 Dynamic Congestion

**Category:** Dynamic Congestion (Real-time) — `Δυναμική Συμφόρηση`
**Indicators:** Data06–Data10
**Pillar:** Economy / Society (mobility pressure)

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data06 | Airport congestion | MarineTraffic / FlightRadar24 | api | API key (paid) | UNVERIFIED |
| Data07 | Port congestion | MarineTraffic | api | API key (paid) | UNVERIFIED |
| Data08 | Road congestion | Google Maps API | api | API key (paid) | UNVERIFIED |
| Data09 | Beach congestion | user reports | user_reports | app | UNVERIFIED |
| Data10 | City congestion | Google Maps API; user reports | api / user_reports | API key (paid) / app | UNVERIFIED |

## Pull process

### Data06 / Data07 — Airport & port congestion (AIS / flight feeds)

1. **Request** — MarineTraffic vessel-positions API and/or FlightRadar24 arrivals API for the Ionian ports/airports (Corfu, Zakynthos, Kefalonia, Lefkada).
2. **Store raw / manifest** — bounded sample under `data/samples/`; full feed under `data/raw/`.
3. **Transform** — count active vessels/aircraft within a port/airport buffer per time window → congestion observation.
4. **Cadence** — near-real-time / ~30-minute where justified.

### Data08 / Data10 — Road & city congestion (Google Maps)

1. **Request** — Google Maps Routes/Directions or Traffic layer. Requires a Google Maps Platform API key in `.env`.
2. **Store raw / manifest** as above.
3. **Transform** — travel-time delay or congestion level per road segment / city zone.
4. **Feasibility** — `RISK` paid API; ToS and cost must be verified before integration (`ROADMAP.md`).

### Data09 — Beach congestion (citizen reports)

1. **Request** — Mobile-app reports via the project's own backend (internal). No external endpoint exists to pull.
2. **Cross-verify** — citizen reports must be cross-checked against sensor/IoT data before updating the twin (`pipelines/quality-rules.md`).

## Notes & blockers

- `BLOCKER` MarineTraffic, FlightRadar24, and Google Maps all require paid API keys and independent ToS/cost verification.
- `BLOCKER` No external source verified in this category yet; all entries are candidate (`UNVERIFIED`).
- Beach/city congestion partly depends on citizen reports, which are the project's own participatory feed, not an external pull.
