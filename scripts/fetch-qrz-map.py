#!/usr/bin/env python3
"""Fetch SM4T QRZ Logbook QSOs and write static/data/qsos.json for the site map.

Requires env QRZ_LOGBOOK_API_KEY. Never prints or writes the key.
Usage: QRZ_LOGBOOK_API_KEY=… python3 scripts/fetch-qrz-map.py
"""
from __future__ import annotations

import html
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://logbook.qrz.com/api"
USER_AGENT = "Leif.radio-map/1.0 (SM4T)"
PAGE_SIZE = 250
REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "static" / "data"


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def api_post(fields: dict[str, str]) -> str:
    key = os.environ.get("QRZ_LOGBOOK_API_KEY", "").strip()
    if not key:
        die("QRZ_LOGBOOK_API_KEY is not set")
    data = urllib.parse.urlencode({**fields, "KEY": key}).encode()
    req = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_response(raw: str) -> tuple[dict[str, str], str]:
    """Split RESULT header from HTML-entity-encoded ADIF body."""
    idx = raw.find("ADIF=")
    if idx < 0:
        # STATUS and error responses have no ADIF
        header: dict[str, str] = {}
        for part in raw.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                header[k.upper()] = urllib.parse.unquote_plus(v)
        return header, ""
    header_raw = raw[:idx]
    header = {}
    for part in header_raw.split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            if k:
                header[k.upper()] = urllib.parse.unquote_plus(v)
    adif = html.unescape(raw[idx + 5 :])
    return header, adif


def parse_adif_records(adif: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for m in re.finditer(r"<([a-z0-9_]+):(\d+)(?::[^>]*)?>([^<]*)", adif, re.I):
        name = m.group(1).lower()
        length = int(m.group(2))
        value = m.group(3)[:length].strip()
        if name == "eor":
            continue
        current[name] = value
        # Detect end of record by looking ahead… handled below via split
    # More reliable: split on <eor>
    for chunk in re.split(r"<eor>", adif, flags=re.I):
        rec: dict[str, str] = {}
        for m in re.finditer(r"<([a-z0-9_]+):(\d+)(?::[^>]*)?>([^<]*)", chunk, re.I):
            name = m.group(1).lower()
            length = int(m.group(2))
            rec[name] = m.group(3)[:length].strip()
        if rec.get("call"):
            records.append(rec)
    return records


def parse_qrz_coord(text: str) -> float | None:
    """Parse QRZ ADIF lat/lon like 'N060 26.364' or 'E015 25.748' → decimal degrees."""
    if not text:
        return None
    m = re.match(r"^([NSEW])\s*(\d{1,3})\s+(\d+(?:\.\d+)?)\s*$", text.strip(), re.I)
    if not m:
        return None
    hemi, deg_s, minutes_s = m.group(1).upper(), m.group(2), m.group(3)
    value = int(deg_s) + float(minutes_s) / 60.0
    if hemi in ("S", "W"):
        value = -value
    return value


def maidenhead_to_latlon(grid: str) -> tuple[float, float] | None:
    """Centre of a 4- or 6-character Maidenhead locator."""
    g = (grid or "").strip().upper()
    if len(g) not in (4, 6, 8) or not re.match(r"^[A-R]{2}\d{2}([A-X]{2})?([0-9]{2})?$", g):
        return None
    lon = (ord(g[0]) - ord("A")) * 20 - 180
    lat = (ord(g[1]) - ord("A")) * 10 - 90
    lon += int(g[2]) * 2
    lat += int(g[3]) * 1
    if len(g) >= 6:
        lon += (ord(g[4]) - ord("A")) * (2 / 24)
        lat += (ord(g[5]) - ord("A")) * (1 / 24)
        lon += 2 / 24 / 2
        lat += 1 / 24 / 2
    else:
        lon += 1.0  # centre of 2° × 1° square
        lat += 0.5
    return lat, lon


def record_to_point(rec: dict[str, str]) -> dict | None:
    lat = parse_qrz_coord(rec.get("lat", ""))
    lon = parse_qrz_coord(rec.get("lon", ""))
    grid = (rec.get("gridsquare") or "").strip().upper() or None
    if lat is None or lon is None:
        if grid:
            mh = maidenhead_to_latlon(grid)
            if mh:
                lat, lon = mh
    if lat is None or lon is None:
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    status = (rec.get("app_qrzlog_status") or "").strip().upper()
    confirmed = status == "C" or (rec.get("lotw_qsl_rcvd") or "").upper() in ("Y", "V")
    return {
        "call": rec["call"].strip().upper(),
        "band": (rec.get("band") or "").strip().lower() or None,
        "mode": (rec.get("mode") or "").strip().upper() or None,
        "date": (rec.get("qso_date") or "").strip() or None,
        "time": (rec.get("time_on") or "").strip() or None,
        "grid": grid,
        "country": (rec.get("country") or "").strip() or None,
        "lat": round(lat, 5),
        "lon": round(lon, 5),
        "confirmed": confirmed,
    }


def fetch_all() -> tuple[list[dict[str, str]], dict[str, str]]:
    status_raw = api_post({"ACTION": "STATUS"})
    status, _ = parse_response(status_raw)
    if status.get("RESULT") != "OK":
        die(f"STATUS failed: {status.get('RESULT')} {status.get('REASON', '')}".strip())

    all_recs: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    after: str | None = None
    while True:
        option = f"MAX:{PAGE_SIZE}"
        if after:
            option += f",AFTERLOGID:{after}"
        raw = api_post({"ACTION": "FETCH", "OPTION": option})
        header, adif = parse_response(raw)
        if header.get("RESULT") != "OK":
            die(f"FETCH failed: {header.get('RESULT')} {header.get('REASON', '')}".strip())
        recs = parse_adif_records(adif)
        if not recs:
            break
        new = 0
        last_id = None
        for rec in recs:
            lid = rec.get("app_qrzlog_logid")
            if lid and lid in seen_ids:
                continue
            if lid:
                seen_ids.add(lid)
                last_id = lid
            all_recs.append(rec)
            new += 1
        print(f"fetched page: {len(recs)} records ({new} new), total {len(all_recs)}")
        if len(recs) < PAGE_SIZE or not last_id or new == 0:
            break
        # QRZ AFTERLOGID appears inclusive of the given id; advance past last seen
        after = last_id
    return all_recs, status


def home_from_records(recs: list[dict[str, str]]) -> dict | None:
    grids = [
        (r.get("my_gridsquare") or "").strip().upper()
        for r in recs
        if (r.get("my_gridsquare") or "").strip()
    ]
    if not grids:
        return None
    # Prefer the most common station grid (portable ops are rarer)
    grid, _ = Counter(grids).most_common(1)[0]
    mh = maidenhead_to_latlon(grid)
    if not mh:
        return None
    lat, lon = mh
    return {"grid": grid, "lat": round(lat, 5), "lon": round(lon, 5), "label": "SM4T"}


def main() -> None:
    recs, status = fetch_all()
    points: list[dict] = []
    skipped = 0
    for rec in recs:
        pt = record_to_point(rec)
        if pt:
            points.append(pt)
        else:
            skipped += 1

    # Newest first
    points.sort(key=lambda p: (p.get("date") or "", p.get("time") or ""), reverse=True)

    with_grid = sum(1 for p in points if p.get("grid"))
    confirmed = sum(1 for p in points if p.get("confirmed"))
    home = home_from_records(recs)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    summary = {
        "generated": generated,
        "callsign": status.get("CALLSIGN", "SM4T"),
        "bookName": status.get("BOOK_NAME"),
        "totalInLog": int(status.get("COUNT") or len(recs)),
        "plotted": len(points),
        "skippedNoLocation": skipped,
        "withGrid": with_grid,
        "confirmed": confirmed,
        "dxcc": int(status.get("DXCC_COUNT") or 0),
        "home": home,
        "bands": dict(Counter(p["band"] for p in points if p.get("band")).most_common()),
        "modes": dict(Counter(p["mode"] for p in points if p.get("mode")).most_common()),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    qsos_path = OUT_DIR / "qsos.json"
    summary_path = OUT_DIR / "qso-summary.json"
    qsos_path.write_text(json.dumps(points, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {qsos_path.relative_to(REPO_ROOT)} ({len(points)} QSOs)")
    print(f"wrote {summary_path.relative_to(REPO_ROOT)}")
    print(
        f"summary: plotted={len(points)} skipped={skipped} withGrid={with_grid} "
        f"confirmed={confirmed} home={home['grid'] if home else None}"
    )


if __name__ == "__main__":
    main()
