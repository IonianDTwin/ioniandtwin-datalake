# Nights spent at tourist accommodation establishments by NUTS 2 region

**Resource:** https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nin2?format=JSON&geo=EL62&time=2022&time=2023

- Status: `200`
- Kind: `sdmx`
- Content-Type: `application/json`
- sha256: `46821a04c9061b605a1e324f9af55e87dba73856fd190dcb7e78ae8bc75f860d`
- Accessed at: `2026-09-22T11:27:00Z`

## Indicators pulled

### Data16 · Tourism intensity (nights/residents)
- **nights per 1000 residents**: `2022: 80,912.16 · 2023: 97,705.53`

### Data26 · Arrivals & overnight stays
- **overnight stays**: `2022: 16,512,634 · 2023: 19,762,799 nights`

### Data31 · Tourism density (nights/km²)
- **nights per km²**: `2022: 7,176.29 · 2023: 8,588.79`

### Data33 · Foreign tourist share (%)
- **foreign share**: `2022: 93.72 · 2023: 93.58 % of total`

## How to read this sample

This source returns a multi-dimensional cube; the pull kept all dimension combinations, so only a few rows are the headline Data01–Data34 values and the rest are sub-breakdowns or context.

**Dimensions:**

- `freq` — frequency: A (Annual)
- `c_resid` — country of residence (origin of the tourist): DOM (Domestic country), FOR (Foreign country), TOTAL (Total)
- `unit` — unit / measure: NR (Number), P_THAB (Per thousand inhabitants), P_KM2 (Per square kilometre), PC_TOT (Percentage of total), PCH_PRE (Percentage change on previous period)
- `nace_r2` — accommodation activity (NACE Rev.2): I551-I553 (Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks), I551 (Hotels and similar accommodation), I552_I553 (Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks), I552 (Holiday and other short-stay accommodation), I553 (Camping grounds, recreational vehicle parks and trailer parks)
- `geo` — region: EL62 (Ionia Nisia)
- `time` — year: 2022, 2023

**Rows mapped to indicators:**
- Data16 · Tourism intensity (nights/residents) — nights per 1000 residents [c_resid=TOTAL, unit=P_THAB, nace_r2=I551-I553]
- Data26 · Arrivals & overnight stays — overnight stays [c_resid=TOTAL, unit=NR, nace_r2=I551-I553]
- Data31 · Tourism density (nights/km²) — nights per km² [c_resid=TOTAL, unit=P_KM2, nace_r2=I551-I553]
- Data33 · Foreign tourist share (%) — foreign share [c_resid=FOR, unit=PC_TOT, nace_r2=I551-I553]

Unmapped rows are the same source broken down further (e.g. domestic vs foreign, hotels vs camping) or %-change context — they are not separate Data01–Data34 indicators.

## Full data (70 rows)

| freq | c_resid | unit | nace_r2 | geo | time | value | indicator | meaning |
|---|---|---|---|---|---|---|---|---|
| A · Annual | DOM · Domestic country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 771517 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 876675 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 1037478 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 1269009 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 250276 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 374721 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 265961 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 392334 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 15685 |  |  |
| A · Annual | DOM · Domestic country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 17613 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 30.83 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 13.63 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 26.08 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 22.32 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 14 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 49.72 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 14.07 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 47.52 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 15.17 |  |  |
| A · Annual | DOM · Domestic country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 12.29 |  |  |
| A · Annual | DOM · Domestic country | PC_TOT · Percentage of total | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 6.28 |  |  |
| A · Annual | DOM · Domestic country | PC_TOT · Percentage of total | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 6.42 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 11286712 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 12932665 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 15475156 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 18493790 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 4091957 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 5455319 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 4188444 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 5561125 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 96487 |  |  |
| A · Annual | FOR · Foreign country | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 105806 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 82.65 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 14.58 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 83.47 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 19.51 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 86.32 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 33.32 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 85.71 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 32.77 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 63.05 |  |  |
| A · Annual | FOR · Foreign country | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 9.66 |  |  |
| A · Annual | FOR · Foreign country | PC_TOT · Percentage of total | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 93.72 | Data33 · Foreign tourist share (%) | Share of nights spent by foreign (non-resident) tourists. (foreign share — % of total) |
| A · Annual | FOR · Foreign country | PC_TOT · Percentage of total | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 93.58 | Data33 · Foreign tourist share (%) | Share of nights spent by foreign (non-resident) tourists. (foreign share — % of total) |
| A · Annual | TOTAL · Total | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 12058229 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 13809340 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 16512634 | Data26 · Arrivals & overnight stays | Total nights spent at tourist accommodation. (overnight stays — nights) |
| A · Annual | TOTAL · Total | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 19762799 | Data26 · Arrivals & overnight stays | Total nights spent at tourist accommodation. (overnight stays — nights) |
| A · Annual | TOTAL · Total | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 4342233 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 5830040 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 4454405 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 5953459 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 112172 |  |  |
| A · Annual | TOTAL · Total | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 123419 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 78.14 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 14.52 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 78.37 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 19.68 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 79.75 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 34.26 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 78.99 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 33.65 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 54.1 |  |  |
| A · Annual | TOTAL · Total | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 10.03 |  |  |
| A · Annual | TOTAL · Total | PC_TOT · Percentage of total | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 100 |  |  |
| A · Annual | TOTAL · Total | PC_TOT · Percentage of total | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 100 |  |  |
| A · Annual | TOTAL · Total | P_KM2 · Per square kilometre | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 7176.29 | Data31 · Tourism density (nights/km²) | Overnight stays per square kilometre (tourism density). (nights per km²) |
| A · Annual | TOTAL · Total | P_KM2 · Per square kilometre | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 8588.79 | Data31 · Tourism density (nights/km²) | Overnight stays per square kilometre (tourism density). (nights per km²) |
| A · Annual | TOTAL · Total | P_THAB · Per thousand inhabitants | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 80912.16 | Data16 · Tourism intensity (nights/residents) | Overnight stays per thousand residents (tourism intensity). (nights per 1000 residents) |
| A · Annual | TOTAL · Total | P_THAB · Per thousand inhabitants | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 97705.53 | Data16 · Tourism intensity (nights/residents) | Overnight stays per thousand residents (tourism intensity). (nights per 1000 residents) |
