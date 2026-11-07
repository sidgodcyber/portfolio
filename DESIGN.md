# DESIGN.md — Siddhi Baluja · Portfolio v3

> Working title: **"The mission terminal."**
> A one-page portfolio set as a working 1-bit computer: figures you can re-plot, folders you can open, a readout you can disturb, and a pixel astronaut who drifts through all of it.

This file is the source of truth for look, feel, motion and structure. Build to it; when something isn't covered, extend this file first, then the code. `content.md` holds the words.

v2 ("Tear the ordinary": paper résumé, galaxy, Fraunces, violet–rose nebula) lives in a private archive repo. Its thesis, a creative-business person who blends tech, was retired with the Nov 2026 copy.

---

## 1. Thesis

Siddhi researches things most people never see: the ionosphere bending a satellite signal, the terrain under a drone that has lost GPS, the ground shaking before a debris flow arrives. The page behaves like her instruments do. It shows its working, in two inks, and lets you touch it.

> **The idea:** Siddhi's own mission files (IonWatch's S4 readout, Trishul Net's debris-flow trace, the lunar rover traverse, a black hole traced from the real equations) become the pages of a working 1-bit terminal.

Emotional target stays from v2: weightless, slightly awed, never loud. Modest palette, extravagant detail.

**Kept from v2:** scroll is travel (parallax star depths and warp streaks), a sky that reacts to the cursor, her portrait as a live object you can push around, joy under every control, full reduced-motion and no-JS paths.

**Dropped:** the paper tear (the first screen now answers who and what straight away), Fraunces and the nebula palette, the WebGPU black hole (it cost 3.5× everything else combined), the HUD, sound, the project drawer.

---

## 2. Tokens

### Colour: a two-ink print job plus one star

| Token | Value | Role |
|---|---|---|
| `--ground` | `#0a0a09` | Page ground. |
| `--tone` / `--tone-2` | `#171614` / `#23211e` | Filled surfaces: dark folders, the secondary button. |
| `--bone` | `#e6e1d7` | The ink on black, and the paper field. Stays under 88% lightness so it reads as bone, not yellow cream. |
| `--bone-2` | `#d6d1c6` | Tone step on paper. |
| `--star` | `#f2b92f` | The gold star on her suit. Used only for the S4 reading, focus rings, button hover and selection. |

Canvas colours in `js/main.js` and inks in `tools/build-art.py` must match `--bone`.

### Type

| Role | Face | Job |
|---|---|---|
| Display | **Departure Mono** | Every heading, buttons, tabs, the wordmark. Drawn on an 11px grid, so sizes are multiples of 11: 22, 33, 44, 55, 66, 77. |
| Text | **IBM Plex Mono** 400/500 | Running text, nav, captions. Running text at 17px, full ink. |

Both are self-hosted in `assets/fonts/` (SIL OFL). Two faces, no third. Sizes: giant, display, head, sub, body, small; nothing below 14px.

Monospace is the brand here, from Siddhi's own mock. The Taste Skill bans it elsewhere, so run its checks with `--allow mono`.

### Signature marks

- `> ` prompt and blinking `_` on the greeting and section headings (`.prompt`).
- `[ HOME ]` brackets on the current nav item.
- **Stepped corners:** panels and buttons use one `clip-path` staircase (`--steps`), never `border-radius`.
- `steps()` easing on every transition, so things redraw like a screen instead of gliding.

### Space

One 12-column grid, one pair of margins `--m` (16–32px), section gap `--gap` (96–192px). Surfaces are filled shapes separated by tone. Only real interface fragments (`data-ui`: the Fig. window, poster, S4 scope) keep a 2px line.

---

## 3. Pictures

One treatment everywhere: **Atkinson dithering in two inks**, made by `tools/build-art.py` and saved to `assets/art/`. Run it after changing any source:

```
python tools/build-art.py <astronaut-colour.png> <astronaut-bw.png>
```

| Picture | Source | What's real about it |
|---|---|---|
| Astronaut | Siddhi's own art | Posterised to five bone inks; the colour version shows while held. |
| Fig. 01–03 | Computed | Photon paths integrated from the Schwarzschild orbit equation, at three viewing angles. |
| Hero limb, poster moon | NASA first-quarter Moon | Dithered. |
| IonWatch | ISS aurora | Dithered. |
| GNSS Guardian | NASA Himalayas | Shi–Tomasi corners tracked with Lucas–Kanade, drawn on top. An illustration, not project output. |
| Trishul Net | Siddhi's `p1_stalta_trigger.png` | Real Illgraben debris-flow recording and its STA/LTA trigger, redrawn in two inks. |
| Lunar Ice | Siddhi's D2, D3, D4 figures | Her real traverse, CPR, ice-criteria and illumination maps. |
| Sand Grain | Klepnev specimen photo | Grains segmented and bracketed with OpenCV. An illustration, not project output. |
| Gravity | A real morning brief | Set as text, an excerpt, client names blacked out. |
| Exhibits | Siddhi's own DFI shots | Dithered; the original fades in on hover. AgeWarp uses one dot per pixel so her face stays readable, and phones get all five ages as a 3 + 2 grid. |
| Contact clip | ISS Expedition 29 | Title cards trimmed, then redrawn to 1-bit live in the browser. |

Credits sit in the footer under "Picture credits" and in `assets/found/credits.json`. No found picture is presented as Siddhi's own work.

**Never on the page:** real client names, or projects that aren't built yet.

---

## 4. The page

| Section | Composition |
|---|---|
| **Home** | From the mock: copy left, astronaut centre, Fig. window right, Moon rising across the foot. Nothing touches the headline. |
| **About Me** | Poster left, letter centre, orbit drawing right. |
| **Areas of Exploration** | The whole field turns to paper. Giant heading, filled bar rows. |
| **Selected Projects** | The filing cabinet: full-bleed folders in alternating ink and paper, six of them, sticky, each sliding over the last. Tabs sit side by side, so earlier tabs stay visible as navigation. Phones get plain stacked folders. |
| **Milestones** | A printed sheet at a one-degree tilt. |
| **Experience** | Text and Anatomy Mirror, then the AgeWarp strip at full width, then three exhibits. |
| **Résumé** | No section of its own: one link in the contact card, pointing at a fixed file, `assets/resume/Siddhi-Baluja-Resume.pdf`. |
| **Beyond Technology** | A note on paper with a tipped-in plate and a perforated foot. |
| **Contact** | The largest type on the page, then the aurora clip with a visit card on it. |
| **Back of the card** | Paper footer revealed like a curtain as Contact lifts away. Sign-off, stamp, the name at full width, credits. |

---

## 5. Interactions

| Thing | Behaviour | Fallback |
|---|---|---|
| **S4 scope** (the live thing) | Simulated signal `I = \|1 + s(x+iy)\|²` with low-passed noise. `S4 = √(⟨I²⟩−⟨I⟩²)/⟨I⟩` is computed from the samples on screen. Under 0.3 weak, under 0.6 moderate, above that strong. Labelled as simulated. | Reduced motion: redraws on input only. No JS: the picture and copy stand alone. |
| **Astronaut** | Drag and she drifts home on a spring; arrow keys nudge; held shows colour. | Static. |
| **Fig. window** | Three buttons switch the viewing angle. | First figure. |
| **Window controls** | □ full screen, _ freezes all motion, × switches the screen off with a CRT collapse and a button to switch back on. | Hidden below 1100px. |
| **Sky** | About 240 square stars in three depths, parallax on scroll, streaks at speed, pushed by the cursor, the odd meteor. 30fps, skipped when the tab is hidden. | One static frame. |
| **Clip** | Bayer-dithered onto a 360×180 canvas at 30fps, only while near the viewport. | Dithered still. |
| **Entrances** | Stepped rise, staggered 70ms; pictures open top-down like a scan. | Content is only hidden once `main.js` has run. |

---

## 6. Performance and access

- No libraries, no build step. All JS is one small file; the only per-frame work is about 240 rects and a small canvas.
- Every control works from the keyboard, with a visible gold focus ring. Phone nav is a full menu.
- `prefers-reduced-motion` removes all travel and keeps all content.
- The page reads completely with JS off.

---

## 7. Checks

Run from the repo root, with the Taste Skill installed:

```
node <skill>/scripts/lint.mjs index.html css js
node <skill>/scripts/inspect.mjs index.html --allow mono,covered-text,pinned-over-picture,long-pin
```

Why those exceptions: `mono` is the brand. The other three are the filing cabinet doing its job; folders are meant to slide over each other, and the tabs are navigation that stays put.

---

*Last updated: 8 Nov 2026. Change this file first; the code follows.*
