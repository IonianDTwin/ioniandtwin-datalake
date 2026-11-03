#!/usr/bin/env python3
"""IonianDTwin refresh runner (design: pipelines/refresh-scheduler.md).

For each enabled job in scripts/refresh/jobs.json:
  1. DETECT  - cheap metadata request; compare the publisher's "updated" stamp with local state.
  2. PULL    - only if changed: full download, saved under a NEW timestamped name in data/raw/refresh/
               (exclusive create, never overwrites), sha256 recorded in data/manifests/refresh-<date>.json.
  3. CANDIDATE - run the job's compute scripts in --check mode against the new file. They reconcile
               definitions and recompute values but write nothing.
  4. RECORD  - state in logs/refresh/state.json, one JSON line per event in logs/refresh/refresh-<YYYY-MM>.log.

It never writes to data/curated or data/indicators and never changes a status label. Promoting a
candidate (replacing the verified raw input, rebuilding the master, folder check) is a reviewed,
manual step. Live sources may later get an automatic promotion path once their definitions are locked.

Usage:
  python3 scripts/refresh/run.py --list
  python3 scripts/refresh/run.py --due              # every enabled job whose cadence interval has passed
  python3 scripts/refresh/run.py --job <id>         # one job now
  python3 scripts/refresh/run.py --job <id> --detect-only
Exit codes: 0 = ok or nothing to do; 1 = a job failed; 2 = guard/lock/config problem;
            3 = new data waiting for review (PENDING REVIEW / BLOCKED; listed in logs/refresh/ATTENTION.txt).

Cron example (WSL; the cron service must be running):
  0 6 * * * cd <repo-root> && .venv/bin/python -I scripts/refresh/run.py --due >> logs/refresh/cron.log 2>&1
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
JOBS = ROOT / "scripts/refresh/jobs.json"
RAW_DIR = ROOT / "data/raw/refresh"
MANIFEST_DIR = ROOT / "data/manifests"
LOG_DIR = ROOT / "logs/refresh"
STATE = LOG_DIR / "state.json"
PY = ROOT / ".venv/bin/python"
INTERVAL = {"30min": timedelta(minutes=30), "daily": timedelta(days=1), "weekly": timedelta(days=7),
            "monthly": timedelta(days=30)}
TIMEOUT = 60
MAX_BYTES = 50 * 1024 * 1024          # bounded pulls only
USER_AGENT = "IonianDTwin-refresh/0.1 (read-only research pull)"


def now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(t: datetime) -> str:
    return t.strftime("%Y%m%dT%H%M%SZ")


def log(event: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    event = {"at": now().strftime("%Y-%m-%dT%H:%M:%SZ"), **event}
    with (LOG_DIR / f"refresh-{now():%Y-%m}.log").open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps(event, ensure_ascii=False))


def guard() -> bool:
    r = subprocess.run([str(ROOT / "scripts/guard-paths.sh")], cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0 and "PASS" in r.stdout


def inside(path: Path) -> Path:
    path = path.resolve()
    if ROOT not in path.parents and path != ROOT:
        raise RuntimeError(f"refusing to write outside the workspace: {path}")
    return path


def fetch(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        body = r.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise RuntimeError(f"response larger than {MAX_BYTES} bytes; refusing (bounded pulls only)")
        return r.status, r.headers.get("Content-Type", ""), body


def content_sha256(doc: dict) -> str:
    """Hash of the parsed JSON with sorted keys. Eurostat can serialise the same content with
    different key order, so the byte sha256 (kept as evidence) may change while the data does not.
    This hash shows whether the content itself changed."""
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save_state(state: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(STATE)


def update_manifest_entry(manifest_stem: str, sample_path: str, fields: dict) -> None:
    path = inside(MANIFEST_DIR / f"{manifest_stem}.json")
    doc = json.loads(path.read_text(encoding="utf-8"))
    for e in doc["evidence"]:
        if e.get("sample_path") == sample_path:
            e.update(fields)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_manifest(entry: dict) -> str:
    path = inside(MANIFEST_DIR / f"refresh-{now():%Y-%m-%d}.json")
    doc = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "manifest_id": path.stem, "created_at": now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": "Automated refresh pulls by scripts/refresh/run.py (candidates; not yet promoted).", "evidence": []}
    doc["evidence"].append(entry)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path.stem


def run_job(job: dict, state: dict, detect_only: bool) -> bool:
    jid = job["id"]
    st = state.setdefault(jid, {})
    st["last_attempt"] = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if "last_content_sha256" not in st and job.get("verified_raw"):
        # Baseline = the content of the raw file the current verified data was built from.
        st["last_content_sha256"] = content_sha256(json.loads((ROOT / job["verified_raw"]).read_text(encoding="utf-8")))
    status, ctype, body = fetch(job["detect"]["url"])
    if status != 200:
        log({"job": jid, "step": "detect", "result": "FAIL", "http": status})
        return False
    updated = json.loads(body).get("updated")
    # Only a completed detection counts as "checked"; a failed attempt is retried on the next run (review F5).
    st["last_checked"] = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    changed = updated != st.get("publisher_updated")
    log({"job": jid, "step": "detect", "publisher_updated": updated, "previous": st.get("publisher_updated"), "changed": changed})
    if not changed or detect_only:
        return True

    t = now()
    status, ctype, body = fetch(job["pull"]["url"])
    if status != 200 or "json" not in ctype:
        log({"job": jid, "step": "pull", "result": "FAIL", "http": status, "content_type": ctype})
        return False
    doc = json.loads(body)
    if not doc.get("value"):
        log({"job": jid, "step": "pull", "result": "FAIL", "http": status, "content_type": ctype})
        return False
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw = inside(RAW_DIR / f"{job['pull']['file_prefix']}-{stamp(t)}.json")
    with raw.open("xb") as f:                    # exclusive create: never overwrite raw evidence
        f.write(body)
    sha = hashlib.sha256(body).hexdigest()
    csha = content_sha256(doc)
    content_changed = csha != st.get("last_content_sha256")
    manifest = append_manifest({
        "source_id": job["source_id"], "url": job["pull"]["url"], "method": "GET (scripts/refresh/run.py)",
        "access_type": "api", "response_status": status, "content_type": ctype, "checksum_sha256": sha,
        "size_bytes": len(body), "accessed_at": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "authentication": "none",
        "sample_path": str(raw.relative_to(ROOT)), "publisher_updated": updated, "content_sha256": csha,
        "verification_status": "CANDIDATE", "note": f"Refresh job {jid}; not promoted."})
    log({"job": jid, "step": "pull", "result": "OK", "file": str(raw.relative_to(ROOT)), "sha256": sha,
         "content_sha256": csha, "content_changed": content_changed, "manifest": manifest})

    ok = True
    for cmd in job.get("candidate", []):
        argv = [str(PY), "-I", str(ROOT / cmd[0])] + [a.replace("{raw}", str(raw)) for a in cmd[1:]]
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=600)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        log({"job": jid, "step": "candidate", "script": cmd[0], "exit": r.returncode, "summary": tail,
             **({"stderr": r.stderr.strip()[-500:]} if r.returncode else {})})
        ok &= r.returncode == 0
    promotion = ("PENDING REVIEW" if content_changed else "NOT NEEDED (content unchanged)") if ok \
        else "BLOCKED: candidate check failed"
    # Record the candidate outcome in the manifest too (review F8).
    update_manifest_entry(manifest, str(raw.relative_to(ROOT)),
                          {"verification_status": "CANDIDATE_OK" if ok else "CANDIDATE_FAILED", "promotion": promotion})
    st.update({"publisher_updated": updated, "last_pull": str(raw.relative_to(ROOT)), "last_sha256": sha,
               "last_content_sha256": csha, "candidate_ok": ok, "promotion": promotion})
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="IonianDTwin refresh runner")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true")
    g.add_argument("--due", action="store_true")
    g.add_argument("--job")
    ap.add_argument("--detect-only", action="store_true")
    args = ap.parse_args()

    jobs = json.loads(JOBS.read_text(encoding="utf-8"))["jobs"]
    if args.list:
        state = load_state()
        for j in jobs:
            s = state.get(j["id"], {})
            print(f"{'ON ' if j['enabled'] else 'off'} {j['id']:26} {j['cadence']:8} {','.join(j['indicators']):24} "
                  f"last_checked={s.get('last_checked', '-')} promotion={s.get('promotion', '-')}"
                  + ("" if j["enabled"] else f"  ({j.get('reason_disabled')})"))
        return 0

    if not guard():
        print("GUARD FAILED: not inside the Digital Twin workspace; nothing done.", file=sys.stderr)
        return 2
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    lock = (LOG_DIR / ".lock").open("w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another refresh run is active; exiting.", file=sys.stderr)
        return 2

    state = load_state()
    if args.job:
        selected = [j for j in jobs if j["id"] == args.job]
        if not selected or not selected[0]["enabled"]:
            print(f"Unknown or disabled job: {args.job}", file=sys.stderr)
            return 2
    else:
        selected = []
        for j in jobs:
            if not j["enabled"]:
                continue
            last = state.get(j["id"], {}).get("last_checked")
            if not last or now() - datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) >= INTERVAL[j["cadence"]]:
                selected.append(j)

    failed = False
    for j in selected:
        try:
            failed |= not run_job(j, state, args.detect_only)
        except Exception as e:  # one failing job must not stop the others or corrupt state
            log({"job": j["id"], "step": "error", "result": "FAIL", "error": repr(e)[:500]})
            failed = True
        save_state(state)
    if not selected:
        print("No jobs due.")
    # Surface anything waiting for a person (review F6): marker file + exit code 3 so cron/mail flags it.
    attention = {jid: s["promotion"] for jid, s in state.items()
                 if str(s.get("promotion", "")).startswith(("PENDING", "BLOCKED"))}
    marker = LOG_DIR / "ATTENTION.txt"
    if attention:
        marker.write_text("".join(f"{jid}: {p}\n" for jid, p in attention.items()), encoding="utf-8")
        print(f"ATTENTION: {len(attention)} job(s) need review: {attention} (see {marker.relative_to(ROOT)})", file=sys.stderr)
    elif marker.exists():
        marker.unlink()
    if failed:
        return 1
    return 3 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
