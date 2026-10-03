# Quality Rules

`PROPOSAL` Data-quality checks for the observation pipeline.

## Checks

- **Coverage** - fraction of Data01-Data34 with a `VERIFIED` source per time window.
- **Freshness** - delay between `observed_at` and `ingested_at` within an allowed bound.
- **Completeness** - missing-value rate per indicator and spatial unit.
- **Plausibility** - value-range and cross-source consistency checks.
- **Spatial consistency (D-014)** - `spatial_ref.level` and `spatial_ref.code` must agree (`NUTS2 ↔ EL62`, `country ↔ EL`, `point ↔ lat,lon`). NUTS 3 (EL621-624) is aggregated to NUTS 2 before emission and is never emitted as a level; finer-than-NUTS2 levels are allowed only for operational indicators (`point`, `municipality`, `tourism_zone`, `beach`, `transport_node`, `poi`).
- **Cross-verification** - citizen reports confirmed against sensor/IoT data before updating the twin.

## Enforcement

`DECISION` ISO 8601 timestamps with explicit time zones. Observations failing hard checks are quarantined, not silently dropped.

## Alerts

`REQUIREMENT` Unverified data must not trigger public alerts, automated enforcement, or policy recommendations.

## Status

`DECISION` Rules are defined (2026-09-24); they are not yet implemented by a pipeline. No data flows yet (D-002), so enforcement is deferred. The spatial-consistency rule (D-014) is partially enforced already in `scripts/verification/build_dashboard.py`: `spatial_ref.level` is derived from the geo code and NUTS 3 is aggregated to NUTS 2 (Data22) or refused.
