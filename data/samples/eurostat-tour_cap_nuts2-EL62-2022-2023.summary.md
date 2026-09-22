# Establishments, bedrooms and bed-places in tourist accommodation, by NUTS 2 region

**Resource:** https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_cap_nuts2?format=JSON&geo=EL62&time=2022&time=2023

- Status: `200`
- Kind: `sdmx`
- Content-Type: `application/json`
- sha256: `90d5c376d69fad77a36e7d077cc63545a4ba0e68afc2e8017578418395495ae3`
- Accessed at: `2026-09-22T11:27:00Z`

## Indicators pulled

### Data27 · Tourism capacity (beds)
- **bed-places**: `2022: 159,790 · 2023: 155,968`

## How to read this sample

This source returns a multi-dimensional cube; the pull kept all dimension combinations, so only a few rows are the headline Data01–Data34 values and the rest are sub-breakdowns or context.

**Dimensions:**

- `freq` — frequency: A (Annual)
- `accomunit` — capacity measure (establishments / bedrooms / bed-places): ESTBL (Establishments), BEDRM (Bedrooms), BEDPL (Bedplaces)
- `unit` — unit / measure: NR (Number), PCH_PRE (Percentage change on previous period)
- `nace_r2` — accommodation activity (NACE Rev.2): I551-I553 (Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks), I551 (Hotels and similar accommodation), I552_I553 (Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks), I552 (Holiday and other short-stay accommodation), I553 (Camping grounds, recreational vehicle parks and trailer parks)
- `geo` — region: EL62 (Ionia Nisia)
- `time` — year: 2022, 2023

**Rows mapped to indicators:**
- Data27 · Tourism capacity (beds) — bed-places [accomunit=BEDPL, unit=NR, nace_r2=I551-I553]

Unmapped rows are the same source broken down further (e.g. domestic vs foreign, hotels vs camping) or %-change context — they are not separate Data01–Data34 indicators.

## Full data (44 rows)

| freq | accomunit | unit | nace_r2 | geo | time | value | indicator | meaning |
|---|---|---|---|---|---|---|---|---|
| A · Annual | BEDPL · Bedplaces | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 106653 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 107952 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 159790 | Data27 · Tourism capacity (beds) | Number of bed-places in tourist accommodation (capacity). (bed-places) |
| A · Annual | BEDPL · Bedplaces | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 155968 | Data27 · Tourism capacity (beds) | Number of bed-places in tourist accommodation (capacity). (bed-places) |
| A · Annual | BEDPL · Bedplaces | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 47944 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 44734 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 53137 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 48016 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 5193 |  |  |
| A · Annual | BEDPL · Bedplaces | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 3282 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 36.1 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 1.22 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 24.8 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | -2.39 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 3.3 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | -6.7 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 6.97 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | -9.64 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 59.15 |  |  |
| A · Annual | BEDPL · Bedplaces | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | -36.8 |  |  |
| A · Annual | BEDRM · Bedrooms | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 53853 |  |  |
| A · Annual | BEDRM · Bedrooms | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 54068 |  |  |
| A · Annual | BEDRM · Bedrooms | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 36.11 |  |  |
| A · Annual | BEDRM · Bedrooms | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 0.4 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 1012 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 989 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 4853 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 4527 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 3820 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | 3518 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 3841 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 3538 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 21 |  |  |
| A · Annual | ESTBL · Establishments | NR · Number | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | 20 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 53.1 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I551 · Hotels and similar accommodation | EL62 · Ionia Nisia | 2023 · 2023 | -2.27 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 33.18 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I551-I553 · Hotels; holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | -6.72 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2022 · 2022 | 28.53 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I552 · Holiday and other short-stay accommodation | EL62 · Ionia Nisia | 2023 · 2023 | -7.91 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 28.76 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I552_I553 · Holiday and other short-stay accommodation; camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | -7.89 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2022 · 2022 | 90.91 |  |  |
| A · Annual | ESTBL · Establishments | PCH_PRE · Percentage change on previous period | I553 · Camping grounds, recreational vehicle parks and trailer parks | EL62 · Ionia Nisia | 2023 · 2023 | -4.76 |  |  |
