# Data05 — EMAS / EU Ecolabel

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/emas-register-greece-2026-10-02.json [.json]  ──( scripts/verification/build_indicator_folders.py )──>  refined-data.json [.json]
  data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json [.json]  ──( scripts/verification/build_indicator_folders.py )──>  refined-data.json [.json]
```

## Quick Navigation (Option A Folder Layout)

| File in this folder | Extension | Purpose |
| :--- | :--- | :--- |
| **`raw-source-description.json`** | `.json` | **1. Raw Data Source Description:** Upstream URL, provider, local `data/raw/` path, raw file extension, `sha256` fingerprint, raw schema fields, variable whitelist, and the exact **conversion script** that transforms raw data into JSON. |
| **`refined-data.json`** | `.json` | **2. Refined Data JSON:** The clean, project-ready JSON data, its `feature_dictionary`, transformation formula, upstream source citation, and strict `observation-schema.json` records. |
| **`README.md`** | `.md` | **3. Human & Agent Guide:** This sidecar overview of both JSON files. |

- **Status:** `VERIFIED`
- **Greek Proposal Name:** EMAS / EU Ecolabel
- **Category:** `environmental_health_pollutants`
- **Refresh Cadence:** `on-change`
- **Raw Input File Extension(s):** `.json`
- **Primary Conversion / Builder Script:** `scripts/verification/build_indicator_folders.py`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `0`

## 1. Overview & Key Note

VERIFIED 2026-10-02: EMAS register REST https://webgate.ec.europa.eu/emas2/public/rest/registration/list (4,523 records, 27 countries; Greece 37, EL62 0) and EU Ecolabel CSV export https://publicstorage.data.env.service.ec.europa.eu/ecolabel/exports/most-recent-export.csv (89,298 licences; Greece 450, tourist-accommodation group Greece 0). Evidence: data/manifests/source-verification-2026-10-02.json.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `EMAS_register_REST` (European Commission — EU EMAS Register)
- **Upstream URL:** `https://webgate.ec.europa.eu/emas2/public/rest/registration/list`
- **Access Method:** `GET (REST JSON list, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/emas-register-greece-2026-10-02.json`
- **Raw File Extension & Format:** `.json` — `application/json (4,523 EU records filtered to 37 Greece records)`
- **SHA-256 Checksum:** `c8546768319f2f35796698a729b29c1375995f556b146877dca61ff2678e3288` (verified in `data/manifests/source-verification-2026-10-02.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_indicator_folders.py`
- **Conversion Command:** `python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `registrationNumber`, `organisationName`, `organisationCountryName`, `city`, `postalCode`, `sitesCount`, `nacesAsString`
- **Dropped / Redacted Fields:** `contactPersonEmail (GDPR PII redacted)`, `contactPersonPhone (GDPR PII redacted)`, `streetAddress`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `registrationNumber` | EMAS registration code (e.g. 'EL-000120') |
| `organisationName` | Registered legal entity name |
| `organisationCountryName` | Country name (filtered to 'Greece') |
| `city` | Municipality / city name (checked against Ionian Islands) |
| `postalCode` | Postal code (checked against 49xxx/28xxx/29xxx/31xxx Ionian prefixes) |
| `nacesAsString` | NACE economic activity classification string |

### Source 2: `EU_Ecolabel_catalogue_CSV` (European Commission — EU Ecolabel Catalogue)
- **Upstream URL:** `https://publicstorage.data.env.service.ec.europa.eu/ecolabel/exports/most-recent-export.csv`
- **Access Method:** `GET (semicolon-delimited CSV export, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json`
- **Raw File Extension & Format:** `.json` — `text/csv (89,298 rows, semicolon-delimited) -> summarized to JSON`
- **SHA-256 Checksum:** `7a3d424d7d8b031b1516416e923b024cd47b83e3417308870b37334b9235592d` (verified in `data/manifests/source-verification-2026-10-02.json`)
- **Conversion Script (`.json` -> `.json`):** `scripts/verification/build_indicator_folders.py`
- **Conversion Command:** `python3 scripts/verification/build_indicator_folders.py`
- **Whitelisted Raw Variables (`kept`):** `group_name`, `company_country`, `licence_number`, `extract_date`
- **Dropped / Redacted Fields:** `vat_number`, `company_contact_details`

| Raw Field / Column | Raw Source Description |
| :--- | :--- |
| `group_name` | Product/service group (checked for 'Tourist accommodation') |
| `company_country` | Country of licence holder ('Greece') |
| `licence_number` | Unique EU Ecolabel licence identifier |
| `extract_date` | Export snapshot date ('2026-10-01') |

## 3. Transformation & Refined Data Dictionary (`refined-data.json`)

**Transformation Rule:** Filter EU EMAS REST registration list to organisationCountryName=='Greece' (37 records) and match city/postalCode against Ionian Islands (EL62 = 0 records). Filter EU Ecolabel CSV export (89,298 licences) to Greece (450 licences) and group_name=='Tourist accommodation' (0 in Greece / 0 in EL62). Contact PII (email/phone) stripped before storage.

| Refined JSONPath | Type | Unit | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| `refined_data.emas.greece_records` | `integer` | `organisations` | `context_metric` | Total EMAS-registered organisations in Greece (37). |
| `refined_data.emas.ionian_islands_el62_records` | `integer` | `organisations` | `target_indicator` | Verified EMAS-registered organisations in Ionian Islands EL62 (0). |
| `refined_data.eu_ecolabel.greece_licences` | `integer` | `licences` | `context_metric` | Total EU Ecolabel licences in Greece across all product groups (450). |
| `refined_data.eu_ecolabel.ionian_islands_el62_tourist_accommodation` | `integer` | `licences` | `target_indicator` | Verified EU Ecolabel tourist-accommodation licences in Ionian Islands EL62 (0). |

## 4. Normalized Observations (`refined-data.json -> observations[]`)

All records in `refined-data.json -> observations` strictly conform to `schemas/observation-schema.json`.

_No observations emitted for this indicator yet._
