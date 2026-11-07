#!/usr/bin/env python3
"""build-art.py — makes every picture in assets/art/ from the sources.

One treatment for the whole site: Atkinson dithering (the classic 1-bit Mac look)
in two inks, bone on near-black. Run from the repo root:

    python tools/build-art.py path/to/astronaut-colour.png path/to/astronaut-bw.png

Needs Pillow, NumPy and OpenCV. Sources live in assets/found (credited in
credits.json) and assets/projects (Siddhi's own exhibit shots).
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

INK = (10, 10, 9)
BONE = (230, 225, 215)
FOUND = Path("assets/found")
OWN = Path("assets/projects")
OUT = Path("assets/art")
OUT.mkdir(exist_ok=True)


def atkinson(gray):
    """gray: float array 0..1. Returns a bool array, True where the dot is lit."""
    h, w = gray.shape
    buf = [list(map(float, row)) for row in gray]
    res = np.zeros((h, w), bool)
    for y in range(h):
        row = buf[y]
        n1 = buf[y + 1] if y + 1 < h else None
        n2 = buf[y + 2] if y + 2 < h else None
        for x in range(w):
            old = row[x]
            lit = old >= 0.5
            res[y, x] = lit
            e = (old - (1.0 if lit else 0.0)) / 8.0
            if x + 1 < w:
                row[x + 1] += e
            if x + 2 < w:
                row[x + 2] += e
            if n1 is not None:
                if x > 0:
                    n1[x - 1] += e
                n1[x] += e
                if x + 1 < w:
                    n1[x + 1] += e
            if n2 is not None:
                n2[x] += e
    return res


def levels(g, lo=0.0, hi=1.0, gamma=1.0):
    g = np.clip((g - lo) / max(hi - lo, 1e-6), 0, 1)
    return g ** gamma


def to_gray(im):
    return np.asarray(im.convert("L"), dtype=np.float32) / 255.0


def cover(im, w, h, cx=0.5, cy=0.5):
    """Crop to the w:h ratio around (cx, cy), then resize to w x h."""
    sw, sh = im.size
    r = w / h
    if sw / sh > r:
        cw, ch = int(sh * r), sh
    else:
        cw, ch = sw, int(sw / r)
    x = int(np.clip(cx * sw - cw / 2, 0, sw - cw))
    y = int(np.clip(cy * sh - ch / 2, 0, sh - ch))
    return im.crop((x, y, x + cw, y + ch)).resize((w, h), Image.LANCZOS)


def save_bits(bits, name, px=2, transparent=False):
    """Writes a 2-colour palette PNG with each dither dot px pixels wide."""
    big = np.repeat(np.repeat(bits, px, 0), px, 1)
    im = Image.fromarray(big.astype(np.uint8), "P")
    im.putpalette(list(INK) + list(BONE))
    kw = {"transparency": 0} if transparent else {}
    im.save(OUT / name, optimize=True, **kw)
    print(f"{name:26s} {im.size}  {(OUT / name).stat().st_size // 1024} KB")


def plate(src, name, w=720, h=450, cx=0.5, cy=0.5, lo=0.0, hi=1.0, gamma=1.0, px=2):
    g = levels(to_gray(cover(Image.open(src).convert("RGB"), w, h, cx, cy)), lo, hi, gamma)
    save_bits(atkinson(g), name, px)


# ── Planet limbs ───────────────────────────────────────────────────────────
def moon_limb(name, w, h, diameter, center_x, top, angle, gamma=0.8, gain=1.5):
    """A cap of the first-quarter Moon, rising from the bottom of the frame."""
    src = Image.open(FOUND / "moon-first-quarter.jpg").convert("L")
    # the disc in the source: centred, radius found from the lit/dark extent
    src = src.rotate(angle, resample=Image.BICUBIC, center=(1200, 1200))
    scale = diameter / 2040.0
    s = int(2400 * scale)
    src = src.resize((s, s), Image.LANCZOS)
    canvas = Image.new("L", (w, h), 0)
    canvas.paste(src, (int(center_x - s / 2), int(top - (s - diameter) / 2)))
    g = levels(np.asarray(canvas, np.float32) / 255 * gain, 0.04, 1.0, gamma)
    save_bits(atkinson(g), name, 2, transparent=True)


# ── Fig. 01: a black hole traced along Schwarzschild null geodesics ────────
def geodesics(n_b=900, n_phi=1400, dist=40.0, rs=1.0):
    """For each impact parameter, r(phi) along the photon path, from
    u'' = -u + (3/2) rs u^2 with u = 1/r. NaN once the ray is captured or gone."""
    b = np.linspace(0.05, 14.0, n_b)
    phi_max = 3.2 * np.pi
    dphi = phi_max / n_phi
    u = np.full(n_b, 1.0 / dist)
    v = np.sqrt(np.maximum(1 / b**2 - u**2 * (1 - rs * u), 0))
    table = np.full((n_phi, n_b), np.nan, np.float32)
    captured = np.zeros(n_b, bool)
    alive = np.ones(n_b, bool)

    def f(u, v):
        return v, -u + 1.5 * rs * u * u

    for i in range(n_phi):
        table[i, alive] = 1.0 / u[alive]
        k1u, k1v = f(u, v)
        k2u, k2v = f(u + dphi / 2 * k1u, v + dphi / 2 * k1v)
        k3u, k3v = f(u + dphi / 2 * k2u, v + dphi / 2 * k2v)
        k4u, k4v = f(u + dphi * k3u, v + dphi * k3v)
        u = u + dphi / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        v = v + dphi / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        captured |= alive & (u > 1 / rs)
        alive &= (u > 1 / (dist * 1.02)) & (u < 1 / rs)
    return b, dphi, table, captured


def black_hole(tilt_deg, name, table_pack, w=880, h=560, zoom=0.0295):
    b_axis, dphi, table, captured = table_pack
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    x = (xs - w / 2) * zoom
    y = (ys - h / 2 - h * 0.02) * zoom
    b = np.hypot(x, y)
    alpha = np.arctan2(y, x)
    bi = np.clip(((b - b_axis[0]) / (b_axis[1] - b_axis[0])).astype(int), 0, len(b_axis) - 1)
    th = np.radians(tilt_deg)
    # the disc's normal, seen from the camera; phi0 is where the ray first crosses it
    phi0 = np.arctan2(np.sin(th), -np.sin(alpha) * np.cos(th))
    phi0 = np.where(phi0 < 0, phi0 + np.pi, phi0)
    img = np.zeros((h, w), np.float32)
    for k in (2, 1, 0):  # back to front, so the direct image lands last
        pi_ = np.clip(((phi0 + k * np.pi) / dphi).astype(int), 0, table.shape[0] - 1)
        r = table[pi_, bi]
        hit = np.isfinite(r) & (r > 3.0) & (r < 11.5)
        # engraved rings, thinning outward; the approaching side burns brighter
        rings = 0.5 + 0.5 * np.cos(r * 11.0)
        line = (rings > 0.72).astype(np.float32)
        doppler = 0.55 + 0.45 * np.cos(alpha)
        fade = np.clip((11.5 - r) / 6.0, 0.15, 1)
        val = line * fade * (0.55 + 0.6 * doppler)
        img = np.where(hit & (val > 0), np.maximum(val, img * (k == 0)), img)
    # the photon ring, and the shadow inside it
    crit = 2.598
    img = np.where(np.abs(b - crit) < 0.035, 1.0, img)
    img = np.where(b < crit - 0.035, 0.0, img)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = BONE
    out[..., 3] = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    im.save(OUT / name, optimize=True)
    print(f"{name:26s} {im.size}  {(OUT / name).stat().st_size // 1024} KB")


# ── Project plates with something real drawn on them ───────────────────────
def gnss():
    """Shi–Tomasi corners tracked with Lucas–Kanade on the real terrain."""
    w, h = 720, 450
    base = cover(Image.open(FOUND / "himalayas-modis.jpg").convert("RGB"), w + 40, h + 40, 0.5, 0.42)
    a = np.asarray(base.convert("L"))
    f0, f1 = a[20 : 20 + h, 20 : 20 + w], a[9 : 9 + h, 34 : 34 + w]
    pts = cv2.goodFeaturesToTrack(f0, 70, 0.08, 34, blockSize=9)
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(f0, f1, pts, None, winSize=(25, 25), maxLevel=3)
    bits = atkinson(levels(f0.astype(np.float32) / 255, 0.08, 0.95, 1.15))
    draw = Image.fromarray(bits.astype(np.uint8) * 255)
    d = ImageDraw.Draw(draw)
    for p, q, ok in zip(pts[:, 0], nxt[:, 0], st[:, 0]):
        if not ok:
            continue
        x, y = p
        qx, qy = x + (q[0] - x) * 2.2, y + (q[1] - y) * 2.2
        d.rectangle([x - 6, y - 6, x + 6, y + 6], fill=0)
        d.rectangle([x - 4, y - 4, x + 4, y + 4], fill=255)
        d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=0)
        d.line([x, y, qx, qy], fill=0, width=4)
        d.line([x, y, qx, qy], fill=255, width=2)
    save_bits(np.asarray(draw) > 127, "gnss.png")


def sand():
    """Grains segmented from the specimen photograph, outlines drawn back on."""
    w, h = 720, 450
    im = cover(Image.open(FOUND / "sand-grains.jpg").convert("RGB"), w, h, 0.5, 0.4)
    g = to_gray(im)
    mask = (g > 0.13).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bits = atkinson(levels(g, 0.05, 0.85, 0.9))
    draw = Image.fromarray(bits.astype(np.uint8) * 255)
    d = ImageDraw.Draw(draw)
    for c in contours:
        if cv2.contourArea(c) < 150:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        m = 6
        for cx, cy, sx, sy in ((x - m, y - m, 1, 1), (x + bw + m, y - m, -1, 1), (x - m, y + bh + m, 1, -1), (x + bw + m, y + bh + m, -1, -1)):
            d.line([cx, cy, cx + 12 * sx, cy], fill=255, width=2)
            d.line([cx, cy, cx, cy + 12 * sy], fill=255, width=2)
    save_bits(np.asarray(draw) > 127, "sand.png")


def trishul():
    """A real Illgraben debris-flow recording and the STA/LTA trigger it set off, from the
    TRISHUL-Net repo. Ink becomes bone; the catalogue's event window becomes a dither tone."""
    a = np.asarray(Image.open(OWN / "trishul-stalta.png").convert("RGB")).astype(int)
    panels = (a[3:184, 4:-4], a[290:471, 4:-4])
    w, h = 720, 450
    tone = np.zeros((h, w), np.float32)
    ink = np.zeros((h, w), bool)

    def fit(mask, height):
        im = Image.fromarray((mask * 255).astype(np.uint8)).resize((w, height), Image.LANCZOS)
        return np.asarray(im, np.float32) / 255

    for i, p in enumerate(panels):
        y0, ph = (0, 244) if i == 0 else (252, 198)
        r, g, b = p[..., 0], p[..., 1], p[..., 2]
        line = (r + g + b < 420) | (r - g > 90)
        shade = (r - b > 12) & ~line
        if i == 1:  # the chart's legend box
            line[:64, 1146:] = False
            shade[:64, 1146:1226] = True
            shade[:64, 1226:] = False
        tone[y0 : y0 + ph] = fit(shade, ph) * 0.2
        ink[y0 : y0 + ph] = fit(line, ph) > 0.28
    save_bits(atkinson(tone) | ink, "trishul.png")


def lunar():
    """Siddhi's own results: the planned traverse, with radar, ice and illumination maps."""
    w, h = 720, 450
    top_h, gap = 208, 4
    t = Image.open(OWN / "lunar-traverse.jpg").convert("RGB").resize((w, top_h), Image.LANCZOS)
    a = np.asarray(t).astype(int)
    route = (a[..., 2] > 170) & (a[..., 1] > 170) & (a[..., 0] < 120)
    shadow = a[..., 2] - a[..., 0] > 26  # the permanently shadowed region, tinted blue in the source
    g = to_gray(t) * np.where(shadow, 0.62, 1.0)
    canvas = np.zeros((h, w), np.float32)
    canvas[:top_h] = levels(g, 0.2, 0.92, 1.15)
    side = (w - 2 * gap) // 3
    y0 = top_h + gap
    for i, n in enumerate(("cpr", "dual", "illum")):
        p = Image.open(OWN / f"lunar-{n}.jpg").convert("RGB").resize((side, side), Image.LANCZOS)
        x = i * (side + gap)
        gamma = {"cpr": 0.55, "dual": 1.0, "illum": 0.65}[n]
        canvas[y0 : y0 + side, x : x + side] = levels(to_gray(p), 0.03, 0.9, gamma)[: h - y0]
    bits = atkinson(canvas)
    k = np.ones((3, 3), np.uint8)
    edge = cv2.dilate(route.astype(np.uint8), k, iterations=2).astype(bool)
    bits[:top_h][edge] = False
    bits[:top_h][route] = True
    bits[top_h:y0] = False
    for i in (1, 2):
        bits[y0:, i * (side + gap) - gap : i * (side + gap)] = False
    save_bits(bits, "lunar.png")


def agewarp():
    """The result strip only, as a plate and as the original that shows on hover."""
    strip = Image.open(OWN / "agewarp.jpg").convert("RGB").crop((52, 146, 1404, 402))
    strip.save(OUT / "agewarp-strip.jpg", quality=88)
    # one dither dot per pixel: at the coarser size faces lose too much
    g = levels(to_gray(strip), 0.02, 0.95, 0.78)
    save_bits(atkinson(g), "agewarp.png", px=1)
    # phones: all five ages at once, three over two
    cell_w, cell_h, pitch, gap = 266, 256, 271, 10
    grid = np.zeros((cell_h * 2 + gap, cell_w * 3 + gap * 2), np.float32)
    for i in range(5):
        x, y = (i % 3) * (cell_w + gap), (i // 3) * (cell_h + gap)
        if i >= 3:
            x += (cell_w + gap) // 2
        grid[y : y + cell_h, x : x + cell_w] = g[:, i * pitch : i * pitch + cell_w]
    save_bits(atkinson(grid), "agewarp-phone.png", px=1)


def astronauts(colour_src, bw_src):
    im = Image.open(colour_src).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()
    im = im.crop(box)
    w = 1000
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(OUT / "astronaut-colour.webp", quality=90, method=6)
    # bone monochrome: luminance posterised to the mock's five inks
    a = np.asarray(im, np.float32)
    lum = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]) / 255
    lum = levels(lum, 0.06, 0.94, 0.92)
    steps = np.array([0.04, 0.3, 0.58, 0.8, 1.0])
    q = steps[np.abs(lum[..., None] - steps).argmin(-1)]
    out = np.empty_like(a)
    for c in range(3):
        out[..., c] = INK[c] + (BONE[c] - INK[c]) * q
    out[..., 3] = a[..., 3]
    mono = Image.fromarray(out.astype(np.uint8), "RGBA")
    mono.save(OUT / "astronaut.webp", quality=90, method=6)
    print("astronaut.webp", mono.size, (OUT / "astronaut.webp").stat().st_size // 1024, "KB")
    # the waving one, bone on ink, for the letter
    b = Image.open(bw_src).convert("L").crop((110, 60, 1190, 1140)).resize((720, 720), Image.LANCZOS)
    g = np.asarray(b, np.float32) / 255
    rgb = np.stack([INK[c] + (BONE[c] - INK[c]) * g for c in range(3)], -1).astype(np.uint8)
    Image.fromarray(rgb).save(OUT / "astronaut-wave.webp", quality=88, method=6)


def clip():
    """The aurora pass without NASA's title cards, at the size the 1-bit canvas reads."""
    c = cv2.VideoCapture(str(FOUND / "aurora-pass-iss.webm"))
    frames = []
    while True:
        ok, f = c.read()
        if not ok:
            break
        frames.append(f)
    w = cv2.VideoWriter(str(OUT / "aurora-pass.webm"), cv2.VideoWriter_fourcc(*"VP80"), 12, (360, 180))
    for f in frames[int(5.4 * 12) : int(15.6 * 12)]:
        g = cv2.cvtColor(f[120:480], cv2.COLOR_BGR2GRAY)
        w.write(cv2.cvtColor(cv2.resize(g, (360, 180), interpolation=cv2.INTER_AREA), cv2.COLOR_GRAY2BGR))
    w.release()


def main():
    clip()
    plate(FOUND / "aurora-iss.webp", "ionwatch.png", lo=0.05, hi=0.8, gamma=1.05)
    plate(OWN / "perihelion.jpg", "perihelion.png", cx=0.56, lo=0.05, hi=0.6, gamma=0.8)
    gnss()
    trishul()
    lunar()
    sand()
    agewarp()
    plate(FOUND / "earthrise.jpg", "earthrise.png", w=480, h=640, cx=0.62, cy=0.62, lo=0.03, hi=0.8, gamma=0.8)
    plate(FOUND / "aurora-pass-iss-poster.jpg", "clip-still.png", w=720, h=360, cy=1.0, lo=0.02, hi=0.9, gamma=1.7)
    plate(OWN / "anatomy-mirror.jpg", "dfi-anatomy.png", w=800, h=450, lo=0.02, hi=0.75, gamma=0.8)
    plate(OWN / "spawning-window.jpg", "dfi-spawning.png", w=640, h=400, lo=0.02, hi=0.85, gamma=0.8)
    plate(OWN / "scale-explorer.jpg", "dfi-scale.png", w=640, h=400, lo=0.25, hi=1.02, gamma=2.2)
    plate(OWN / "mascot.jpg", "dfi-mascot.png", w=640, h=400, cy=0.0, lo=0.05, hi=0.95, gamma=1.0)
    moon_limb("limb.png", 1100, 300, 2300, 760, 14, 58, gain=1.25)
    moon_limb("poster-moon.png", 360, 170, 620, 60, 18, 40, gamma=0.9, gain=1.15)
    pack = geodesics()
    for tilt, name in ((6, "fig-01.png"), (24, "fig-02.png"), (72, "fig-03.png")):
        black_hole(tilt, name, pack)
    if len(sys.argv) > 2:
        astronauts(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
