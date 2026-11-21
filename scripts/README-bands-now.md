# Bandöppningar just nu / Band openings right now

Front-page grid (under "SM4T – senaste dygnet") showing how many distinct CW
stations per band (80–10 m) and continent (EU NA SA AF AS OC) that RBN skimmers
near Borlänge (JP70RM) heard in the last 60 minutes.

## Pieces

| File | Role |
|------|------|
| `scripts/fetch-bands-now.py` | Collector. Writes `static/data/bands-now.json` (gitignored). |
| `scripts/data/cty.dat` | Call → continent table from country-files.com. Refresh now and then: `curl -o scripts/data/cty.dat https://www.country-files.com/cty/cty.dat` |
| `layouts/partials/bands-now.html` | Block markup + i18n strings (`bands_now.*` in `i18n/sv.yaml`, `i18n/en.yaml`). Included from `layouts/partials/home/profile.html`. |
| `static/js/bands-now.js` | Fetches the json, draws the grid, re-reads every 5 min. |
| `assets/css/custom.css` | `.bands-now*` / `.bn-l0..3` styles (light + dark). |

Run locally: `python3 scripts/fetch-bands-now.py && hugo --quiet -d /tmp/h`

## Data source

RBN's public `https://www.reversebeacon.net/spots.php` (the JSON the RBN web
page polls): CW only (`m=1`), `ma=3600`, `cde=<skimmer list>`, one request per
band (`b=<band code>`). The endpoint returns at most 100 spots per request,
newest first; when a band hits the cap it is re-queried per DX continent
(`cox=EU` …). A cell that still hits the cap is shown as "≥N" (lower bound;
it is always in the top colour anyway). Typically 10–30 small requests per run,
0.6 s apart.

Why not the telnet feed (telnet.reversebeacon.net:7000)? A 3–5 minute capture
per run would only show a few minutes, not the last hour, and would hold a
connection open on every run. spots.php gives a true 60-minute window with a
handful of short requests.

Skimmers: active RBN skimmers (from `spotters=1`) with a Nordic prefix
(SM/SA–SM, 7S, 8S, LA–LN, OH/OF–OJ, OZ/OU/OV, 5P/5Q, OX, OY, TF, JW/JX)
within 1000 km of JP70RM. If fewer than 4 are active, the nearest other
skimmers within 1000 km fill up. The page lists the skimmers that
contributed spots.

Kp (latest 3-hour planetary Kp) and 10.7 cm flux come from NOAA SWPC JSON.

## Colours (distinct stations per cell, last 60 min)

- grey: 0
- yellow: 1–2
- light green: 3–9
- green: 10 or more

Change `LEVELS` in the collector to adjust; the page reads `levels` from the json.

## Schedule / deploy

No separate workflow and no commits: the collector runs as a step in
`.github/workflows/hugo.yml`, which already builds on every push and on
`cron: "*/15 * * * *"`. The json goes straight into the Pages artifact, so the
git history does not grow. GitHub often delays scheduled runs (30–90 min);
the page warns when the data is older than 75 min and shows "data saknas"
when it is missing or older than 6 h.
