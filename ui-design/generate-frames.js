/**
 * FactGuard — Placeholder Frame Generator
 * =========================================
 * Generates 100 placeholder image frames for testing the canvas
 * scroll-sequence animation WITHOUT needing your real video frames.
 *
 * HOW TO RUN:
 *   npm install canvas
 *   node generate-frames.js
 *
 * OUTPUT:
 *   Creates 100 files: assets/frames/001.jpg ... assets/frames/100.jpg
 *
 * ── REPLACING WITH YOUR REAL FRAMES ──────────────────────────────────
 * Once you have exported your actual video frames:
 *   1. Name them 001.jpg, 002.jpg ... 100.jpg  (zero-padded 3 digits)
 *   2. Drop them into:  ui-design/assets/frames/
 *   3. Adjust TOTAL_FRAMES in sequence.js if you have more/fewer frames
 *   4. Delete this script — it's no longer needed
 * ─────────────────────────────────────────────────────────────────────
 */

const { createCanvas } = require('canvas');
const fs   = require('fs');
const path = require('path');

const TOTAL_FRAMES = 100;
const WIDTH  = 1920;
const HEIGHT = 1080;
const OUT    = path.join(__dirname, 'assets', 'frames');

// Palette transitions: Day City → Purple Night City (matching our hero images)
//   Frame 1  → teal/gold  (hero.png mood)
//   Frame 50 → transition orange/gold
//   Frame 100 → deep purple (hero2.png mood)
function getColors(t) {
  // t = 0..1
  const lerp = (a, b, t) => Math.round(a + (b - a) * t);
  if (t < 0.5) {
    const s = t / 0.5;
    return {
      bg1: [lerp(2,  20, s), lerp(20, 10, s), lerp(40, 30, s)],
      bg2: [lerp(10, 80, s), lerp(80, 40, s), lerp(80, 20, s)],
      accent: [lerp(47,200,s), lerp(244,100,s), lerp(221,50,s)],
    };
  } else {
    const s = (t - 0.5) / 0.5;
    return {
      bg1: [lerp(20, 30, s), lerp(10,  5, s), lerp(30,40, s)],
      bg2: [lerp(80, 60, s), lerp(40, 10, s), lerp(20,80, s)],
      accent: [lerp(200,155,s), lerp(100,30,s), lerp(50,229,s)],
    };
  }
}

function r(v) { return `rgb(${v[0]},${v[1]},${v[2]})`; }

console.log(`Generating ${TOTAL_FRAMES} placeholder frames → ${OUT}`);

for (let i = 1; i <= TOTAL_FRAMES; i++) {
  const t = (i - 1) / (TOTAL_FRAMES - 1);
  const colors = getColors(t);

  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx    = canvas.getContext('2d');

  // ── Background gradient ──
  const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
  grad.addColorStop(0, r(colors.bg1));
  grad.addColorStop(1, r(colors.bg2));
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // ── Grid lines ──
  ctx.strokeStyle = `rgba(255,253,187,0.08)`;
  ctx.lineWidth = 1;
  for (let x = 0; x < WIDTH; x += 60) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, HEIGHT); ctx.stroke();
  }
  for (let y = 0; y < HEIGHT; y += 60) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(WIDTH, y); ctx.stroke();
  }

  // ── Glowing orb (moves from right to left as frames progress) ──
  const orbX = WIDTH * (1 - t * 0.6);
  const orbY = HEIGHT * 0.5;
  const orbGrad = ctx.createRadialGradient(orbX, orbY, 0, orbX, orbY, 400);
  orbGrad.addColorStop(0, `rgba(${colors.accent.join(',')},0.4)`);
  orbGrad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = orbGrad;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // ── City silhouette (simple procedural) ──
  ctx.fillStyle = `rgba(0,0,0,0.6)`;
  const buildingCount = 18;
  for (let b = 0; b < buildingCount; b++) {
    const bx = (b / buildingCount) * WIDTH;
    const bw = (WIDTH / buildingCount) * 0.65;
    const bh = 100 + Math.sin(b * 1.7 + t * Math.PI) * 200 + 100;
    ctx.fillRect(bx, HEIGHT - bh, bw, bh);
  }

  // ── Frame number text ──
  ctx.fillStyle = 'rgba(255,253,187,0.25)';
  ctx.font = 'bold 48px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`FRAME ${String(i).padStart(3, '0')} / ${TOTAL_FRAMES}`, WIDTH / 2, HEIGHT / 2);

  // ── Progress bar at bottom ──
  ctx.fillStyle = 'rgba(47,244,221,0.35)';
  ctx.fillRect(0, HEIGHT - 6, WIDTH * t, 6);

  // ── Save as JPEG ──
  const fname  = path.join(OUT, String(i).padStart(3, '0') + '.jpg');
  const buffer = canvas.toBuffer('image/jpeg', { quality: 0.88 });
  fs.writeFileSync(fname, buffer);

  if (i % 10 === 0) process.stdout.write(`  [${i}/${TOTAL_FRAMES}] ✓\n`);
}

console.log('\n✅ Done! Drop your real frames into assets/frames/ to replace these.');
