# Refresh scheduler — design and first implementation (`PROPOSAL`, 2026-11-03)

Goal: once an indicator's definition is locked (`VERIFIED` + a `DECISION` entry), a scheduler keeps its data current for the digital twin without weakening the evidence rules. The proposal's 30-minute ingestion cycle (D-005) applies to the live sources; statistical sources follow their publishers' calendars.

## 0. Status (2026-11-03)

**Implemented:**
- `scripts/refresh/run.py` + `scripts/refresh/jobs.json`. Three Eurostat jobs are enabled (`tour_occ_nin2m`, `tour_occ_nim` Greece, `tour_ce_omn12`); seven are listed but disabled, each with its reason.
- `scripts/verification/compute-data29-provisional.py`: the provisional estimate of section 3, with its backtest.

**Tested end to end on 2026-11-03:**
- All three jobs detected the publisher's update stamp, pulled, recorded sha256 in `data/manifests/refresh-2026-11-03.json`, and ran their candidate checks (all passed).
- A repeat run correctly found no change, and `--due` found no job due.

**Content hash (precaution).** The runner records the byte sha256 and a second **content hash** (parsed JSON, sorted keys), and compares the content with the verified raw file. If a publisher ever re-serialises unchanged data, it is then not mistaken for new data. *Correction (review round 2):* an earlier note claimed two identical Eurostat responses had different byte hashes. That was wrong: all three refreshed files are byte-identical to the verified files. No re-serialisation has been observed. All three were content-identical, so no promotion was needed.

**Hardened after review round 2:**
- a failed detection no longer counts as "checked" (retried on the next run);
- jobs waiting for review are written to `logs/refresh/ATTENTION.txt` and the run exits with code 3, so cron flags it;
- the manifest records the candidate outcome (`CANDIDATE_OK` / `CANDIDATE_FAILED`);
- candidate scripts verify they received the expected dataset.

Tested offline with a simulated publisher revision.

**Not automated (by design):** promotion. When content changes, the job state reads `PENDING REVIEW`. A person replaces the verified raw input, reruns the compute scripts and the folder check, and records the change. The scheduler is not yet installed in cron (owner action; command in `run.py`).

## 1. Rules the scheduler must keep

1. **Only locked indicators are scheduled.** `PROPOSAL`, `PARTIAL` and `UNVERIFIED` indicators are not.
2. **Change detection before download.** Poll cheap metadata first (Eurostat `updated`, HTTP `ETag`/`Last-Modified`, the publisher's file list). Download only when it changed.
3. **Raw data is immutable.** Every pull is saved under a new timestamped name in `data/raw/` (or `data/samples/`), with sha256, HTTP status and URL written to a dated manifest. Nothing is overwritten.
4. **Fail closed.** The run order is: pull → compute script → `build_dashboard.py` → `build_indicator_folders.py --check`. If any step fails, the previous master snapshot stays published and the owner is notified. Definition checks, such as the Data29 dashboard reconciliation, run on every refresh.
5. **No automatic status changes.** The scheduler never changes a status label and never triggers public alerts from unverified data (`AGENTS.md`).
6. **Provisional values are labelled.** A value estimated before the official release (section 3) carries `provisional` in its series label and is replaced when the official figure arrives.
7. **Read-only, bounded, within rate limits.** Credentials stay in `.env`; no scraping around access controls.

## 2. Source cadence and publication lag

`VERIFIED` = observed through the API on 2026-11-03; otherwise `ASSUMPTION` until checked.

| Source | Feeds | Granularity | Latest available (2026-11-03) | Lag / release pattern | Poll |
|---|---|---|---|---|---|
| Eurostat `tour_occ_nin2m` | Data29 (EL62 monthly), Data16/26/31 later | monthly by NUTS 2, **released per year** | 2025 complete (updated 2026-10-20); no 2026 months | about 10 months after year-end (2025 appeared Oct 2026) `VERIFIED` once; pattern `ASSUMPTION` | weekly |
| Eurostat `tour_occ_nim` | Data29 (Greece) | monthly, country | **2026-08** (updated 2026-10-30) | about 2 months `VERIFIED` | weekly |
| Eurostat `tour_ce_omn12` | Data19, Data29 platform series | monthly by NUTS 2 | **2026-03** (updated 2026-10-02) | released quarterly, about 6 months `VERIFIED` | weekly |
| Eurostat `tour_occ_nin2`, `tour_occ_arn2`, `tour_cap_nuts2` | Data16, 26, 27, 30, 31, 32, 33 | annual | 2025 | annual | monthly |
| EU Tourism Dashboard export | Data02/04/23/25/28 (+ reconciliation) | annual | 2024 release | annual | monthly |
| EEA bathing water | Data02, Data03 | annual season | 2024 | annual (spring) | monthly |
| CAMS European analysis (ADS) | Data15, Data01 proxy | hourly analysis | daily | about 1 day | daily |
| Open-Meteo | Data13, Data14 | hourly / daily | live | none | 30 min |
| OpenSky | Data06 | live | live | none; anonymous rate limits | 30 min |
| EMAS register, EU Ecolabel export | Data05 | snapshot | 2026-10-01 | on change | monthly |
| Fraport Greece monthly traffic PDFs | island monthly proxy (`PROPOSAL`) | monthly by airport | Aug 2025 checked | a few days after month-end, marked preliminary `ASSUMPTION` | monthly |

## 3. Current-year monthly data for EL62 (`PROPOSAL`, needs an owner decision and review)

Official EL62 monthly nights for year *Y* arrive only around the following autumn. To feed the twin during *Y*, a provisional monthly estimate can be built from the faster sources:

- **Base:** Greece monthly nights (`tour_occ_nim`, about 2 months lag) × EL62's share of Greece for the same month, averaged over the last available years from `tour_occ_nin2m`.
- **Cross-checks:** EL62 platform nights (`tour_ce_omn12`, quarterly) and Fraport monthly passengers at CFU/EFL/ZTH/PVK (a few days lag).
- **Replacement:** when `tour_occ_nin2m` publishes year *Y*, provisional values are replaced and the error is logged, so the method's accuracy is measured over time.

This is a methodology choice (D-level). Implemented 2026-11-03 as a `PROPOSAL` (owner request), pending review: `scripts/verification/compute-data29-provisional.py`, output in `data/curated/provisional-data29-el62-monthly-2026-08.json`. It is not merged into the master snapshot or the indicator folder.

**Rule, fixed before testing:**
- EL62's monthly share of Greek nights is averaged over all earlier published years, excluding 2020–2021 (COVID);
- that share is multiplied by Greece's nights for the month.

**Backtest** (rule applied to past years, compared with the published EL62 values):

| Year | Reference years | Error on annual nights | Mean error, 3 busiest months | Top-3-month share est. vs actual |
|---|---|---|---|---|
| 2023 | 2022 | −8.56 % | 8.87 % | 63.57 vs 63.81 |
| 2024 | 2022–23 | −4.29 % | 4.30 % | 63.72 vs 63.99 |
| 2025 | 2022–24 | −0.02 % | 2.25 % | 63.75 vs 63.91 |

Accuracy improves with more reference years. The seasonality measure is within 0.3 points in every test year. The estimates are negatively biased in 2023–24, consistent with the Ionian share of Greek nights rising after COVID.

**2026 estimates** (Greece data to August 2026): Jul 4.67 M, Aug 5.02 M EL62 nights. No annual seasonality figure is computed from a partial year.

## 4. Implementation sketch

- `scripts/refresh/jobs.json`: one job per source, with cadence, change-detection URL, pull command, downstream compute scripts and affected indicators. Generated from `indicators/source-indicator-map.json` (`cadence` field) and locked decisions.
- `scripts/refresh/run.py --job <id> | --due`: lock file, change detection, pull, manifest entry, compute, build, check, structured log (`logs/refresh/` is local-only), owner notification on failure.
- Trigger: `cron` on the workstation (WSL) for the pilot. In production, the platform's scheduler (the proposal names a cron job and Kafka) calls the same `run.py`, so the logic is identical in both.
- Each completed run writes a new dated master snapshot. The previous one stays until the check passes.
