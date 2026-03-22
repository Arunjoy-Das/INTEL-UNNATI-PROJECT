/* ═══════════════════════════════════════════════════
   FACTGUARD – app.js
   - Animated canvas dot grid background
   - Mock verify pipeline with animated steps
   - Stats counter animation
   - Language detection display
═══════════════════════════════════════════════════ */

/* ── 1. ANIMATED CANVAS DOT GRID ── */
(function () {
  const canvas = document.getElementById('bg-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];
  const SPACING = 40;
  const COLOR   = 'rgba(255,253,187,1)';

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    buildGrid();
  }

  function buildGrid() {
    particles = [];
    const cols = Math.ceil(W / SPACING);
    const rows = Math.ceil(H / SPACING);
    for (let r = 0; r <= rows; r++) {
      for (let c = 0; c <= cols; c++) {
        particles.push({
          x: c * SPACING,
          y: r * SPACING,
          baseX: c * SPACING,
          baseY: r * SPACING,
          alpha: Math.random() * 0.4 + 0.05,
          phase: Math.random() * Math.PI * 2,
          speed: Math.random() * 0.005 + 0.002,
        });
      }
    }
  }

  let frame = 0;
  function draw() {
    ctx.clearRect(0, 0, W, H);
    frame += 0.01;

    // Draw faint grid lines
    ctx.strokeStyle = 'rgba(255,253,187,0.04)';
    ctx.lineWidth = 1;
    const cols = Math.ceil(W / SPACING);
    const rows = Math.ceil(H / SPACING);
    for (let c = 0; c <= cols; c++) {
      ctx.beginPath();
      ctx.moveTo(c * SPACING, 0);
      ctx.lineTo(c * SPACING, H);
      ctx.stroke();
    }
    for (let r = 0; r <= rows; r++) {
      ctx.beginPath();
      ctx.moveTo(0, r * SPACING);
      ctx.lineTo(W, r * SPACING);
      ctx.stroke();
    }

    // Draw pulsing dots at intersections
    for (const p of particles) {
      const a = Math.sin(frame * p.speed * 60 + p.phase) * 0.3 + 0.1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1.2, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,253,187,${a})`;
      ctx.fill();
    }

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw();
})();


/* ── 2. LANGUAGE DETECTION (mock) ── */
const langMap = {
  'hi': 'HINDI  [HI]',
  'or': 'ODIA   [OR]',
  'en': 'ENGLISH [EN]',
};

function detectLang(text) {
  // Simple heuristic: check for Devanagari or Odia script chars
  if (/[\u0900-\u097F]/.test(text)) return 'hi';
  if (/[\u0B00-\u0B7F]/.test(text)) return 'or';
  return 'en';
}

const textarea = document.getElementById('claim-input');
const langDisplay = document.getElementById('lang-display');

textarea.addEventListener('input', function () {
  const lang = detectLang(this.value.trim());
  langDisplay.textContent = langMap[lang] || '—';
});


/* ── 3. MOCK VERIFY PIPELINE ── */
const verifyBtn    = document.getElementById('verify-btn');
const loadingPanel = document.getElementById('loading-panel');
const resultPanel  = document.getElementById('result-panel');

const steps       = [
  { el: document.getElementById('step-1'), label: '[ LANGUAGE DETECTION     ]', duration: 600 },
  { el: document.getElementById('step-2'), label: '[ CLAIM OPTIMIZATION     ]', duration: 900 },
  { el: document.getElementById('step-3'), label: '[ VECTOR SEARCH          ]', duration: 1000 },
  { el: document.getElementById('step-4'), label: '[ VERIFICATION ENGINE    ]', duration: 800 },
];

// Pre-baked demo results for demo purposes
const demoData = [
  {
    claim: 'Drinking hot water cures diseases',
    verdict: 'FALSE',
    confidence: 0.95,
    source: 'WHO — Hot water has not been proven to cure diseases. (who.int/myth-busters)',
  },
  {
    claim: 'COVID-19 vaccines have been approved by regulatory authorities',
    verdict: 'TRUE',
    confidence: 0.98,
    source: 'WHO — mRNA vaccines passed multi-phase clinical trials and received emergency use authorization. (who.int)',
  },
  {
    claim: 'Eating onions prevents virus infection',
    verdict: 'MISLEADING',
    confidence: 0.79,
    source: 'ICMR — Onions have some antimicrobial properties but cannot prevent viral infections. (icmr.gov.in)',
  },
];

function fillResult(data) {
  document.getElementById('extracted-claim').textContent = data.claim;
  document.getElementById('source-ref').textContent       = data.source;

  const badge = document.getElementById('verdict-badge');
  badge.textContent = data.verdict;
  badge.className   = `verdict-badge ${data.verdict}`;

  const pct = Math.round(data.confidence * 100);
  document.getElementById('conf-label').textContent = `CONFIDENCE: ${pct}%`;
  setTimeout(() => {
    document.getElementById('conf-bar').style.width = pct + '%';
  }, 100);
}

verifyBtn.addEventListener('click', async function () {
  const text = textarea.value.trim();
  if (!text) {
    textarea.focus();
    textarea.style.borderColor = '#FC4402';
    setTimeout(() => textarea.style.borderColor = '', 800);
    return;
  }

  // Reset
  resultPanel.style.display  = 'none';
  loadingPanel.style.display = 'block';
  steps.forEach(s => { s.el.className = 'load-step'; s.el.textContent = s.label + ' ░░░░░░░░░░'; });
  verifyBtn.disabled = true;
  verifyBtn.textContent = 'PROCESSING…';

  // Animate each step
  for (let i = 0; i < steps.length; i++) {
    const s = steps[i];
    s.el.classList.add('active');
    let fill = '';
    const tick = setInterval(() => {
      fill += '█';
      s.el.textContent = s.label + ' ' + fill.padEnd(10, '░');
    }, s.duration / 10);

    await new Promise(res => setTimeout(res, s.duration));
    clearInterval(tick);
    s.el.textContent = s.label + ' ██████████ ✓';
    s.el.classList.remove('active');
    s.el.classList.add('done');
  }

  // Show result
  const demo = demoData[Math.floor(Math.random() * demoData.length)];
  fillResult(demo);

  loadingPanel.style.display = 'none';
  resultPanel.style.display  = 'block';
  resultPanel.scrollIntoView({ behavior: 'smooth', block: 'center' });

  verifyBtn.disabled = false;
  verifyBtn.textContent = 'CHECK FACTS >';
});


/* ── 4. COUNTER ANIMATION ── */
function animateCounter(el) {
  const target   = parseInt(el.dataset.target, 10);
  const duration = 2000;
  const start    = performance.now();

  function tick(now) {
    const elapsed  = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 4);
    el.textContent = Math.round(eased * target);
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      animateCounter(e.target);
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach(el => observer.observe(el));


/* ══════════════════════════════════════════════════════
   ANIMATION ENGINE
══════════════════════════════════════════════════════ */

/* ── 5. PAGE INTRO: remove overlay after animation finishes ── */
const pageIntro = document.getElementById('page-intro');
if (pageIntro) {
  // The CSS animation takes ~2.7s total; remove from DOM after
  setTimeout(() => {
    pageIntro.style.display = 'none';
  }, 2800);
}

/* ── 6. CURSOR GLOW TRACKER ── */
const cursorGlow = document.getElementById('cursor-glow');
if (cursorGlow) {
  let mouseX = -999, mouseY = -999;
  let glowX = -999, glowY = -999;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Smooth lerp so the glow lags behind cursor slightly
  function lerpGlow() {
    glowX += (mouseX - glowX) * 0.08;
    glowY += (mouseY - glowY) * 0.08;
    cursorGlow.style.left = glowX + 'px';
    cursorGlow.style.top  = glowY + 'px';
    requestAnimationFrame(lerpGlow);
  }
  lerpGlow();

  document.addEventListener('mouseleave', () => { cursorGlow.style.opacity = '0'; });
  document.addEventListener('mouseenter', () => { cursorGlow.style.opacity = '1'; });
}

/* ── 7. HERO PARALLAX: title shifts up slightly on scroll ── */
const heroTitle = document.getElementById('hero-title');
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  if (heroTitle && scrollY < window.innerHeight) {
    heroTitle.style.transform = `translateY(${scrollY * 0.25}px)`;
  }
}, { passive: true });

/* ── 8. NAVBAR SHRINK: add .scrolled class when page scrolls ── */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
}, { passive: true });

/* ── 9. SCROLL REVEAL ENGINE ── */
// Targets: .reveal-up, .reveal-left, .reveal-right, .reveal-fade, .reveal-wipe
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      // Only unobserve non-repeating elements
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.12,
  rootMargin: '0px 0px -60px 0px',
});

document.querySelectorAll(
  '.reveal-up, .reveal-left, .reveal-right, .reveal-fade, .reveal-wipe'
).forEach(el => revealObserver.observe(el));

/* ── 10. SECTION TITLE CLIP-PATH REVEAL ── */
const titleRevealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      titleRevealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll('.section-title-reveal').forEach(el => {
  titleRevealObserver.observe(el);
});

/* ── 11. PIPELINE STEP connector line draw + step reveal ── */
const pipeObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Slight stagger per step
      setTimeout(() => {
        entry.target.classList.add('is-visible');
        // Trigger connectors
        const connector = entry.target.querySelector('.step-connector');
        if (connector) connector.style.transition = 'height 0.8s cubic-bezier(0.77,0,0.18,1)';

        // Trigger wipe on example block inside this step
        const wipe = entry.target.querySelector('.reveal-wipe');
        if (wipe) setTimeout(() => wipe.classList.add('is-visible'), 400);

      }, 0);
      pipeObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.pipeline-step').forEach((el, i) => {
  // Make them start invisible
  el.style.opacity = '0';
  el.style.transform = 'translateX(-30px)';
  el.style.transition = `opacity 0.65s cubic-bezier(0.16,1,0.3,1) ${i * 0.15}s, transform 0.65s cubic-bezier(0.16,1,0.3,1) ${i * 0.15}s`;
  pipeObserver.observe(el);
});

// When "is-visible" is added to pipeline-step, make it visible
const pipeStyleObserver = new MutationObserver((mutations) => {
  mutations.forEach(m => {
    if (m.target.classList.contains('is-visible')) {
      m.target.style.opacity = '1';
      m.target.style.transform = 'translateX(0)';
    }
  });
});
document.querySelectorAll('.pipeline-step').forEach(el => {
  pipeStyleObserver.observe(el, { attributes: true, attributeFilter: ['class'] });
});

/* ── 12. SECTION SUPER TEXT: staggered word-by-word reveal ── */
// Wrap each word in the about headings in a span for animation
document.querySelectorAll('.section-super').forEach(el => {
  el.style.overflow = 'hidden';
});

