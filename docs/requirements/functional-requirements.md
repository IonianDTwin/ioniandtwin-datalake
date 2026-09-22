# Functional Requirements

`ASSUMPTION` Derived from the technical proposal. Not yet validated against any operational system.

## Web Dashboard

- `REQUIREMENT` Geospatial visualisation of the urban and natural environment with multi-layer overlays (environmental zones, weather, mobility networks).
- `REQUIREMENT` Display of sustainability indicators, analytics, forecasts, alerts, and reports.
- `REQUIREMENT` Natural-language interaction (LLM) for queries, explanations, reports, and automated policy recommendations.
- `REQUIREMENT` Predictive alerts for tourism overload and infrastructure stress.

## Mobile application

- `REQUIREMENT` Real-time alerts to residents and visitors, including alternative-activity suggestions based on environmental indicators.
- `REQUIREMENT` Participatory reports: traffic congestion, 5G/network problems, water outages, beach congestion.
- `PROPOSAL` Users act as field sensors; reports are cross-verified against IoT data before updating the twin.

## Data and analytics

- `REQUIREMENT` Data Lake ingestion of heterogeneous raw data; ETL/ELT into a Data Warehouse.
- `REQUIREMENT` Indicator generation, ML-based forecasting, clustering, and anomaly detection.
- `REQUIREMENT` ~30-minute periodic ingestion for asynchronous sources; near-real-time only where justified.
- `PROPOSAL` Vector database / RAG for semantic analysis of citizen reports (deferred until contracts are stable).
- `PROPOSAL` Kafka for time-series API streaming (deferred).

## Access and interoperability

- `REQUIREMENT` API Gateway exposing anonymised, aggregated data to businesses.
- `REQUIREMENT` Open Data Repository for the academic community.

## Scope of this workstation

`DECISION` None of the above is implemented yet. This repository only records and normalises the requirements.
