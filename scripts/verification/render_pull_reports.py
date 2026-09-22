#!/usr/bin/env python3
"""Render self-contained, indicator-annotated visual reports for pull-tested JSON samples.

For each JSON sample this produces, next to the JSON file:
  * `<name>.html`       — self-contained viewer: resource link at the top, decoded data
                          table where each row is annotated with its Data01–Data34 indicator
                          and a plain-English meaning, plus embedded raw JSON.
  * `<name>.summary.md` — Markdown summary (resource link + annotated decoded table).

It also builds a navigation index (`INDEX.html` + `INDEX.md`) that groups all Data01–Data34
by category and links each indicator to the sample report(s) that carry its data.

Payload shapes auto-detected:
  * SDMX 2.1 JSON (Eurostat)  — numeric value indices decoded into dimension rows.
  * Flat JSON (Open-Meteo)    — current/daily blocks with units.
  * OData JSON (Copernicus)   — list of product objects.

The Data01–Data34 annotation comes from `indicators/source-indicator-map.json`.

Usage:
  # render every JSON sample referenced by a manifest (annotated)
  python3 scripts/verification/render_pull_reports.py \
      --manifest data/manifests/source-verification-2026-09-22.json

  # build the per-indicator navigation index
  python3 scripts/verification/render_pull_reports.py \
      --index --manifest data/manifests/source-verification-2026-09-22.json

  # render a single file with explicit metadata
  python3 scripts/verification/render_pull_reports.py \
      --json data/samples/foo.json --source-key OpenMeteo_forecast \
      --name "Foo" --url "https://..."
"""
from __future__ import annotations

import argparse
import html
import json
from collections import defaultdict
from pathlib import Path

DEFAULT_MAP = "indicators/source-indicator-map.json"

# Human meaning for each SDMX dimension code (used in the per-sample explainer).
DIM_MEANING = {
    "freq": "frequency",
    "c_resid": "country of residence (origin of the tourist)",
    "unit": "unit / measure",
    "nace_r2": "accommodation activity (NACE Rev.2)",
    "geo": "region",
    "time": "year",
    "accomunit": "capacity measure (establishments / bedrooms / bed-places)",
}


def _esc(s) -> str:
    return html.escape(str(s))


# ---------------------------------------------------------------- decode

def _decode_sdmx(data: dict):
    dims = data["dimension"]
    ids = data["id"]
    labels: dict[str, dict[str, str]] = {}
    code_lists: dict[str, list[str]] = {}
    for k in ids:
        cat = dims[k]["category"]
        lab = cat.get("label", {})
        codes = list(cat["index"].keys())
        code_lists[k] = codes
        labels[k] = lab
    rows: list[dict] = []
    for ki, val in data.get("value", {}).items():
        i = int(ki)
        combo: dict[str, str] = {}
        rem = i
        for k in reversed(ids):
            codes = code_lists[k]
            pos = rem % len(codes)
            rem //= len(codes)
            combo[k] = codes[pos]
        combo["value"] = val if not isinstance(val, list) else ", ".join(map(str, val))
        rows.append(combo)
    return list(ids) + ["value"], rows, labels


def _decode_openmeteo(data: dict):
    cols = ["block", "field", "unit", "time", "value"]
    rows: list[dict] = []
    cur = data.get("current", {})
    cur_units = data.get("current_units", {})
    for k, v in cur.items():
        if k == "time":
            continue
        rows.append({"block": "current", "field": k, "unit": cur_units.get(k, ""),
                     "time": cur.get("time", ""), "value": v})
    daily = data.get("daily", {})
    daily_units = data.get("daily_units", {})
    times = daily.get("time", [])
    for k in daily:
        if k == "time":
            continue
        for t, v in zip(times, daily[k]):
            rows.append({"block": "daily", "field": k, "unit": daily_units.get(k, ""),
                         "time": t, "value": v})
    return cols, rows, None


def _decode_odata(data: dict):
    values = data.get("value", [])
    cols: list[str] = []
    for item in values:
        for k in item:
            if k not in cols:
                cols.append(k)
    cols = [c for c in cols if not c.startswith("@")] or cols
    rows = [{k: item.get(k, "") for k in cols} for item in values]
    return cols, rows, None


def _decode_generic(data: dict):
    cols = ["key", "value"]
    rows = [{"key": k, "value": v} for k, v in data.items() if not isinstance(v, (dict, list))]
    return cols, rows, None


def decode(data: dict):
    if isinstance(data.get("value"), dict) and "dimension" in data and "id" in data:
        kind = "sdmx"
        cols, rows, labels = _decode_sdmx(data)
    elif "current" in data and "daily" in data:
        kind = "openmeteo"
        cols, rows, labels = _decode_openmeteo(data)
    elif isinstance(data.get("value"), list):
        kind = "odata"
        cols, rows, labels = _decode_odata(data)
    else:
        kind = "generic"
        cols, rows, labels = _decode_generic(data)
    return kind, cols, rows, labels


# ---------------------------------------------------------------- indicator map

def load_map(path: str = DEFAULT_MAP) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def indicators_by_id(mapping: dict) -> dict[str, dict]:
    return {ind["indicator_id"]: ind for ind in mapping.get("indicators", [])}


def series_for(mapping: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for ind in mapping.get("indicators", []):
        for s in ind.get("series", []):
            s = dict(s)
            s["indicator_id"] = ind["indicator_id"]
            s["indicator_name"] = ind["name"]
            out[s.get("source_key")].append(s)
    return out


def _match_series(kind: str, row: dict, source_series: list[dict]) -> list[dict]:
    hits = []
    for s in source_series:
        if kind == "sdmx":
            dims = s.get("dims", {})
            if dims and all(row.get(k) == v for k, v in dims.items()):
                hits.append(s)
        else:  # flat / open-meteo
            if "field" in s and row.get("field") == s["field"]:
                hits.append(s)
    return hits


def annotate(kind: str, row: dict, source_series: list[dict]):
    hits = _match_series(kind, row, source_series)
    if not hits:
        row["indicator"] = ""
        row["meaning"] = ""
        return
    s = hits[0]
    row["indicator"] = f"{s['indicator_id']} · {s['indicator_name']}"
    parts = []
    if s.get("label"):
        parts.append(s["label"])
    if s.get("unit"):
        parts.append(s["unit"])
    meaning = " — ".join(p for p in parts if p)
    if s.get("description"):
        meaning = f"{s['description']} ({meaning})" if meaning else s["description"]
    row["meaning"] = meaning


def _explainer(kind: str, cols: list[str], labels, source_key: str, mapping: dict) -> dict:
    """Build a short 'how to read this sample' block for SDMX datasets."""
    if kind != "sdmx" or not labels:
        return {}
    dims = [c for c in cols if c not in ("value", "indicator", "meaning")]
    dim_lines = []
    for c in dims:
        vals = labels.get(c) or {}
        codes = list(vals.keys())
        shown = ", ".join(f"{v} ({vals[v]})" if vals.get(v) and vals[v] != v else v for v in codes)
        meaning = DIM_MEANING.get(c, c)
        dim_lines.append((c, meaning, shown))
    mapped = []
    if mapping and source_key:
        for s in series_for(mapping).get(source_key, []):
            dims_str = ", ".join(f"{k}={v}" for k, v in s.get("dims", {}).items())
            mapped.append(f"{s['indicator_id']} · {s['indicator_name']} — {s.get('label','')} [{dims_str}]")
    return {"dims": dim_lines, "mapped": mapped}


def _explainer_html(exp: dict) -> str:
    if not exp:
        return ""
    dim_rows = "".join(
        f"<li><code>{_esc(k)}</code> — {_esc(meaning)}: {_esc(v)}</li>"
        for k, meaning, v in exp["dims"]
    )
    mapped = "".join(f"<li>{_esc(m)}</li>" for m in exp["mapped"]) or "<li><em>none</em></li>"
    return f"""<details>
  <summary><strong>How to read this sample</strong></summary>
  <div class="legend">
    <p>This source returns a multi-dimensional cube; the pull kept <em>all</em> dimension combinations, so only a few rows are the headline Data01–Data34 values and the rest are sub-breakdowns or context.</p>
    <p><strong>Dimensions:</strong></p>
    <ul>{dim_rows}</ul>
    <p><strong>Rows mapped to indicators:</strong></p>
    <ul>{mapped}</ul>
    <p>Unmapped rows are the same source broken down further (e.g. domestic vs foreign, hotels vs camping) or %-change context — they are not separate Data01–Data34 indicators.</p>
  </div>
</details>
"""


def _explainer_md(exp: dict) -> str:
    if not exp:
        return ""
    lines = ["## How to read this sample", "",
             "This source returns a multi-dimensional cube; the pull kept all dimension combinations, so only a few rows are the headline Data01–Data34 values and the rest are sub-breakdowns or context.", "",
             "**Dimensions:**", ""]
    for k, meaning, v in exp["dims"]:
        lines.append(f"- `{k}` — {meaning}: {v}")
    lines.append("")
    lines.append("**Rows mapped to indicators:**")
    for m in exp["mapped"]:
        lines.append(f"- {m}")
    if not exp["mapped"]:
        lines.append("- none")
    lines.append("")
    lines.append("Unmapped rows are the same source broken down further (e.g. domestic vs foreign, hotels vs camping) or %-change context — they are not separate Data01–Data34 indicators.")
    lines.append("")
    return "\n".join(lines)


def _headline_summary(kind: str, rows: list[dict], source_series: list[dict]) -> list[dict]:
    """Group matched rows by indicator into a prominent 'what we pulled' summary."""
    groups: dict[str, dict] = {}
    order: list[str] = []
    for s in source_series:
        vals = [r for r in rows if _match_series(kind, r, [s])]
        if not vals:
            continue
        iid = s["indicator_id"]
        if iid not in groups:
            groups[iid] = {"indicator_id": iid, "indicator_name": s["indicator_name"], "series": []}
            order.append(iid)
        if kind == "sdmx":
            parts = [f"{r.get('time', '?')}: {_fmt_val(r.get('value', ''))}" for r in vals]
            value_str = " · ".join(parts)
            unit = s.get("unit", "")
        else:
            r = vals[0]
            value_str = _fmt_val(r.get("value", ""))
            unit = r.get("unit", "") or s.get("unit", "")
        groups[iid]["series"].append({"label": s.get("label", ""), "value": value_str, "unit": unit})
    return [groups[i] for i in order]


def _headline_html(heads: list[dict]) -> str:
    if not heads:
        return "<section class=\"headline\"><h2>Indicators pulled</h2>" \
               "<p class=\"nohead\">No Data01–Data34 indicator is mapped in this sample.</p></section>"
    cards = ""
    for h in heads:
        items = "".join(
            f"<li><span class=\"label\">{_esc(s['label'])}</span> "
            f"<span class=\"value\">{_esc(s['value'])}</span>"
            + (f" <span class=\"unit\">{_esc(s['unit'])}</span>" if s.get("unit") else "")
            + "</li>"
            for s in h["series"]
        )
        cards += (
            f'<div class="card"><div class="card-id">{_esc(h["indicator_id"])}</div>'
            f'<div class="card-name">{_esc(h["indicator_name"])}</div>'
            f'<ul class="card-series">{items}</ul></div>'
        )
    return f"<section class=\"headline\"><h2>Indicators pulled</h2><div class=\"cards\">{cards}</div></section>"


def _headline_md(heads: list[dict]) -> str:
    if not heads:
        return "## Indicators pulled\n\n_No Data01–Data34 indicator is mapped in this sample._\n"
    lines = ["## Indicators pulled", ""]
    for h in heads:
        lines.append(f"### {h['indicator_id']} · {h['indicator_name']}")
        for s in h["series"]:
            label = s.get("label", "")
            unit = s.get("unit", "")
            value = s["value"] + (f" {unit}" if unit else "")
            lines.append(f"- **{label}**: `{value}`" if label else f"- `{value}`")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- rendering

def _meta_items(meta: dict):
    return [
        ("Resource", meta.get("url")),
        ("Status", meta.get("status")),
        ("Content-Type", meta.get("content_type")),
        ("Checksum (sha256)", meta.get("checksum_sha256")),
        ("Accessed at", meta.get("accessed_at")),
        ("Raw JSON", meta.get("json_rel", "")),
    ]


def _display_cells(kind, cols, row, labels):
    out = {}
    for c in cols:
        v = row.get(c, "")
        if kind == "sdmx" and labels and c in labels and v:
            lab = labels[c].get(str(v), "")
            out[c] = v if not lab else f"{v} · {lab}"
        else:
            out[c] = v
    return out


def _render_html(meta: dict, kind: str, cols: list[str], rows: list[dict], labels, raw_json: str, exp: dict, heads: list[dict]) -> str:
    name = _esc(meta.get("name", "Pull report"))
    url = meta.get("url") or ""
    head_rows = "".join(
        f'<tr><th>{_esc(k)}</th><td>'
        + (f'<a href="{_esc(v)}">{_esc(v)}</a>' if k == "Resource" and v else _esc(v) if v else "<em>—</em>")
        + "</td></tr>"
        for k, v in _meta_items(meta)
    )
    if "indicator" in cols:
        thead = "".join(f"<th>{_esc(c)}</th>" for c in cols)
        body = "".join(
            "<tr>" + "".join(f"<td>{_esc(_display_cells(kind, cols, r, labels).get(c, ''))}</td>" for c in cols) + "</tr>"
            for r in rows
        )
    else:
        thead = "".join(f"<th>{_esc(c)}</th>" for c in cols)
        body = "".join("<tr>" + "".join(f"<td>{_esc(r.get(c, ''))}</td>" for c in cols) + "</tr>" for r in rows)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}</title>
<style>
  :root {{ --fg:#1a1a1a; --muted:#666; --line:#ddd; --accent:#0b57d0; --chip:#e8f0fe; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font: 14px/1.45 -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; color: var(--fg); }}
  header {{ padding: 20px 24px 16px; border-bottom: 1px solid var(--line); background:#f7f9fc; }}
  h1 {{ margin: 0 0 12px; font-size: 20px; }}
  .meta {{ display:grid; grid-template-columns: max-content 1fr; gap: 4px 16px; }}
  .meta th {{ text-align:left; color: var(--muted); font-weight:600; vertical-align:top; }}
  .meta td {{ word-break: break-all; }}
  a {{ color: var(--accent); }}
  main {{ padding: 16px 24px 24px; }}
  h2 {{ font-size: 16px; margin: 20px 0 8px; }}
  .legend {{ margin: 12px 0; }}
  .legend li {{ margin: 4px 0; }}
  .headline {{ margin-bottom: 8px; }}
  .headline h2 {{ margin-top: 0; }}
  .nohead {{ color: var(--muted); }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }}
  .card {{ border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 8px; padding: 12px 14px; background: #fff; }}
  .card-id {{ font-family: ui-monospace, Menlo, monospace; font-size: 15px; font-weight: 700; color: var(--accent); }}
  .card-name {{ font-weight: 600; margin: 2px 0 8px; }}
  .card-series {{ list-style: none; margin: 0; padding: 0; }}
  .card-series li {{ padding: 4px 0; border-top: 1px dashed var(--line); }}
  .card-series .label {{ color: var(--muted); font-size: 12px; display: block; }}
  .card-series .value {{ font-weight: 700; color: #0b7a3d; }}
  .card-series .unit {{ color: var(--muted); font-size: 12px; }}
  .badge {{ display:inline-block; padding: 2px 8px; border-radius:999px; background:var(--chip); color:var(--accent); font-size:12px; margin-right:6px; }}
  .tablewrap {{ overflow:auto; border:1px solid var(--line); border-radius:6px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
  th, td {{ padding: 6px 10px; border-bottom: 1px solid var(--line); text-align:left; vertical-align:top; }}
  th {{ background:#f2f5f9; position: sticky; top: 0; }}
  tr:nth-child(even) td {{ background:#fafbfd; }}
  td.ind {{ font-weight:600; color:var(--accent); white-space:nowrap; }}
  td.meaning {{ color:var(--muted); }}
  details {{ margin-top: 20px; }}
  pre {{ max-height: 420px; overflow:auto; background:#0f172a; color:#e2e8f0; padding: 14px; border-radius:6px; font: 12px/1.5 ui-monospace, Menlo, Consolas, monospace; }}
</style>
</head>
<body>
<header>
  <h1>{name}</h1>
  <div><span class="badge">decoded · {_esc(kind)}</span></div>
  <table class="meta">{head_rows}</table>
</header>
<main>
  {_headline_html(heads)}
  {_explainer_html(exp)}
  <h2>Full data ({len(rows)} rows)</h2>
  <div class="tablewrap"><table><thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></div>
  <details>
    <summary>Raw JSON ({len(raw_json)} bytes)</summary>
    <pre>{_esc(raw_json)}</pre>
  </details>
</main>
</body>
</html>
"""


def _render_md(meta: dict, kind: str, cols: list[str], rows: list[dict], labels, exp: dict, heads: list[dict]) -> str:
    name = meta.get("name", "Pull report")
    lines = [f"# {name}", ""]
    url = meta.get("url")
    if url:
        lines.append(f"**Resource:** {url}")
        lines.append("")
    lines.append(f"- Status: `{meta.get('status', '')}`")
    lines.append(f"- Kind: `{kind}`")
    if meta.get("content_type"):
        lines.append(f"- Content-Type: `{meta['content_type']}`")
    if meta.get("checksum_sha256"):
        lines.append(f"- sha256: `{meta['checksum_sha256']}`")
    if meta.get("accessed_at"):
        lines.append(f"- Accessed at: `{meta['accessed_at']}`")
    lines.append("")
    lines.append(_headline_md(heads))
    lines.append(_explainer_md(exp))
    lines.append(f"## Full data ({len(rows)} rows)")
    lines.append("")
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join("---" for _ in cols) + "|")
    for r in rows:
        cells = []
        for c in cols:
            v = _display_cells(kind, cols, r, labels).get(c, "")
            cells.append(str(v).replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def render(json_path: Path, meta: dict, mapping: dict | None = None) -> tuple[Path, Path]:
    raw = json_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    kind, cols, rows, labels = decode(data)

    src_series = []
    src_key = meta.get("source_key", "")
    if mapping and src_key:
        src_series = series_for(mapping).get(src_key, [])
    if src_series:
        for r in rows:
            annotate(kind, r, src_series)
        if "indicator" not in cols:
            cols = cols + ["indicator", "meaning"]

    exp = _explainer(kind, cols, labels, src_key, mapping)
    heads = _headline_summary(kind, rows, src_series)
    meta = dict(meta)
    meta["json_rel"] = json_path.name
    html_path = json_path.with_suffix(".html")
    md_path = json_path.with_suffix(".summary.md")
    html_path.write_text(_render_html(meta, kind, cols, rows, labels, raw, exp, heads), encoding="utf-8")
    md_path.write_text(_render_md(meta, kind, cols, rows, labels, exp, heads), encoding="utf-8")
    return html_path, md_path


# ---------------------------------------------------------------- index

def _fmt_val(v) -> str:
    if isinstance(v, float):
        if v == int(v):
            return f"{int(v):,}"
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def _collect_index_data(mapping: dict, manifest: dict, root: Path):
    """Return {indicator_id: {indicator, series:[{..., values, sample_files}]}}."""
    ind_by_id = indicators_by_id(mapping)
    series_map = series_for(mapping)
    result: dict[str, dict] = {}

    def ensure(ind_id):
        if ind_id not in result:
            ind = ind_by_id.get(ind_id, {"indicator_id": ind_id, "name": ind_id})
            result[ind_id] = {"indicator": ind, "series": []}

    # value rows keyed by (source_key, dims-signature)
    samples = {}
    for ev in manifest.get("evidence", []):
        p = ev.get("sample_path")
        if not p or not p.lower().endswith(".json"):
            continue
        path = root / p
        if not path.exists():
            continue
        kind, cols, rows, labels = decode(json.loads(path.read_text(encoding="utf-8")))
        src_key = ev.get("source_id", "")
        samples[src_key] = {"path": path, "kind": kind, "rows": rows, "meta": ev}
        for ind in mapping.get("indicators", []):
            for s in ind.get("series", []):
                if s.get("source_key") != src_key:
                    continue
                vals = []
                for r in rows:
                    if _match_series(kind, r, [s]):
                        vals.append(r)
                if vals:
                    ensure(ind["indicator_id"])
                    entry = dict(s)
                    entry["values"] = vals
                    entry["path"] = path
                    result[ind["indicator_id"]]["series"].append(entry)
    return result


def _series_value_summary(series: dict, kind: str) -> str:
    vals = series.get("values", [])
    if not vals:
        return ""
    if kind == "sdmx":
        time_idx = "time"
        parts = []
        for r in vals:
            t = r.get("time", "?")
            parts.append(f"{t}: {_fmt_val(r.get('value', ''))}")
        return " · ".join(parts)
    # flat: single value
    r = vals[0]
    unit = r.get("unit", "")
    return f"{_fmt_val(r.get('value', ''))} {unit}".strip()


def build_index(mapping: dict, manifest: dict, root: Path, out_dir: Path):
    data = _collect_index_data(mapping, manifest, root)
    cat_order = list(mapping.get("categories", {}).keys())
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for ind in mapping.get("indicators", []):
        by_cat[ind["category"]].append(ind)

    # HTML
    rows_html = []
    for cat in cat_order:
        inds = by_cat.get(cat, [])
        if not inds:
            continue
        cname = mapping["categories"].get(cat, {}).get("name", cat)
        cname_el = mapping["categories"].get(cat, {}).get("name_el", "")
        rows_html.append(f'<h2 id="cat-{cat}">{_esc(cname)} <span style="color:var(--muted)">{_esc(cname_el)}</span></h2>')
        for ind in inds:
            iid = ind["indicator_id"]
            status = ind.get("status", "UNVERIFIED")
            badge = {"VERIFIED": "ver", "PARTIAL": "part", "PROPOSAL": "prop", "UNVERIFIED": "unv"}.get(status, "unv")
            rows_html.append(f'<div class="indcard" id="{iid}">')
            rows_html.append(f'<div class="indhead"><span class="ind-id">{_esc(iid)}</span> '
                             f'<span class="ind-name">{_esc(ind["name"])}</span> '
                             f'<span class="badge {badge}">{_esc(status)}</span></div>')
            if ind.get("name_el"):
                rows_html.append(f'<div class="ind-el">{_esc(ind["name_el"])}</div>')
            rows_html.append(f'<div class="ind-meta">Source: {_esc(ind.get("source", ""))} · '
                             f'Access: {_esc(ind.get("access_type", ""))} · Auth: {_esc(ind.get("auth", ""))}</div>')
            if ind.get("note"):
                rows_html.append(f'<div class="ind-note">{_esc(ind["note"])}</div>')
            series = data.get(iid, {}).get("series", [])
            if series:
                rows_html.append('<ul class="series">')
                for s in series:
                    link_html = ""
                    if s.get("path"):
                        base = s["path"].with_suffix("")
                        link_html = (f' — <a href="{_esc(s["path"].with_suffix(".html").name)}">viewer</a> · '
                                     f'<a href="{_esc(s["path"].with_suffix(".summary.md").name)}">md</a>')
                    label = s.get("label", "series")
                    unit = f" ({s.get('unit','')})" if s.get("unit") else ""
                    summary = _series_value_summary(s, "sdmx" if "dims" in s else "flat")
                    rows_html.append(f'<li><strong>{_esc(label)}</strong>{_esc(unit)}: '
                                     f'<span class="val">{_esc(summary)}</span>{link_html}</li>')
                rows_html.append("</ul>")
            rows_html.append("</div>")

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>IonianDTwin — indicator data index</title>
<style>
  :root {{ --fg:#1a1a1a; --muted:#666; --line:#ddd; --accent:#0b57d0; }}
  body {{ margin:0; font:14px/1.45 -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; color:var(--fg); }}
  header {{ padding:20px 24px 16px; border-bottom:1px solid var(--line); background:#f7f9fc; }}
  h1 {{ margin:0 0 8px; font-size:20px; }}
  main {{ padding:16px 24px 32px; max-width: 960px; }}
  h2 {{ font-size:17px; margin:24px 0 8px; border-bottom:2px solid var(--line); padding-bottom:4px; }}
  a {{ color:var(--accent); }}
  .indcard {{ border:1px solid var(--line); border-radius:8px; padding:10px 14px; margin:10px 0; }}
  .indhead {{ font-weight:600; }}
  .ind-id {{ color:var(--accent); font-family: ui-monospace, Menlo, monospace; }}
  .ind-el {{ color:var(--muted); font-size:13px; }}
  .ind-meta, .ind-note {{ color:var(--muted); font-size:13px; margin-top:4px; }}
  .series {{ margin:6px 0 0 0; padding-left:18px; }}
  .series li {{ margin:3px 0; }}
  .val {{ color:#0b7a3d; }}
  .badge {{ display:inline-block; padding:1px 8px; border-radius:999px; font-size:11px; font-weight:600; margin-left:6px; }}
  .ver {{ background:#e6f4ea; color:#0b7a3d; }}
  .part {{ background:#fef7e0; color:#b26a00; }}
  .prop {{ background:#e8f0fe; color:#0b57d0; }}
  .unv {{ background:#f1f3f4; color:#666; }}
</style></head>
<body>
<header><h1>IonianDTwin — indicator data index</h1>
<p style="margin:0;color:var(--muted)">Data01–Data34 grouped by category. Green values are verified pulls; each verified series links to its viewer and Markdown summary.</p></header>
<main>
{''.join(rows_html)}
</main></body></html>
"""

    # Markdown
    md_lines = ["# IonianDTwin — indicator data index", "",
                "Data01–Data34 grouped by category, with verified values and links to the sample reports in `data/samples/`.",
                ""]
    for cat in cat_order:
        inds = by_cat.get(cat, [])
        if not inds:
            continue
        cname = mapping["categories"].get(cat, {}).get("name", cat)
        cname_el = mapping["categories"].get(cat, {}).get("name_el", "")
        md_lines.append(f"## {cname} — {cname_el}")
        md_lines.append("")
        for ind in inds:
            iid = ind["indicator_id"]
            el = f" ({ind['name_el']})" if ind.get("name_el") else ""
            md_lines.append(f"### {iid} · {ind['name']}{el} — `{ind.get('status','UNVERIFIED')}`")
            md_lines.append("")
            md_lines.append(f"- Source: {ind.get('source','')}")
            md_lines.append(f"- Access: `{ind.get('access_type','')}` · Auth: `{ind.get('auth','')}`")
            if ind.get("note"):
                md_lines.append(f"- Note: {ind['note']}")
            series = data.get(iid, {}).get("series", [])
            for s in series:
                label = s.get("label", "series")
                unit = f" ({s['unit']})" if s.get("unit") else ""
                summary = _series_value_summary(s, "sdmx" if "dims" in s else "flat")
                links = ""
                if s.get("path"):
                    links = (f" → [viewer]({s['path'].with_suffix('.html').name}) · "
                             f"[md]({s['path'].with_suffix('.summary.md').name})")
                md_lines.append(f"  - **{label}**{unit}: `{summary}`{links}")
            md_lines.append("")
    md_text = "\n".join(md_lines)

    idx_html = out_dir / "INDEX.html"
    idx_md = out_dir / "INDEX.md"
    idx_html.write_text(html_doc, encoding="utf-8")
    idx_md.write_text(md_text, encoding="utf-8")
    return idx_html, idx_md


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", help="manifest JSON with an 'evidence' list")
    ap.add_argument("--json", help="single JSON file to render")
    ap.add_argument("--index", action="store_true", help="build the per-indicator navigation index")
    ap.add_argument("--map", default=DEFAULT_MAP, help="path to source-indicator map JSON")
    ap.add_argument("--source-key", help="manifest source_id key for a single file (e.g. OpenMeteo_forecast)")
    ap.add_argument("--name", help="display name for a single file")
    ap.add_argument("--url", help="resource URL for a single file")
    ap.add_argument("--status", default="VERIFIED")
    ap.add_argument("--content-type", default="")
    ap.add_argument("--checksum", default="")
    ap.add_argument("--accessed-at", default="")
    args = ap.parse_args()

    mapping = load_map(args.map)

    if args.manifest:
        man = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        root = Path(args.manifest).resolve().parent.parent.parent

        if args.index:
            out_dir = root / "data" / "samples"
            h, m = build_index(mapping, man, root, out_dir)
            print(f"index: {h}")
            print(f"index: {m}")
            return 0

        count = 0
        for ev in man.get("evidence", []):
            p = ev.get("sample_path")
            if not p:
                continue
            path = root / p
            if not path.exists():
                print(f"skip (missing): {path}")
                continue
            if path.suffix.lower() != ".json":
                print(f"skip (not JSON): {path.name}")
                continue
            meta = {
                "name": ev.get("name", path.stem),
                "url": ev.get("url", ""),
                "status": ev.get("verification_status") or ev.get("response_status"),
                "content_type": ev.get("content_type", ""),
                "checksum_sha256": ev.get("checksum_sha256", ""),
                "accessed_at": ev.get("accessed_at", ""),
                "source_key": ev.get("source_id", ""),
            }
            h, m = render(path, meta, mapping)
            print(f"rendered: {h.name} + {m.name}")
            count += 1
        print(f"done: {count} sample(s)")
        return 0

    if args.json:
        import hashlib
        from datetime import datetime, timezone
        path = Path(args.json)
        meta = {
            "name": args.name or path.stem,
            "url": args.url or "",
            "status": args.status,
            "content_type": args.content_type,
            "checksum_sha256": args.checksum or hashlib.sha256(path.read_bytes()).hexdigest(),
            "accessed_at": args.accessed_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_key": args.source_key or "",
        }
        h, m = render(path, meta, mapping)
        print(f"rendered: {h}")
        print(f"rendered: {m}")
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
