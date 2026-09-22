# Pull Workflow — 09 Density & Typology

**Category:** Density & Typology — `Πυκνότητα & Τυπολογία`
**Indicators:** Data31–Data33
**Pillar:** Economy

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data31 | Tourism density (nights/km²) | EU Tourism Dashboard (Eurostat) | api | none | **VERIFIED** |
| Data32 | Dominant tourism typology | EU Tourism Dashboard (Eurostat) | api | none | **VERIFIED** (dimension available) |
| Data33 | Foreign tourist share (%) | EU Tourism Dashboard (Eurostat) | api | none | **VERIFIED** |

## Pull process

### Data31 — Tourism density (Eurostat)

`VERIFIED` Exposed directly as unit `P_KM2` (per square kilometre) in `tour_occ_nin2`.

1. **Request**:
   ```bash
   curl -sS "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023"
   ```
2. **Transform** — `c_resid=TOTAL`, `unit=P_KM2`, `nace_r2=I551-I553`.
3. **Sample (verified)** — 2022 = 7,176.29 · 2023 = 8,588.79 nights/km².

### Data32 — Dominant tourism typology

1. **Source** — the `nace_r2` breakdown (hotels vs. holiday/short-stay vs. camping) in the same `tour_occ_nin2` / `tour_occ_arn2` responses.
2. **Transform** — classify the dominant accommodation type per spatial unit from the `nace_r2` shares (dimension verified present in the sample).

### Data33 — Foreign tourist share (%)

`VERIFIED` Exposed directly as unit `PC_TOT` with `c_resid=FOR` in `tour_occ_nin2`.

1. **Request** — same `tour_occ_nin2` endpoint above.
2. **Transform** — `c_resid=FOR`, `unit=PC_TOT`, `nace_r2=I551-I553`.
3. **Sample (verified)** — 2022 = 93.72 % · 2023 = 93.58 % foreign share.

## Notes & blockers

- `VERIFIED` All three indicators are directly pullable today from a single endpoint (`tour_occ_nin2`).
- `PROPOSAL` Data32's exact classification rule (e.g. "hotels dominant" vs. a typology index) is not defined in the proposal; confirm before emitting.
