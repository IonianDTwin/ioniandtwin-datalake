#!/usr/bin/env python3
"""Render the data-preparation progress report as a self-contained GitHub-style HTML.

Converts docs/data-preparation-progress.md to HTML and wraps it in the
github-markdown-css (light) theme, so the output looks like the file will when
viewed on GitHub. The CSS is embedded inline - the HTML opens offline with no
network/CORS dependency.

Usage:
  python3 scripts/verification/render_progress_html.py \
      [--md docs/data-preparation-progress.md] \
      [--out /path/to/IonianDTwin-data-preparation-progress.html]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
CSS = Path(__file__).resolve().parent / "github-markdown-light.css"
DEFAULT_MD = ROOT / "docs" / "data-preparation-progress.md"


def colorize(body: str) -> str:
    """Wrap status and cadence tokens in colored badges."""
    badges = {
        "VERIFIED": "verified",
        "PARTIAL": "partial",
        "PROPOSAL": "proposal",
        "UNVERIFIED": "unverified",
        "live": "cad-live",
        "daily": "cad-daily",
        "quarterly": "cad-quarterly",
        "annual": "cad-annual",
        "on-change": "cad-on-change",
        "paused": "cad-paused",
    }
    for token, cls in badges.items():
        body = body.replace(
            f"<code>{token}</code>",
            f'<code class="badge {cls}">{token}</code>',
        )
    return body

# GitHub-style page wrapper: centered, wide container like GitHub's file view.
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
body {{
  box-sizing: border-box;
  background-color: #ffffff;
  margin: 0;
}}
.markdown-body {{
  box-sizing: border-box;
  min-width: 200px;
  max-width: 1012px;
  margin: 0 auto;
  padding: 32px 24px 64px;
}}
.filebar {{
  box-sizing: border-box;
  max-width: 1012px;
  margin: 0 auto;
  padding: 16px 24px 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 13px;
  color: #57606a;
}}
.filebar code {{
  background-color: #f6f8fa;
  padding: 2px 6px;
  border-radius: 6px;
  font-size: 12px;
  color: #24292f;
}}
/* status + cadence badges */
.badge {{
  display: inline-block;
  border-radius: 9999px;
  padding: 2px 8px;
  font-weight: 600;
  font-size: 85%;
  line-height: 1.5;
  white-space: nowrap;
}}
.badge.verified      {{ background:#dafbe1; color:#116329; }}
.badge.partial       {{ background:#fff8c5; color:#7d4e00; }}
.badge.proposal      {{ background:#ddf4ff; color:#0969da; }}
.badge.unverified    {{ background:#ffebe9; color:#cf222e; }}
.badge.cad-live      {{ background:#dafbe1; color:#116329; }}
.badge.cad-daily     {{ background:#ddf4ff; color:#0969da; }}
.badge.cad-quarterly {{ background:#fbefff; color:#8250df; }}
.badge.cad-annual    {{ background:#fff1e5; color:#bc4c00; }}
.badge.cad-on-change {{ background:#d2f9f1; color:#1b7c83; }}
.badge.cad-paused    {{ background:#eaeef2; color:#57606a; }}
@media (max-width: 767px) {{
  .markdown-body {{ padding: 16px; }}
  .filebar {{ padding: 12px 16px 0; }}
}}
</style>
</head>
<body>
<div class="filebar">IonianDTwin &middot; <code>{path}</code> &middot; GitHub-style preview</div>
<article class="markdown-body">
{body}
</article>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=str(DEFAULT_MD))
    ap.add_argument("--out", default=None,
                    help="output HTML path (default: alongside the .md)")
    args = ap.parse_args()

    md_path = Path(args.md).resolve()
    text = md_path.read_text(encoding="utf-8")

    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    body = colorize(body)

    # Derive the <title> from the first top-level heading, else the filename.
    title = md_path.stem.replace("-", " ").title()
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    out_path = Path(args.out) if args.out else md_path.with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        PAGE.format(title=title, css=CSS.read_text(encoding="utf-8"),
                    path=str(md_path.relative_to(ROOT)), body=body),
        encoding="utf-8",
    )
    print(f"rendered {md_path.relative_to(ROOT)} -> {out_path} ({out_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
