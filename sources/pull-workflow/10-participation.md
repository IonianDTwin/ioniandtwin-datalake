# Pull Workflow — 10 Participation

**Category:** Participation — `Συμμετοχικότητα`
**Indicator:** Data34
**Pillar:** Society

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data34 | User feedback | TripAdvisor / Google Reviews API; EU Tourism Dashboard | api | API key | UNVERIFIED |

## Pull process

### Data34 — User feedback / sentiment

1. **Review-platform feed** — TripAdvisor / Google Reviews APIs (paid, ToS/privacy-sensitive). `UNVERIFIED`; separate feasibility track.
2. **Citizen reports** — the project's own participatory feed (mobile app) is the deployed app's primary sentiment source; ingest it internally, cross-verified against sensors.
3. **Transform** — sentiment analysis (local-first LLM) over reviews/reports into a visitor-satisfaction indicator. Batch ~30 minutes.
4. **Privacy** — reviews/free text are potentially sensitive; apply GDPR-oriented governance, pseudonymisation, and data minimisation (`SECURITY_PRIVACY_ETHICS.md`).

## Notes & blockers

- `BLOCKER` TripAdvisor / Google Reviews require API keys and carry ToS/privacy constraints; not pull-tested.
- `RISK` Sentiment is an LLM-derived indicator; its formula, polarity, and thresholds must be defined and exposed before use (composite transparency requirement).
