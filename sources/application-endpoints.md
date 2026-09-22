# Application Endpoints

`VERIFIED` Both supplied URLs are client-side routes of a single public SPA.

| App route | URL | Server behaviour |
|---|---|---|
| Indicators | `https://bold-matsumoto.213-158-90-162.plesk.page/#/indicators` | `#/` fragment; served by `GET /` |
| Data sources | `https://bold-matsumoto.213-158-90-162.plesk.page/#/resources/data-sources` | `#/` fragment; served by `GET /` |

## Inspection evidence

- Host `213.158.90.162`, nginx, HTTP/2.
- `GET /` → `200`, `text/html`, 1,552,985 bytes, last-modified `2026-09-18 15:52:09 GMT`.
- `GET /robots.txt` → `404` (no robots directives present).
- Document sha256 `445f8f176cb8fc7d175a0769848a29063eb69ccc897ad599875dc5c56e2d1806`.
- Accessed 2026-09-21T12:32Z.

## What the frontend declares (metadata, not verified data)

- SPA stack: React + Leaflet + CARTO basemap (`cartocdn.com`), bilingual EL/EN.
- Public static assets load from the same origin; no separate API host or `/api` route is referenced in the HTML — indicator/source data is embedded in the JS bundle and appears demo/simulated.

## Status

`VERIFIED` Application reachable and inspected (bounded, read-only). `BLOCKER` Live data access behind the UI is not yet verified — see `source-verification-matrix.md` and `docs/validation/api-verification-report.md`.
