# Notiser / Notes

Short news items shown in a right-hand column on the front page (and as a full list at `/notiser/` and `/en/notes/`). They are **not** regular posts: they do not appear in the main post list, the main RSS feed, or Todoist.

Swedish is the root language; always add both a `.sv.md` and an `.en.md` file.

## File path and naming

```
content/notiser/YYYY-MM-DD-slug.sv.md
content/notiser/YYYY-MM-DD-slug.en.md
```

Recommended slugs for the daily routines:

- Morse novel: `YYYY-MM-DD-morsenovell`
- Propagation: `YYYY-MM-DD-propagation`

## Front matter

`notis_type` is the notis kind. Do **not** set Hugo’s own `type` field; the section already provides that.

```
+++
title = "Morsenovell: The Robot Who Learned to Knit"
date = 2026-11-18T07:00:00+01:00
notis_type = "youtube"
link = "https://youtu.be/PIIRCrEsGLc"
+++

Dagens morsenovell, 4:40 lång, 25 WPM.
```

Fields:

- `title` — short heading (translated in each language file)
- `date` — keep the same in both files; use Europe/Stockholm offset (`+01:00` or `+02:00`)
- `notis_type` — `youtube` | `propagation` | `winlink` | `other`
- `link` — optional. External URLs (`https://…`) open as they are. Site-relative paths such as `/posts/2026-11-18-winlink-wednesday/` are prefixed with `/en` on the English site.
- Body — one to three short lines, translated.

English example of the same notis (`content/notiser/2026-11-18-morsenovell.en.md`):

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

From the repo root:

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

Propagation example:

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

`--date` can be `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` (Europe/Stockholm if no offset). Omit it to use the current time. `--slug` defaults to `morsenovell` for `youtube`, `propagation` for `propagation`, `winlink` for `winlink`, and `notis` for `other`. The script refuses to overwrite an existing file unless you pass `--force`.

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
