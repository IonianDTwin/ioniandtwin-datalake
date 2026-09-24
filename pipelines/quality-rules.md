# Quality Rules

`PROPOSAL` Data-quality checks for the observation pipeline.

## Checks

- **Coverage** — fraction of Data01–Data34 with a `VERIFIED` source per time window.
- **Freshness** — delay between `observed_at` and `ingested_at` within an allowed bound.
- **Completeness** — missing-value rate per indicator and spatial unit.
- **Plausibility** — value-range and cross-source consistency checks.
- **Cross-verification** — citizen reports confirmed against sensor/IoT data before updating the twin.

## Enforcement

`DECISION` ISO 8601 timestamps with explicit time zones. Observations failing hard checks are quarantined, not silently dropped.

## Alerts

`REQUIREMENT` Unverified data must not trigger public alerts, automated enforcement, or policy recommendations.

## Status

`DECISION` Rules are defined (2026-09-24); they are not yet implemented by a pipeline. No data flows yet (D-002), so enforcement is deferred.
