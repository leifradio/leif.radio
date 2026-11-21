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
+++

⛅ Halvklart på eftermiddagen, ☁️ mulet på kvällen. 🌡️ −2 °C till −4 °C. Ingen nederbörd enligt SMHI.
```

Fields:

- `title` — short heading (translated in each language file)
- `date` — keep the same in both files; use Europe/Stockholm offset (`+01:00` or `+02:00`). The front page and the list sort by this timestamp, newest first.
- `notis_type` — `weather` | `propagation` | `youtube` (the three official kinds)
- `link` — optional. External URLs (`https://…`) open as they are. Site-relative paths such as `/posts/2026-11-18-winlink-wednesday/` are prefixed with `/en` on the English site.
- Body — one to three short lines, translated. For weather, use a real forecast (SMHI) and do not invent figures.

English example of a Morse novel (`content/notiser/2026-11-18-morsenovell.en.md`):

```
+++
title = "The Robot Who Learned to Knit"
date = 2026-11-18T07:00:00+01:00
notis_type = "youtube"
link = "https://youtu.be/PIIRCrEsGLc"
+++

Today's Morse novel, 4:40 long, 25 WPM.
```

## Helper script

From the repo root.

Weather, as the 06:45 routine should call it (`--slug vader`). Put weather emoji in the body text, one per period (and 🌡️ for the temperature). Look up each SMHI `Wsymb2` / `symbol_code` with:

```
python3 scripts/add-notis.py --map-wsymb 4
```

That prints `⛅` (half-clear). Then write the text and create the files:

```
python3 scripts/add-notis.py \
  --type weather \
  --title-sv "Väder i Borlänge 18 nov" \
  --title-en "Weather in Borlänge 18 Nov" \
  --text-sv "⛅ Halvklart på eftermiddagen, ☁️ mulet på kvällen. 🌡️ −2 °C till −4 °C. Ingen nederbörd enligt SMHI." \
  --text-en "⛅ Half-clear this afternoon, ☁️ overcast this evening. 🌡️ −2 °C to −4 °C. No precipitation according to SMHI." \
  --date 2026-11-18T06:45:00 \
  --slug vader
```

The header always uses the generic Väder/Weather cloud. Do not invent figures; only a real SMHI forecast.


Morse novel:

```
python3 scripts/add-notis.py \
  --type youtube \
  --title-sv "The Robot Who Learned to Knit" \
  --title-en "The Robot Who Learned to Knit" \
  --text-sv "Dagens morsenovell, 4:40 lång, 25 WPM." \
  --text-en "Today's Morse novel, 4:40 long, 25 WPM." \
  --url "https://youtu.be/PIIRCrEsGLc" \
  --date 2026-11-18T07:00:00 \
  --slug morsenovell
```

Also add the video to the YouTube list (see [YouTube-filmer](#youtube-filmer) below):

```
python3 scripts/add-youtube.py \
  --id PIIRCrEsGLc \
  --date 2026-11-18 \
  --title "The Robot Who Learned to Knit" \
  --category morsenovell \
  --wpm 25 \
  --length 4:40
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

## SMHI Wsymb2 → emoji

`scripts/add-notis.py` maps SMHI’s Wsymb2 (also `symbol_code` in the SNOW1gv1 API) to a body-text emoji via `emoji_from_wsymb2()` and `--map-wsymb`. Use one emoji per period in the text (afternoon, evening, and so on). Temperature uses 🌡️, which is not a Wsymb2 code.

| Wsymb2 | SMHI meaning | Emoji |
|------:|---|---|
| 1 | Clear sky | ☀️ |
| 2 | Nearly clear sky | 🌤️ |
| 3 | Variable cloudiness | ⛅ |
| 4 | Half-clear sky | ⛅ |
| 5 | Cloudy sky | 🌥️ |
| 6 | Overcast | ☁️ |
| 7 | Fog | 🌫️ |
| 8–10 | Rain showers | 🌦️ |
| 11 | Thunderstorm | ⛈️ |
| 12–14 | Sleet showers | 🌨️ |
| 15–17 | Snow showers | 🌨️ |
| 18–20 | Rain | 🌧️ |
| 21 | Thunder | ⛈️ |
| 22–24 | Sleet | 🌨️ |
| 25–27 | Snowfall | ❄️ |


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

## YouTube-filmer

The Telegrafi / CW section has a child page that lists videos from the [@Leifradio](https://www.youtube.com/@Leifradio) channel:

- Swedish: `/telegrafi/youtube/`
- English: `/en/cw/youtube/`

The list is built from `data/youtube.yaml`. After a new Morse novel (or a training video) has been uploaded and the notis has been written, add the video so it appears on the page:

```
python3 scripts/add-youtube.py \
  --id DdQ6KymlNU0 \
  --date 2026-11-19 \
  --title "The Postman of the Last Island" \
  --category morsenovell \
  --wpm 25 \
  --length 4:51
```

`--id` can also be a full `https://youtu.be/…` URL. `--category` is `morsenovell`, `traning` or `ovrigt`. `--wpm` and `--length` are optional (`length` is `M:SS`). If `--title` is omitted, the script fetches it from YouTube oembed (and refuses to add the entry if oembed returns 401/404).

An existing entry with the same id is updated in place. The script only writes `data/youtube.yaml`. It does not commit.

Then commit the data file together with the notis files, for example:

```
git add data/youtube.yaml content/notiser/YYYY-MM-DD-morsenovell.sv.md content/notiser/YYYY-MM-DD-morsenovell.en.md
git commit -m "Notis: Morsenovell YYYY-MM-DD"
git push origin main
```
