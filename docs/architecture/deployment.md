# Deployment

`PROPOSAL` Deployment assumptions from the proposal. No deployment exists yet.

## Assumptions

- `PROPOSAL` Local-first LLM inference on self-hosted hardware (AirLLM, QWEN, up to 70B).
- `PROPOSAL` Data Lake → Data Warehouse on managed storage (MariaDB and Postgres named in the proposal for vector/semantic data).
- `PROPOSAL` Kafka for time-series API streaming (deferred).
- `PROPOSAL` Web Dashboard and Mobile App backend as hosted services.
- `PROPOSAL` API Gateway and Open Data Repository for external consumers.

## Status

`DECISION` Nothing is deployed. Deployment planning is deferred until source access and data contracts are verified. There is no CI/CD, no hosting account, and no production credentials in this repository.

## Open questions

- `BLOCKER` Target hosting environment (cloud vs on-prem) is unspecified in the technical proposal.
- `BLOCKER` LLM local-hardware requirements (GPU/memory for 70B-class inference) are unverified.
- `RISK` Database choice (MariaDB vs Postgres vs a warehouse engine) is unresolved; the proposal names both but does not assign roles precisely.
