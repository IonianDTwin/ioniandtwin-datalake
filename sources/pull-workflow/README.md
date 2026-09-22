# Pull Workflow — IonianDTwin data-source playbook

`DECISION` This directory is the **agentic pull workflow** for IonianDTwin. It is a set of Markdown playbooks that an agent (human or model) can follow to pull or create data sources for the Digital Twin, one file per indicator section (category).

## Purpose

Turn the Data01–Data34 indicator catalogue into **executable, per-section pull recipes** so that a future agent can, without re-deriving the research, know:

1. which source feeds each indicator,
2. what access method the source needs (API / PDF / download / internal / partner / user reports),
3. the exact endpoint or file URL (verified where possible),
4. whether credentials are required and where they live,
5. the pull steps: request → store raw → manifest → transform → observation,
6. the current verification status.

## The workflow loop

For each indicator section, an agent follows the same loop:

1. **Read** the category playbook in this directory (e.g. `08-tourism-performance.md`).
2. **Resolve** the source for the target indicator(s) from the table.
3. **Branch on access type**:
   - `api` → run the recorded command (or a `scripts/verification/pull-*.sh`), capture the response.
   - `download`/`pdf` → download the file, record its checksum, extract text if needed.
   - `internal`/`partner`/`user_reports` → do **not** fabricate a source; record a `BLOCKER` and request the feed from the owner.
   - `unknown` → do not guess an endpoint; mark `UNVERIFIED` and ask.
4. **Store raw** immutably under `data/raw/` (or a bounded sample under `data/samples/`), never in Git.
5. **Manifest** the pull in `data/manifests/source-verification-YYYY-MM-DD.json` with URL, method, params, status, content-type, checksum, timestamp, evidence path.
6. **Transform** into a normalised observation per `schemas/observation-schema.json` (ISO 8601, explicit timezone, spatial_ref, provenance).
7. **Quality-check** per `pipelines/quality-rules.md` (coverage, freshness, completeness, plausibility, cross-verification).
8. **Label** the outcome `VERIFIED` / `PARTIAL` / `INACCESSIBLE` / `UNVERIFIED` and update `sources/source-verification-matrix.md`.

## File convention

- One file per proposal category, named `NN-category.md` (NN = 01…10), plus this `README.md`.
- Shared sections in every file: **Indicators & sources**, **Pull process**, **Notes & blockers**.
- Endpoints are recorded as templates; real API keys are never written here — they live in the untracked `.env`.

## Verified so far (2026-09-22)

- `VERIFIED` Eurostat SDMX 2.1 API — `tour_occ_nin2`, `tour_occ_arn2`, `tour_cap_nuts2` for geo `EL62` (Ionia Nisia).
- `VERIFIED` Open-Meteo weather + UV (no-key substitute; not in the proposal/app).
- `PARTIAL` Copernicus CDSE catalogue (public catalogue; download gated by token).
- `INACCESSIBLE` OpenWeatherMap without an API key (HTTP 401).
- `VERIFIED` GSTC Destination Criteria v2.0 PDF (governance reference).

Evidence: `data/manifests/source-verification-2026-09-22.json`, `docs/validation/api-verification-report.md`, `docs/validation/pdf-verification-report.md`.

## Indicator sections

| File | Category (EN) | Data IDs |
|---|---|---|
| `01-environmental-health.md` | Environmental Health & Pollutants | Data01–05 |
| `02-dynamic-congestion.md` | Dynamic Congestion | Data06–10 |
| `03-sustainable-transport.md` | Sustainable Transport | Data11–12 |
| `04-climate-adaptation.md` | Climate Adaptation | Data13–15 |
| `05-social-pressure-infrastructure.md` | Social Pressure & Infrastructure | Data16–19 |
| `06-digital-infrastructure.md` | Digital Infrastructure | Data20–21 |
| `07-spatial-sustainability.md` | Spatial Sustainability | Data22–25 |
| `08-tourism-performance.md` | Tourism Performance | Data26–30 |
| `09-density-typology.md` | Density & Typology | Data31–33 |
| `10-participation.md` | Participation | Data34 |

## Guardrails (non-negotiable)

- Read-only, bounded requests only; no scraping, no access-control bypass.
- Never invent an endpoint, license, credential, schema, or successful result.
- A failed pull is recorded as an access constraint, never as "source absent".
- Unverified data must not drive public alerts, enforcement, or policy recommendations.

## Non-API sources

Indicators whose data comes from a public webpage/PDF/file (not a JSON API) follow a different procedure — see `sources/procedures/` (overview + `download-extract.md`).
