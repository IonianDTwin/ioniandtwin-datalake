# Pull Workflow — 08 Tourism Performance

**Category:** Tourism Performance — `Τουριστική Απόδοση`
**Indicators:** Data26–Data30
**Pillar:** Economy

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data26 | Arrivals & overnight stays | EU Tourism Dashboard (Eurostat) | api | none | **VERIFIED** |
| Data27 | Tourism capacity (beds) | EU Tourism Dashboard (Eurostat) | api | none | **VERIFIED** |
| Data28 | Occupancy rate (%) | social media & booking services | api | API key | UNVERIFIED |
| Data29 | Seasonality (%) | EU Tourism Dashboard (Eurostat) | api | none | UNVERIFIED (monthly series needed) |
| Data30 | Average length of stay | EU Tourism Dashboard (Eurostat); booking services | api | none / API key | `PROPOSAL` derivable from Data26 |

## Pull process

### Data26 — Arrivals & overnight stays (Eurostat)

`VERIFIED` Two Eurostat NUTS2 datasets pull-test cleanly for geo `EL62` (Ionia Nisia).

1. **Request**:
   ```bash
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023"   # arrivals
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023"  # nights
   ```
2. **Transform** — `c_resid=TOTAL`, `unit=NR`, `nace_r2=I551-I553`.
3. **Sample (verified)** — arrivals 2022 = 2,785,360 · 2023 = 3,332,407; nights 2022 = 16,512,634 · 2023 = 19,762,799.

### Data27 — Tourism capacity / beds (Eurostat)

`VERIFIED` Bed-places are available via `tour_cap_nuts2` (`accomunit=BEDPL`).

1. **Request**:
   ```bash
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023"
   ```
2. **Sample (verified)** — bed-places 2022 = 159,790 · 2023 = 155,968.

### Data28 — Occupancy rate (%)

1. **Source** — booking/social services (paid, ToS unverified). `UNVERIFIED`.
2. `PROPOSAL` fallback: occupancy can be estimated from capacity (Data27) and nights/arrivals (Data26), but the proposal names booking services — confirm the feed before substituting.

### Data29 — Seasonality (%)

1. **Source** — a monthly Eurostat nights/arrivals series (e.g. `tour_occ_nim` family). The annual NUTS2 datasets are verified, but the **monthly** series must be identified and pulled in the next round.
2. **Transform** — monthly distribution / peak-month share → seasonality %.

### Data30 — Average length of stay

1. `PROPOSAL` derivable from Data26 as `nights ÷ arrivals`.
2. Sample (derived, not a sourced value): 2022 ≈ 16,512,634 ÷ 2,785,360 ≈ **5.9 nights**; 2023 ≈ 19,762,799 ÷ 3,332,407 ≈ **5.9 nights**.
3. Confirm the formula and unit before emitting this observation.

## Notes & blockers

- `VERIFIED` Data26 and Data27 are directly pullable today.
- `BLOCKER` Data28 (booking APIs) and Data29 (monthly series) remain unverified.
- `PROPOSAL` Data30 formula is a candidate derivation, not a proposal-defined formula.
