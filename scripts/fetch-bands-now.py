#!/usr/bin/env python3
"""Collect "which bands are open right now" data for the leif.radio front page.

Writes static/data/bands-now.json (gitignored; produced during the Pages build).

Method
  * Source: Reverse Beacon Network's public spots.php (the same JSON the RBN
    web page polls), CW only, max age 60 minutes, filtered to skimmers near
    Borlänge (JP70RM).
  * Skimmers: currently active RBN skimmers with a Nordic prefix within
    MAX_KM of JP70RM. If fewer than MIN_SKIMMERS are active, the nearest other
    skimmers within MAX_KM are added.
  * spots.php returns at most 100 spots per request, newest first. We ask
    once per band; if a band hits the cap, we ask again per DX continent for
    that band, so quieter continents are not crowded out by EU. A cell that
    still hits the cap is marked "capped" (its count is a lower bound).
  * Each cell = number of distinct DX calls on that continent heard on that
    band in the last 60 min. Continents come from cty.dat (country-files.com,
    copy in scripts/data/cty.dat).
  * Kp and 10.7 cm flux from NOAA SWPC JSON.

Never raises out of main: on failure it writes {"ok": false, ...} so the
build continues and the page shows "data saknas".
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "data" / "bands-now.json"
CTY = Path(__file__).resolve().parent / "data" / "cty.dat"

UA = "Leif.radio-bands/1.0 (SM4T; https://leif.radio/)"
RBN = "https://www.reversebeacon.net/spots.php"
KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
FLUX_URL = "https://services.swpc.noaa.gov/products/summary/10cm-flux.json"

HOME = (60.5208, 15.4583)  # JP70RM
GRID = "JP70RM"
MAX_KM = 1000
MIN_SKIMMERS = 4
WINDOW_S = 3600
CAP = 100
PAUSE_S = 0.6  # be polite between requests

BANDS = [(80, 7), (40, 12), (30, 17), (20, 22), (17, 27), (15, 32), (12, 37), (10, 42)]
CONTS = ["EU", "NA", "SA", "AF", "AS", "OC"]
# Thresholds for the colour levels (distinct stations per cell, 60 min)
LEVELS = [1, 3, 10]  # >=1 level 1 (yellow), >=3 level 2, >=10 level 3 (green)

NORDIC = re.compile(
    r"^(S[A-M]|7S|8S|L[A-N]|J[WX]|O[F-J]|O[UVZ]|5[PQ]|OX|XP|OY|TF)\d"
)


def get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:  # spots.php answers 400 + JSON for a stale hash
        if e.code == 400:
            return e.read()
        raise


def km(a: tuple[float, float], b: tuple[float, float]) -> float:
    p = math.pi / 180
    h = math.sin((b[0] - a[0]) * p / 2) ** 2 + math.cos(a[0] * p) * math.cos(b[0] * p) * math.sin((b[1] - a[1]) * p / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


# --- cty.dat ---------------------------------------------------------------

class Cty:
    def __init__(self, path: Path):
        self.prefix: dict[str, str] = {}
        self.exact: dict[str, str] = {}
        text = path.read_text(encoding="latin-1")
        for rec in text.split(";"):
            rec = rec.strip()
            if not rec:
                continue
            head, _, rest = rec.partition("\n")
            f = head.split(":")
            if len(f) < 8:
                continue
            cont = f[3].strip()
            items = [f[7].strip()] + [x.strip() for x in rest.replace("\n", "").split(",")]
            for it in items:
                if not it:
                    continue
                exact = it.startswith("=")
                ccont = cont
                m = re.search(r"\{(\w\w)\}", it)
                if m:
                    ccont = m.group(1)
                key = re.sub(r"[=*]|\(.*?\)|\[.*?\]|\{.*?\}|<.*?>|~.*?~", "", it).upper()
                if not key:
                    continue
                (self.exact if exact else self.prefix)[key] = ccont
        self.maxlen = max(len(k) for k in self.prefix)

    def lookup_one(self, call: str) -> str | None:
        if call in self.exact:
            return self.exact[call]
        for n in range(min(len(call), self.maxlen), 0, -1):
            c = self.prefix.get(call[:n])
            if c:
                return c
        return None

    def cont(self, call: str) -> str | None:
        call = call.upper().strip()
        if call in self.exact:
            return self.exact[call]
        if "/" in call:
            parts = [p for p in call.split("/") if p and p not in {"P", "M", "MM", "AM", "QRP", "A", "B", "R", "LH"} and not re.fullmatch(r"\d", p)]
            if not parts:
                return None
            if len(parts) > 1:
                # The shorter part is normally the location prefix (EA8/DF4UE).
                parts.sort(key=len)
            call = parts[0]
        return self.lookup_one(call)


# --- RBN -------------------------------------------------------------------

class Rbn:
    def __init__(self):
        self.h = ""
        self.requests = 0

    def query(self, **params: str) -> dict:
        for _ in range(2):
            q = {"h": self.h, "m": "1", "s": "0", "r": str(CAP), **params}
            if not self.h:
                q = {}
            if self.requests:
                time.sleep(PAUSE_S)
            self.requests += 1
            d = json.loads(get(RBN + "?" + urllib.parse.urlencode(q)).decode("utf-8"))
            if d.get("ver_h") and d.get("ver_h") != self.h:
                self.h = str(d["ver_h"])
                if not q or d.get("error") == 888:
                    continue
            if d.get("error"):
                raise RuntimeError(f"spots.php error {d.get('error')}")
            return d
        raise RuntimeError("spots.php: could not get a valid hash")


def pick_skimmers(spotters: list) -> list[dict]:
    active = []
    for s in spotters:
        if not isinstance(s, list) or len(s) < 3 or s[1] is None or s[2] is None:
            continue
        d = km(HOME, (float(s[1]), float(s[2])))
        if d <= MAX_KM:
            active.append({"call": str(s[0]).upper(), "km": round(d), "nordic": bool(NORDIC.match(str(s[0]).upper()))})
    active.sort(key=lambda x: x["km"])
    chosen = [a for a in active if a["nordic"]]
    if len(chosen) < MIN_SKIMMERS:
        for a in active:
            if a not in chosen:
                chosen.append(a)
            if len(chosen) >= MIN_SKIMMERS:
                break
    chosen.sort(key=lambda x: x["km"])
    return chosen


def collect() -> dict:
    cty = Cty(CTY)
    rbn = Rbn()
    first = rbn.query(ma=str(WINDOW_S), spotters="1")
    skimmers = pick_skimmers(first.get("spotters") or [])
    if not skimmers:
        raise RuntimeError("no active skimmers near JP70RM")
    cde = ",".join(s["call"] for s in skimmers)

    cells: dict[str, dict[str, set]] = {f"{m}m": {c: set() for c in CONTS} for m, _ in BANDS}
    capped: dict[str, list[str]] = {}
    heard_by: dict[str, int] = {}
    seen_ids: set[str] = set()
    now = int(time.time())
    cutoff = now - WINDOW_S

    def absorb(band: str, d: dict) -> int:
        n = 0
        for sid, row in (d.get("spots") or {}).items():
            if not isinstance(row, list) or len(row) < 11 or sid in seen_ids:
                continue
            seen_ids.add(sid)
            de, dx, epoch = str(row[0]).upper(), str(row[2]).upper(), int(row[10] or 0)
            if epoch < cutoff:
                continue
            n += 1
            c = cty.cont(dx)
            if c in cells[band]:
                cells[band][c].add(dx)
            heard_by[de] = heard_by.get(de, 0) + 1
        return n

    for meters, code in BANDS:
        band = f"{meters}m"
        d = rbn.query(cde=cde, b=str(code), ma=str(WINDOW_S))
        rows = len(d.get("spots") or {})
        absorb(band, d)
        if rows >= CAP:
            # Re-ask per continent so EU does not hide the rest.
            for c in CONTS:
                dc = rbn.query(cde=cde, b=str(code), ma=str(WINDOW_S), cox=c)
                absorb(band, dc)
                if len(dc.get("spots") or {}) >= CAP:
                    capped.setdefault(band, []).append(c)

    for s in skimmers:
        s["spots"] = heard_by.get(s["call"], 0)
        s.pop("nordic", None)

    return {
        "bands": [
            {"band": f"{m}m", "cells": {c: len(cells[f"{m}m"][c]) for c in CONTS}, "capped": capped.get(f"{m}m", [])}
            for m, _ in BANDS
        ],
        "skimmers": skimmers,
        "requests": rbn.requests,
    }


def solar() -> dict:
    out: dict = {"ok": False}
    try:
        kp = json.loads(get(KP_URL, 20))
        last = kp[-1]
        if isinstance(last, dict):
            out["kp"], out["kpTime"] = float(last["Kp"]), last["time_tag"] + "Z"
        else:  # older list-of-lists format
            out["kp"], out["kpTime"] = float(last[1]), str(last[0]).replace(" ", "T")[:19] + "Z"
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["kpError"] = str(e)
    try:
        fl = json.loads(get(FLUX_URL, 20))
        row = fl[-1] if isinstance(fl, list) else fl
        out["sfi"] = int(float(row.get("flux") or row.get("Flux")))
        out["sfiTime"] = str(row.get("time_tag") or row.get("TimeStamp"))[:19] + "Z"
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["sfiError"] = str(e)
    return out


def main() -> int:
    updated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    doc: dict = {
        "ok": False, "updated": updated, "grid": GRID, "windowMinutes": WINDOW_S // 60,
        "mode": "CW", "continents": CONTS, "levels": LEVELS, "source": "Reverse Beacon Network (spots.php)",
    }
    try:
        doc.update(collect())
        doc["ok"] = True
    except Exception as e:  # noqa: BLE001
        doc["error"] = f"{type(e).__name__}: {e}"
        print(f"fetch-bands-now: {doc['error']}", file=sys.stderr)
    doc["solar"] = solar()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"fetch-bands-now: ok={doc['ok']} requests={doc.get('requests')} -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
