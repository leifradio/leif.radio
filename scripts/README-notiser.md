# Notiser / Notes

Short news items shown in a right-hand column on the front page (and as a full list at `/notiser/` and `/en/notes/`). They are **not** regular posts: they do not appear in the main post list, the main RSS feed, or Todoist.

The official kinds are three daily notes, shown newest first (by `date`, including the time):

- Weather in Borlänge (`weather`)
- Propagation (`propagation`)
- Morse novels (`youtube`)

Swedish is the root language; always add both a `.sv.md` and an `.en.md` file.

## File path and naming

```
content/notiser/YYYY-MM-DD-slug.sv.md
content/notiser/YYYY-MM-DD-slug.en.md
```

Recommended slugs for the daily routines:

- Weather (around 06:45): `YYYY-MM-DD-vader`
- Morse novel (around 07:00): `YYYY-MM-DD-morsenovell`
- Propagation (around 08:00): `YYYY-MM-DD-propagation`

## Front matter

`notis_type` is the notis kind. Do **not** set Hugo’s own `type` field; the section already provides that.

```
+++
title = "Väder i Borlänge 18 nov"
date = 2026-11-18T06:45:00+01:00
notis_type = "weather"
weather_icon = "partly"
+++

Halvklart i eftermiddag, mulet i kväll. Temperaturen sjunker från cirka −2 °C till omkring −4 °C. Ingen nederbörd enligt SMHI.
```

Fields:

- `title` — short heading (translated in each language file)
- `date` — keep the same in both files; use Europe/Stockholm offset (`+01:00` or `+02:00`). The front page and the list sort by this timestamp, newest first.
- `notis_type` — `weather` | `propagation` | `youtube` (the three official kinds)
- `weather_icon` — for `weather` only, optional: `clear` | `partly` | `cloudy` | `rain` | `snow` | `sleet` | `thunder` | `fog`. Picks the symbol on the site. If omitted, a generic cloud is used.
- `link` — optional. External URLs (`https://…`) open as they are. Site-relative paths such as `/posts/2026-11-18-winlink-wednesday/` are prefixed with `/en` on the English site.
- Body — one to three short lines, translated. For weather, use a real forecast (SMHI) and do not invent figures.

English example of a Morse novel (`content/notiser/2026-11-18-morsenovell.en.md`):

```
+++
title = "Morse novel: The Robot Who Learned to Knit"
date = 2026-11-18T07:00:00+01:00
notis_type = "youtube"
link = "https://youtu.be/PIIRCrEsGLc"
+++

Today's Morse novel, 4:40 long, 25 WPM.
```

## Helper script

From the repo root.

Weather, as the 06:45 routine should call it (`--slug vader`). Pass `--icon` (or `--wsymb` with the SMHI symbol code) so the symbol matches the forecast:

```
python3 scripts/add-notis.py \
  --type weather \
  --title-sv "Väder i Borlänge 18 nov" \
  --title-en "Weather in Borlänge 18 Nov" \
  --text-sv "Kort, faktabaserad prognos från SMHI." \
  --text-en "A short, factual forecast from SMHI." \
  --date 2026-11-18T06:45:00 \
  --slug vader \
  --icon partly
```

`--icon` is one of `clear`, `partly`, `cloudy`, `rain`, `snow`, `sleet`, `thunder`, `fog`. If you have the SMHI `Wsymb2` / `symbol_code` (1–27) for the representative daytime weather, you can set the icon from that instead:

```
python3 scripts/add-notis.py --type weather ... --slug vader --wsymb 4
```

`--icon` wins if both are given. To only look up the mapping:

```
python3 scripts/add-notis.py --map-wsymb 4
```

That prints `partly` and exits.

Morse novel:

```
python3 scripts/add-notis.py \
  --type youtube \
  --title-sv "Morsenovell: The Robot Who Learned to Knit" \
  --title-en "Morse novel: The Robot Who Learned to Knit" \
  --text-sv "Dagens morsenovell, 4:40 lång, 25 WPM." \
  --text-en "Today's Morse novel, 4:40 long, 25 WPM." \
  --url "https://youtu.be/PIIRCrEsGLc" \
  --date 2026-11-18T07:00:00 \
  --slug morsenovell
```

Propagation:

```
python3 scripts/add-notis.py \
  --type propagation \
  --title-sv "HF-läget 18 nov" \
  --title-en "HF conditions 18 Nov" \
  --text-sv "Kort sammanfattning av dagens fönster på 20 och 40 m." \
  --text-en "A short summary of today's 20 m and 40 m windows." \
  --date 2026-11-18T08:00:00 \
  --slug propagation
```

`--date` can be `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` (Europe/Stockholm if no offset). Omit it to use the current time. `--slug` defaults to `vader` for `weather`, `morsenovell` for `youtube`, and `propagation` for `propagation`. The script refuses to overwrite an existing file unless you pass `--force`.

## SMHI Wsymb2 → weather_icon

`scripts/add-notis.py` maps SMHI’s Wsymb2 (also `symbol_code` in the SNOW1gv1 API) to `weather_icon` via `icon_from_wsymb2()` and `--wsymb` / `--map-wsymb`. Pick the code that best represents the daytime forecast (for 18 Nov that was 4, half-clear).

| Wsymb2 | SMHI meaning | weather_icon |
|------:|---|---|
| 1 | Clear sky | `clear` |
| 2 | Nearly clear sky | `clear` |
| 3 | Variable cloudiness | `partly` |
| 4 | Half-clear sky | `partly` |
| 5 | Cloudy sky | `cloudy` |
| 6 | Overcast | `cloudy` |
| 7 | Fog | `fog` |
| 8–10 | Rain showers | `rain` |
| 11 | Thunderstorm | `thunder` |
| 12–14 | Sleet showers | `sleet` |
| 15–17 | Snow showers | `snow` |
| 18–20 | Rain | `rain` |
| 21 | Thunder | `thunder` |
| 22–24 | Sleet | `sleet` |
| 25–27 | Snowfall | `snow` |

The script only writes the two Markdown files. It does not commit.

## Publish

```
git add content/notiser/YYYY-MM-DD-slug.sv.md content/notiser/YYYY-MM-DD-slug.en.md
git commit -m "Notis: kort svensk titel"
git push origin main
```

GitHub Pages builds automatically from `main`. No Todoist task is created for a notis.

## URLs

- Swedish list: https://leif.radio/notiser/
- English list: https://leif.radio/en/notes/
- Swedish RSS: https://leif.radio/notiser/index.xml
- English RSS: https://leif.radio/en/notes/index.xml
