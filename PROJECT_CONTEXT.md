# PROJECT_CONTEXT — IonianDTwin

## Purpose

`DECISION` IonianDTwin is a university Digital Twin project for the sustainable management of tourism and urban/environmental systems in the Ionian Islands Region (Περιφέρεια Ιονίων Νήσων, NUTS 2 level).

`REQUIREMENT` The long-term sustainability of popular tourist destinations requires balanced development across the three sustainability dimensions: economy, society–culture, and environment. The system is built to monitor, predict, and intelligently balance the urban and tourism ecosystems of the region.

## Source of requirements

- **Requirements baseline:** the supplied technical proposal, an annex in Greek — `Παράρτημα - Συνοδευτικό Πρότασης με Τεχνικές Λεπτομέρειες.docx` ("Annex – Accompanying Proposal with Technical Details").

`ASSUMPTION` The proposal is a requirements baseline, not proof that any source, API, indicator definition, license, or access route is operational.

## Proposed system components

`REQUIREMENT` Two interconnected software subsystems:

1. **Central Digital Twin platform (Web Dashboard)** — the primary spatial and sustainability management infrastructure for institutional users. High-fidelity representation of the urban and natural environment; multi-layer overlay correlating environmental zones, weather, and mobility networks; analytics and ML models producing forecasts, alerts, and sustainability indicators; LLM-based natural-language interface for queries, explanations, reports, and policy recommendations.
2. **Mobile application** — real-time alerts to residents and visitors; bidirectional interface where users act as field sensors and submit short problem reports (traffic congestion, 5G network problems, water outages).

## Spatial and temporal model

- `REQUIREMENT` **Macro level:** Region / NUTS 2 strategic governance (aggregate indicators: tourism intensity, seasonality, carrying capacity).
- `REQUIREMENT` **Micro level:** municipality, tourism zone, beach, transport node, point of interest (operational indicators for local intervention).
- `PROPOSAL` Coupling is achieved via spatial-downscaling techniques.
- `REQUIREMENT` Periodic ingestion approximately every 30 minutes for asynchronous sources; event-driven / near-real-time only where technically justified.

## Data architecture

`PROPOSAL` Data Lake (heterogeneous raw) → ETL/ELT (clean, homogenise, enrich with spatial/temporal attributes) → Data Warehouse (analytical) → indicators, ML, forecasting, anomaly detection → dashboard/API. Raw citizen reports are cross-verified against IoT sensor data before they update the twin.

## Local-first LLM strategy

`REQUIREMENT` Privacy-first, local-first LLM processing (AirLLM, QWEN, and similar approaches allowing local execution of large models). Online/free APIs (OpenRouter, Opencode) are a deliberate fallback only for load beyond local hardware. Batch processing every ~30 minutes; streaming responses are not required.

## Standards alignment

`REQUIREMENT` Alignment with the Global Sustainable Tourism Council **GSTC v2.0** sustainability criteria.

## Indicator baseline

`REQUIREMENT` The proposal presents **Data01–Data34** across: environmental health and pollutants, dynamic congestion, sustainable transport, climate adaptation, social pressure and infrastructure, digital infrastructure, spatial sustainability, tourism performance, density and typology, and participatory feedback. The normalised catalogue lives in `indicators/indicator-catalogue.md`.

## Known requirements inconsistencies (resolved 2026-09-24)

- `DECISION` (confirmed, D-007) The main catalogue ends at Data34, but one GSTC mapping references **Data35** — a transcription error for **Data34** (user feedback); user confirmed "35" → "34".
- `DECISION` (confirmed, D-008) The Climate Adaptation category's duplicated `Data 15` label (`Ποιότητα Αέρα` and `Πρόταση AI για εσωτερικές δραστηριότητες`) — Data15 = Air quality; the corrected source removed the indoor-activities entry.
- Both resolved and documented; the original text is preserved as evidence. See `RISKS_AND_ASSUMPTIONS.md` and `DECISIONS.md` (D-007/D-008).

## Composite indicators (from proposal)

`PROPOSAL` Tourist Pressure Index, Environmental Burden Index, Infrastructure Resilience Index, plus monitored indicators: tourism density per area, infrastructure pressure, traffic load, environmental burden, seasonality, and visitor satisfaction (sentiment analysis).
