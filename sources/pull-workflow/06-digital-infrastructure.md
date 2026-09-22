# Pull Workflow — 06 Digital Infrastructure

**Category:** Digital Infrastructure — `Ψηφιακή Υποδομή`
**Indicators:** Data20–Data21
**Pillar:** Society

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data20 | Internet speed (>100 Mb/s) | user reports | user_reports | app | UNVERIFIED |
| Data21 | 4G/5G availability | user reports | user_reports | app | UNVERIFIED |

## Pull process

### Data20 / Data21 — Internet speed & 4G/5G availability

1. **Source** — participatory reports from the mobile app (the project's own backend), plus any official broadband/coverage map if confirmed later.
2. **Cross-verify** — citizen reports against network/coverage data before updating the twin.
3. **Transform** — aggregate reports per spatial unit into coverage/speed observations (`Data20` speed class, `Data21` availability).

## Notes & blockers

- `BLOCKER` No external machine-readable source is named in the proposal; this is a participatory feed.
- `PROPOSAL` An official coverage map (e.g. national broadband/telecom regulator) could supplement the reports — confirm availability and terms before use.
