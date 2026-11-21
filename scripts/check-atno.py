#!/usr/bin/env python3
"""Detect new DXCC entities (ATNOs) in the QRZ log and create notiser.

Reads the compact log written by fetch-qrz-map.py (data/qso-log.json),
falling back to static/data/qsos.json. Compares the set of worked DXCC
entities with data/atno-baseline.json.

On the first run (no baseline file) the baseline is initialised with every
entity already in the log, and no notiser are created.

Later runs create a bilingual notis for each new entity via add-notis.py
and then update the baseline. Entities are never removed from the baseline,
so a partial fetch cannot look like a new ATNO later.

Usage:
  python3 scripts/check-atno.py
  python3 scripts/check-atno.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Stockholm")
REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO_ROOT / "data" / "atno-baseline.json"
QSO_LOG_PATH = REPO_ROOT / "data" / "qso-log.json"
QSOS_PATH = REPO_ROOT / "static" / "data" / "qsos.json"
CTY_PATH = REPO_ROOT / "scripts" / "data" / "cty.dat"
ADD_NOTIS = REPO_ROOT / "scripts" / "add-notis.py"

MONTHS_SV = (
    "",
    "januari",
    "februari",
    "mars",
    "april",
    "maj",
    "juni",
    "juli",
    "augusti",
    "september",
    "oktober",
    "november",
    "december",
)
MONTHS_EN = (
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
CONT_SV = {
    "EU": "Europa",
    "NA": "Nordamerika",
    "SA": "Sydamerika",
    "AF": "Afrika",
    "AS": "Asien",
    "OC": "Oceanien",
    "AN": "Antarktis",
}
CONT_EN = {
    "EU": "Europe",
    "NA": "North America",
    "SA": "South America",
    "AF": "Africa",
    "AS": "Asia",
    "OC": "Oceania",
    "AN": "Antarctica",
}
PORTABLE_SUFFIXES = frozenset(
    {"P", "M", "AM", "MM", "QRP", "LH", "J", "JT", "PM", "AE", "AG", "AA"}
)


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


@dataclass(frozen=True)
class CtyEntity:
    name: str
    cq: int | None
    itu: int | None
    cont: str | None
    prefix: str
    aliases: tuple[str, ...] = ()


def _as_int(value: str) -> int | None:
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        return None


def parse_cty(path: Path) -> list[CtyEntity]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks = re.split(r";\s*", text)
    entities: list[CtyEntity] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        header, _, rest = chunk.partition("\n")
        parts = [p.strip() for p in header.split(":")]
        if len(parts) < 8:
            continue
        name, cq_s, itu_s, cont, _lat, _lon, _tz, prefix = parts[:8]
        if not name or not prefix:
            continue
        aliases = tuple(a.strip() for a in rest.replace("\n", "").split(",") if a.strip())
        entities.append(
            CtyEntity(
                name=name.strip(),
                cq=_as_int(cq_s),
                itu=_as_int(itu_s),
                cont=(cont.strip().upper() or None),
                prefix=prefix.strip().lstrip("*"),
                aliases=aliases,
            )
        )
    return entities


def build_cty_indexes(
    entities: list[CtyEntity],
) -> tuple[dict[str, CtyEntity], list[tuple[str, CtyEntity]], dict[str, CtyEntity]]:
    exact: dict[str, CtyEntity] = {}
    prefixes: list[tuple[str, CtyEntity]] = []
    by_name: dict[str, CtyEntity] = {}
    for ent in entities:
        by_name[normalize_name(ent.name)] = ent
        aliases = ent.aliases
        for raw in [ent.prefix, *aliases]:
            token = raw.strip()
            if not token:
                continue
            # Zone / continent overrides in parentheses etc. are stripped for matching.
            token = re.sub(r"[(\[{<].*$", "", token).strip()
            if not token:
                continue
            if token.startswith("="):
                exact[token[1:].upper()] = ent
            else:
                prefixes.append((token.upper(), ent))
    prefixes.sort(key=lambda item: len(item[0]), reverse=True)
    return exact, prefixes, by_name


def normalize_name(name: str) -> str:
    text = unicodedata.normalize("NFKD", name or "")
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"\brepublic of\b", " ", text)
    text = re.sub(r"\bthe\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def call_candidates(call: str) -> list[str]:
    call = (call or "").upper().strip()
    if not call:
        return []
    out: list[str] = [call]
    if "/" not in call:
        return out
    parts = [p for p in call.split("/") if p]
    if len(parts) == 1:
        return out
    if len(parts) >= 3:
        # e.g. KH0/W1AW/QRP → drop trailing portable suffix, then reconsider.
        if parts[-1] in PORTABLE_SUFFIXES or parts[-1].isdigit():
            parts = parts[:-1]
    if len(parts) == 1:
        out.append(parts[0])
        return _unique(out)
    a, b = parts[0], parts[1]
    if b in PORTABLE_SUFFIXES or b.isdigit():
        out.append(a)
    elif len(a) <= len(b):
        # Prefix/call (SM/G3ABC or KH0/W1AW): entity follows the prefix.
        out.extend([a, b])
    else:
        # Call/prefix (G3ABC/SM): entity often follows the suffix.
        out.extend([b, a])
    return _unique(out)


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def lookup_cty(
    call: str,
    exact: dict[str, CtyEntity],
    prefixes: list[tuple[str, CtyEntity]],
) -> CtyEntity | None:
    for cand in call_candidates(call):
        if cand in exact:
            return exact[cand]
        for pfx, ent in prefixes:
            if cand.startswith(pfx):
                return ent
    return None


def load_qsos() -> list[dict]:
    if QSO_LOG_PATH.is_file():
        raw = json.loads(QSO_LOG_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and isinstance(raw.get("qsos"), list):
            return raw["qsos"]
        if isinstance(raw, list):
            return raw
        die(f"{QSO_LOG_PATH.relative_to(REPO_ROOT)} has no qsos list")
    if QSOS_PATH.is_file():
        raw = json.loads(QSOS_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            return raw
        die(f"{QSOS_PATH.relative_to(REPO_ROOT)} is not a list")
    die("no QSO log found; run scripts/fetch-qrz-map.py first")
    raise AssertionError


def entity_key(qso: dict) -> str | None:
    dxcc = qso.get("dxcc")
    if isinstance(dxcc, int) or (isinstance(dxcc, str) and str(dxcc).isdigit()):
        return str(int(dxcc))
    country = (qso.get("country") or "").strip()
    if country:
        return "name:" + normalize_name(country)
    return None


def qso_sort_key(qso: dict) -> tuple[str, str]:
    return (qso.get("date") or "", qso.get("time") or "")


def first_qso_by_entity(qsos: list[dict]) -> dict[str, dict]:
    first: dict[str, dict] = {}
    for qso in sorted(qsos, key=qso_sort_key):
        key = entity_key(qso)
        if not key:
            continue
        if key not in first:
            first[key] = qso
    return first


def facts_for(qso: dict, cty: CtyEntity | None) -> dict:
    name = (qso.get("country") or "").strip() or (cty.name if cty else "")
    cont = (qso.get("cont") or "").strip().upper() or None
    cqz = qso.get("cqz")
    if not isinstance(cqz, int):
        cqz = int(cqz) if isinstance(cqz, str) and cqz.isdigit() else None
    # Fill gaps from cty.dat only when it refers to the same entity.
    if cty and (not name or names_compatible(name, cty.name)):
        name = name or cty.name
        cont = cont or cty.cont
        if cqz is None:
            cqz = cty.cq
    elif cty and not name:
        name = cty.name
        cont = cont or cty.cont
        if cqz is None:
            cqz = cty.cq
    return {
        "name": name or "Unknown entity",
        "cont": cont,
        "cqz": cqz,
        "prefix": cty.prefix if cty else None,
    }


def names_compatible(a: str, b: str) -> bool:
    na, nb = normalize_name(a), normalize_name(b)
    if not na or not nb:
        return False
    return na == nb or na in nb or nb in na


def parse_qso_local(qso: dict) -> datetime | None:
    date = (qso.get("date") or "").strip()
    time = (qso.get("time") or "").strip()
    if not re.fullmatch(r"\d{8}", date):
        return None
    year, month, day = int(date[:4]), int(date[4:6]), int(date[6:8])
    if time and re.fullmatch(r"\d{4,6}", time):
        hour = int(time[:2])
        minute = int(time[2:4])
        second = int(time[4:6]) if len(time) >= 6 else 0
        try:
            utc = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
        except ValueError:
            return None
        return utc.astimezone(TZ)
    try:
        return datetime(year, month, day, tzinfo=timezone.utc)
    except ValueError:
        return None


def format_date(dt: datetime, lang: str) -> str:
    months = MONTHS_SV if lang == "sv" else MONTHS_EN
    return f"{dt.day} {months[dt.month]} {dt.year}"


def format_band(band: str | None) -> str:
    if not band:
        return ""
    band = band.strip().lower()
    if band.endswith("m") and not band.endswith(" m"):
        return f"{band[:-1]} m"
    return band


def slug_for(key: str, facts: dict, qso: dict) -> str:
    prefix = (facts.get("prefix") or "").strip().lower()
    prefix = re.sub(r"[^a-z0-9]+", "", prefix)
    if prefix:
        return f"atno-{prefix}"
    if key.isdigit():
        return f"atno-dxcc-{key}"
    name = slugify(facts.get("name") or qso.get("country") or key)
    return f"atno-{name or 'entity'}"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:40].strip("-")


def notis_bodies(qso: dict, facts: dict) -> tuple[str, str]:
    call = qso.get("call") or "—"
    band = format_band(qso.get("band"))
    mode = (qso.get("mode") or "").strip().upper()
    local = parse_qso_local(qso)
    entity = facts["name"]
    band_mode = " ".join(p for p in (band, mode) if p)

    if local and qso.get("time"):
        when_sv = f"den {format_date(local, 'sv')} kl. {local.strftime('%H:%M')}"
        when_en = f"on {format_date(local, 'en')} at {local.strftime('%H:%M')}"
    elif local:
        when_sv = f"den {format_date(local, 'sv')}"
        when_en = f"on {format_date(local, 'en')}"
    else:
        when_sv = when_en = ""

    if band_mode and when_sv:
        qso_sv = f"QSO med {call} på {band_mode} {when_sv}."
        qso_en = f"A QSO with {call} on {band_mode} {when_en}."
    elif band_mode:
        qso_sv = f"QSO med {call} på {band_mode}."
        qso_en = f"A QSO with {call} on {band_mode}."
    elif when_sv:
        qso_sv = f"QSO med {call} {when_sv}."
        qso_en = f"A QSO with {call} {when_en}."
    else:
        qso_sv = f"QSO med {call}."
        qso_en = f"A QSO with {call}."

    cont = facts.get("cont")
    cqz = facts.get("cqz")
    where_sv_parts: list[str] = []
    where_en_parts: list[str] = []
    if cont in CONT_SV:
        where_sv_parts.append(f"ligger i {CONT_SV[cont]}")
        where_en_parts.append(f"is in {CONT_EN[cont]}")
    if isinstance(cqz, int):
        if where_sv_parts:
            where_sv_parts.append(f"CQ-zon {cqz}")
            where_en_parts.append(f"CQ zone {cqz}")
        else:
            where_sv_parts.append(f"CQ-zon {cqz}")
            where_en_parts.append(f"CQ zone {cqz}")
    if where_sv_parts:
        if len(where_sv_parts) == 2 and where_sv_parts[0].startswith("ligger"):
            fact_sv = f"{entity} {where_sv_parts[0]}, {where_sv_parts[1]}."
            fact_en = f"{entity} {where_en_parts[0]}, {where_en_parts[1]}."
        elif where_sv_parts[0].startswith("ligger"):
            fact_sv = f"{entity} {where_sv_parts[0]}."
            fact_en = f"{entity} {where_en_parts[0]}."
        else:
            fact_sv = f"{entity}, {where_sv_parts[0]}."
            fact_en = f"{entity}, {where_en_parts[0]}."
        return f"{qso_sv} {fact_sv}", f"{qso_en} {fact_en}"
    return qso_sv, qso_en


def baseline_entry(key: str, qso: dict, facts: dict) -> dict:
    entry: dict = {
        "name": facts["name"],
        "first": {
            "date": qso.get("date"),
            "band": qso.get("band"),
            "mode": qso.get("mode"),
        },
    }
    # Callsigns are already public in static/data/qsos.json.
    if qso.get("call"):
        entry["first"]["call"] = qso["call"]
    if qso.get("time"):
        entry["first"]["time"] = qso["time"]
    if key.isdigit():
        entry["dxcc"] = int(key)
    if facts.get("cont"):
        entry["cont"] = facts["cont"]
    if isinstance(facts.get("cqz"), int):
        entry["cqz"] = facts["cqz"]
    return entry


def write_baseline(entities: dict[str, dict]) -> None:
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(entities),
        "entities": dict(sorted(entities.items(), key=lambda kv: (not kv[0].isdigit(), int(kv[0]) if kv[0].isdigit() else kv[0]))),
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_baseline() -> dict[str, dict] | None:
    if not BASELINE_PATH.is_file():
        return None
    raw = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    ents = raw.get("entities")
    if not isinstance(ents, dict):
        die(f"{BASELINE_PATH.relative_to(REPO_ROOT)} has no entities object")
    return ents


def add_notis(title_sv: str, title_en: str, text_sv: str, text_en: str, slug: str) -> None:
    cmd = [
        sys.executable,
        str(ADD_NOTIS),
        "--type",
        "atno",
        "--title-sv",
        title_sv,
        "--title-en",
        title_en,
        "--text-sv",
        text_sv,
        "--text-en",
        text_en,
        "--slug",
        slug,
    ]
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        die(result.stderr.strip() or f"add-notis.py failed for {slug}")
    sys.stdout.write(result.stdout)


def main() -> None:
    p = argparse.ArgumentParser(description="Create Ny ATNO notiser for new DXCC entities")
    p.add_argument("--dry-run", action="store_true", help="Show what would happen; write nothing")
    args = p.parse_args()

    qsos = load_qsos()
    first = first_qso_by_entity(qsos)
    if not first:
        die("no QSOs with a DXCC entity (dxcc or country) in the log")

    cty_list = parse_cty(CTY_PATH)
    exact, prefixes, by_name = build_cty_indexes(cty_list)

    def resolve(qso: dict) -> CtyEntity | None:
        ent = lookup_cty(qso.get("call") or "", exact, prefixes)
        if ent:
            return ent
        country = normalize_name(qso.get("country") or "")
        return by_name.get(country) if country else None

    baseline = load_baseline()
    if baseline is None:
        entities: dict[str, dict] = {}
        missing_dxcc = 0
        for key, qso in first.items():
            if not key.isdigit():
                missing_dxcc += 1
            entities[key] = baseline_entry(key, qso, facts_for(qso, resolve(qso)))
        print(
            f"initialising baseline with {len(entities)} DXCC entities "
            f"from {len(qsos)} QSOs"
            + (f" ({missing_dxcc} without a QRZ dxcc number)" if missing_dxcc else "")
        )
        if args.dry_run:
            print("dry-run: not writing", BASELINE_PATH.relative_to(REPO_ROOT))
            return
        write_baseline(entities)
        print(f"wrote {BASELINE_PATH.relative_to(REPO_ROOT)}")
        print("no notiser created on first run")
        return

    new_keys = [key for key in first if key not in baseline]
    # Keep a stable order: by first-QSO date, then name.
    new_keys.sort(key=lambda k: (qso_sort_key(first[k]), (first[k].get("country") or "")))
    if not new_keys:
        print(f"no new ATNO; baseline has {len(baseline)} entities, log has {len(first)}")
        return

    created: list[str] = []
    pending: dict[str, dict] = {}
    for key in new_keys:
        qso = first[key]
        facts = facts_for(qso, resolve(qso))
        name = facts["name"]
        title_sv = f"Ny ATNO: {name}"
        title_en = f"New ATNO: {name}"
        text_sv, text_en = notis_bodies(qso, facts)
        slug = slug_for(key, facts, qso)
        print(f"new ATNO {key}: {title_sv}")
        print(f"  {text_sv}")
        print(f"  {text_en}")
        if args.dry_run:
            print(f"  dry-run: would write slug {slug}")
        else:
            add_notis(title_sv, title_en, text_sv, text_en, slug)
        pending[key] = baseline_entry(key, qso, facts)
        created.append(name)

    if args.dry_run:
        print(f"dry-run: {len(pending)} notiser, baseline not updated")
        return

    baseline.update(pending)
    write_baseline(baseline)
    print(f"updated {BASELINE_PATH.relative_to(REPO_ROOT)} ({len(baseline)} entities)")
    print(f"created {len(created)} ATNO notis/notiser")


if __name__ == "__main__":
    main()
