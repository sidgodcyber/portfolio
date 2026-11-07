# Siddhi Baluja — Portfolio v3 · "The mission terminal"

A one-page portfolio set as a working 1-bit computer. No frameworks, no build step, no dependencies.

```
index.html             the page; all the copy lives here
css/styles.css         tokens and every component
js/main.js             everything that moves
assets/art/            the dithered pictures the page uses (generated)
assets/found/          open-licence sources + credits.json
assets/projects/       Siddhi's own exhibit shots and project figures
assets/fonts/          Departure Mono, IBM Plex Mono (SIL OFL)
assets/resume/         the downloadable résumé; replace it to update
tools/build-art.py     sources → assets/art
DESIGN.md              the design system; change this first
content.md             the words on the page
```

## Run it

Serve the folder with any static server, for example `python -m http.server`, and open `index.html`. It also opens straight from the file system; the only difference is that the contact clip stays a still, because browsers won't let a canvas read a local video.

Deploy to any static host.

## Common edits

- **Résumé:** replace `assets/resume/Siddhi-Baluja-Resume.pdf` with the new PDF, keeping that exact file name. The link in the contact card keeps working.
- **Copy:** edit `content.md`, then the same text in `index.html`.
- **A project's repo link:** add `<a class="more" …>` inside that folder's `.folder-text`.
- **Colours:** `:root` in `css/styles.css`. Then match `BONE` in `js/main.js` and in `tools/build-art.py`, and rebuild the art.
- **Pictures:** add the source, then a `plate(...)` line in `tools/build-art.py`, and run:

  ```
  python tools/build-art.py <astronaut-colour.png> <astronaut-bw.png>
  ```

  It needs Pillow, NumPy and OpenCV. Credit anything found in `assets/found/credits.json` and in the footer.

## Licences

Fonts are under the SIL Open Font License (see `assets/fonts/`). Found pictures keep their own licences, listed in `assets/found/credits.json` and in the footer. Everything else is © Siddhi Baluja.
