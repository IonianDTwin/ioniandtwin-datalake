# Source-extraction procedures

`DECISION` These Markdown files describe how to get data from sources that are **not a direct API** — public webpages, PDFs, and downloadable files. They exist because those sources need a repeatable "download → verify → extract → normalise" process, not just a `curl` call.

## Do we need these? — access-pattern audit (2026-09-22)

Every unverified/partial indicator was classified by how its source is actually reached (bounded, read-only checks):

| Indicator | Source | Access pattern | Procedure MD needed? |
|---|---|---|---|
| Data32 | Eurostat `nace_r2` breakdown | **Data already pulled** — needs a classification rule, not a new source | No (see note below) |
| Data29 | Eurostat monthly `tour_occ_nim` | Direct API (`VERIFIED` HTTP 200 at geo=EL; NUTS2 monthly not available) | No — extend `pull-eurostat-tourism.sh` |
| Data02/03 | EEA bathing-water status / waterbase | Public webpage/PDF/file | **Yes** — download + extract |
| Data04 | Blue Flag (FEE) | Public webpage (interactive list; no clean CSV confirmed) | **Yes** — but URL/export to confirm |
| Data05 | EMAS register / EU Ecolabel | Public webpage/file | **Yes** — download + extract |
| Data24 | EEA CDDA / Natura 2000 | Public webpage/file | **Yes** — download + extract |
| Data28 | Booking / social APIs | Paid/ToS-gated API | No — feasibility track |
| Data01/03/06–12/17–21/34 | CAMS/IoT, Google/MarineTraffic/FlightRadar/KTEL, utilities, reviews | Internal / partner / paid / ToS | No — document a *request*, not a download |

**Conclusion:** procedure files are useful for a specific, small class — the public **document/webpage** sources (Data02/03, Data04, Data05, Data24). For those, follow `download-extract.md`.

## The two kinds of "pull"

1. **API pull** — covered by `scripts/verification/pull-*.sh` and `sources/pull-workflow/`. Output: raw JSON → annotated report.
2. **Document extraction** — covered here. Output: raw file → checksum manifest → extracted text/tables → observations.

The GSTC PDF (`data/raw/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf`) is the worked example of pattern 2 — it was downloaded, checksummed, and text-extracted with `pypdf`. See `download-extract.md`.

## Data32 clarification (not a missing source)

`VERIFIED` Data32 ("dominant tourism typology") data is **already in the pulled Eurostat samples**. The `nace_r2` breakdown gives accommodation-type shares of nights for EL62:

- Hotels (`I551`): ≈73% (2022) / 70% (2023)
- Holiday & short-stay (`I552`): ≈26% / 30%
- Camping (`I553`): <1%

"Dominant typology" = **hotels** (`ASSUMPTION`). The only thing missing is the *definition/classification rule* in the proposal, not the data. Resolve the rule, and Data32 flips to `VERIFIED` with no new pull.
