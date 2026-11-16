#!/usr/bin/env python3
"""Fetch SM4T reception data for the leif.radio live-status box.

Writes data/live-status.json and static/data/live-status.json (both gitignored).
Never raises out of main: a failed fetch writes a fallback document so the
Hugo build can still run.

Sources (all public, no API key):
  - Reverse Beacon Network spots.php (recent spots + skimmer coordinates)
  - RBN daily history zips for completed UTC days in the 24 h window
  - PSKReporter retrieve query for the last 24 h (non-CW / digital only)
  - N0NBH solar XML at hamqsl.com

Callsign rule: dx/sender must be exactly SM4T or SM4T/… .
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import math
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "Leif.radio-status/1.0 (SM4T; https://leif.radio/)"
CALL = "SM4T"
WINDOW_HOURS = 24
QRV_MINUTES = 30
RBN_SPOTS_URL = "https://www.reversebeacon.net/spots.php"
RBN_HISTORY_URL = "https://data.reversebeacon.net/rbn_history/{date}.zip"
PSK_URL = "https://retrieve.pskreporter.info/query"
SOLAR_URL = "https://www.hamqsl.com/solarxml.php"
# Public RBN redistributor with CORS; also used as a build-time supplement.
# The /spots/SM4T endpoint is a prefix match (it also returns SM4TIW etc.),
# so every row is still filtered with is_our_call().
VAIL_URL = "https://vailrerbn.com/api/v1/spots/SM4T?hours=24"
# JP70RM / Borlänge, used if RBN call_info for SM4T is missing
HOME_FALLBACK = {"lat": 60.5208, "lon": 15.4583, "grid": "JP70RM"}

# RBN band codes from /spots.php?meta=1 (meters lookup)
BAND_CODE_METERS = {
    91: 630, 3: 160, 7: 80, 84: 60, 12: 40, 17: 30,
    22: 20, 27: 17, 32: 15, 37: 12, 42: 10, 50: 6, 55: 4, 62: 2,
}
# tx_mode / mode codes from the same meta document
MODE_CODES = {
    1: "CW", 2: "SSB", 5: "FM", 10: "PSK31", 11: "RTTY", 12: "BPSK",
    13: "GMSK", 14: "FSK", 15: "SSTV", 16: "MFSK", 17: "QPSK",
    21: "JT65", 32: "JT9", 34: "FT8", 38: "MSK144", 44: "JS8", 45: "FT4",
    999: "other",
}
# Frequency edges in kHz, longest wavelength first
BAND_EDGES = (
    ("160m", 1800, 2000),
    ("80m", 3500, 4000),
    ("60m", 5351, 5450),
    ("40m", 7000, 7300),
    ("30m", 10100, 10150),
    ("20m", 14000, 14350),
    ("17m", 18068, 18168),
    ("15m", 21000, 21450),
    ("12m", 24890, 24990),
    ("10m", 28000, 29700),
    ("6m", 50000, 54000),
    ("4m", 70000, 70500),
    ("2m", 144000, 148000),
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SPOT_FIELDS = ("de", "freq", "dx", "db", "wpm", "time", "diff", "band", "type", "mode", "epoch")
CALL_INFO_FIELDS = ("pfx", "country", "cont", "ccode", "ituz", "cqz", "lat", "long", "grid", "gsrc")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def is_our_call(dx: str | None) -> bool:
    call = (dx or "").strip().upper()
    return call == CALL or call.startswith(CALL + "/")


def norm_spotter(call: str | None) -> str:
    """RBN skimmers often appear as ON6URE-1 officially and ON6URE on Vail."""
    return re.sub(r"-\d+$", "", (call or "").strip().upper())


def band_from_freq(freq_khz: float | None, band_code: int | None = None) -> str:
    if band_code is not None and band_code in BAND_CODE_METERS:
        return f"{BAND_CODE_METERS[band_code]}m"
    if freq_khz is None:
        return ""
    for name, lo, hi in BAND_EDGES:
        if lo <= freq_khz <= hi:
            return name
    return ""


def mode_name(code: Any, raw: str | None = None) -> str:
    if raw:
        text = raw.strip()
        if text:
            return text.upper()
    try:
        return MODE_CODES.get(int(code), "") or ""
    except (TypeError, ValueError):
        return ""


def parse_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def http_get(url: str, timeout: int = 30, allow_http_errors: tuple[int, ...] = ()) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        body = exc.read() if exc.fp is not None else b""
        if exc.code in allow_http_errors:
            return body
        # Re-raise, but keep the body available on the exception for callers.
        exc._body = body  # type: ignore[attr-defined]
        raise


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def fallback_doc(now: datetime, reason: str) -> dict[str, Any]:
    return {
        "ok": False,
        "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "windowHours": WINDOW_HOURS,
        "qrv": False,
        "error": reason,
        "rbn": {"ok": False},
        "psk": {"ok": False},
        "solar": {"ok": False},
        "home": HOME_FALLBACK,
    }


# --- RBN spots.php ---------------------------------------------------------

def _spots_query(params: dict[str, str], timeout: int = 30) -> dict[str, Any]:
    url = RBN_SPOTS_URL + "?" + urllib.parse.urlencode(params)
    # A missing or stale `h` hash is returned as HTTP 400 with JSON {error:888, ver_h:…}.
    raw = http_get(url, timeout=timeout, allow_http_errors=(400,))
    if not raw:
        raise RuntimeError("RBN spots.php returned an empty body")
    return json.loads(raw.decode("utf-8"))


def fetch_spots_php(cutoff_epoch: int) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Return (spots, call_info) for SM4T in the window. Raises on hard failure."""
    # The site requires a short version hash `h`. A request without it returns
    # {"error": 888, "ver_h": "..."}; we then retry with that hash.
    first = _spots_query({})
    ver_h = str(first.get("ver_h") or "")
    if not ver_h:
        raise RuntimeError("RBN spots.php did not return ver_h")

    ma = max(1, int(time.time()) - cutoff_epoch + 60)
    payload = _spots_query({"h": ver_h, "cdx": CALL, "s": "0", "r": "100", "ma": str(ma)})
    if payload.get("error") == 888 and payload.get("ver_h"):
        ver_h = str(payload["ver_h"])
        payload = _spots_query({"h": ver_h, "cdx": CALL, "s": "0", "r": "100", "ma": str(ma)})
    if payload.get("error"):
        raise RuntimeError(f"RBN spots.php error {payload.get('error')}")

    call_info: dict[str, dict[str, Any]] = {}
    for call, values in (payload.get("call_info") or {}).items():
        if not isinstance(values, list):
            continue
        info = {CALL_INFO_FIELDS[i]: values[i] if i < len(values) else None for i in range(len(CALL_INFO_FIELDS))}
        lat, lon = parse_float(info.get("lat")), parse_float(info.get("long"))
        call_info[str(call).upper()] = {
            "call": str(call),
            "country": (info.get("country") or "").strip(),
            "cont": (info.get("cont") or "").strip(),
            "lat": lat,
            "lon": lon,
            "grid": (info.get("grid") or "").strip(),
        }

    spots: list[dict[str, Any]] = []
    for _sid, values in (payload.get("spots") or {}).items():
        if not isinstance(values, list) or len(values) < 11:
            continue
        row = {SPOT_FIELDS[i]: values[i] if i < len(values) else None for i in range(len(SPOT_FIELDS))}
        dx = str(row.get("dx") or "")
        if not is_our_call(dx):
            continue
        epoch = parse_int(row.get("epoch"))
        if epoch is None or epoch < cutoff_epoch:
            continue
        freq = parse_float(row.get("freq"))
        band_code = parse_int(row.get("band"))
        spots.append({
            "source": "spots.php",
            "spotter": str(row.get("de") or "").strip(),
            "dx": dx.strip(),
            "freq": freq,
            "band": band_from_freq(freq, band_code),
            "mode": mode_name(row.get("mode")),
            "snr": parse_int(row.get("db")),
            "epoch": epoch,
        })
    return spots, call_info


# --- RBN daily history zips ------------------------------------------------

def parse_history_date(value: str) -> int | None:
    text = (value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return int(datetime.strptime(text, fmt).replace(tzinfo=timezone.utc).timestamp())
        except ValueError:
            continue
    return None


def fetch_history_day(day: datetime, cutoff_epoch: int) -> list[dict[str, Any]]:
    """Download one completed UTC day's zip and return matching spots. 404 → []."""
    date_str = day.strftime("%Y%m%d")
    url = RBN_HISTORY_URL.format(date=date_str)
    try:
        raw = http_get(url, timeout=90)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return []
        raise
    spots: list[dict[str, Any]] = []
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        names = zf.namelist()
        if not names:
            return []
        with zf.open(names[0]) as handle:
            text = io.TextIOWrapper(handle, encoding="utf-8", errors="replace", newline="")
            reader = csv.DictReader(text)
            for row in reader:
                dx = row.get("dx") or ""
                if not is_our_call(dx):
                    continue
                epoch = parse_history_date(row.get("date") or "")
                if epoch is None or epoch < cutoff_epoch:
                    continue
                freq = parse_float(row.get("freq"))
                band = (row.get("band") or "").strip() or band_from_freq(freq)
                if band and not band.endswith("m") and band.isdigit():
                    band = f"{band}m"
                spots.append({
                    "source": "rbn_history",
                    "spotter": (row.get("callsign") or "").strip(),
                    "dx": dx.strip(),
                    "freq": freq,
                    "band": band,
                    "mode": mode_name(None, row.get("tx_mode") or row.get("mode")),
                    "snr": parse_int(row.get("db")),
                    "epoch": epoch,
                })
    return spots


def history_days(now: datetime) -> list[datetime]:
    """Completed UTC days that overlap the 24 h window (never 'today')."""
    cutoff = now - timedelta(hours=WINDOW_HOURS)
    days: list[datetime] = []
    day = cutoff.date()
    today = now.date()
    while day < today:
        days.append(datetime(day.year, day.month, day.day, tzinfo=timezone.utc))
        day += timedelta(days=1)
    return days


def _spot_rank(spot: dict[str, Any]) -> tuple[int, int, int]:
    """Later epoch wins; official RBN beats Vail; stronger SNR is the last tie-break."""
    src = spot.get("source") or ""
    official = 2 if src == "spots.php" or src.startswith("rbn_history") else 1
    return (int(spot.get("epoch") or 0), official, int(spot.get("snr") or -99))


def parse_iso_epoch(value: str) -> int | None:
    text = (value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return int(datetime.fromisoformat(text).timestamp())
    except ValueError:
        return None


def fetch_vailrerbn(cutoff_epoch: int) -> list[dict[str, Any]]:
    """24 h spots from Vail ReRBN. Prefix match, so apply is_our_call()."""
    raw = http_get(VAIL_URL, timeout=20)
    payload = json.loads(raw.decode("utf-8"))
    spots: list[dict[str, Any]] = []
    for row in payload.get("spots") or []:
        if not isinstance(row, dict):
            continue
        dx = str(row.get("callsign") or "")
        if not is_our_call(dx):
            continue
        epoch = parse_iso_epoch(str(row.get("timestamp") or ""))
        if epoch is None or epoch < cutoff_epoch:
            continue
        freq = parse_float(row.get("frequency"))
        spots.append({
            "source": "vailrerbn",
            "spotter": str(row.get("spotter") or "").strip(),
            "dx": dx.strip(),
            "freq": freq,
            "band": band_from_freq(freq),
            "mode": mode_name(None, row.get("mode")),
            "snr": parse_int(row.get("snr")),
            "epoch": epoch,
            "grid": (row.get("spotter_grid") or "").strip(),
        })
    return spots


def dedup_spots(spots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse the same reception reported by both spots.php and a history zip."""
    chosen: dict[tuple[Any, ...], dict[str, Any]] = {}
    for spot in spots:
        freq = spot.get("freq")
        freq_key = int(round(freq)) if isinstance(freq, (int, float)) else None
        epoch = spot.get("epoch") or 0
        key = (
            norm_spotter(spot.get("spotter")),
            (spot.get("dx") or "").upper(),
            freq_key,
            int(epoch) // 120,
        )
        prev = chosen.get(key)
        if prev is None or _spot_rank(spot) > _spot_rank(prev):
            chosen[key] = spot
    return list(chosen.values())


# --- PSKReporter -----------------------------------------------------------

def locator_to_latlon(locator: str) -> tuple[float, float] | None:
    loc = (locator or "").strip().upper()
    if len(loc) < 4 or not loc[0].isalpha() or not loc[1].isalpha():
        return None
    if not (loc[2].isdigit() and loc[3].isdigit()):
        return None
    lon = (ord(loc[0]) - ord("A")) * 20 - 180
    lat = (ord(loc[1]) - ord("A")) * 10 - 90
    lon += int(loc[2]) * 2
    lat += int(loc[3]) * 1
    if len(loc) >= 6 and loc[4].isalpha() and loc[5].isalpha():
        lon += (ord(loc[4]) - ord("A") + 0.5) * (2 / 24)
        lat += (ord(loc[5]) - ord("A") + 0.5) * (1 / 24)
    else:
        lon += 1.0
        lat += 0.5
    return lat, lon


def fetch_psk(cutoff_epoch: int) -> dict[str, Any]:
    params = {
        "senderCallsign": CALL,
        "flowStartSeconds": str(-WINDOW_HOURS * 3600),
        "rronly": "1",
    }
    url = PSK_URL + "?" + urllib.parse.urlencode(params)
    raw = http_get(url, timeout=45)
    root = ET.fromstring(raw)
    reports: list[dict[str, Any]] = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag.lower() != "receptionreport":
            continue
        sender = el.get("senderCallsign") or el.get("sendercallsign") or ""
        if not is_our_call(sender):
            continue
        flow = parse_int(el.get("flowStartSeconds") or el.get("flowstartseconds"))
        if flow is not None and flow < cutoff_epoch:
            continue
        recv = (el.get("receiverCallsign") or el.get("receivercallsign") or "").strip()
        locator = (el.get("receiverLocator") or el.get("receiverlocator") or "").strip()
        coords = locator_to_latlon(locator)
        freq_hz = parse_float(el.get("frequency"))
        freq_khz = (freq_hz / 1000.0) if freq_hz and freq_hz > 1000 else freq_hz
        mode = (el.get("mode") or "").strip().upper()
        # CW on PSKReporter is almost always a duplicate of an RBN spot.
        if mode == "CW":
            continue
        reports.append({
            "receiver": recv,
            "locator": locator,
            "lat": coords[0] if coords else None,
            "lon": coords[1] if coords else None,
            "band": band_from_freq(freq_khz),
            "mode": mode,
            "snr": parse_int(el.get("sNR") or el.get("snr")),
            "epoch": flow,
        })
    receivers: list[dict[str, Any]] = []
    by_recv: dict[str, dict[str, Any]] = {}
    for rep in reports:
        key = (rep.get("receiver") or "").upper() or (rep.get("locator") or "")
        if not key:
            continue
        slot = by_recv.setdefault(key, {
            "call": rep.get("receiver") or "",
            "lat": rep.get("lat"),
            "lon": rep.get("lon"),
            "count": 0,
            "lastBand": "",
            "lastMode": "",
            "lastSnr": None,
            "lastEpoch": 0,
        })
        slot["count"] += 1
        if (rep.get("epoch") or 0) >= (slot.get("lastEpoch") or 0):
            slot["lastBand"] = rep.get("band") or ""
            slot["lastMode"] = rep.get("mode") or ""
            slot["lastSnr"] = rep.get("snr")
            slot["lastEpoch"] = rep.get("epoch") or 0
            if rep.get("lat") is not None:
                slot["lat"] = rep.get("lat")
                slot["lon"] = rep.get("lon")
    receivers = list(by_recv.values())
    return {"ok": True, "reportCount": len(reports), "receivers": receivers}


# --- Solar -----------------------------------------------------------------

def fetch_solar() -> dict[str, Any]:
    raw = http_get(SOLAR_URL, timeout=20)
    root = ET.fromstring(raw)
    def text(*names: str) -> str:
        for name in names:
            el = root.find(f".//{name}")
            if el is not None and el.text and el.text.strip():
                return el.text.strip()
        return ""

    sfi_raw, k_raw, a_raw, updated = text("solarflux"), text("kindex"), text("aindex"), text("updated")
    sfi, k_index, a_index = parse_int(sfi_raw), parse_int(k_raw), parse_int(a_raw)
    if sfi is None and k_index is None:
        raise RuntimeError("solar XML missing SFI and K-index")
    return {
        "ok": True,
        "sfi": sfi,
        "kIndex": k_index,
        "aIndex": a_index,
        "updated": updated,
        "source": "N0NBH / hamqsl.com",
    }


# --- Assemble --------------------------------------------------------------

def home_from_call_info(call_info: dict[str, dict[str, Any]]) -> dict[str, Any]:
    info = call_info.get(CALL)
    if info and info.get("lat") is not None and info.get("lon") is not None:
        return {"lat": info["lat"], "lon": info["lon"], "grid": info.get("grid") or HOME_FALLBACK["grid"]}
    return dict(HOME_FALLBACK)


def build_rbn(
    spots: list[dict[str, Any]],
    call_info: dict[str, dict[str, Any]],
    home: dict[str, Any],
    sources_used: list[str],
    limited: bool,
) -> dict[str, Any]:
    # Most recent first for last-heard; equal timestamps prefer the stronger SNR.
    spots = sorted(spots, key=lambda s: (s.get("epoch") or 0, s.get("snr") or -99))
    by_band: dict[str, int] = defaultdict(int)
    skimmers: dict[str, dict[str, Any]] = {}
    farthest: dict[str, Any] | None = None

    for spot in spots:
        band = spot.get("band") or ""
        if band:
            by_band[band] += 1
        call = (spot.get("spotter") or "").strip()
        if not call:
            continue
        info = call_info.get(call.upper()) or {}
        lat = info.get("lat")
        lon = info.get("lon")
        km = None
        if lat is not None and lon is not None:
            km = round(haversine_km(home["lat"], home["lon"], lat, lon))
        slot = skimmers.setdefault(call.upper(), {
            "call": call,
            "country": info.get("country") or "",
            "lat": lat,
            "lon": lon,
            "grid": info.get("grid") or "",
            "km": km,
            "count": 0,
            "lastBand": "",
            "lastSnr": None,
            "lastEpoch": 0,
        })
        slot["count"] += 1
        if (spot.get("epoch") or 0) >= (slot.get("lastEpoch") or 0):
            slot["lastBand"] = spot.get("band") or ""
            slot["lastSnr"] = spot.get("snr")
            slot["lastEpoch"] = spot.get("epoch") or 0
    last = spots[-1] if spots else None
    last_heard = None
    if last:
        last_heard = {
            "time": datetime.fromtimestamp(last["epoch"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "epoch": last["epoch"],
            "band": last.get("band") or "",
            "mode": last.get("mode") or "",
            "spotter": last.get("spotter") or "",
            "snr": last.get("snr"),
            "freq": last.get("freq"),
        }

    band_order = {name: i for i, (name, *_rest) in enumerate(BAND_EDGES)}
    by_band_list = [
        {"band": band, "count": by_band[band]}
        for band in sorted(by_band, key=lambda b: band_order.get(b, 99))
    ]
    skimmer_list = sorted(skimmers.values(), key=lambda s: (-(s.get("km") or -1), s["call"]))
    with_km = [s for s in skimmer_list if s.get("km") is not None]
    if with_km:
        far = with_km[0]
        farthest = {
            "spotter": far["call"],
            "km": far["km"],
            "country": far.get("country") or "",
            "band": far.get("lastBand") or "",
            "snr": far.get("lastSnr"),
            "time": datetime.fromtimestamp(far["lastEpoch"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if far.get("lastEpoch") else None,
        }

    compact = [
        {
            "spotter": s.get("spotter") or "",
            "dx": s.get("dx") or CALL,
            "band": s.get("band") or "",
            "mode": s.get("mode") or "",
            "snr": s.get("snr"),
            "freq": s.get("freq"),
            "epoch": s.get("epoch"),
        }
        for s in spots
    ]
    return {
        "ok": True,
        "spotCount": len(spots),
        "byBand": by_band_list,
        "lastHeard": last_heard,
        "farthest": farthest,
        "skimmers": skimmer_list,
        "spots": compact,
        "sources": sources_used,
        "limited": limited,
    }


def collect() -> dict[str, Any]:
    now = utcnow()
    cutoff = now - timedelta(hours=WINDOW_HOURS)
    cutoff_epoch = int(cutoff.timestamp())
    rbn_spots: list[dict[str, Any]] = []
    call_info: dict[str, dict[str, Any]] = {}
    rbn_errors: list[str] = []
    sources_used: list[str] = []
    php_count = 0

    try:
        php_spots, call_info = fetch_spots_php(cutoff_epoch)
        rbn_spots.extend(php_spots)
        php_count = len(php_spots)
        sources_used.append("spots.php")
    except Exception as exc:
        rbn_errors.append(f"spots.php: {exc}")

    # spots.php returns at most 100 rows. If we got fewer than that for the
    # 24 h window, the live query is already complete and we can skip the
    # daily zips (they only exist for finished UTC days anyway).
    try:
        vail_spots = fetch_vailrerbn(cutoff_epoch)
        if vail_spots:
            rbn_spots.extend(vail_spots)
            sources_used.append("vailrerbn")
            # Grids from Vail fill in skimmers that spots.php did not geocode.
            for spot in vail_spots:
                call = (spot.get("spotter") or "").upper()
                grid = spot.get("grid") or ""
                if not call or call in call_info or not grid:
                    continue
                coords = locator_to_latlon(grid)
                if not coords:
                    continue
                call_info[call] = {
                    "call": spot.get("spotter") or "",
                    "country": "",
                    "cont": "",
                    "lat": coords[0],
                    "lon": coords[1],
                    "grid": grid,
                }
    except Exception as exc:
        rbn_errors.append(f"vailrerbn: {exc}")

    need_history = "spots.php" not in sources_used or php_count >= 100
    if need_history:
        for day in history_days(now):
            try:
                hist = fetch_history_day(day, cutoff_epoch)
                if hist:
                    rbn_spots.extend(hist)
                    sources_used.append(f"rbn_history:{day.strftime('%Y%m%d')}")
            except Exception as exc:
                rbn_errors.append(f"rbn_history {day.strftime('%Y%m%d')}: {exc}")

    rbn: dict[str, Any]
    home = home_from_call_info(call_info)
    if rbn_spots or "spots.php" in sources_used:
        merged = dedup_spots(rbn_spots)
        # spots.php caps at 100 rows; if we hit that cap and have no zip for
        # today, today's count may be incomplete.
        limited = php_count >= 100
        rbn = build_rbn(merged, call_info, home, sources_used, limited)
        if rbn_errors:
            rbn["warnings"] = rbn_errors
    else:
        rbn = {"ok": False, "error": "; ".join(rbn_errors) if rbn_errors else "no RBN data"}

    try:
        psk = fetch_psk(cutoff_epoch)
    except Exception as exc:
        psk = {"ok": False, "error": str(exc)}

    try:
        solar = fetch_solar()
    except Exception as exc:
        solar = {"ok": False, "error": str(exc)}

    last_epoch = (rbn.get("lastHeard") or {}).get("epoch") if rbn.get("ok") else None
    qrv = bool(last_epoch and (int(now.timestamp()) - int(last_epoch)) <= QRV_MINUTES * 60)

    ok = bool(rbn.get("ok") or psk.get("ok") or solar.get("ok"))
    doc = {
        "ok": ok,
        "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "windowHours": WINDOW_HOURS,
        "qrv": qrv,
        "rbn": rbn,
        "psk": psk,
        "solar": solar,
        "home": home,
    }
    if not ok:
        doc["error"] = "all sources failed"
    return doc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        action="append",
        type=Path,
        help="Output path (repeatable). Defaults to data/ and static/data/ under the repo root.",
    )
    args = parser.parse_args()
    outputs = args.out or [
        REPO_ROOT / "data" / "live-status.json",
        REPO_ROOT / "static" / "data" / "live-status.json",
    ]

    now = utcnow()
    try:
        doc = collect()
    except Exception as exc:
        print(f"error: unexpected failure: {exc}", file=sys.stderr)
        doc = fallback_doc(now, str(exc))

    for path in outputs:
        write_json(path, doc)

    rbn = doc.get("rbn") or {}
    psk = doc.get("psk") or {}
    solar = doc.get("solar") or {}
    last = (rbn.get("lastHeard") or {}) if rbn.get("ok") else {}
    print(
        f"live-status ok={doc.get('ok')} updated={doc.get('updated')} "
        f"rbn={rbn.get('spotCount') if rbn.get('ok') else 'fail'} "
        f"last={last.get('time', '-')} {last.get('band', '')} "
        f"{last.get('spotter', '')} {last.get('snr', '')} "
        f"sources={','.join((rbn.get('sources') or []) if rbn.get('ok') else [])} "
        f"psk={psk.get('reportCount') if psk.get('ok') else 'fail'} "
        f"sfi={solar.get('sfi') if solar.get('ok') else 'fail'} "
        f"k={solar.get('kIndex') if solar.get('ok') else 'fail'} "
        f"qrv={doc.get('qrv')}"
    )
    if rbn.get("warnings"):
        print("warnings: " + "; ".join(rbn["warnings"]))
    # Always exit 0 so a failed fetch cannot break the Pages build.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
