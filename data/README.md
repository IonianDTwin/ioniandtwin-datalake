# data/ — Holistic Data Handling & Provenance Contract

`DECISION` This file is the single holistic reference for how humans and agents handle raw, edited, and curated data across IonianDTwin. Raw archives, secrets, caches, and local databases stay out of Git.

---

## 1. Directory Architecture (Zero Raw Duplication + Per-Indicator Edited Folders)

```text
data/
├── README.md                             # This file: global data-handling contract
├── raw/                                  # UNTRACKED in Git (.gitignore); immutable raw fetches shared by source
├── samples/                              # TRACKED small raw API test pulls referenced by early manifests
├── manifests/                            # TRACKED SHA-256 provenance manifests of all raw/sample pulls
├── indicators/                           # TRACKED per-indicator edited folders (data01..data34)
│   ├── data04-blue-flags/
│   │   ├── raw-source-description.json   # 1. Raw source URL, sha256, raw schema & conversion script
│   │   ├── refined-data.json             # 2. Refined project JSON, feature dictionary & observations
│   │   └── README.md                     # 3. Human/agent sidecar guide mirroring both JSONs
│   ├── ... (data01 through data34)
└── curated/                              # TRACKED master roll-ups built by scripts/verification/build_dashboard.py
    ├── README.md
    ├── observations-2026-10-20.json      # Canonical master snapshot (99 schema-valid observations)
    ├── observations-2026-10-20.csv
    └── composite-2026-10-20.json         # Composite indicator prototype (Tourism Pressure Index)
```

### Why `data/raw/` and `data/indicators/` are separated:
1. **Zero Duplication of Large Raw Files:** Multi-hundred-megabyte raw files (e.g., 250 MB Ookla shapefile ZIPs, Eurostat GISCO polygons, EU Tourism Dashboard CSVs) and multi-indicator Eurostat SDMX pulls are stored **once** in `data/raw/` (or `data/samples/` for small bounded API pulls) and never duplicated across indicator folders.
2. **All-JSON Edited Standard:** While raw payloads in `data/raw/` preserve their native upstream format (`.nc`, `.zip`, `.geojson`, `.csv`, `.xlsx`, `.pdf`) so their SHA-256 checksum matches the upstream response, **every edited summary and observation file inside `data/indicators/` and `data/curated/` is UTF-8 JSON**.

---

## 2. Option A Folder Contract (`raw-source-description.json` + `refined-data.json` + `README.md`)

Every indicator folder `data/indicators/dataXX-<slug>/` follows the industry-standard Medallion (Bronze/Silver-Gold) split so neither humans nor agents ever have to guess where data came from, how it was converted, or what a JSON key represents:

1. **`raw-source-description.json` (Upstream Raw Source & Conversion Contract):**
   - `raw_sources[]`: each upstream source's `source_id`, `provider`, clickable `upstream_url`, `access_method`, local `raw_file_path` (in `data/raw/` or `data/samples/`), `raw_format` (e.g. `.csv`, `.zip`, `.nc`, `.geojson`, `.json`), `sha256` fingerprint, `raw_schema_description` (every raw column/field explained), `raw_variables_kept` (whitelist), `raw_variables_dropped` (e.g. redacted PII or unused dimensions), and the exact **`conversion_script` + `conversion_command`** that converts the raw file into JSON.
2. **`refined-data.json` (Refined Project Data & Observations):**
   - `source_citations[]` & `conversion_script`: direct links back to the raw source and conversion script.
   - `transformation_rule`: plain-prose & mathematical specification of how the raw variables are filtered, spatially joined, or aggregated.
   - `feature_dictionary`: maps every JSON path in `refined_data` to `{type, unit, role, description}`, where `role` is one of:
     - `target_indicator` — final indicator value emitted to `observations`
     - `proxy_indicator` — verified proxy where direct measurement is unavailable (e.g., `Data01` NO2/CO)
     - `input_variable` — intermediate variable feeding a formula (e.g., `tests_count`, `classified_sites`)
     - `filter_dimension` / `spatial_dimension` / `temporal_dimension` — slicing keys
     - `internal_disaggregation` — NUTS3 island breakdown kept for audit context
     - `quality_metric` / `context_metric` — completeness or diagnostic field
   - `refined_data`: the structured indicator summary/breakdown.
   - `observations`: strict `schemas/observation-schema.json`-compliant array.
3. **`README.md` (Human & Agent Sidecar):**
   - Mirrors both `raw-source-description.json` and `refined-data.json` in structured Markdown tables.

Regenerate and verify all 34 indicator folders after any data update:

```bash
python3 scripts/verification/build_indicator_folders.py
```

---

## 3. Global Data Quality & Spatial Rules

### A. Spatial Reference & Aggregation Rule (`D-014`)
- **NUTS 2 (`EL62` = Ionian Islands)** is the strict regional analysis reference.
- **Operational micro levels:** `municipality`, `tourism_zone`, `beach`, `transport_node`, `poi`, `point`.
- **Country proxy (`EL`):** Used only when NUTS2 is not published upstream (e.g., `Data29` monthly Eurostat `tour_occ_nim` series).
- **NUTS 3 (`EL621` Zakynthos, `EL622` Kerkyra, `EL623` Ithaki/Kefallinia, `EL624` Lefkada) is an internal disaggregation only:** NUTS3 breakdowns may be stored inside `extracted-summary.json` (`role: internal_disaggregation`), but must be aggregated to `NUTS2/EL62` before emitting canonical observations in `observations.json`. No observation may carry `spatial_ref.level = "NUTS3"`.

### B. Provenance & Checksum Discipline
- Every raw fetch in `data/raw/` or `data/samples/` must have a recorded entry in `data/manifests/source-verification-YYYY-MM-DD.json` with `url`, `accessed_at`, `response_status`, and `checksum_sha256`.
- Every observation in `observations.json` must carry a valid `provenance` object (`access_method`, `request_url`, and `raw_checksum_sha256` / `raw_manifest` where applicable) conforming to `schemas/observation-schema.json` (`additionalProperties: false`).
- **GDPR / PII Redaction:** Personal contact fields (emails, phone numbers, exact personal identifiers) in public registers (such as `Data05` EMAS) must be stripped before writing to `data/samples/` or `data/indicators/` and listed under `raw_variables_dropped`.
