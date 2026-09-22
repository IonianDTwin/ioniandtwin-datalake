# PDF & Document Sources

`VERIFIED` One document-oriented source has been downloaded and verified (2026-09-22). It is a governance/standards reference, not a time-series data source.

## Verified document

- **GSTC Destination Criteria v2.0 (with SDGs)** — the standards document the proposal aligns with and the deployed app cites.
  - URL: `https://www.gstc.org/wp-content/uploads/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`
  - HTTP 200, `application/pdf`, 497,680 bytes, 18 pages, `%PDF-1.7`.
  - `sha256`: `f40695269f6f771df59f0edf27bf25d0cabf797e1dc7e3deebbb7a51c7e57eb6`.
  - File: `data/raw/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`.
  - Use: anchors the GSTC A–D mapping of Data01–Data34; not ingested as observations.

## Proposal document (carried forward)

- `VERIFIED` `Παράρτημα - Συνοδευτικό Πρότασης με Τεχνικές Λεπτομέρειες.docx` (52,185 bytes; `sha256` `b55eb175…2819560`) — located and text-extracted. Source of the Data01–Data34 catalogue.

## Candidate downloadable documents (unverified)

- `PROPOSAL` Eurostat tourism methodology / indicator definitions.
- `PROPOSAL` Copernicus CAMS/CMEMS API documentation.
- `PROPOSAL` OpenWeatherMap / Meteo.gr terms of use.
- `PROPOSAL` Official Ionian Islands statistics reports (e.g., arrivals, occupancy).

Each would follow the same download pattern as the GSTC PDF: `GET` → checksum → manifest → extract text (`pypdf`) → record evidence.

## Status

`VERIFIED` GSTC PDF downloaded and checksummed. `BLOCKER` Remaining documents not yet located/verified.
