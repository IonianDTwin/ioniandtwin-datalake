# API Verification Report

`VERIFIED` Live, bounded, read-only pull tests performed 2026-09-22T11:27Z. No credentials used; no access-control bypass. Evidence manifest: `data/manifests/source-verification-2026-09-22.json`.

## Summary

| Source | Access | Result | Maps to |
|---|---|---|---|
| Eurostat `tour_occ_nin2` (nights, NUTS2) | HTTPS API, public | `VERIFIED` HTTP 200 JSON | Data16, 26, 29, 31, 33 |
| Eurostat `tour_occ_arn2` (arrivals, NUTS2) | HTTPS API, public | `VERIFIED` HTTP 200 JSON | Data26 |
| Eurostat `tour_cap_nuts2` (bed-places, NUTS2) | HTTPS API, public | `VERIFIED` HTTP 200 JSON | Data27 |
| Open-Meteo (weather + UV) | HTTPS API, no key | `VERIFIED` HTTP 200 JSON | Data13, 14 (substitute) |
| OpenWeatherMap | HTTPS API, API key | `INACCESSIBLE` HTTP 401 (needs key) | Data13, 14 |
| Copernicus CDSE catalogue | HTTPS OData, public | `PARTIAL` HTTP 200; download needs token | Data01–03 (platform) |

## Verified pull tests

### 1. Eurostat — official tourism statistics (priority source)

`VERIFIED` The Eurostat SDMX 2.1 REST API returns clean JSON for the Ionian Islands (geo `EL62`, label **"Ionia Nisia"**, NUTS 2021) without any authentication.

Reproducible command: `scripts/verification/pull-eurostat-tourism.sh`

Sample values extracted from the responses (`geo=EL62`, `c_resid=TOTAL`, `nace_r2=I551-I553`, `unit=NR`):

- Nights spent (`tour_occ_nin2`): **2022 = 16,512,634**, **2023 = 19,762,799** → Data26
- Arrivals (`tour_occ_arn2`): **2022 = 2,785,360**, **2023 = 3,332,407** → Data26
- Bed-places (`tour_cap_nuts2`, `accomunit=BEDPL`): **2022 = 159,790**, **2023 = 155,968** → Data27
- Tourism intensity (`tour_occ_nin2`, `unit=P_THAB`, per thousand inhabitants): **2022 = 80,912.16**, **2023 = 97,705.53** → Data16
- Tourism density (`tour_occ_nin2`, `unit=P_KM2`, per km²): **2022 = 7,176.29**, **2023 = 8,588.79** → Data31
- Foreign tourist share (`tour_occ_nin2`, `c_resid=FOR`, `unit=PC_TOT`): **2022 = 93.72 %**, **2023 = 93.58 %** → Data33

`VERIFIED` The dataset exposes ready-made derived units (`P_THAB`, `P_KM2`, `PC_TOT`, `PCH_PRE`), which directly feed several proposal indicators without local aggregation.

### 2. Open-Meteo — weather + UV (no-key substitute)

`VERIFIED` `GET https://api.open-meteo.com/v1/forecast?...` returns `200` with `temperature_2m`, `relative_humidity_2m`, `apparent_temperature` (current) and `uv_index_max` (daily) for Corfu (39.62, 19.92), Europe/Athens timezone.

`DECISION` Open-Meteo is **not** named in the technical proposal or the deployed app (which list OpenWeatherMap and Meteo.gr). It is recorded here as a `PROPOSAL` no-key substitute so the weather/UV vertical slice is runnable today. It does **not** replace the proposal's named sources; it is an interim fallback that must be re-confirmed against project requirements before production use.

### 3. OpenWeatherMap — access constraint

`VERIFIED` `GET .../data/2.5/weather?lat=39.62&lon=19.92&appid=INVALID_TEST_KEY` returns **HTTP 401** with `{"cod":401,"message":"Invalid API key..."}`. This confirms OpenWeatherMap requires a valid API key. `INACCESSIBLE` until a key is supplied in the untracked `.env` and authorized.

### 4. Copernicus Data Space Ecosystem — platform reachable, download gated

`VERIFIED` `GET https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$top=1&$format=json` returns **HTTP 200** with Sentinel-3 product metadata. The public catalogue is reachable, but actual CAMS/CMEMS/Sentinel product download requires a registration token. Recorded `PARTIAL`.

## Evidence per test

Each pull records URL, method, parameters, response status, content type, `sha256` checksum, and timestamp in `data/manifests/source-verification-2026-09-22.json`. Retained bounded samples live in `data/samples/`; the GSTC PDF in `data/raw/`.

## Next

- Remaining credential-gated sources (OpenWeatherMap with a key, CAMS/CMEMS with a registration token, CDSE data download) are still to be pulled.
- Map monthly Eurostat datasets (`tour_occ_nim`-family) to Data29 seasonality in the next pull round.
