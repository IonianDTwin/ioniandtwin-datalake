# Evaluation Plan

`PROPOSAL` Evaluation methodology for the IonianDTwin vertical slice. Adapted conceptually from general reproducibility conventions.

## Data-quality evaluation

- Coverage: fraction of Data01–Data34 with a `VERIFIED` source per time window.
- Freshness: delay between source publication and ingestion.
- Completeness: missing-value rate per indicator and spatial unit.
- Plausibility: range and cross-source consistency checks.

## Composite-indicator evaluation

- Transparency: every composite must expose its formula, weights, units, and polarity.
- Sensitivity: how the composite responds to weight changes.
- Backtesting: historical fit where a reference series exists.

## Source verification evaluation

- For each candidate source: access type, terms/license, schema stability, refresh frequency, and whether a bounded read-only pull test passed.

## LLM evaluation (later)

- Faithfulness: does the natural-language output stay grounded in retrieved indicators?
- No-fabrication: refusal to state unsupported values.

## Status

`BLOCKER` No evaluation has run. This plan is a scaffold until the first vertical slice exists.
