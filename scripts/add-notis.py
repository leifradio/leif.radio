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
VALID_TYPES = ("youtube", "propagation", "weather", "atno", "winlink", "other")
DEFAULT_SLUG = {
    "youtube": "morsenovell",
    "propagation": "propagation",
    "weather": "vader",
    "atno": "atno",
    "winlink": "winlink",
    "other": "notis",
}

# SMHI Wsymb2 / SNOW symbol_code (1–27) → emoji for the notis body text.
# Temperature in the text uses 🌡️ (not a Wsymb2 code).
WSYMB2_TO_EMOJI = {
    1: "☀️",   # clear sky
    2: "🌤️",   # nearly clear sky
    3: "⛅",   # variable cloudiness
    4: "⛅",   # half-clear sky
    5: "🌥️",   # cloudy sky
    6: "☁️",   # overcast
    7: "🌫️",   # fog
    8: "🌦️",   # light rain showers
    9: "🌦️",   # moderate rain showers
    10: "🌦️",  # heavy rain showers
    11: "⛈️",  # thunderstorm
    12: "🌨️",  # light sleet showers
    13: "🌨️",  # moderate sleet showers
    14: "🌨️",  # heavy sleet showers
    15: "🌨️",  # light snow showers
    16: "🌨️",  # moderate snow showers
    17: "🌨️",  # heavy snow showers
    18: "🌧️",  # light rain
    19: "🌧️",  # moderate rain
    20: "🌧️",  # heavy rain
    21: "⛈️",  # thunder
    22: "🌨️",  # light sleet
    23: "🌨️",  # moderate sleet
    24: "🌨️",  # heavy sleet
    25: "❄️",  # light snowfall
    26: "❄️",  # moderate snowfall
    27: "❄️",  # heavy snowfall
}

# Optional front-matter name, kept for compatibility; not shown as the header icon.
WEATHER_ICONS = ("clear", "partly", "cloudy", "rain", "snow", "sleet", "thunder", "fog")
WSYMB2_TO_ICON = {
    1: "clear", 2: "clear", 3: "partly", 4: "partly", 5: "cloudy", 6: "cloudy",
    7: "fog", 8: "rain", 9: "rain", 10: "rain", 11: "thunder", 12: "sleet",
    13: "sleet", 14: "sleet", 15: "snow", 16: "snow", 17: "snow", 18: "rain",
    19: "rain", 20: "rain", 21: "thunder", 22: "sleet", 23: "sleet", 24: "sleet",
    25: "snow", 26: "snow", 27: "snow",
}


def _wsymb2_code(code: int) -> int:
    try:
        code = int(code)
    except (TypeError, ValueError):
        die(f"invalid Wsymb2 code {code!r}; expected an integer 1–27")
    if code not in WSYMB2_TO_EMOJI:
        die(f"unknown Wsymb2 code {code}; expected 1–27")
    return code


def emoji_from_wsymb2(code: int) -> str:
    """Map an SMHI Wsymb2 / symbol_code (1–27) to a weather emoji for the body text."""
    return WSYMB2_TO_EMOJI[_wsymb2_code(code)]


def icon_from_wsymb2(code: int) -> str:
    """Map an SMHI Wsymb2 / symbol_code (1–27) to a weather_icon name (optional front matter)."""
    return WSYMB2_TO_ICON[_wsymb2_code(code)]


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


def render(
    title: str,
    date: datetime,
    notis_type: str,
    link: str | None,
    body: str,
    weather_icon: str | None = None,
) -> str:
    lines = [
        "+++",
        f"title = {toml_str(title)}",
        f"date = {format_hugo_date(date)}",
        f"notis_type = {toml_str(notis_type)}",
    ]
    if weather_icon:
        lines.append(f"weather_icon = {toml_str(weather_icon)}")
    if link:
        lines.append(f"link = {toml_str(link)}")
    lines.append("+++")
    lines.append("")
    lines.append(body.strip() + "\n")
    return "\n".join(lines)


def main() -> None:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--map-wsymb", type=int, metavar="CODE")
    pre_args, _ = pre.parse_known_args()
    if pre_args.map_wsymb is not None:
        print(emoji_from_wsymb2(pre_args.map_wsymb))
        return

    p = argparse.ArgumentParser(description="Add a bilingual notis under content/notiser/")
    p.add_argument("--type", required=True, choices=VALID_TYPES, help="youtube, propagation, weather, atno, winlink or other")
    p.add_argument("--title-sv", required=True)
    p.add_argument("--title-en", required=True)
    p.add_argument("--text-sv", required=True, help="Body in Swedish, 1–3 lines")
    p.add_argument("--text-en", required=True, help="Body in English, 1–3 lines")
    p.add_argument("--url", default="", help="Optional link (YouTube URL or site-relative path)")
    p.add_argument("--date", default="", help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS (Europe/Stockholm if no offset)")
    p.add_argument("--slug", default="", help="Filename slug; default depends on --type")
    p.add_argument(
        "--icon",
        default="",
        choices=("",) + WEATHER_ICONS,
        help="Optional weather_icon front matter (not shown in the header). Prefer emoji in the body text",
    )
    p.add_argument(
        "--wsymb",
        type=int,
        default=None,
        metavar="CODE",
        help="SMHI Wsymb2 / symbol_code 1–27; optional weather_icon front matter only. Prefer putting emoji in the text via --map-wsymb",
    )
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

    weather_icon = (args.icon or "").strip() or None
    if args.wsymb is not None:
        mapped = icon_from_wsymb2(args.wsymb)
        if weather_icon and weather_icon != mapped:
            print(
                f"warning: --icon {weather_icon} overrides --wsymb {args.wsymb} ({mapped})",
                file=sys.stderr,
            )
        if not weather_icon:
            weather_icon = mapped
    if weather_icon and args.type != "weather":
        die("--icon / --wsymb can only be used with --type weather")
    if weather_icon and weather_icon not in WEATHER_ICONS:
        die(f"invalid --icon {weather_icon!r}; expected one of {', '.join(WEATHER_ICONS)}")

    NOTIS_DIR.mkdir(parents=True, exist_ok=True)
    link = args.url.strip() or None
    sv_path.write_text(
        render(args.title_sv, date, args.type, link, args.text_sv, weather_icon),
        encoding="utf-8",
    )
    en_path.write_text(
        render(args.title_en, date, args.type, link, args.text_en, weather_icon),
        encoding="utf-8",
    )
    print(sv_path.relative_to(REPO_ROOT))
    print(en_path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
