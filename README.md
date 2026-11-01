# leif.radio – SM4T

Hemsidan för amatörradiostationen SM4T, byggd med [Hugo](https://gohugo.io/) och temat [PaperMod](https://github.com/adityatelange/hugo-PaperMod). Sidan publiceras automatiskt på GitHub Pages (https://leif.radio/) varje gång något läggs till i grenen `main`.

## Lägga till ett inlägg

1. Skapa en ny Markdown-fil i `content/posts/`, t.ex. `content/posts/2026-11-15-cq-ww-cw.md`. Det går att göra direkt på GitHub med **Add file → Create new file**.
2. Börja filen med ett huvud så här:

   ```
   +++
   title = "CQ WW CW 2026"
   date = 2026-11-15T18:00:00+01:00
   draft = false
   tags = ["tävling", "cw"]
   +++

   Själva texten skriver du här, i vanlig Markdown.
   ```

3. Spara (commit) till `main`. Efter någon minut syns inlägget på sidan.

Tävlingsrapporter läggs på samma sätt i `content/tavlingar/`. Sidorna *Om mig / Stationen* och *Utrustning* finns i `content/om.md` och `content/utrustning.md`.

## Bygga lokalt (valfritt)

```
git clone --recurse-submodules https://github.com/leifradio/leif.radio
cd leif.radio
hugo server
```
