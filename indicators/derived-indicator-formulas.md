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
> not derived. **Data07 (2026-10-14):** transitioned from live AIS to the
> **Anticipated Schedule-Based Congestion** model (see below) — the live
> count-in-buffer proxy is superseded. Open questions are recorded in
> `docs/data-preparation-progress.md`.

## Formula register

| Indicator | Default formula | Basis / borrowed from | Implementation plan |
| --- | --- | --- | --- |
| Data03 - Clean beach water | share of classified waters rated ≥ "Sufficient" | EEA WISE Bathing Water classes | compute from the Data02 pull (country-level) |
| Data06 - Airport congestion | `min(1, aircraft-in-approach-buffer ÷ threshold)` → low/medium/high | EUROCONTROL ATFM delay / airport punctuality proxy - **verified & implemented** 2026-10-20 | `scripts/verification/pull-data06-airport-congestion.py` (OpenSky live states; 25km buffer, alt<=3000m) |
| Data07 - Port congestion | `S = min(1, 0.4·N_ships/B_max + 0.4·(L_cruise+L_ferry_pax)/C_pax + 0.2·L_ferry_veh/C_veh)` → low (<0.50) / medium (<0.85) / high (≥0.85) | Anticipated schedule-based congestion (research-notes 2026-10-15 §4); replaces the live-AIS count-in-buffer proxy (World Bank CPPI / UNCTAD time-in-port are the underlying standard metrics) - **proposal** 2026-10-14 | `scripts/verification/compute-data07-anticipated-congestion.py` (cruise schedules + Greek NAP ferry baseline) |
| Data22 - Tourist diversity (zones) | `1 − HHI` of NUTS3 nights shares | Herfindahl-Hirschman Index (standard concentration measure) - **adopted (provisional)** 2026-10-03 | `tour_occ_nin3` over EL621-EL624 → aggregate to NUTS2/EL62, emit one regional value |
| Data24 - Protected land (%) | `area(union(Natura2000 Habitats ∪ Birds) ∩ EL62 land) ÷ area(EL62 land) × 100` | EEA Natura 2000 + Eurostat GISCO NUTS boundary (standard protected-area share) | `scripts/verification/compute-data24-protected-land.py` - clip to EL62 land polygon (terrestrial split), union, divide by EL62 area (EPSG:3035 equal-area) |
| Data25 - Accommodation in high-value areas | *(no longer derived)* - "Share of accommodations in areas with high-nature value" read directly from the EU Tourism Dashboard (`TOUR_DES_13`) | EU Tourism Dashboard (proposal source) - 43 % EL62 (2023) | ingest the dashboard CSV value (no overlay needed); flag: exact "high-nature value" operationalisation to pin down |
| Data29 - Seasonality | *(no longer derived)* - peak-season share read directly from the dashboard (`TOUR_SOE_02`) | EU Tourism Dashboard - 71.08 % EL62 (2023) | ingest the dashboard CSV value; flag: exact month window to confirm |
| Data30 - Length of stay | `nights ÷ arrivals` | standard tourism statistic - **confirmed** 2026-10-03 | derive from Data26 |
| Data32 - Dominant typology | `nace_r2` category with highest nights share | Eurostat NACE Rev. 2 - **adopted (provisional)** 2026-10-03 | already pulled; emits "hotels" (≈73 %) |
| Tourism Pressure Index (composite) | `0.4·intensity_norm + 0.4·density_norm + 0.2·seasonality_norm` | prototype (proposal names it, no weights) | `scripts/verification/build_dashboard.py` (bounds: intensity /150,000, density /12,000) |

## Anticipated Port Congestion (Data07) — 2026-10-14

`DECISION` **Data07 is now an anticipated (schedule-based) indicator, not a live-AIS
feed.** Live crowdsourced AIS has zero receiver coverage in Corfu harbour (proven
2026-10-14) and provides no forecasting; scheduled operational itineraries give a
forward-looking load ($t+1$ day → $t+6$ months) with no daemon or scraper to maintain.

### Formula (research-notes 2026-10-15 §4A)

For port `P` and forecast date `D`:

$$S(P,D) = \min\left(1.0,\; w_{berth}\!\cdot\!\tfrac{N_{ships}}{B_{max}} + w_{pax}\!\cdot\!\tfrac{L_{cruise}+L_{ferry\_pax}}{C_{pax}} + w_{veh}\!\cdot\!\tfrac{L_{ferry\_veh}}{C_{veh}}\right)$$

- `N_ships` = planned cruise calls on `D`; `L_cruise = N_ships · 2,500` (per-call PAX, `ASSUMPTION`).
- `L_ferry_pax` / `L_ferry_veh` = empirical inbound ferry throughput (Greek NAP, Mar–Nov 2025) averaged by `(month, day-of-week)` with month→overall fallback.
- `B_max` (berths) follows research-notes §4A: Corfu 5, Kefalonia 3, Zakynthos 3, Lefkada 2, Paxos 1, Ithaki 1.
- `C_pax` / `C_veh` (terminal handling capacity) and the weights `0.4/0.4/0.2` are `ASSUMPTION`/`PROPOSAL` defaults.

Levels: **low** `S < 0.50` · **medium** `0.50 ≤ S < 0.85` · **high** `S ≥ 0.85`.

### Ports & empirical ferry baselines (inbound arrivals/day, Mar–Nov 2025)

| Port | B_max | ferry PAX/day | ferry VEH/day |
| --- | --- | --- | --- |
| Corfu | 5 | 3,558.5 | 1,030.3 |
| Kefalonia | 3 | 1,475.6 | 508.2 |
| Zakynthos | 3 | 1,893.9 | 578.7 |
| Lefkada | 2 | 156.1 | 42.0 |
| Paxos | 1 | 475.1 | 76.1 |
| Ithaki | 1 | 307.9 | 107.6 |

### Implementation & outputs

- Script: `scripts/verification/compute-data07-anticipated-congestion.py` (stdlib only; deterministic — re-runs reproduce identical scores, only the `generated_at_utc`/`ingested_at` timestamps differ).
- Master timetable: `data/curated/scheduled-port-traffic-el62.json` (cruise calls + ferry baselines + daily scores).
- Observations: `data/curated/observations-data07-anticipated-congestion-<date>.json` / `.csv` (one schema-compliant `forecast` observation per port per day, `spatial_ref.level = transport_node`).
- First run (2026-10-14): 366 observations over 2026-10-01 → 2026-11-30 (low 342 · medium 21 · high 3); peak days — Corfu 2026-10-08 (5 ships, S=0.983), Kefalonia 2026-10-01 (3 ships, S=0.945).

### Switch-later hooks (Data07)

- **Cruise PAX per call** — 2,500 is a flat default; swap for per-vessel capacity when the OLKE declaration feed carries `PAX_max` (research-notes §2B: 2,000–5,500 PAX/ship).
- **Ferry seasonality** — the `(month, day-of-week)` averages already encode the 2025 rhythm; refresh with a newer NAP export to track year-on-year change.
- **Capacities/weights** — `C_pax`, `C_veh`, `B_max` and the weights are all single-line edits in the port registry, not a re-architecture.

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
