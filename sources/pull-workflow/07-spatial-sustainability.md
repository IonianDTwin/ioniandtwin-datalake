# Pull Workflow — 07 Spatial Sustainability

**Category:** Spatial Sustainability — `Χωροταξική Αειφορία`
**Indicators:** Data22–Data25
**Pillar:** Environment / Society

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data22 | Tourist diversity (zones) | EU Tourism Dashboard maps | api / download | none | UNVERIFIED (candidate) |
| Data23 | Density of cultural elements | EU Tourism Dashboard maps | api / download | none | UNVERIFIED (candidate) |
| Data24 | Protected land (%) | EU Tourism Dashboard maps | api / download | none | UNVERIFIED (candidate) |
| Data25 | Accommodation in high-value areas | EU Tourism Dashboard maps | api / download | none | UNVERIFIED (candidate) |

## Pull process

### Data22–Data25 — Spatial/zone indicators (maps)

1. **Locate** the exact Eurostat/ESTAT spatial dataset or dashboard export for each indicator (tourist zones, cultural elements, protected land, accommodation in high-value areas). Do not fabricate a dataset code.
2. **Request/download** the CSV/GeoJSON export via the Eurostat bulk download or API (same SDMX 2.1 pattern as the verified `tour_occ_nin2`).
3. **Store raw / manifest** — file to `data/raw/`, checksum in `data/manifests/`.
4. **Transform** — join to spatial units (NUTS2 / municipality / tourism zone) and emit observations with `spatial_ref.level` and `geometry` per `schemas/observation-schema.json`.

## Notes & blockers

- `BLOCKER` The specific Eurostat datasets for these four indicators are not yet identified; the Eurostat **API mechanism** is verified, but the dataset codes remain to be confirmed.
- `PROPOSAL` Protected land (%) may also be available from Natura 2000 / EEA land-cover datasets — confirm the authoritative source before use.
