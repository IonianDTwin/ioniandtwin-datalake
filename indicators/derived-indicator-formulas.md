# Derived / engineered indicator formulas

`PROPOSAL` Working note: for every indicator that is **computed** from pulled data
rather than ingested directly, we record the default formula, its basis, and the
implementation plan. These are **reversible defaults** - if the proposal author
supplies a different definition, we swap it (recorded in the internal decision log).

> None of the formulas below is specified in the technical proposal. They are
> candidate constructs, chosen from standard conventions so they are defensible
> now and cheap to change later. **Adoption status (2026-10-03):** Data22 and Data32
> are **adopted (provisional)**; Data30 is **confirmed**. Data02, Data04, Data23, Data25,
> Data28 and Data29 are now **read directly from the EU Tourism Dashboard**,
> not derived. Open questions are recorded in `docs/data-preparation-progress.md`.

## Formula register

| Indicator | Default formula | Basis / borrowed from | Implementation plan |
| --- | --- | --- | --- |
| Data03 - Clean beach water | share of classified waters rated ≥ "Sufficient" | EEA WISE Bathing Water classes | compute from the Data02 pull (country-level) |
| Data06 - Airport congestion | `min(1, aircraft-in-approach-buffer ÷ threshold)` → low/medium/high | EUROCONTROL ATFM delay / airport punctuality (standard air-congestion metric) - **proposal** 2026-10-03 | OpenSky live states, count-in-buffer; live-only |
| Data07 - Port congestion | `min(1, vessels-in-port-buffer ÷ threshold)` → low/medium/high | World Bank CPPI / UNCTAD median-time-in-port (standard port metrics) - **proposal** 2026-10-03 | aisstream/EMODnet live AIS, count-in-buffer; live-only |
| Data22 - Tourist diversity (zones) | `1 − HHI` of NUTS3 nights shares | Herfindahl-Hirschman Index (standard concentration measure) - **adopted (provisional)** 2026-10-03 | `tour_occ_nin3` over EL621-EL624 → aggregate to NUTS2/EL62, emit one regional value |
| Data24 - Protected land (%) | `area(union(Natura2000 Habitats ∪ Birds) ∩ EL62 land) ÷ area(EL62 land) × 100` | EEA Natura 2000 + Eurostat GISCO NUTS boundary (standard protected-area share) | `scripts/verification/compute-data24-protected-land.py` - clip to EL62 land polygon (terrestrial split), union, divide by EL62 area (EPSG:3035 equal-area) |
| Data25 - Accommodation in high-value areas | *(no longer derived)* - "Share of accommodations in areas with high-nature value" read directly from the EU Tourism Dashboard (`TOUR_DES_13`) | EU Tourism Dashboard (proposal source) - 43 % EL62 (2023) | ingest the dashboard CSV value (no overlay needed); flag: exact "high-nature value" operationalisation to pin down |
| Data29 - Seasonality | *(no longer derived)* - peak-season share read directly from the dashboard (`TOUR_SOE_02`) | EU Tourism Dashboard - 71.08 % EL62 (2023) | ingest the dashboard CSV value; flag: exact month window to confirm |
| Data30 - Length of stay | `nights ÷ arrivals` | standard tourism statistic - **confirmed** 2026-10-03 | derive from Data26 |
| Data32 - Dominant typology | `nace_r2` category with highest nights share | Eurostat NACE Rev. 2 - **adopted (provisional)** 2026-10-03 | already pulled; emits "hotels" (≈73 %) |
| Tourism Pressure Index (composite) | `0.4·intensity_norm + 0.4·density_norm + 0.2·seasonality_norm` | prototype (proposal names it, no weights) | `scripts/verification/build_dashboard.py` (bounds: intensity /150,000, density /12,000) |

## Switch-later hooks

- **Data22** - if the author means accommodation-type mix or visitor-origin mix
  instead of spatial spread, the only change is the input: `nace_r2` shares
  (already pulled) or `c_resid`/country-of-origin shares.
- **Data25** - if the author means a UNESCO/cultural core instead of natural/coastal,
  swap the geometry source (UNESCO WHC buffer vs Natura 2000/coast). The metric
  (% of beds inside the zone) is unchanged.
- **Composite weights** - the 0.4/0.4/0.2 split is provisional; any alternative
  weighting is a one-line change in the build script, not a re-architecture.

## Benchmark note (2026-10-01)

- **HERIT-DATA** (Interreg MED) - defines tourism-flow/pressure indicators for
  cultural-heritage destinations; no public canonical formula list was extractable
  in this pass.
- **EU Tourism Dashboard** - a Eurostat front-end; uses the standard intensity
  (nights/1,000 residents), density (nights/km²) and peak-share seasonality
  definitions, which we already follow.

## Data availability findings (2026-10-03)

- **Data22** is computable: `tour_occ_nin3` has NUTS3 nights for EL621-EL624. Prototype values (1 − HHI): 2021 = 0.636 · 2022 = 0.651 · 2023 = 0.632 · 2024 = 0.631 · 2025 = 0.640. Flag: dashboard "Tourism diversity" reads 0 for EL62 (different concept).
- **Data25 is resolved** via the EU Tourism Dashboard (`TOUR_DES_13`, 43 % EL62 2023) - the ELSTAT bed-places path (regional-unit only) is no longer needed for the value.
- **Data28** - net occupancy 65.4 % (EL62 2023) from the dashboard; the earlier gross nights/(beds×365) derivation is superseded.

## Provenance

Every derived value must keep its formula in `provenance.formula` and be emitted
with `status: PROPOSAL` until the author confirms the definition.

## Spatial aggregation (D-014)

All derived indicators are emitted at **NUTS2 / EL62**. NUTS 3 (EL621-624) inputs are
an internal disaggregation: sum them, then apply the formula, and emit a single regional
observation. Never emit a `NUTS3` level. Implemented for Data22 in
`scripts/verification/build_dashboard.py`.
