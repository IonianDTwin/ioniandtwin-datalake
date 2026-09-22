# Data Flow

`PROPOSAL` End-to-end data flow from the proposal. Not implemented.

## Flow

1. **Collect** — 30-minute cron pulls for the 34 indicators (IoT sensors, weather API, Google Maps traffic) plus real-time mobile reports.
2. **Cross-verify** — citizen reports are cross-checked against IoT sensor data before updating the twin.
3. **Structure** — raw data normalised to JSON.
4. **Curate** — clean, homogenise, enrich with spatial/temporal attributes; move to Data Warehouse.
5. **Analyse** — statistical extraction of indicators; ML forecasting, clustering, anomaly detection.
6. **Serve** — dashboard, mobile alerts, API Gateway (anonymised), Open Data portal.
7. **Optional RAG** — citizen reports → embeddings → vector DB (MariaDB/Postgres) → LLM semantic analysis (deferred).

## Provenance chain

`DECISION` Every retained raw response keeps: source URL, owner, documentation, access timestamp, method, request parameters, response status, content type, schema observations, and evidence location. Raw payloads are immutable where retained; checksums and manifests in `data/manifests/`.

## ISO 8601

`DECISION` All observations use ISO 8601 timestamps with explicit time zones.
