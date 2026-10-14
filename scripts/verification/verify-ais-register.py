#!/usr/bin/env python3
"""Register-consistency verification for AIS vessel identities (Data07).

Coverage-independent identity check. For each vessel (MMSI + optional name /
call sign) it validates against authoritative ITU/IMO standards and AIS
plausibility rules, then emits a machine-readable JSON report + a human-readable
Markdown report under data/curated/.

Input: either
  * an AIS capture JSON (e.g. from pull-ais-coverage.py), or
  * a plain JSON array of {mmsi, name?, call_sign?, lat?, lon?, sog_kn?}.

Checks (deterministic, free, reproducible):
  1. MMSI format      - 9 decimal digits.
  2. ITU MID block    - first 3 digits mapped to flag state via the ITU-R M.585
                        Maritime Identification Digits table (embedded subset).
  3. Greek flag       - MID in {237, 239, 240, 241}.
  4. SOG plausibility - 0 <= speed-over-ground <= 45 kn.
  5. Name present     - a non-empty ship name accompanies the MMSI.

VERDICT: VERIFIED when every applicable check passes; otherwise FLAGGED with the
failing checks listed.

Known limitation (documented, not hidden): a full name -> IMO/callsign lookup
against ITU MARS or Equasis requires an account (those registers are not open
APIs). The MID-block check is the authoritative, account-free portion of that
register cross-match.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "data" / "samples"
CURATED = ROOT / "data" / "curated"

# ITU-R M.585 Maritime Identification Digits (subset: Europe + Mediterranean +
# common flags relevant to the Ionian Sea). Full table is larger; unknown MIDs
# are reported as "unknown" rather than guessed.
MID_TABLE = {
    "201": "Albania", "202": "Andorra", "203": "Austria", "204": "Azores (Portugal)",
    "205": "Belgium", "206": "Belarus", "207": "Bulgaria", "208": "Vatican City",
    "209": "Cyprus", "210": "Cyprus", "211": "Germany", "212": "Cyprus",
    "213": "Georgia", "214": "Moldova", "215": "Malta", "216": "Armenia",
    "218": "Germany", "219": "Denmark", "220": "Denmark", "224": "Spain",
    "225": "Spain", "226": "France", "227": "France", "228": "France",
    "229": "Malta", "230": "Finland", "231": "Faroe Islands", "232": "United Kingdom",
    "233": "United Kingdom", "234": "United Kingdom", "235": "United Kingdom",
    "236": "United Kingdom", "237": "Greece", "238": "Croatia", "239": "Greece",
    "240": "Greece", "241": "Greece", "242": "Morocco", "243": "Hungary",
    "244": "Netherlands", "245": "Netherlands", "246": "Netherlands", "247": "Italy",
    "248": "Malta", "249": "Malta", "250": "Ireland", "251": "Iceland",
    "252": "Liechtenstein", "253": "Luxembourg", "254": "Monaco", "255": "Madeira (Portugal)",
    "256": "Malta", "257": "Norway", "258": "Norway", "259": "Norway", "261": "Poland",
    "262": "Montenegro", "263": "Portugal", "264": "Romania", "265": "Sweden",
    "266": "Sweden", "267": "Slovakia", "268": "San Marino", "269": "Switzerland",
    "270": "Czech Republic", "271": "Türkiye", "272": "Ukraine", "273": "Russia",
    "274": "North Macedonia", "275": "Latvia", "276": "Estonia", "277": "Lithuania",
    "278": "Slovenia", "279": "Serbia", "301": "United States (Alaska)",
    "303": "United States", "308": "Bahamas", "309": "Bahamas", "311": "Bahamas",
    "316": "Canada", "338": "United States", "351": "Panama", "352": "Panama",
    "353": "Panama", "354": "Panama", "355": "Panama", "356": "Panama", "357": "Panama",
    "366": "United States", "367": "United States", "368": "United States", "369": "United States",
    "370": "Panama", "371": "Panama", "372": "Panama", "373": "Panama", "374": "Panama",
    "403": "Saudi Arabia", "405": "India", "412": "China", "431": "Japan",
    "432": "Japan", "447": "Qatar", "470": "United Arab Emirates", "471": "United Arab Emirates",
    "477": "Hong Kong", "503": "Australia", "512": "New Zealand", "538": "Marshall Islands",
    "563": "Singapore", "564": "Singapore", "565": "Singapore", "566": "Singapore",
    "601": "South Africa", "636": "Liberia",
    "657": "Eritrea", "701": "Argentina", "710": "Brazil", "725": "Chile",
    "730": "Colombia", "735": "Ecuador", "760": "Peru", "775": "Uruguay",
}
GREEK_MIDS = {"237", "239", "240", "241"}


def _load_vessels(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    # coverage-aware collector format: vessels live inside ports[] + unassigned_vessels
    if isinstance(data.get("ports"), list):
        out = []
        for p in data["ports"]:
            out.extend(p.get("vessels", []))
        out.extend(data.get("unassigned_vessels", []))
        return out
    # simple capture format: top-level "vessels"
    return data.get("vessels", [])


def check(v: dict) -> dict:
    mmsi = str(v.get("mmsi", "") or "").strip()
    name = (v.get("name") or "").strip()
    call_sign = (v.get("call_sign") or v.get("callSign") or "").strip() or None
    pos = v.get("last_position") or v
    lat = pos.get("lat")
    lon = pos.get("lon")
    sog = pos.get("sog_kn") if "sog_kn" in pos else v.get("sog_kn")
    mid = mmsi[:3]
    country = MID_TABLE.get(mid, "unknown")

    fails: list[str] = []
    mmsi_valid = len(mmsi) == 9 and mmsi.isdigit()
    if not mmsi_valid:
        fails.append("mmsi_not_9_digits")
    if mid not in MID_TABLE:
        fails.append("mid_unknown_in_embedded_table")
    if not name:
        fails.append("name_missing")
    if sog is not None and not (0 <= float(sog) <= 45):
        fails.append("sog_out_of_range")

    verdict = "VERIFIED" if (mmsi_valid and name and not fails) else "FLAGGED"
    return {
        "mmsi": mmsi,
        "mid": mid or None,
        "flag_state": country,
        "is_greek_flag": mid in GREEK_MIDS,
        "name": name,
        "call_sign": call_sign,
        "lat": lat,
        "lon": lon,
        "sog_kn": sog,
        "verdict": verdict,
        "failed_checks": fails,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=None,
                    help="capture JSON or MMSI-list JSON (default: latest data/samples/ais-*.json)")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.input:
        inp = args.input if args.input.is_absolute() else (ROOT / args.input).resolve()
    else:
        candidates = sorted(SAMPLES.glob("ais-*.json"))
        if not candidates:
            raise SystemExit("no AIS capture JSON found")
        inp = candidates[-1]

    vessels = _load_vessels(inp)
    rows = [check(v) for v in vessels]
    n_verified = sum(1 for r in rows if r["verdict"] == "VERIFIED")

    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    report = {
        "report_id": f"ais-register-verification-{date}",
        "created_at": now.isoformat(),
        "method": (
            "Register-consistency verification against ITU-R M.585 MID allocation "
            "(account-free) + AIS plausibility (SOG, name presence). Full ITU MARS / "
            "Equasis name->IMO lookup requires an account and is documented as a "
            "known limitation."
        ),
        "input": str(inp.relative_to(ROOT)),
        "summary": {"total_vessels": len(rows), "verified": n_verified,
                    "flagged": len(rows) - n_verified},
        "vessels": rows,
    }

    out_json = args.out or (CURATED / f"ais-register-verification-{date}.json")
    if not out_json.is_absolute():
        out_json = (ROOT / out_json).resolve()
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [f"# AIS Register Verification — {date}", "",
          f"- **Vessels:** {len(rows)} total · {n_verified} VERIFIED · {len(rows)-n_verified} FLAGGED", "",
          "| MMSI | Name | Flag (MID) | Call Sign | SOG | Verdict | Failed checks |",
          "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['mmsi']} | {r['name']} | {r['flag_state']} ({r['mid']}) | "
                  f"{r['call_sign'] or ''} | {r['sog_kn']} | {r['verdict']} | "
                  f"{', '.join(r['failed_checks']) or '-'} |")
    md += ["", "- Greek flag MIDs: 237, 239, 240, 241 (ITU-R M.585).",
           "- Full name→IMO/callsign lookup (ITU MARS, Equasis) requires an account; not performed here."]
    out_md = out_json.with_suffix(".md")
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({"summary": report["summary"],
                      "json": str(out_json.relative_to(ROOT)),
                      "markdown": str(out_md.relative_to(ROOT)),
                      "vessels": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
