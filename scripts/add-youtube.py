#!/usr/bin/env python3
"""Add or update a YouTube video entry in data/youtube.yaml.

Used by the daily Morse-novel routine (and any one-off training video) so the
Telegrafi / CW YouTube page stays current.

Does not commit or push. See scripts/README-notiser.md (YouTube-filmer).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "youtube.yaml"
VALID_CATEGORIES = ("morsenovell", "traning", "ovrigt")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
LENGTH_RE = re.compile(r"^\d+:[0-5]\d$")


def die(msg: str, code: int = 1) -> None:
    print(f"add-youtube.py: {msg}", file=sys.stderr)
    raise SystemExit(code)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Append or update a video in data/youtube.yaml."
    )
    p.add_argument("--id", required=True, help="YouTube video id (11 characters)")
    p.add_argument("--date", required=True, help="Publication date YYYY-MM-DD (Europe/Stockholm)")
    p.add_argument(
        "--title",
        help="Title shown on the page. If omitted, the title is taken from YouTube oembed.",
    )
    p.add_argument(
        "--category",
        required=True,
        choices=VALID_CATEGORIES,
        help="morsenovell, traning or ovrigt",
    )
    p.add_argument("--wpm", default=None, help="Speed, e.g. 25 or 30/35/40/50")
    p.add_argument("--length", default=None, help="Duration as M:SS or MM:SS")
    return p.parse_args()


def normalize_id(raw: str) -> str:
    raw = raw.strip()
    m = re.search(r"(?:youtu\.be/|v=|/video/|/embed/)([A-Za-z0-9_-]{11})", raw)
    if m:
        raw = m.group(1)
    if not ID_RE.match(raw):
        die(f"invalid YouTube id {raw!r}; expected 11 characters or a youtu.be URL")
    return raw


def parse_date(raw: str) -> str:
    raw = raw.strip()
    try:
        return date.fromisoformat(raw[:10]).isoformat()
    except ValueError:
        die(f"invalid date {raw!r}; expected YYYY-MM-DD")
    raise AssertionError


def fetch_oembed_title(video_id: str) -> str:
    url = f"https://www.youtube.com/oembed?url=https://youtu.be/{video_id}&format=json"
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        die(f"YouTube oembed returned HTTP {e.code} for {video_id}; not adding it")
    except Exception as e:
        die(f"could not fetch oembed title for {video_id}: {e}")
    title = (data.get("title") or "").strip()
    if not title:
        die(f"oembed for {video_id} had no title")
    return title


def yaml_scalar(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    # Unquoted if plain enough (no leading specials, no colon+space, etc.)
    if re.fullmatch(r"[A-Za-z0-9_./+-]+", text) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        # dates should stay unquoted actually; years-only too. Quote if unsure.
        pass
    if re.fullmatch(r"[A-Za-z0-9_./+-]+", text) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", text) or re.fullmatch(r"\d+:[0-5]\d", text):
        return text
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def unquote(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}:
        inner = raw[1:-1]
        return inner.replace('\\"', '"').replace("\\\\", "\\")
    return raw


def load_videos(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    videos: list[dict] = []
    current: dict | None = None
    in_list = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.fullmatch(r"videos:\s*", line):
            in_list = True
            continue
        if not in_list:
            continue
        m = re.match(r"^  - (\w+):\s*(.*)$", line)
        if m:
            if current:
                videos.append(current)
            current = {m.group(1): unquote(m.group(2))}
            continue
        m = re.match(r"^    (\w+):\s*(.*)$", line)
        if m and current is not None:
            current[m.group(1)] = unquote(m.group(2))
            continue
        die(f"{path} line {lineno}: could not parse {line!r}")
    if current:
        videos.append(current)
    return videos


HEADER = """# Videos on the @Leifradio YouTube channel (https://www.youtube.com/@Leifradio).
# Only include IDs that have been verified (oembed 200). The shortcode sorts
# newest first and groups by category: traning, morsenovell, ovrigt.
#
# Add or update an entry with:
#   python3 scripts/add-youtube.py --id ID --date YYYY-MM-DD --title "..." --category morsenovell [--wpm 25 --length 4:51]

videos:
"""


def dump_videos(path: Path, videos: list[dict]) -> None:
    # Newest first, then title, for a stable readable file.
    def sort_key(v: dict) -> tuple:
        return (v.get("date") or "", v.get("title") or "", v.get("id") or "")

    videos = sorted(videos, key=sort_key, reverse=True)
    order = ("id", "date", "title", "category", "wpm", "length")
    chunks = [HEADER]
    for v in videos:
        first = True
        for key in order:
            if key not in v or v[key] in (None, ""):
                continue
            prefix = "  - " if first else "    "
            chunks.append(f"{prefix}{key}: {yaml_scalar(v[key])}\n")
            first = False
        extras = [k for k in v if k not in order and v[k] not in (None, "")]
        for key in extras:
            prefix = "  - " if first else "    "
            chunks.append(f"{prefix}{key}: {yaml_scalar(v[key])}\n")
            first = False
    path.write_text("".join(chunks), encoding="utf-8")


def maybe_int(value: str) -> int | str:
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def main() -> None:
    args = parse_args()
    video_id = normalize_id(args.id)
    day = parse_date(args.date)
    title = (args.title or "").strip()
    if not title:
        title = fetch_oembed_title(video_id)
    length = (args.length or "").strip() or None
    if length and not LENGTH_RE.match(length) and not re.fullmatch(r"\d+:[0-5]\d", length):
        die(f"invalid length {length!r}; expected M:SS or MM:SS")
    wpm = (args.wpm or "").strip() or None

    entry: dict = {
        "id": video_id,
        "date": day,
        "title": title,
        "category": args.category,
    }
    if wpm is not None:
        entry["wpm"] = maybe_int(wpm)
    if length is not None:
        entry["length"] = length

    videos = load_videos(DATA_FILE)
    existing = next((v for v in videos if v.get("id") == video_id), None)
    if existing:
        videos = [v for v in videos if v.get("id") != video_id]
        action = "updated"
    else:
        action = "added"
    videos.append(entry)
    dump_videos(DATA_FILE, videos)
    print(f"{action} {video_id} ({args.category}) in {DATA_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
