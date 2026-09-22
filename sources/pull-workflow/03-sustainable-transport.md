# Pull Workflow — 03 Sustainable Transport

**Category:** Sustainable Transport — `Βιώσιμες Μεταφορές`
**Indicators:** Data11–Data12
**Pillar:** Society (low-impact mobility)

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data11 | KTEL (bus) congestion | local transport telematics | internal / partner | partner | UNVERIFIED |
| Data12 | Urban transit congestion | local transport telematics | internal / partner | partner | UNVERIFIED |

## Pull process

### Data11 / Data12 — KTEL & urban transit (telematics)

1. **Request** — local transport (KTEL/urban) telematics feed from the transport authority/operator. No public external endpoint is assumed.
2. **Store raw / manifest** — when the partner feed is provided.
3. **Transform** — occupancy or delay per route/stop into congestion observations (`Data11` bus, `Data12` urban transit).
4. **Cadence** — ~30-minute batch per the proposal.

## Notes & blockers

- `BLOCKER` Internal/partner feed — must be requested from the operator; do not fabricate an endpoint.
- `PROPOSAL` The deployed app lists "PeopleFlows" (peopleflows.di.ionio.gr) as a mobility source but it is not mapped here in the proposal; treat as a separate feasibility track.
