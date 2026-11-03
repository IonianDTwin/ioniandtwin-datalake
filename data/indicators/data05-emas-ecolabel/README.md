# Data05 — EMAS / EU Ecolabel

## Pipeline Lineage (Raw Extension -> Conversion Script -> Refined JSON)

```text
  data/samples/emas-register-greece-2026-10-02.json [.json]  ──( none retained (ad hoc extraction 2026-10-02) )──>  refined-data.json [.json]
  data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json [.json]  ──( none retained (ad hoc extraction 2026-10-02) )──>  refined-data.json [.json]
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
- **Primary Conversion / Builder Script:** `scripts/verification/compute-data05-certifications.py (observations from the Greece extracts); extraction of the extracts themselves: none retained (2026-10-02)`
- **Refined Output Format:** `.json` (`refined-data.json`)
- **Observations Emitted:** `4`

## 1. Overview & Key Note

VERIFIED 2026-10-02: EMAS register REST https://webgate.ec.europa.eu/emas2/public/rest/registration/list (4,523 records, 27 countries; Greece 37, EL62 0) and EU Ecolabel CSV export https://publicstorage.data.env.service.ec.europa.eu/ecolabel/exports/most-recent-export.csv (89,298 licences; Greece 450, tourist-accommodation group Greece 0). Evidence: data/manifests/source-verification-2026-10-02.json. Observations (2026-11-03): EL62 EMAS registrations = 0, EL62 EU Ecolabel tourist-accommodation licences = 0, with Greece context (37 / 0), from scripts/verification/compute-data05-certifications.py.

## 2. Raw Source Provenance & Conversion (`raw-source-description.json`)

### Source 1: `EMAS_register_REST` (European Commission — EU EMAS Register)
- **Upstream URL:** `https://webgate.ec.europa.eu/emas2/public/rest/registration/list`
- **Access Method:** `GET (REST JSON list, no key)`
- **Local Raw File (`data/raw/` or `data/samples/`):** `data/samples/emas-register-greece-2026-10-02.json`
- **Raw File Extension & Format:** `.json` — `application/json (4,523 EU records filtered to 37 Greece records)`
- **SHA-256 Checksum (of the local file, recomputed at build):** `93a97b63c7d8bc59addb9ee8b15c4f449e99acccad1f667d6c7cee66efd6f059`
- **Evidence Manifest:** `data/manifests/source-verification-2026-10-02.json`
- **SHA-256 of the full upstream response (not retained):** `c8546768319f2f35796698a729b29c1375995f556b146877dca61ff2678e3288`
- **Lineage Note:** The local file is a Greece-only extract (37 records) of the full 14,650,764-byte EU register response. The full response was not retained; its hash is upstream_response_sha256 (manifest checksum_sha256). The extract hash matches the manifest's sample_checksum_sha256, which was updated after the 2026-10-14 PII redaction (commit 640336d). No extraction script was kept.
- **Conversion Script (`.json` -> `.json`):** `none retained (ad hoc extraction 2026-10-02)`
- **Conversion Command:** `none retained; reproduce by re-pulling upstream_url and filtering as in transformation_rule`
- **Whitelisted Raw Variables (`kept`):** `registrationNumber`, `organisationName`, `organisationCountryName`, `city`, `postalCode`, `sitesCount`, `nacesAsString`
- **Dropped / Redacted Fields:** `email (GDPR PII, redacted 2026-10-14)`, `phone (GDPR PII, redacted 2026-10-14)`, `all non-Greece records`

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
- **SHA-256 Checksum (of the local file, recomputed at build):** `6ed15e62b9fdbe0de4fc00480fe444b222a244ce68e86249f4bf454d9beebe59`
- **Evidence Manifest:** `data/manifests/source-verification-2026-11-03.json`
- **SHA-256 of the full upstream response (not retained):** `7a3d424d7d8b031b1516416e923b024cd47b83e3417308870b37334b9235592d`
- **Lineage Note:** The local file is a JSON summary of the full 17,153,575-byte CSV export (89,298 licences). The full export was not retained; its hash is upstream_response_sha256 (manifest checksum_sha256). The summary's own hash was first recorded in data/manifests/source-verification-2026-11-03.json from the copy committed in 82bf2f4. No extraction script was kept.
- **Conversion Script (`.json` -> `.json`):** `none retained (ad hoc extraction 2026-10-02)`
- **Conversion Command:** `none retained; reproduce by re-pulling upstream_url and filtering as in transformation_rule`
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

| `observation_id` | `observed_at` | `spatial_ref` | `value` | `unit` | `temporal_granularity` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EMAS_register_REST:Data05:emas_registrations:EL62:2026-10-01` | `2026-10-01T22:12:00+00:00` | `NUTS2/EL62` | **0** | `organisations` | `instant` |
| `EMAS_register_REST:Data05:emas_registrations:EL:2026-10-01` | `2026-10-01T22:12:00+00:00` | `country/EL` | **37** | `organisations` | `instant` |
| `EU_Ecolabel_catalogue_CSV:Data05:ecolabel_tourist_accommodation:EL62:2026-10-01` | `2026-10-01T22:12:00+00:00` | `NUTS2/EL62` | **0** | `licences` | `instant` |
| `EU_Ecolabel_catalogue_CSV:Data05:ecolabel_tourist_accommodation:EL:2026-10-01` | `2026-10-01T22:12:00+00:00` | `country/EL` | **0** | `licences` | `instant` |
