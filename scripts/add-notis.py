#!/usr/bin/env python3
"""Create a bilingual notis (short news item) for leif.radio.

Writes:
  content/notiser/YYYY-MM-DD-slug.sv.md
  content/notiser/YYYY-MM-DD-slug.en.md

Does not commit or push. See scripts/README-notiser.md.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Stockholm")
REPO_ROOT = Path(__file__).resolve().parents[1]
NOTIS_DIR = REPO_ROOT / "content" / "notiser"
VALID_TYPES = ("youtube", "propagation", "weather", "winlink", "other")
DEFAULT_SLUG = {
    "youtube": "morsenovell",
    "propagation": "propagation",
    "weather": "vader",
    "winlink": "winlink",
    "other": "notis",
}


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_date(value: str | None) -> datetime:
    if not value:
        return datetime.now(TZ)
    value = value.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=TZ)
            return dt
        except ValueError:
            continue
    die(f"invalid --date {value!r}; use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")
    raise AssertionError


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:50].strip("-")


def toml_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def format_hugo_date(dt: datetime) -> str:
    offset = dt.strftime("%z")
    if len(offset) == 5:
        offset = f"{offset[:3]}:{offset[3:]}"
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + offset


def render(title: str, date: datetime, notis_type: str, link: str | None, body: str) -> str:
    lines = [
        "+++",
        f"title = {toml_str(title)}",
        f"date = {format_hugo_date(date)}",
        f"notis_type = {toml_str(notis_type)}",
    ]
    if link:
        lines.append(f"link = {toml_str(link)}")
    lines.append("+++")
    lines.append("")
    lines.append(body.strip() + "\n")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="Add a bilingual notis under content/notiser/")
    p.add_argument("--type", required=True, choices=VALID_TYPES, help="youtube, propagation, weather, winlink or other")
    p.add_argument("--title-sv", required=True)
    p.add_argument("--title-en", required=True)
    p.add_argument("--text-sv", required=True, help="Body in Swedish, 1–3 lines")
    p.add_argument("--text-en", required=True, help="Body in English, 1–3 lines")
    p.add_argument("--url", default="", help="Optional link (YouTube URL or site-relative path)")
    p.add_argument("--date", default="", help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS (Europe/Stockholm if no offset)")
    p.add_argument("--slug", default="", help="Filename slug; default depends on --type")
    p.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = p.parse_args()

    date = parse_date(args.date or None)
    slug = args.slug.strip() or DEFAULT_SLUG[args.type]
    slug = slugify(slug)
    if not slug:
        die("slug is empty after sanitising")

    stem = f"{date.strftime('%Y-%m-%d')}-{slug}"
    sv_path = NOTIS_DIR / f"{stem}.sv.md"
    en_path = NOTIS_DIR / f"{stem}.en.md"
    if not args.force and (sv_path.exists() or en_path.exists()):
        die(f"{stem} already exists; pass --force to overwrite")

    NOTIS_DIR.mkdir(parents=True, exist_ok=True)
    link = args.url.strip() or None
    sv_path.write_text(render(args.title_sv, date, args.type, link, args.text_sv), encoding="utf-8")
    en_path.write_text(render(args.title_en, date, args.type, link, args.text_en), encoding="utf-8")
    print(sv_path.relative_to(REPO_ROOT))
    print(en_path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
