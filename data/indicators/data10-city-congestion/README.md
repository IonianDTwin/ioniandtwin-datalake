# Data10 — City congestion

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  [UNVERIFIED source track — no raw file or conversion script active yet]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `UNVERIFIED`
- **Greek Proposal Name:** —
- **Category:** `dynamic_congestion`
- **Refresh Cadence:** `live`
- **Raw Input File Extension(s):** `None (UNVERIFIED)`
- **Primary Conversion / Builder Script:** `None (UNVERIFIED source track — no synthetic data invented)`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `0`

## 1. Overview & Key Note

—

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

No raw payload ingested yet (`UNVERIFIED` source track — no synthetic data invented).
## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** UNVERIFIED source track: Urban zone traffic delay index fused with geolocated citizen congestion reports. No values are invented.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.status` | `string` | `enum` | `quality_metric` | Verification status ('UNVERIFIED' - no synthetic data emitted). |
| `refined_data.candidate_source` | `string` | `text` | `context_metric` | Candidate provider: Google Maps Platform + Mobile App citizen reports. |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

_No observations emitted for this indicator yet._
