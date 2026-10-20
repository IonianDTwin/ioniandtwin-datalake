# Pull Workflow — 02 Dynamic Congestion

**Category:** Dynamic Congestion (Real-time) — `Δυναμική Συμφόρηση`
**Indicators:** Data06–Data10
**Pillar:** Economy / Society (mobility pressure)

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data06 | Airport congestion | OpenSky Network / FlightRadar24 | api | none (OpenSky) / API key (FlightRadar24) | PARTIAL |
| Data07 | Port congestion | CruiseMapper + Greek NAP (anticipated model) | download | none | PROPOSAL |
| Data08 | Road congestion | Google Maps API | api | API key (paid) | UNVERIFIED |
| Data09 | Beach congestion | user reports | user_reports | app | UNVERIFIED |
| Data10 | City congestion | Google Maps API; user reports | api / user_reports | API key (paid) / app | UNVERIFIED |

## Pull process

### Data06 — Airport congestion (live flight feed)

1. **Request** — FlightRadar24 arrivals API or the free OpenSky Network states API (`opensky-network.org/api/states/all`, no key) for the Ionian airports (Corfu, Zakynthos, Kefalonia, Lefkada).
2. **Store raw / manifest** — bounded sample under `data/samples/`; full feed under `data/raw/`.
3. **Transform** — count active aircraft within an airport approach buffer per time window → congestion observation.
4. **Cadence** — near-real-time / ~30-minute where justified.

### Data07 — Anticipated port congestion (schedule-based compute, 2026-10-14)

`DECISION` Data07 no longer pulls a live AIS feed (zero receiver coverage in Corfu harbour; snapshots only, no forecasting). It is computed from planned cruise schedules + the empirical ferry baseline:

1. **Inputs** — `scratch/cruise-pressure/schedules.json` (CruiseMapper one-time read) + `scratch/ais-routes/export_sailing_traffic.csv` (Greek NAP, Mar–Nov 2025).
2. **Compute** — `scripts/verification/compute-data07-anticipated-congestion.py` (see `indicators/derived-indicator-formulas.md` §Anticipated Port Congestion).
3. **Outputs** — `data/curated/scheduled-port-traffic-el62.json` + `observations-data07-anticipated-congestion-*.json` / `.csv`.
4. **Cadence** — daily forecast recompute; refresh the OLKE port-authority schedule feed (production) and the NAP export (baseline) as they update.

### Data08 / Data10 — Road & city congestion (Google Maps)

1. **Request** — Google Maps Routes/Directions or Traffic layer. Requires a Google Maps Platform API key in `.env`.
2. **Store raw / manifest** as above.
3. **Transform** — travel-time delay or congestion level per road segment / city zone.
4. **Feasibility** — `RISK` paid API; ToS and cost must be verified before integration (`ROADMAP.md`).

### Data09 — Beach congestion (citizen reports)

1. **Request** — Mobile-app reports via the project's own backend (internal). No external endpoint exists to pull.
2. **Cross-verify** — citizen reports must be cross-checked against sensor/IoT data before updating the twin (`pipelines/quality-rules.md`).

## Notes & blockers

- `BLOCKER` FlightRadar24 and Google Maps require paid API keys and independent ToS/cost verification (MarineTraffic is maritime-only and no longer relevant to Data06/07).
- Data06 (`PARTIAL`) has a free no-key OpenSky live-states route; Data07 (`PROPOSAL`) is now computed from schedules, not pulled. Data08-10 remain candidate (`UNVERIFIED`).
- Beach/city congestion partly depends on citizen reports, which are the project's own participatory feed, not an external pull.
