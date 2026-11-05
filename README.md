# leif.radio

Website for Leif.radio, amateur radio by Leif, built with [Hugo](https://gohugo.io/) and the [Blowfish](https://github.com/nunocoracao/blowfish) theme. It is published automatically to GitHub Pages (https://leif.radio/) whenever something is pushed to `main`.

## Two languages: Swedish and English

The site is bilingual. **Swedish is the main language** and is served at the root (https://leif.radio/), **English** is served under https://leif.radio/en/. A language switcher in the header (and in the mobile menu) jumps between the two versions of the same page.

Hugo does not translate anything by itself: every page exists as two files side by side, told apart by the language code in the filename:

- `index.sv.md`: the Swedish version (write this one first)
- `index.en.md`: the English translation

Files with the same name (apart from `.sv`/`.en`) in the same folder are linked as translations of each other. Both versions share the photos in the folder (e.g. `feature.jpg`). Keep `date` the same in both files; title, description and captions are translated.

**Tags:** ordinary words are translated, technical tags stay identical in both languages:

- Translated: e.g. `nyheter` (sv) / `news` (en), `portabelt` (sv) / `portable` (en). Use the Swedish word in `index.sv.md` and the English word in `index.en.md`.
- Identical in both: callsigns (`sm4t`), bands (`20m`, `40m`), modes and networks (`cw`, `rbn`), gear names (`TX500MP`, `CHA Feather`) and place names (`dalarna`).

Swedish tag pages live under `/tags/…` and English ones under `/en/tags/…`. The tags overview page titles are set in `content/tags/_index.sv.md` (Taggar) and `_index.en.md` (Tags). Menus are in `config/_default/menus.sv.toml` / `menus.en.toml`, and per-language site texts (description, welcome text) in `languages.sv.toml` / `languages.en.toml`. Extra Swedish theme strings live in `i18n/sv.yaml`.

If a page only has an `.sv.md` file it is shown only on the Swedish site (and the switcher is hidden on it).

## Adding a post

Each post is a folder (a *page bundle*) in `content/posts/`:

```
content/posts/2026-11-15-hilltop-activation/
├── index.sv.md     # the post in Swedish
├── index.en.md     # the same post in English
├── feature.jpg     # cover image (shown at the top and in lists)
├── antenna.jpg     # other photos
└── log.jpg
```

1. Create `content/posts/YYYY-MM-DD-slug/index.sv.md`. On GitHub: **Add file → Create new file** and type the path, e.g. `content/posts/2026-11-15-hilltop-activation/index.sv.md`. Then add the English translation as `index.en.md` in the same folder.
2. Start each file with a header like this (example from `index.en.md`):

   ```
   +++
   title = "Hilltop activation"
   date = 2026-11-15T18:00:00+01:00
   draft = false
   tags = ["sota", "portable", "cw"]
   +++

   Write the post here in plain Markdown.

   ![The antenna on the summit](antenna.jpg)
   ```

3. Upload photos into the same folder (**Add file → Upload files**). A file named `feature.jpg` (or `feature.png`) becomes the cover image automatically; other images are shown where you reference them in the text, like `![caption](antenna.jpg)`. Keep photos around 1600 px wide.
4. Commit to `main`. The post shows up on the site within a minute or two.

A post without photos can also be a pair of single files, e.g. `content/posts/2026-11-15-cq-ww-cw.sv.md` and `content/posts/2026-11-15-cq-ww-cw.en.md`.

Contest reports go in `content/contests/` the same way. The *About / Station* and *Gear* pages are `content/about.sv.md` / `about.en.md` and `content/gear.sv.md` / `gear.en.md`. Site settings live in `config/_default/`.


## QSO map (QRZ logbook)

The pages [/karta/](https://leif.radio/karta/) (Swedish) and [/en/map/](https://leif.radio/en/map/) show every QSO from the SM4T QRZ Logbook on an OpenStreetMap map. Markers are coloured by band; the data files are generated from the QRZ Logbook API.

Refresh the data (needs the API key in the environment, never commit the key):

```
export QRZ_LOGBOOK_API_KEY='…'   # from QRZ → Logbook → Settings → API
python3 scripts/fetch-qrz-map.py
```

That writes `static/data/qsos.json` and `static/data/qso-summary.json`. Commit those files (or let the daily routine do it) and push to `main`.

## Building locally (optional)

```
git clone --recurse-submodules https://github.com/leifradio/leif.radio
cd leif.radio
hugo server
```
