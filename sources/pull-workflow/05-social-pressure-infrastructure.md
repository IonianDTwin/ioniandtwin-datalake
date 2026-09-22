# Pull Workflow — 05 Social Pressure & Infrastructure

**Category:** Social Pressure & Infrastructure — `Κοινωνική Πίεση & Υποδομές`
**Indicators:** Data16–Data19
**Pillar:** Society / Economy

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data16 | Tourism intensity (nights/residents) | EU Tourism Dashboard (Eurostat) | api | none | **VERIFIED** |
| Data17 | Hospital / infrastructure congestion | official announcements; user reports | web / user_reports | none / app | UNVERIFIED |
| Data18 | Power / water outage | official announcements; user reports | web / user_reports | none / app | UNVERIFIED |
| Data19 | Short-term rental share (Airbnb) | EU Tourism Dashboard; Airbnb | api | none / API key | UNVERIFIED |

## Pull process

### Data16 — Tourism intensity (Eurostat)

`VERIFIED` The Eurostat API exposes tourism intensity directly as unit `P_THAB` (per thousand inhabitants) for geo `EL62` (Ionia Nisia).

1. **Request**:
   ```bash
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023"
   ```
2. **Transform** — select `c_resid=TOTAL`, `unit=P_THAB`, `nace_r2=I551-I553`.
3. **Sample (verified)** — 2022 = 80,912.16 · 2023 = 97,705.53 nights per 1000 residents.
4. **Observation** — `indicator_id=Data16`, `unit=per_thousand_inhabitants`.

### Data17 / Data18 — Hospital & utility congestion/outages

1. **Source** — official municipal/regional announcements plus citizen reports. No single public machine-readable endpoint is assumed.
2. **Cross-verify** — citizen reports against official/announcement data before updating the twin.

### Data19 — Short-term rental share

1. **EU Tourism Dashboard** — locate the relevant Eurostat dataset (accommodation by type / short-term rentals); not yet identified.
2. **Airbnb** — `UNVERIFIED` paid/partner API; separate feasibility track (`ROADMAP.md`).

## Notes & blockers

- `VERIFIED` Data16 is directly pullable today; the rest of this category is candidate/internal.
- `RISK` Hospital/utility data is operational and privacy-sensitive; obtain from official channels only.
