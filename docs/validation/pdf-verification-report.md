# PDF / Document Verification Report

## Verified this session (2026-09-22)

### GSTC Destination Criteria v2.0 — downloaded and verified

`VERIFIED` Download of the Global Sustainable Tourism Council Destination Criteria v2.0 reference PDF succeeded (the standards document the proposal aligns with, and which the deployed app cites as `GSTC-Destination-Criteria-v2.0-2022.pdf`).

Evidence:

- URL: `https://www.gstc.org/wp-content/uploads/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`
- Method: `GET` (bounded, read-only, no credentials).
- Response: HTTP `200`, `content-type: application/pdf`, 497,680 bytes.
- `sha256`: `f40695269f6f771df59f0edf27bf25d0cabf797e1dc7e3deebbb7a51c7e57eb6`.
- File: `data/raw/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`.
- Format: `%PDF-1.7`, 18 pages.
- Metadata: Author `GSTC`; title page "GSTC Destination Criteria Version 2.0, 6 December 2019, with Performance indicators and SDGs"; preamble describes the four themes (sustainable management; socio-economic; cultural; environmental) used for the GSTC A–D mapping in `indicators/indicator-catalogue.md`.
- Reproducible command: `scripts/verification/pull-gstc-pdf.sh`.

`DECISION` This PDF is a **governance/standards reference**, not a time-series data source. It is used to anchor the GSTC mapping of Data01–Data34 and is not ingested as observations.

### Technical proposal text extraction (carried forward)

- `VERIFIED` `Παράρτημα - Συνοδευτικό Πρότασης με Τεχνικές Λεπτομέρειες.docx` (52,185 bytes; `sha256` `b55eb175fe5f0ec8a1297a383c4e09709600a7a9dec6212ebebb3745b2819560`) — user-supplied source document, text-extracted locally.
- `VERIFIED` Extracted text retained at `/tmp/proposal.txt` (52,972 bytes; 2026-09-21). It is the source of the Data01–Data34 catalogue and the source candidates.

## Not yet performed

- `BLOCKER` No other external PDFs verified (e.g., Eurostat tourism methodology, Copernicus CAMS/CMEMS documentation). Deferred — a methodology PDF download would follow the same pattern as the GSTC PDF.

## Evidence

- Manifest: `data/manifests/source-verification-2026-09-22.json` (GSTC entry).
- Checksums: `data/manifests/source-verification-2026-09-22.sha256`.
