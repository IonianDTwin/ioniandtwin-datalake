# Verification scripts

`DECISION` Reproducible, public, read-only, bounded pull tests. Each script writes a bounded sample into `data/samples/` or `data/raw/`, prints the response status and `sha256`, and — for JSON — renders a **self-contained visual report** (HTML + Markdown summary) next to the raw JSON.

## Run

```bash
scripts/verification/pull-eurostat-tourism.sh   # official tourism statistics (EL62 = Ionia Nisia)
scripts/verification/pull-open-meteo.sh         # weather + UV (no-key substitute)
scripts/verification/pull-gstc-pdf.sh           # GSTC Destination Criteria v2.0 PDF (no JSON report)
```

Each JSON pull produces three files side by side:

- `data/samples/<name>.json` — immutable raw response.
- `data/samples/<name>.html` — open in a browser: resource link at the top, decoded data table where every row is annotated with its **Data01–Data34 indicator + plain-English meaning**, and embedded raw JSON. No network/CORS needed.
- `data/samples/<name>.summary.md` — terminal/agent-friendly Markdown with the same annotated table.

The **per-indicator navigation index** lives at `data/samples/INDEX.html` (browser) and `data/samples/INDEX.md` (Markdown): Data01–Data34 grouped by category, each verified indicator showing its values and links to the sample reports.

## The indicator annotation map

The Data01–Data34 annotation and the index are driven by one authoritative file:

- `indicators/source-indicator-map.json` — for every indicator: name, category, status, source, access/auth, and (where verified) the exact dimension/filter (`series[].match`) that selects it from a sample.

To change how a data point is labelled, edit that file and re-render.

## Re-render existing samples from a manifest

```bash
python3 scripts/verification/render_pull_reports.py \
  --manifest data/manifests/source-verification-2026-09-22.json
```

## Build / refresh the per-indicator index

```bash
python3 scripts/verification/render_pull_reports.py \
  --index --manifest data/manifests/source-verification-2026-09-22.json
```

## Export normalized observations (the publication data file)

```bash
python3 scripts/verification/export_observations.py \
  --manifest data/manifests/source-verification-2026-09-22.json
```

Writes `data/curated/observations-<date>.json` (schema-aligned) + `.csv`, one record per verified data point.

This reads each `sample_path` (and its `url`, `status`, `content_type`, `checksum_sha256`, `accessed_at`, `source_id`) and regenerates the `.html` + `.summary.md` companions and the `INDEX.*`, so the visual view always matches the manifest evidence.

## Render a single file manually

```bash
python3 scripts/verification/render_pull_reports.py \
  --json data/samples/foo.json --source-key OpenMeteo_forecast \
  --name "Foo" --url "https://..." --status 200
```

Checksum and access timestamp are auto-computed if omitted. `--source-key` selects the annotation set (must match a `series[].source_key` in the map).

## Why this beats a plain JSON viewer

- Eurostat returns SDMX-JSON whose `value` map keys are numeric indices into the dimension arrays; the renderer decodes them into readable `freq / c_resid / unit / nace_r2 / geo / time` rows with labels, and maps each row to its `DataNN` indicator.
- The HTML is fully self-contained (data embedded), so it opens reliably from the filesystem with no CORS/network dependency and no external CDN.
- The resource link and provenance (status, content-type, sha256, timestamp) sit at the top of every report.
- The index answers "which DataNN does this number belong to?" in one place, with the verified value and a link back to the full sample.

## Rules

- Read-only, bounded requests only. No credentials, no access-control bypass, no scraping.
- A non-200 response is recorded as an access constraint, never as "the source does not exist".
- Real API keys (OpenWeatherMap, Google Maps, Copernicus data download, MarineTraffic, FlightRadar24) go in an untracked `.env`; these scripts never read or write secrets.

## Status

- `VERIFIED` Eurostat tourism datasets, Open-Meteo weather/UV, Copernicus CDSE catalogue, GSTC PDF.
- `INACCESSIBLE` OpenWeatherMap without a key (HTTP 401). Credential-gated sources remain unverified until a key is provided and authorized.
