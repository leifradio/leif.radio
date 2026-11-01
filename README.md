# leif.radio – SM4T

Website for amateur radio station SM4T, built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme. It is published automatically to GitHub Pages (https://leif.radio/) whenever something is pushed to `main`.

## Adding a post

1. Create a new Markdown file in `content/posts/`, e.g. `content/posts/2026-11-15-cq-ww-cw.md`. You can do this right on GitHub with **Add file → Create new file**.
2. Start the file with a header like this:

   ```
   +++
   title = "CQ WW CW 2026"
   date = 2026-11-15T18:00:00+01:00
   draft = false
   tags = ["contest", "cw"]
   +++

   Write the post here in plain Markdown.
   ```

3. Commit to `main`. The post shows up on the site within a minute or two.

Contest reports go in `content/contests/` the same way. The *About / Station* and *Gear* pages are `content/about.md` and `content/gear.md`.

## Building locally (optional)

```
git clone --recurse-submodules https://github.com/leifradio/leif.radio
cd leif.radio
hugo server
```
