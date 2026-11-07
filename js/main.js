/* main.js — everything that moves. No libraries; the page reads fine without it. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)');
  let frozen = false;
  const moving = () => !calm.matches && !frozen;

  /* ── The sky: square stars in three depths ──────────────── */
  const sky = $('#sky');
  const ctx = sky.getContext('2d');
  const BONE = '#e6e1d7';
  let W = 0, H = 0, stars = [], sparks = [], meteor = null;
  let lastY = scrollY, vel = 0, mx = -999, my = -999;

  function seed() {
    W = sky.width = innerWidth;
    H = sky.height = innerHeight;
    const n = Math.min(240, Math.round((W * H) / 6000));
    stars = Array.from({ length: n }, () => {
      const depth = Math.random();
      return {
        x: Math.random() * W,
        y: Math.random() * H,
        z: depth,
        s: depth > 0.9 ? 3 : depth > 0.55 ? 2 : 1,
        a: 0.3 + depth * 0.7,
        t: Math.random() * 6.28,
      };
    });
    sparks = Array.from({ length: Math.max(3, Math.round(W / 420)) }, () => ({
      x: Math.random() * W, y: Math.random() * H, z: 0.4 + Math.random() * 0.4, r: 7 + Math.floor(Math.random() * 3) * 4,
    }));
  }

  function drawSky(now) {
    const y = scrollY;
    vel += (y - lastY - vel) * 0.25;
    lastY = y;
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = BONE;
    const warp = Math.min(Math.abs(vel) * 0.5, 44);
    for (const s of stars) {
      let py = (s.y - y * s.z * 0.22) % H;
      if (py < 0) py += H;
      let px = s.x;
      const dx = px - mx, dy = py - my, d2 = dx * dx + dy * dy;
      if (d2 < 16900) {
        const push = (1 - d2 / 16900) * 14;
        const d = Math.sqrt(d2) || 1;
        px += (dx / d) * push;
        py += (dy / d) * push;
      }
      ctx.globalAlpha = s.a * (0.72 + 0.28 * Math.sin(now * 0.0013 + s.t));
      ctx.fillRect(px | 0, py | 0, s.s, s.s + warp * s.z);
    }
    ctx.globalAlpha = 1;
    for (const s of sparks) {
      let py = (s.y - y * s.z * 0.22) % H;
      if (py < 0) py += H;
      const x = s.x | 0, yy = py | 0, r = s.r;
      ctx.fillRect(x - r, yy, r * 2 + 1, 1);
      ctx.fillRect(x, yy - r, 1, r * 2 + 1);
      ctx.fillRect(x - 1, yy - 1, 3, 3);
    }
    if (!meteor && Math.random() < 0.003) {
      meteor = { x: Math.random() * W * 0.7 + W * 0.2, y: Math.random() * H * 0.4, l: 0 };
    }
    if (meteor) {
      meteor.l += 1;
      for (let i = 0; i < 14; i += 1) {
        ctx.globalAlpha = 1 - i / 14;
        ctx.fillRect((meteor.x - meteor.l * 12 + i * 8) | 0, (meteor.y + meteor.l * 6 - i * 4) | 0, 2, 2);
      }
      ctx.globalAlpha = 1;
      if (meteor.l > 34) meteor = null;
    }
  }

  let last = 0;
  function loop(now) {
    requestAnimationFrame(loop);
    if (document.hidden || now - last < 33) return;
    last = now;
    if (moving()) { drawSky(now); stepAstro(); stepScope(); }
    if (clipRunning) drawClip();
  }

  addEventListener('resize', () => { seed(); if (!moving()) drawSky(0); });
  addEventListener('pointermove', (e) => { if (e.pointerType === 'mouse') { mx = e.clientX; my = e.clientY; } }, { passive: true });

  /* ── The astronaut: push her, she drifts home ───────────── */
  const astro = $('#astro');
  let ax = 0, ay = 0, avx = 0, avy = 0, ar = 0, held = false, px0 = 0, py0 = 0;
  function stepAstro() {
    if (!held) {
      avx += -ax * 0.006; avy += -ay * 0.006;
      avx *= 0.965; avy *= 0.965;
      ax += avx; ay += avy;
    }
    const parallax = Math.min(scrollY, innerHeight) * -0.12;
    ar = ax * 0.02;
    astro.style.transform = `translate3d(${ax.toFixed(1)}px,${(ay + parallax).toFixed(1)}px,0) rotate(${ar.toFixed(2)}deg)`;
  }
  astro.addEventListener('pointerdown', (e) => {
    held = true; px0 = e.clientX; py0 = e.clientY;
    astro.classList.add('held');
    astro.setPointerCapture(e.pointerId);
  });
  astro.addEventListener('pointermove', (e) => {
    if (!held) return;
    const dx = e.clientX - px0, dy = e.clientY - py0;
    px0 = e.clientX; py0 = e.clientY;
    ax += dx; ay += dy; avx = dx * 0.6; avy = dy * 0.6;
    if (!moving()) stepAstro();
  });
  const release = () => { held = false; astro.classList.remove('held'); };
  astro.addEventListener('pointerup', release);
  astro.addEventListener('pointercancel', release);
  astro.addEventListener('keydown', (e) => {
    const k = { ArrowLeft: [-9, 0], ArrowRight: [9, 0], ArrowUp: [0, -9], ArrowDown: [0, 9] }[e.key];
    if (!k) return;
    e.preventDefault();
    avx += k[0]; avy += k[1];
  });

  /* ── Fig. window: three angles on one black hole ────────── */
  const figImgs = $$('.fig-stack img');
  const figBtns = $$('.fig-tabs button');
  figBtns.forEach((b, i) => b.addEventListener('click', () => {
    figImgs.forEach((im, j) => im.classList.toggle('on', i === j));
    figBtns.forEach((x, j) => { x.classList.toggle('on', i === j); x.setAttribute('aria-pressed', String(i === j)); });
    $('#figNo').textContent = `Fig. 0${i + 1}`;
  }));

  /* ── The S4 scope ───────────────────────────────────────── *
   * A direct line plus a scattered component, I = |1 + s(x + iy)|²,
   * with x, y low-passed noise. S4 = sqrt(<I²> − <I>²) / <I>,
   * taken over the samples actually on screen.                 */
  const trace = $('#s4Trace');
  const range = $('#s4Range');
  const tctx = trace.getContext('2d');
  const N = trace.width, TH = trace.height;
  const samples = new Float32Array(N);
  let gx = 0, gy = 0, head = 0, sinceRead = 0, scopeSeen = false;
  const gauss = () => Math.sqrt(-2 * Math.log(Math.random() + 1e-9)) * Math.cos(6.283 * Math.random());
  function nextSample() {
    const s = (range.value / 100) * 0.9;
    gx = gx * 0.86 + gauss() * 0.5;
    gy = gy * 0.86 + gauss() * 0.5;
    const re = 1 + s * gx * 0.75, im = s * gy * 0.75;
    samples[head] = re * re + im * im;
    head = (head + 1) % N;
  }
  function readS4() {
    let a = 0, b = 0;
    for (let i = 0; i < N; i += 1) { a += samples[i]; b += samples[i] * samples[i]; }
    a /= N; b /= N;
    const s4 = Math.sqrt(Math.max(b - a * a, 0)) / a;
    $('#s4Val').textContent = `S4 ${s4.toFixed(2)}`;
    $('#s4Band').textContent = s4 < 0.3 ? 'weak scintillation' : s4 < 0.6 ? 'moderate scintillation' : 'strong scintillation';
  }
  function drawTrace() {
    tctx.fillStyle = '#0a0a09';
    tctx.fillRect(0, 0, N, TH);
    tctx.fillStyle = BONE;
    tctx.fillRect(0, (TH * 0.74) | 0, N, 1); // the undisturbed level
    for (let i = 0; i < N; i += 1) {
      const v = samples[(head + i) % N];
      const h = Math.min(TH - 2, Math.round(v * TH * 0.26));
      tctx.fillRect(i, TH - h, 1, 2);
      if (i % 2 === 0) tctx.fillRect(i, TH - h + 2, 1, h);
    }
  }
  function primeScope() { for (let i = 0; i < N; i += 1) nextSample(); drawTrace(); readS4(); }
  function stepScope() {
    if (!scopeSeen) return;
    nextSample(); nextSample();
    drawTrace();
    if ((sinceRead += 1) > 7) { sinceRead = 0; readS4(); }
  }
  range.addEventListener('input', primeScope);

  /* ── Footage, redrawn in one bit ────────────────────────── */
  const clip = $('#clip');
  const bitsCanvas = $('#clipBits');
  const visit = $('.visit');
  const bctx = bitsCanvas.getContext('2d', { willReadFrequently: true });
  const BW = bitsCanvas.width, BH = bitsCanvas.height;
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map((v) => (v + 0.5) * 16);
  let clipRunning = false;
  function drawClip() {
    if (clip.readyState < 2) return;
    bctx.drawImage(clip, 0, 0, BW, BH);
    let f;
    try { f = bctx.getImageData(0, 0, BW, BH); } catch { clipRunning = false; return; } // file:// taints the canvas; the still stays
    const d = f.data;
    for (let y = 0, i = 0; y < BH; y += 1) {
      const row = (y & 3) << 2;
      for (let x = 0; x < BW; x += 1, i += 4) {
        const l = d[i] * d[i] * 0.0105; // a curve, so city lights stay points against the dark
        const on = l > BAYER[row | (x & 3)];
        d[i] = on ? 230 : 10; d[i + 1] = on ? 225 : 10; d[i + 2] = on ? 215 : 9; d[i + 3] = 255;
      }
    }
    bctx.putImageData(f, 0, 0);
    visit.classList.add('bits');
  }
  new IntersectionObserver(([e]) => {
    const go = e.isIntersecting && moving();
    if (go) { clip.play().catch(() => {}); clipRunning = true; }
    else { clip.pause(); clipRunning = false; }
  }, { rootMargin: '200px' }).observe(visit);

  /* ── Entrances ──────────────────────────────────────────── */
  const seen = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add(e.target.classList.contains('folder') ? 'seen' : 'in');
      if (e.target.id === 'ionwatch') scopeSeen = true;
      seen.unobserve(e.target);
    }
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  $$('.rv, .folder').forEach((el) => {
    const sibs = [...el.parentElement.children].filter((c) => c.classList.contains('rv'));
    el.style.setProperty('--d', Math.max(sibs.indexOf(el), 0));
    seen.observe(el);
  });

  /* ── Nav: which section are we in ───────────────────────── */
  const links = $$('#siteNav a');
  const spy = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      const id = e.target.dataset.section;
      links.forEach((a) => {
        const here = a.dataset.spy === id;
        a.classList.toggle('here', here);
        if (here) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    }
  }, { rootMargin: '-45% 0px -50% 0px' });
  $$('[data-section]').forEach((s) => spy.observe(s));

  const menuBtn = $('#menuBtn');
  const nav = $('#siteNav');
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.textContent = open ? 'Close' : 'Menu';
  };
  menuBtn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  links.forEach((a) => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  /* Folder tabs: a stuck folder has no scroll position of its own, so work it out. */
  $$('.tab').forEach((tab) => tab.addEventListener('click', (e) => {
    const cab = $('#cabinet');
    const folder = tab.closest('.folder');
    if (getComputedStyle(folder).position !== 'sticky') return;
    e.preventDefault();
    const i = [...cab.children].indexOf(folder);
    const barH = $('.bar').offsetHeight;
    let top = cab.getBoundingClientRect().top + scrollY - barH;
    for (let k = 0; k < i; k += 1) top += cab.children[k].offsetHeight;
    scrollTo({ top, behavior: calm.matches ? 'auto' : 'smooth' });
    history.replaceState(null, '', tab.getAttribute('href'));
  }));

  /* ── Window controls ────────────────────────────────────── */
  $('#winMax').addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen?.();
  });
  const winMin = $('#winMin');
  winMin.addEventListener('click', () => {
    frozen = !frozen;
    document.body.classList.toggle('still', frozen);
    winMin.setAttribute('aria-pressed', String(frozen));
    winMin.setAttribute('aria-label', frozen ? 'Resume motion' : 'Freeze all motion');
    if (frozen) { clip.pause(); clipRunning = false; } else if (visit.getBoundingClientRect().top < innerHeight) { clip.play().catch(() => {}); clipRunning = true; }
  });
  const crt = $('#crt');
  $('#winOff').addEventListener('click', () => { crt.hidden = false; $('#crtOn').focus(); });
  $('#crtOn').addEventListener('click', () => { crt.hidden = true; $('#winOff').focus(); });

  /* ── Start ──────────────────────────────────────────────── */
  seed();
  primeScope();
  drawSky(0);
  requestAnimationFrame(loop);
  calm.addEventListener('change', () => drawSky(0));
})();
