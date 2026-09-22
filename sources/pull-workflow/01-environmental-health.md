# Pull Workflow — 01 Environmental Health & Pollutants

**Category:** Environmental Health & Pollutants — `Περιβαλλοντική Υγεία & Ρύποι`
**Indicators:** Data01–Data05
**Pillar:** Environment

## Indicators & sources

| ID | Indicator | Source | Access | Auth | Status |
|---|---|---|---|---|---|
| Data01 | Airport CO2 levels | Copernicus CAMS; local IoT stations | api / internal | registration / partner | UNVERIFIED |
| Data02 | Excellent bathing waters (%) | Copernicus CMEMS; EU Tourism Dashboard | api | registration / none | UNVERIFIED |
| Data03 | Clean beach water (reports) | Copernicus CMEMS; user reports | api / user_reports | registration / app | UNVERIFIED |
| Data04 | Blue Flags | EU Tourism Dashboard | download / web | none | UNVERIFIED |
| Data05 | EMAS / EU Ecolabel | EU Tourism Dashboard | download / web | none | UNVERIFIED |

## Pull process

### Data01 — Airport CO2 (CAMS + local IoT)

1. **Request** — CAMS Regional air-quality API (particulate/CO2 at entry gates). Requires an Atmosphere Data Store registration token in `.env`.
2. **Store raw** — netCDF/GRIB or JSON response to `data/raw/cams-…`.
3. **Manifest** — record endpoint, params, checksum, timestamp in `data/manifests/`.
4. **Transform** — extract the point/zone value nearest the airport POI into an observation (`indicator_id=Data01`).
5. **Cross-check** — local IoT station readings where available.

### Data02 / Data03 — Bathing & beach water (CMEMS + reports)

1. **Request** — CMEMS marine water-quality product via the Copernicus Marine Data Store (registration token required).
2. **Store raw / manifest** as above.
3. **Transform** — map water-quality class to "% excellent bathing waters" (`Data02`) and clean-beach reports (`Data03`).
4. **Cross-verify** — citizen reports against CMEMS/IoT (`quality.cross_verified`).

### Data04 / Data05 — Blue Flags & EMAS/Ecolabel (documents)

1. **Locate** the authoritative published listing (candidate: official Blue Flag / EMAS register publications). Do not fabricate a URL.
2. **Download** the listing PDF/CSV, checksum, and manifest it (same pattern as the verified GSTC PDF in `pdf-and-document-sources.md`).
3. **Transform** — count certified sites per spatial unit into observations.

## Notes & blockers

- `BLOCKER` CAMS/CMEMS data download requires a registration token (not yet provided). The CDSE **catalogue** is `PARTIAL`-verified (public), but product download is gated.
- `RISK` "Air quality" appears both here (Data01, CO2 at entry gates) and in Climate Adaptation (Data15) — see `indicator-catalogue.md` for the overlap; do not silently merge.
- Blue Flag data is published by the Foundation for Environmental Education; "EU Tourism Dashboard" is the proposal's candidate source. Confirm the actual authoritative feed before pulling.
