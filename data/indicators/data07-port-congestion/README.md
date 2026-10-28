# Data07 — Port congestion

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  scratch/cruise-pressure/schedules.json [.json]  ──( scripts/verification/compute-data07-anticipated-congestion.py )──>  refined-data.json [.json]
  scratch/ais-routes/export_sailing_traffic.csv [.csv]  ──( scripts/verification/compute-data07-anticipated-congestion.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `PROPOSAL`
- **Greek Proposal Name:** —
- **Category:** `dynamic_congestion`
- **Refresh Cadence:** `daily`
- **Raw Input File Extension(s):** `.csv` + `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/compute-data07-anticipated-congestion.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `366`

## 1. Overview & Key Note

Anticipated schedule-based congestion (2026-10-14): cruise schedules (CruiseMapper one-time read) + Greek National Access Point ferry baseline -> scripts/verification/compute-data07-anticipated-congestion.py. Live AIS excluded (zero Corfu receiver coverage; snapshots only, no forecasting). Formula S=min(1, 0.4*N_ships/B_max + 0.4*(L_cruise+L_ferry_pax)/C_pax + 0.2*L_ferry_veh/C_veh); weights/capacities/per-call cruise PAX are PROPOSAL/ASSUMPTION defaults.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `CruiseMapper_schedules` (CruiseMapper (one-time schedule capture; OLKE port authority candidate for production))
- **Upstream URL:** `https://www.cruisemapper.com/ports/<port-slug>?month=<yyyy-mm>#schedule`
- **Access Method:** `One-time bounded read parsed to JSON`
- **Local Raw File (`data/raw/` or `data/samples/`):** `scratch/cruise-pressure/schedules.json`
- **Raw File Extension & Format:** `.json` — `application/json (117 planned cruise calls across Ionian ports)`
- **SHA-256 Checksum:** `1490dd5a7fabf8dc265fafa127cac6cfa77cfba59e15293c1b2c333ea496ae98` (verified in `data/manifests/source-verification-2026-10-14.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/compute-data07-anticipated-congestion.py`
- **Conversion Command:** `python3 scripts/verification/compute-data07-anticipated-congestion.py`
- **Whitelisted Raw Variables (`kept`):** `port_id`, `date`, `ship`, `arrival`, `departure`
- **Dropped / Redacted Fields:** `igoumenitsa_mainland_calls (outside EL62)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `ports[].id` | Port identifier ('corfu', 'kefalonia', 'zakynthos', 'lefkada', 'paxos', 'ithaki') |
| `ports[].calls[].date` | Planned call date (YYYY-MM-DD) |
| `ports[].calls[].ship` | Vessel name |
| `ports[].calls[].arrival / departure` | Scheduled berth arrival and departure window |

### Source 2: `GreekNAP_sailing_traffic` (Greek National Access Point (NAP) — Domestic Ferry Sailing Traffic)
- **Upstream URL:** `file:///home/scrublife/ionian-dtwin/scratch/ais-routes/export_sailing_traffic.csv`
- **Access Method:** `CSV bulk export (184,436 domestic ferry legs, Mar-Nov 2025)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `scratch/ais-routes/export_sailing_traffic.csv`
- **Raw File Extension & Format:** `.csv` — `text/csv (184,436 rows)`
- **SHA-256 Checksum:** `b756f6eb2c4eac53f996983ee215e0289bfab6fe53827696806abe2393f5fa7b` (verified in `data/manifests/source-verification-2026-10-14.json`)
- **Conversion Script (`.csv` -> `.json`):** `scripts/verification/compute-data07-anticipated-congestion.py`
- **Conversion Command:** `python3 scripts/verification/compute-data07-anticipated-congestion.py`
- **Whitelisted Raw Variables (`kept`):** `date`, `arrivalport`, `passengercount`, `vehiclecount`
- **Dropped / Redacted Fields:** `routecode`, `routecodenames`, `mainland_arrival_ports (IGO, KYL, GPA)`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `date` | Sailing date |
| `arrivalport` | Destination port code (CFU/LFK, PKE/SAI/FIS, ZTH, VSS/LEV, PAX, PIS) |
| `passengercount` | Disembarking passenger count on leg |
| `vehiclecount` | Disembarking vehicle count on leg |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** PROPOSAL (held pending sign-off, D-019): Fuse planned cruise calls with empirical Greek NAP inbound ferry passenger/vehicle daily baselines across 6 EL62 ports via `scripts/verification/compute-data07-anticipated-congestion.py`. S(P,D) = min(1, 0.4*N_ships/B_max + 0.4*(L_cruise+L_ferry_pax)/C_pax + 0.2*L_ferry_veh/C_veh).

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.assumptions.weights` | `object` | `weights` | `input_variable` | PROPOSAL formula weights: berth=0.4, pax=0.4, veh=0.2. |
| `refined_data.assumptions.capacities` | `object` | `ships_pax_veh` | `input_variable` | PROPOSAL daily port berth, passenger, and vehicle capacity thresholds. |
| `refined_data.forecast_window` | `object` | `ISO-8601 date` | `temporal_dimension` | 61-day evaluation window (2026-10-01 to 2026-11-30; 366 port-days). |
| `refined_data.ports[].daily_schedule[].congestion_score` | `number` | `score (0-1)` | `target_indicator` | Anticipated daily port congestion score (0.0 to 1.0). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CruiseMapper_schedules:Data07:corfu:2026-10-01` | `2026-10-01` | `transport_node/corfu` | **0.657** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:kefalonia:2026-10-01` | `2026-10-01` | `transport_node/kefalonia` | **0.945** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:zakynthos:2026-10-01` | `2026-10-01` | `transport_node/zakynthos` | **0.146** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:lefkada:2026-10-01` | `2026-10-01` | `transport_node/lefkada` | **0.535** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:paxos:2026-10-01` | `2026-10-01` | `transport_node/paxos` | **0.084** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:ithaki:2026-10-01` | `2026-10-01` | `transport_node/ithaki` | **0.091** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:corfu:2026-10-02` | `2026-10-02` | `transport_node/corfu` | **0.505** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:kefalonia:2026-10-02` | `2026-10-02` | `transport_node/kefalonia` | **0.153** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:zakynthos:2026-10-02` | `2026-10-02` | `transport_node/zakynthos` | **0.166** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:lefkada:2026-10-02` | `2026-10-02` | `transport_node/lefkada` | **0.003** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:paxos:2026-10-02` | `2026-10-02` | `transport_node/paxos` | **0.102** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:ithaki:2026-10-02` | `2026-10-02` | `transport_node/ithaki` | **0.11** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:corfu:2026-10-03` | `2026-10-03` | `transport_node/corfu` | **0.334** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:kefalonia:2026-10-03` | `2026-10-03` | `transport_node/kefalonia` | **0.132** | `index (0-1)` | `forecast` |
| `CruiseMapper_schedules:Data07:zakynthos:2026-10-03` | `2026-10-03` | `transport_node/zakynthos` | **0.152** | `index (0-1)` | `forecast` |
| _… (351 more observations in `refined-data.json`)_ | | | | | |
