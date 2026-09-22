# SECURITY, PRIVACY & ETHICS — IonianDTwin

## Data sensitivity

`REQUIREMENT` Treat the following as potentially sensitive: citizen reports, reviews, exact locations, inferred mobility, contact data, and free text.

`REQUIREMENT` Apply data minimisation, access control, pseudonymisation/anonymisation where applicable, retention rules, audit logging, and GDPR-oriented governance.

## Alerts and enforcement

`REQUIREMENT` Unverified data must not directly trigger public alerts, automated enforcement, or policy recommendations.

## LLM processing

`PROPOSAL` Privacy-first, local-first LLM processing. Online/free APIs (OpenRouter, Opencode) are a deliberate fallback only, selectable via platform settings, and must not receive personal data unless approved.

## Secrets

`REQUIREMENT` Credentials live only in an untracked `.env` file. `.env.example` documents variable names only. Keys, tokens, passwords, personal data, and private configuration never appear in Markdown, shell history, Git commits, issues, or generated reports.

## Source access

`REQUIREMENT` Read-only, bounded, public requests only for verification. No bypassing of authentication, robots directives, rate limits, paywalls, or licensing. No scraping of prohibited services.

## Threat model (initial)

`PROPOSAL` Trust boundaries to review before any production ingestion:
1. External source APIs → ingestion (input validation, rate limits, provenance capture).
2. Mobile app reports → backend (spam, fabrication, personal data minimisation).
3. Dashboard/API → institutional users (authentication, authorisation, least privilege).
4. Business API Gateway → anonymised aggregates only (no raw personal data).
5. Local LLM → prompts/embeddings (no PII exfiltration, retention limits).
6. Open Data Repository → public consumers (anonymisation, licensing).

This is a starting list, not an audit. A full security review is scheduled after source access and data contracts are stable.
