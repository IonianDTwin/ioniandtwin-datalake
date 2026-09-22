# data/

`DECISION` Raw data, secrets, generated outputs, caches, and local databases stay out of Git unless expressly approved.

## Subdirectories

- `raw/` — immutable raw source responses and downloads (out of Git; `.gitkeep` only).
- `staging/` — working transforms before curation.
- `curated/` — cleaned, schema-valid observations (`observations-*.json` / `.csv`). **Tracked in Git** — these are small, public, non-sensitive aggregates intended for publication.
- `samples/` — small, explicitly-approved sample datasets for tests/docs. Also holds the **visual reports** (`.html` + `.summary.md` next to each `.json`) and the **navigation index** (`INDEX.html` / `INDEX.md`) that groups Data01–Data34 by category and links each verified indicator to its sample report.
- `manifests/` — provenance manifests with checksums and source metadata.

## Rules

- Keep retained raw payloads immutable; use checksums and manifests.
- Preserve the provenance chain raw → observation → indicator.
- A raw document (e.g., the proposal `.docx`) is copied here only with user approval.
