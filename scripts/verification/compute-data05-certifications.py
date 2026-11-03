#!/usr/bin/env python3
"""Emit Data05 (EMAS / EU Ecolabel) observations from the retained Greece extracts.

Lineage:
  data/samples/emas-register-greece-2026-10-02.json        (37 Greek EMAS registrations; email/phone redacted)
  data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json (Greek EU Ecolabel licences, by product group)
    --( this script )--> data/curated/observations-data05-certifications-2026-10-01.json / .csv

The EL62 counts are re-derived here, not copied from the extract summaries:
  * EMAS: a Greek registration is counted for EL62 when its postal code starts with an Ionian prefix
    (Corfu 49, Kefalonia/Ithaki 28, Zakynthos 29, Lefkada 31) or its city/name matches an Ionian
    place name (Greek or Latin). The script fails if this disagrees with the extract's own
    "ionian_islands_el62_records".
  * EU Ecolabel: the extract keeps Greece-level counts by product group. Tourist-accommodation
    licences in EL62 are bounded above by Greek tourist-accommodation licences; when that is 0,
    EL62 is 0. Licence addresses were not retained, so a non-zero Greek count could not be
    attributed to EL62 from this extract (the script would then fail and ask for a re-pull).

Observations: register snapshots at their access time (instant). Counts of certified
organisations are polarity "positive".
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EMAS = ROOT / "data/samples/emas-register-greece-2026-10-02.json"
ECO = ROOT / "data/samples/eu-ecolabel-catalogue-greece-2026-10-02.json"
OUT = ROOT / "data/curated/observations-data05-certifications-2026-10-01.json"
ACCESSED = "2026-10-01T22:12:00+00:00"   # manifest source-verification-2026-10-02, both registers
# Greek postal-code prefixes of the Ionian regional units (Hellenic Post / ELTA numbering):
# 49xxx Kerkyra, 28xxx Kefallinia & Ithaki, 29xxx Zakynthos, 31xxx Lefkada. `ASSUMPTION`: that
# no mainland area uses 31xxx (neighbouring Aetolia-Acarnania is 30xxx, Preveza 48xxx); confirm
# against the ELTA list before using this rule on a register with non-zero Ionian candidates.
IONIAN_POSTAL = ("49", "28", "29", "31")
IONIAN_NAMES = re.compile(r"kerkyr|kerkir|corfu|zakyn|zante|kefal|cephal|argostol|lixour|lefk|ithak|paxo|"
                          r"κέρκυρ|κερκυρ|ζάκυνθ|ζακυνθ|κεφαλ|αργοστ|λευκ|ιθάκ|ιθακ|παξ", re.I)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    emas = json.loads(EMAS.read_text(encoding="utf-8"))
    recs = emas["greece_sample"]
    hits = [r for r in recs
            if re.sub(r"\D", "", str(r.get("postalCode", "")))[:2] in IONIAN_POSTAL
            or IONIAN_NAMES.search(f"{r.get('city', '')} {r.get('organisationName', '')}")]
    emas_el62 = len(hits)
    print(f"EMAS: {len(recs)} Greek registrations, {emas_el62} matched to EL62 {[r['registrationNumber'] for r in hits]}")
    if len(recs) != emas["greece_records"] or emas_el62 != emas["ionian_islands_el62_records"]:
        print("FAIL: re-derived EMAS counts disagree with the extract", file=sys.stderr)
        return 1

    eco = json.loads(ECO.read_text(encoding="utf-8"))
    gr_tourist = eco["tourist_accommodation_group"]["greece"]
    gr_total = eco["greece_licences"]
    if sum(eco["greece_group_breakdown"].values()) != gr_total:
        print("FAIL: Ecolabel group breakdown does not sum to the Greek total", file=sys.stderr)
        return 1
    if gr_tourist != 0:
        print("FAIL: Greek tourist-accommodation licences > 0; EL62 cannot be attributed from this extract. Re-pull.", file=sys.stderr)
        return 1
    eco_el62 = 0
    print(f"EU Ecolabel: {gr_total} Greek licences, {gr_tourist} tourist accommodation in Greece -> EL62 = {eco_el62}")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def ob(oid, label, src, level, code, value, unit, raw, url, formula, manifest):
        return {"observation_id": oid, "indicator_id": "Data05", "indicator_name": "EMAS / EU Ecolabel",
                "series_label": label, "source_id": src, "observed_at": ACCESSED, "observed_period_end": None,
                "temporal_granularity": "instant", "ingested_at": now,
                "spatial_ref": {"level": level, "code": code, "geometry": None},
                "value": value, "unit": unit, "polarity": "positive",
                "provenance": {"raw_checksum_sha256": sha256(raw), "raw_manifest": manifest,
                               "access_method": "derived", "request_url": url,
                               "request_params": {"formula": formula}}}

    obs = [
        ob("EMAS_register_REST:Data05:emas_registrations:EL62:2026-10-01", "EMAS-registered organisations",
           "EMAS_register_REST", "NUTS2", "EL62", emas_el62, "organisations", EMAS, emas["url"],
           "count of Greek registrations with an Ionian postal prefix (49/28/29/31) or Ionian place name",
           "source-verification-2026-10-02"),
        ob("EMAS_register_REST:Data05:emas_registrations:EL:2026-10-01", "EMAS-registered organisations",
           "EMAS_register_REST", "country", "EL", len(recs), "organisations", EMAS, emas["url"],
           "count of registrations with organisationCountryName = Greece", "source-verification-2026-10-02"),
        ob("EU_Ecolabel_catalogue_CSV:Data05:ecolabel_tourist_accommodation:EL62:2026-10-01",
           "EU Ecolabel licences, tourist accommodation group", "EU_Ecolabel_catalogue_CSV", "NUTS2", "EL62",
           eco_el62, "licences", ECO, eco["url"],
           "bounded by Greek tourist-accommodation licences (= 0)", "source-verification-2026-11-03"),
        ob("EU_Ecolabel_catalogue_CSV:Data05:ecolabel_tourist_accommodation:EL:2026-10-01",
           "EU Ecolabel licences, tourist accommodation group", "EU_Ecolabel_catalogue_CSV", "country", "EL",
           gr_tourist, "licences", ECO, eco["url"],
           "count of Greek licences in group 'Tourist accommodation'", "source-verification-2026-11-03"),
    ]
    print(f"{len(obs)} observations")
    if args.check:
        return 0
    OUT.write_text(json.dumps(obs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with OUT.with_suffix(".csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["observation_id", "spatial_code", "value", "unit"])
        for o in obs:
            w.writerow([o["observation_id"], o["spatial_ref"]["code"], o["value"], o["unit"]])
    print(f"wrote {OUT.relative_to(ROOT)} (+ .csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
