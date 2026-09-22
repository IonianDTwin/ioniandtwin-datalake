# data/samples — pulled samples + visual reports

`VERIFIED` Bounded, public, read-only pull samples and their generated views.

## Start here

- **`INDEX.html`** — open in a browser: all Data01–Data34 grouped by category, with verified values and links to each sample's report.
- **`INDEX.md`** — the same index in Markdown (for terminal/agent reading).

## Per-source files

Each pull produces three files side by side:

- `<name>.json` — immutable raw response.
- `<name>.html` — self-contained viewer: "Indicators pulled" summary at the top, then the full decoded data, then raw JSON.
- `<name>.summary.md` — Markdown version of the same.

## Provenance

Checksums and request metadata live in `../manifests/source-verification-2026-09-22.json` and `…-2026-09-22.sha256`. Normalised observations derived from these samples live in `../curated/`.
