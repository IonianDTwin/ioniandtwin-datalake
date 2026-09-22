#!/usr/bin/env bash
# Pull-test Eurostat tourism statistics for the Ionian Islands (NUTS 2 = EL62, "Ionia Nisia").
# Public, read-only, bounded. No credentials required.
# Writes raw JSON samples to data/samples/ and renders a self-contained visual report
# (HTML + Markdown summary) for each, via render_pull_reports.py.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/data/samples"
RENDER="$ROOT/scripts/verification/render_pull_reports.py"
mkdir -p "$OUT"

BASE="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
GEO="EL62"          # Ionia Nisia (NUTS 2021)
YEARS="time=2022&time=2023"

declare -a DATASETS=(
  "tour_occ_nin2:Nights spent (NUTS 2):Eurostat_tour_occ_nin2"
  "tour_occ_arn2:Arrivals (NUTS 2):Eurostat_tour_occ_arn2"
  "tour_cap_nuts2:Capacity - bed-places (NUTS 2):Eurostat_tour_cap_nuts2"
)

for entry in "${DATASETS[@]}"; do
  ds="${entry%%:*}"
  rest="${entry#*:}"
  label="${rest%%:*}"
  skey="${rest#*:}"
  url="${BASE}/${ds}?format=JSON&geo=${GEO}&${YEARS}"
  out="${OUT}/eurostat-${ds}-${GEO}-2022-2023.json"
  echo "== ${label} (${ds}) =="
  echo "   ${url}"
  code="$(curl -sS --max-time 40 -o "${out}" -w '%{http_code}' "${url}")"
  echo "   HTTP ${code} -> ${out}"
  sha256sum "${out}"
  python3 "${RENDER}" --json "${out}" --name "Eurostat — ${label} (${ds})" \
    --url "${url}" --status "${code}" --content-type "application/json" \
    --source-key "${skey}"
done

echo "done."
