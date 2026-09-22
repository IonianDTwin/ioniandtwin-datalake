#!/usr/bin/env bash
# Download and checksum the GSTC Destination Criteria v2.0 (with SDGs) reference PDF.
# Public, read-only, bounded. No credentials required.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="$ROOT/data/raw"
mkdir -p "$OUT"

URL="https://www.gstc.org/wp-content/uploads/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf"
OUTFILE="${OUT}/GSTC-Destination-Criteria-v2.0-with-SDGs.pdf"

echo "== GSTC Destination Criteria v2.0 (with SDGs) =="
echo "   ${URL}"
code="$(curl -sS -L --max-time 120 -o "${OUTFILE}" -w '%{http_code}' "${URL}")"
echo "   HTTP ${code} -> ${OUTFILE}"
sha256sum "${OUTFILE}"
echo "   Verify header and page count with: python3 -c \"from pypdf import PdfReader; r=PdfReader('${OUTFILE}'); print(len(r.pages))\""
