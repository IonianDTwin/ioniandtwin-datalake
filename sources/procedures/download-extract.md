# Procedure — download & extract a public document/file

`DECISION` Reusable procedure for sources that publish data as a PDF, CSV, XLSX, GeoJSON, or a plain webpage (not a JSON API). Use this for Data02/03 (bathing water), Data04 (Blue Flags), Data05 (EMAS/Ecolabel), Data24 (protected land).

## Steps

1. **Locate the authoritative URL** — the publisher's own page (EEA, FEE, European Commission, etc.), not a mirror. Do not invent a URL; if the link is uncertain, record it as a `BLOCKER` and ask.

2. **Download (bounded, read-only)**:
   ```bash
   curl -sS -L --max-time 120 -o data/raw/<name>.<ext> "<URL>" -w "HTTP %{http_code} | %{content_type} | %{size_download}B\n"
   ```

3. **Verify** — record the file type and checksum:
   ```bash
   sha256sum data/raw/<name>.<ext>
   ```

4. **Manifest it** — add an evidence entry to `data/manifests/source-verification-YYYY-MM-DD.json` with `url`, `method`, `response_status`, `content_type`, `checksum_sha256`, `accessed_at`, `sample_path`.

5. **Extract**:
   - PDF text/tables → `python3 -c "from pypdf import PdfReader; ..."`
   - CSV/TSV → read directly.
   - XLSX → `openpyxl` (if available) or export to CSV.
   - GeoJSON/GPKG → read with `geopandas`/`json` and preserve geometry in `spatial_ref.geometry`.

6. **Normalise** — map the extracted values to Data01–Data34 observations per `schemas/observation-schema.json` (ISO 8601 `observed_at`, explicit `spatial_ref`, `provenance.raw_checksum_sha256`).

7. **Label the outcome** — `VERIFIED` / `PARTIAL` / `INACCESSIBLE` in `sources/source-verification-matrix.md`, and update the indicator's `status` in `indicators/source-indicator-map.json`.

## Worked example (already completed)

GSTC Destination Criteria v2.0 PDF — the standards reference, not a time-series source:

- URL: `https://www.gstc.org/wp-content/uploads/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`
- `GET` → HTTP 200, `application/pdf`, 497,680 bytes, 18 pages, `%PDF-1.7`.
- `sha256`: `f40695269f6f771df59f0edf27bf25d0cabf797e1dc7e3deebbb7a51c7e57eb6`.
- Extracted with `pypdf` (`PdfReader` → 18 pages, metadata Author `GSTC`).
- Reproducible script: `scripts/verification/pull-gstc-pdf.sh`.

## Rules

- Read-only, bounded requests only. No scraping, no access-control bypass, no robots violation.
- A failed download is an access constraint, never "the source does not exist".
- Never cite a document without reading it.

## Status of candidate documents

| Source | Indicator | State |
|---|---|---|
| GSTC Destination Criteria v2.0 | (standards alignment) | `VERIFIED` — done |
| EEA bathing-water status | Data02/03 | URL to confirm, then apply this procedure |
| Blue Flag list (FEE) | Data04 | Interactive page; confirm an export/list URL first |
| EMAS register / EU Ecolabel | Data05 | URL to confirm |
| EEA CDDA / Natura 2000 | Data24 | URL to confirm |
