# Target Architecture

`PROPOSAL` High-level architecture from the proposal. Deferred implementation.

## Layers

1. **Ingestion** — scheduled (~30 min) pulls for 34 indicators; real-time mobile reports.
2. **Data Lake** — heterogeneous structured, semi-structured, unstructured raw data.
3. **ETL/ELT** — clean, homogenise, enrich with spatial/temporal attributes.
4. **Data Warehouse** — curated analytical repository feeding indicators and models.
5. **Analytics** — statistics, indicator extraction, ML (forecasting, clustering, anomaly detection).
6. **LLM layer** — local-first (AirLLM, QWEN); online APIs as fallback; vector DB / RAG for citizen reports (deferred).
7. **Serving** — Web Dashboard, Mobile App backend, API Gateway, Open Data Repository.

## Spatial model

- Macro: Region / NUTS 2 strategic indicators.
- Micro: municipality, tourism zone, beach, transport node, POI.
- Coupling via spatial-downscaling techniques.

## Service modules (planned, not implemented)

`services/api`, `services/ingestion`, `services/analytics`, `services/forecasting`, `services/alerts`, `services/rag` — each is a `.gitkeep` placeholder; see `services/README.md` for why they are currently empty.

## Deferred

`DECISION` Kafka streaming, RAG/vector infrastructure, forecasting, and alerts are deferred until source access, data contracts, legal constraints, and quality checks are verified.
