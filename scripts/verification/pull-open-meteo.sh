#!/usr/bin/env bash
# Pull-test weather/UV (no-key substitute: Open-Meteo) for the Ionian Islands.
# Public, read-only, bounded. No credentials required.
# Writes raw JSON to data/samples/ and renders a self-contained visual report.
# NOTE: the proposal/app name OpenWeatherMap and Meteo.gr. Open-Meteo is used here
# only as a no-key fallback for the vertical slice (documented in sources/).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/data/samples"
RENDER="$ROOT/scripts/verification/render_pull_reports.py"
mkdir -p "$OUT"

# Corfu (Kerkyra) representative coordinates for the Ionian Islands.
LAT="39.62"
LON="19.92"
URL="https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature&daily=uv_index_max&timezone=Europe%2FAthens&forecast_days=1"
STAMP="$(date -u +%Y-%m-%d)"
OUTFILE="${OUT}/open-meteo-corfu-forecast-${STAMP}.json"

echo "== Open-Meteo forecast + UV (Corfu) =="
echo "   ${URL}"
code="$(curl -sS --max-time 40 -o "${OUTFILE}" -w '%{http_code}' "${URL}")"
echo "   HTTP ${code} -> ${OUTFILE}"
sha256sum "${OUTFILE}"
python3 "${RENDER}" --json "${OUTFILE}" --name "Open-Meteo — Corfu weather + UV" \
  --url "${URL}" --status "${code}" --content-type "application/json; charset=utf-8" \
  --source-key "OpenMeteo_forecast"
