# Arrivals at tourist accommodation establishments by NUTS 2 region

**Resource:** https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_arn2?format=JSON&geo=EL62&time=2022&time=2023

- Status: `200`
- Kind: `sdmx`
- Content-Type: `application/json`
- sha256: `0855dc90f5b85a3f4251318da56456cec0585fe55843caf434f26c499f72b724`
- Accessed at: `2026-09-22T11:27:00Z`

## Indicators pulled

### Data26 · Arrivals & overnight stays
- **arrivals**: `2022: 2,785,360 · 2023: 3,332,407`

## How to read this sample

This source returns a multi-dimensional cube; the pull kept all dimension combinations, so only a few rows are the headline Data01–Data34 values and the rest are sub-breakdowns or context.

**Dimensions:**

- `freq` — frequency: A (Annual)
- `c_resid` — country of residence (origin of the tourist): DOM (Domestic country), FOR (Foreign country), TOTAL (Total)
- `unit` — unit / measure: NR (Number), PCH_PRE (Percentage change on previous period)
- `nace_r2` — accommodation activity (NACE Rev.2): I551-I553 (Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks), I551 (Hotels and similar accommodation), I552_I553 (Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks), I552 (Holiday and other short-stay accommodation), I553 (Camping grounds, recreational vehicle parks and trailer parks)
- `geo` — region: EL62 (Ionia Nisia)
- `time` — year: 2022, 2023

**Rows mapped to indicators:**
- Data26 · Arrivals & overnight stays — arrivals [c_resid=TOTAL, unit=NR, nace_r2=I551-I553]

Unmapped rows are the same source broken down further (e.g. domestic vs foreign, hotels vs camping) or %-change context — they are not separate Data01–Data34 indicators.

## Full data (60 rows)

| freq | c_resid | unit | nace_r2 | geo | time | value | indicator | meaning |
|---|---|---|---|---|---|---|---|---|
| A · Annual | DOM · Domestic country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 265106 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 301667 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 305361 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 362918 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 36818 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 57424 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 40255 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 61251 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 3437 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 3827 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 45.19 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 13.79 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 40.35 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 18.85 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 14.4 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 55.97 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 15.08 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 52.16 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 22.93 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 11.35 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 1864203 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 2243247 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 2479999 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 2969489 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 596336 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 704223 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 615796 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 726242 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 19460 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 22019 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 63.13 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 20.33 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 66.84 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 19.74 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 79.72 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 18.09 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 79.17 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 17.94 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 63.83 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 13.15 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 2129309 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 2544914 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 2785360 | Data26 · Arrivals & overnight stays | Total arrivals at tourist accommodation. (arrivals) |
| A · Annual | TOTAL · Total | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 3332407 | Data26 · Arrivals & overnight stays | Total arrivals at tourist accommodation. (arrivals) |
| A · Annual | TOTAL · Total | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 633154 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 761647 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 656051 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 787493 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 22897 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 25846 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 60.66 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 19.52 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 63.45 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 19.64 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 73.95 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 20.29 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 73.25 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 20.04 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 56.04 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 12.88 |  |  |
