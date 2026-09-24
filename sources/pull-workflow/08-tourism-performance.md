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
| Data29 | Seasonality (%) | EU Tourism Dashboard (Eurostat) | api | none | `PARTIAL` (country-level monthly verified; no NUTS2 monthly) |
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

1. **Source** — Eurostat `tour_occ_nim` (monthly nights). `PARTIAL`: monthly data is published at **country level only** (`geo=EL`); the NUTS2 query (`geo=EL62`) returns an empty value set (no monthly NUTS2 publication).
2. **Request** (verified 2026-09-24):
   ```bash
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&geo=EL&freq=M&c_resid=TOTAL&unit=NR&nace_r2=I551-I553&time=2023-01&time=2023-02&time=2023-03&time=2023-04&time=2023-05&time=2023-06&time=2023-07&time=2023-08&time=2023-09&time=2023-10&time=2023-11&time=2023-12"
   ```
   Note: monthly `time` codes use `YYYY-MM` format (e.g. `2023-07`), not `YYYY-MMM`/`YYYYM01`.
3. **Transform** — seasonality % = peak-month share of annual nights (or a Jul+Aug / Jun–Sep share).
4. **Sample (verified, Greece 2023)** — total 147,209,821 nights; peak Aug 31,687,354 (21.53 %); Jul+Aug 41.54 %; Jun–Sep 71.95 %.

### Data30 — Average length of stay

1. `PROPOSAL` derivable from Data26 as `nights ÷ arrivals`.
2. Sample (derived, not a sourced value): 2022 ≈ 16,512,634 ÷ 2,785,360 ≈ **5.9 nights**; 2023 ≈ 19,762,799 ÷ 3,332,407 ≈ **5.9 nights**.
3. Confirm the formula and unit before emitting this observation.

## Notes & blockers

- `VERIFIED` Data26 and Data27 are directly pullable today.
- `BLOCKER` Data28 (booking APIs) remains unverified.
- `PARTIAL` Data29: monthly nights verified at country level (Greece); no NUTS2 monthly publication — use country level as a documented proxy.
- `PROPOSAL` Data30 formula is a candidate derivation, not a proposal-defined formula.
