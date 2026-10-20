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
| Data19 | Short-term rental share (Airbnb) | Eurostat tour_ce_omn12 ÷ tour_occ_nin2 | api | none | **VERIFIED** |

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

### Data19 — Short-term rental share (Eurostat platform nights)

`VERIFIED` (2026-10-15) InsideAirbnb is non-viable for EL62 (no Ionian Islands coverage; Greece is Athens/Crete only). The authoritative source is Eurostat `tour_ce_omn12` (platform-mediated guest nights — the EC data-sharing agreement with Airbnb, Booking.com, Expedia, Tripadvisor), with `tour_occ_nin2` as the conventional-nights denominator.

1. **Request**:
   ```bash
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_ce_omn12?geo=EL62&indic_to=NGT_SP&c_resid=TOTAL&month=TOTAL&time=2018&time=2019&time=2020&time=2021&time=2022&time=2023&time=2024&time=2025&lang=en"
   ```
2. **Compute** — `scripts/verification/pull-data19-platform-rentals.py`: share % = platform nights ÷ (conventional nights + platform nights) × 100.
3. **Outputs** — `data/curated/data19-platform-rental-share.json` + `observations-data19-platform-rental-share-*.json` / `.csv`.
4. **Cadence** — annual (Eurostat release).

## Notes & blockers

- `VERIFIED` Data16 (Eurostat intensity) and Data19 (Eurostat platform-nights share) are directly pullable today; Data17/18 remain candidate/internal.
- `RISK` Hospital/utility data is operational and privacy-sensitive; obtain from official channels only.
