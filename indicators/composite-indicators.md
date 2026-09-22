# Composite Indicators

`PROPOSAL` From the technical proposal. No formula, weight, or polarity is defined there; these are candidate constructs only.

## Named composites (proposal)

- Tourist Pressure Index (`Δείκτης Τουριστικής Πίεσης`)
- Environmental Burden Index (`Δείκτης Περιβαλλοντικής Επιβάρυνσης`)
- Infrastructure Resilience Index (`Δείκτης Ανθεκτικότητας Υποδομών`)

## Named monitored indicators (proposal)

- Tourism density per area (`Δείκτη Τουριστικής Πυκνότητας ανά περιοχή`)
- Infrastructure pressure (`Δείκτη Πίεσης Υποδομών`)
- Traffic load (`Δείκτη Κυκλοφοριακής Επιβάρυνσης`)
- Environmental burden (`Δείκτη Περιβαλλοντικής Επιβάρυνσης`)
- Seasonality (`Δείκτη Εποχικότητας`)
- Visitor satisfaction via sentiment analysis (`Δείκτη Ικανοποίησης Επισκεπτών`)

## Required transparency

`DECISION` Every composite must expose formula, weights, units, and polarity (see `docs/research/evaluation-plan.md`). Composites are deferred until the underlying observation schema and data-quality rules are stable.

## Status

`BLOCKER` No aggregation method defined. Deferred until the observation schema and data-quality rules are stable (see `pipelines/quality-rules.md`).
