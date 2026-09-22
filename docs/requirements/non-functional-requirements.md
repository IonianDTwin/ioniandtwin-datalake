# Non-Functional Requirements

`ASSUMPTION` Derived from the technical proposal. Unverified until an implementation exists.

## Performance and scale

- `PROPOSAL` Batch LLM processing every ~30 minutes; streaming responses are not required.
- `PROPOSAL` Time-series API data via Kafka where necessary (deferred).
- `PROPOSAL` Local execution of large models (up to 70B) via AirLLM / QWEN.

## Privacy and security

- `REQUIREMENT` Local-first LLM processing for user-data protection; online APIs only as fallback.
- `REQUIREMENT` GDPR-oriented governance; data minimisation, pseudonymisation/anonymisation, retention, audit logging.
- `REQUIREMENT` Secrets only in untracked `.env`.

## Reliability and data quality

- `REQUIREMENT` Cross-verification of citizen reports against IoT sensor data.
- `REQUIREMENT` Unverified data must not trigger public alerts or enforcement.
- `PROPOSAL` Data-quality checks in `pipelines/quality-rules.md`.

## Interoperability and standards

- `REQUIREMENT` GSTC v2.0 alignment.
- `DECISION` ISO 8601 timestamps with explicit time zones.
- `PROPOSAL` JSON structuring of raw data.

## Accessibility and openness

- `REQUIREMENT` Open Data publication (anonymised) for academia and residents.
- `PROPOSAL` WCAG-oriented accessibility for the dashboard (to be specified).

## Compliance

- `RISK` Data licensing, API terms of use, and GDPR legal basis are unverified for every candidate source and must be established before production ingestion.
