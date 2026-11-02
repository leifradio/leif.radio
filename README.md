# leif.radio – SM4T

Website for amateur radio station SM4T, built with [Hugo](https://gohugo.io/) and the [Blowfish](https://github.com/nunocoracao/blowfish) theme. It is published automatically to GitHub Pages (https://leif.radio/) whenever something is pushed to `main`.

## Adding a post

Each post is a folder (a *page bundle*) in `content/posts/`:

```
content/posts/2026-11-15-hilltop-activation/
├── index.md        # the post
├── feature.jpg     # cover image (shown at the top and in lists)
├── antenna.jpg     # other photos
└── log.jpg
```

1. Create `content/posts/YYYY-MM-DD-slug/index.md`. On GitHub: **Add file → Create new file** and type the path, e.g. `content/posts/2026-11-15-hilltop-activation/index.md`.
2. Start the file with a header like this:

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

A post without photos can still be a single file, e.g. `content/posts/2026-11-15-cq-ww-cw.md`.

Contest reports go in `content/contests/` the same way. The *About / Station* and *Gear* pages are `content/about.md` and `content/gear.md`. Site settings live in `config/_default/`.

## Building locally (optional)

```
git clone --recurse-submodules https://github.com/leifradio/leif.radio
cd leif.radio
hugo server
```
