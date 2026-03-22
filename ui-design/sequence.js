/**
 * FactGuard — Real Image Sequence Engine
 * ========================================
 * GSAP + ScrollTrigger · Scroll-Scrubbed Real Frame Playback
 *
 * ── IMAGE SOURCE ───────────────────────────────────────────────────────
 * File pattern : ezgif-frame-001.jpg  →  ezgif-frame-180.jpg
 * Location     : ui-design/assets/frames/
 * ── TO CHANGE FRAMES IN THE FUTURE ────────────────────────────────────
 * Update TOTAL_FRAMES, FILE_PREFIX, FILE_EXT and FRAMES_DIR below.
 * ──────────────────────────────────────────────────────────────────────
 */

'use strict';

/* ══════════════════════════════════════════════════
   CONFIG  ← edit here if you rename or move frames
══════════════════════════════════════════════════ */
const TOTAL_FRAMES  = 180;                    // ezgif-frame-001 … ezgif-frame-180
const FRAMES_DIR    = './assets/frames/ezgif-39aa8771a519ec62-jpg/';     // path relative to index.html
const FILE_PREFIX   = 'ezgif-frame-';         // filename prefix before the number
const FILE_EXT      = '.jpg';                 // file extension
const ZERO_PAD      = 3;                      // "001", "042" etc.

const SCRUB_END     = '+=450%';               // how long the section stays pinned
const SCRUB_SMOOTH  = 0.5;                    // scrub smoothing (0 = instant)

/* ══════════════════════════════════════════════════
   CANVAS SETUP
══════════════════════════════════════════════════ */
const canvas = document.getElementById('seq-canvas');
const ctx    = canvas.getContext('2d');
let W, H;

function resizeCanvas() {
  W = canvas.width  = window.innerWidth;
  H = canvas.height = window.innerHeight;
  renderFrame(currentFrame);   // redraw current frame at new size
}
window.addEventListener('resize', () => {
  clearTimeout(window._resizeTimer);
  window._resizeTimer = setTimeout(resizeCanvas, 80);
});

/* ══════════════════════════════════════════════════
   STATE
══════════════════════════════════════════════════ */
const images   = new Array(TOTAL_FRAMES);   // pre-allocated image array
let loadedCount = 0;
let currentFrame = 0;

/* ══════════════════════════════════════════════════
   COVER-FIT DRAW
   Replicates CSS background-size: cover.
   Scales image so it fills the entire canvas
   without distortion, cropped from the centre.
══════════════════════════════════════════════════ */
function drawImageCover(img) {
  const imgW  = img.naturalWidth;
  const imgH  = img.naturalHeight;

  // Scale factor so the smaller dimension fills the canvas
  const scale = Math.max(W / imgW, H / imgH);

  const drawW = imgW * scale;
  const drawH = imgH * scale;

  // Centre the image (negative offsets crop the overflow)
  const drawX = (W - drawW) / 2;
  const drawY = (H - drawH) / 2;

  ctx.drawImage(img, drawX, drawY, drawW, drawH);
}

/* ══════════════════════════════════════════════════
   VIGNETTE OVERLAY
   A subtle darkening around the edges to give
   a cinematic, focused look to every frame.
══════════════════════════════════════════════════ */
function drawVignette() {
  const grad = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.9);
  grad.addColorStop(0, 'rgba(0,0,0,0)');
  grad.addColorStop(1, 'rgba(0,0,0,0.60)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);
}

/* ══════════════════════════════════════════════════
   CRT SCAN LINE OVERLAY
   Subtle horizontal line texture.
   Remove this call if you don't want it.
══════════════════════════════════════════════════ */
function drawScanLines() {
  ctx.fillStyle = 'rgba(0,0,0,0.04)';
  for (let y = 0; y < H; y += 4) {
    ctx.fillRect(0, y, W, 1.5);
  }
}

/* ══════════════════════════════════════════════════
   RENDER FRAME
   Core render function called by the GSAP onUpdate
   callback on every scroll tick.
══════════════════════════════════════════════════ */
function renderFrame(idx) {
  idx = Math.max(0, Math.min(TOTAL_FRAMES - 1, Math.round(idx)));
  currentFrame = idx;

  ctx.clearRect(0, 0, W, H);

  const img = images[idx];

  if (img && img.complete && img.naturalWidth > 0) {
    // ── Real image loaded: draw with cover fit ──
    drawImageCover(img);
    drawVignette();
    drawScanLines();
  } else {
    // ── Placeholder while loading: black with cyan border ──
    // (only shown briefly before first batch arrives)
    ctx.fillStyle = '#020100';
    ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = 'rgba(47,244,221,0.12)';
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 60) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke(); }
    for (let y = 0; y < H; y += 60) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke(); }
  }
}

/* ══════════════════════════════════════════════════
   PRELOAD ALL 180 FRAMES
   Loads all images simultaneously in the background.
   Fires onAllLoaded() when every image has resolved
   (success or error — we never block on a miss).
══════════════════════════════════════════════════ */
function preloadImages() {
  const barEl    = document.getElementById('load-bar-fill');
  const statusEl = document.getElementById('load-status-text');

  for (let i = 0; i < TOTAL_FRAMES; i++) {
    const frameNum = String(i + 1).padStart(ZERO_PAD, '0');   // "001" … "180"
    const src      = `${FRAMES_DIR}${FILE_PREFIX}${frameNum}${FILE_EXT}`;

    const img = new Image();
    img.src   = src;

    img.onload = img.onerror = () => {
      loadedCount++;

      // Update loading progress bar
      const pct = (loadedCount / TOTAL_FRAMES) * 100;
      if (barEl) barEl.style.width = pct + '%';
      if (statusEl) statusEl.textContent = `LOADING ${loadedCount} / ${TOTAL_FRAMES}`;

      if (loadedCount === TOTAL_FRAMES) onAllLoaded();
    };

    images[i] = img;
  }

  console.log(`[FactGuard] Preloading ${TOTAL_FRAMES} frames from ${FRAMES_DIR}`);
}

/* ══════════════════════════════════════════════════
   ON ALL LOADED
   Hides the loading indicator, re-renders the
   current frame with real pixels, refreshes GSAP.
══════════════════════════════════════════════════ */
function onAllLoaded() {
  const loadEl = document.getElementById('load-indicator');
  if (loadEl) {
    loadEl.style.opacity = '0';
    setTimeout(() => (loadEl.style.display = 'none'), 600);
  }

  renderFrame(currentFrame);
  ScrollTrigger.refresh();

  console.log(`[FactGuard] All ${TOTAL_FRAMES} frames preloaded. ✓`);
}

/* ══════════════════════════════════════════════════
   OVERLAY OPACITY
   Drives the text/UI panel visibility.
   Tied to scroll progress (0 → 1).
══════════════════════════════════════════════════ */
function updateOverlay(progress) {
  // FACTGUARD title: full → invisible by 35% progress
  const titleEl = document.getElementById('seq-title');
  if (titleEl) {
    const op = Math.max(0, 1 - progress / 0.35);
    titleEl.style.opacity   = op;
    titleEl.style.transform = `translateX(-50%) translateY(calc(-54% + ${progress * -80}px))`;
  }

  // Bottom panels: disappear by 20%
  const botEl = document.getElementById('seq-bottom');
  if (botEl) botEl.style.opacity = Math.max(0, 1 - progress / 0.20).toString();

  // Scene 2 tagline: fades in after 65%
  const s2El = document.getElementById('seq-scene2-label');
  if (s2El) s2El.style.opacity = Math.max(0, (progress - 0.65) / 0.20).toString();
}

/* ══════════════════════════════════════════════════
   GSAP SCROLLTRIGGER
   Pins #seq-container, ties scroll progress (0→1)
   to the image frame index (0 → TOTAL_FRAMES - 1).
   scrub: true  →  scrolling forward plays, backward rewinds.
══════════════════════════════════════════════════ */
function initScrollTrigger() {
  gsap.registerPlugin(ScrollTrigger);

  ScrollTrigger.create({
    trigger : '#seq-container',
    pin     : true,               // ← container stays fixed while scrolling
    start   : 'top top',
    end     : SCRUB_END,
    scrub   : SCRUB_SMOOTH,       // ← scroll tied, bidirectional scrub

    onUpdate(self) {
      const frameIndex = Math.round(self.progress * (TOTAL_FRAMES - 1));
      renderFrame(frameIndex);
      updateOverlay(self.progress);
    },
  });
}

/* ══════════════════════════════════════════════════
   BOOT
══════════════════════════════════════════════════ */
(function boot() {
  // 1. Size canvas
  W = canvas.width  = window.innerWidth;
  H = canvas.height = window.innerHeight;

  // 2. Draw black screen while images load
  ctx.fillStyle = '#020100';
  ctx.fillRect(0, 0, W, H);

  // 3. Start GSAP ScrollTrigger
  initScrollTrigger();

  // 4. Preload all 180 real frames in background
  preloadImages();
})();
