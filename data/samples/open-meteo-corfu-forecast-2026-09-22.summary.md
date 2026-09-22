# Open-Meteo weather forecast (temperature, humidity, UV index)

**Resource:** https://api.open-meteo.com/v1/forecast?latitude=39.62&longitude=19.92&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1

- Status: `200`
- Kind: `openmeteo`
- Content-Type: `application/json; charset=utf-8`
- sha256: `e16e6108febd130fbab834a943df510a3d982714d4d7e18a7f01ac5e50f93e23`
- Accessed at: `2026-09-22T11:27:00Z`

## Indicators pulled

### Data13 · Weather conditions (temp, rain, …)
- **air temperature**: `26.5 °C`
- **relative humidity**: `57 %`
- **apparent (feels-like) temperature**: `28.8 °C`

### Data14 · High UV and protection
- **max UV index**: `5.9`


## Full data (5 rows)

| block | field | unit | time | value | indicator | meaning |
|---|---|---|---|---|---|---|
| current | interval | seconds | 2026-09-22T14:15 | 900 |  |  |
| current | temperature_2m | °C | 2026-09-22T14:15 | 26.5 | Data13 · Weather conditions (temp, rain, …) | Current air temperature at the location. (air temperature — °C) |
| current | relative_humidity_2m | % | 2026-09-22T14:15 | 57 | Data13 · Weather conditions (temp, rain, …) | Current relative humidity at 2 m. (relative humidity — %) |
| current | apparent_temperature | °C | 2026-09-22T14:15 | 28.8 | Data13 · Weather conditions (temp, rain, …) | Perceived temperature. (apparent (feels-like) temperature — °C) |
| daily | uv_index_max |  | 2026-09-22 | 5.9 | Data14 · High UV and protection | Maximum daily UV index; used for sun-protection guidance. (max UV index) |
