import { useRef, useState, useEffect } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

const TOTAL_FRAMES = 180;
const FRAMES_DIR = '/assets/frames/ezgif-39aa8771a519ec62-jpg/';
const FILE_PREFIX = 'ezgif-frame-';
const FILE_EXT = '.jpg';
const ZERO_PAD = 3;

const SCRUB_END = '+=800%';
const LERP_FACTOR = 0.1;

// Priority loading: load first few frames + every Nth frame first
const PRIORITY_BATCH_SIZE = 8;  // First 8 frames for instant display
const PRIORITY_STEP = 10;       // Then every 10th frame for scrubbing

export default function HeroCanvas() {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [loadedCount, setLoadedCount] = useState(0);

  // High-performance refs
  const imagesRef = useRef(new Array(TOTAL_FRAMES).fill(null)); // Pre-sized Image Pool
  const targetFrameRef = useRef(0);
  const smoothFrameRef = useRef(0);
  const triggerRef = useRef(null);
  const canvasInstanceRef = useRef({ w: 0, h: 0 });
  const lastDrawnFrame = useRef(-1); // Skip redundant draws

  useGSAP(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: false }); // Opaque canvas = faster compositing
    if (!ctx) return;

    // ── RENDER LOGIC (Optimized) ──
    const drawImageCover = (img, w, h) => {
      const imgW = img.naturalWidth;
      const imgH = img.naturalHeight;
      const scale = Math.max(w / imgW, h / imgH);
      const drawW = imgW * scale;
      const drawH = imgH * scale;
      const drawX = (w - drawW) / 2;
      const drawY = (h - drawH) / 2;
      ctx.drawImage(img, drawX, drawY, drawW, drawH);
    };

    const render = (idx) => {
      const frameIdx = Math.max(0, Math.min(TOTAL_FRAMES - 1, Math.round(idx)));
      
      // Skip if already drawn this exact frame (prevents redundant GPU work)
      if (frameIdx === lastDrawnFrame.current) return;
      
      const img = imagesRef.current[frameIdx];
      const { w, h } = canvasInstanceRef.current;

      if (img && img.complete && img.naturalWidth > 0) {
        lastDrawnFrame.current = frameIdx;
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        ctx.clearRect(0, 0, w, h);
        drawImageCover(img, w, h);

        // Vignette overlay
        const grad = ctx.createRadialGradient(w / 2, h / 2, h * 0.3, w / 2, h / 2, h * 0.9);
        grad.addColorStop(0, 'rgba(0,0,0,0)');
        grad.addColorStop(1, 'rgba(0,0,0,0.65)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // Scan lines
        ctx.fillStyle = 'rgba(0,0,0,0.04)';
        for (let y = 0; y < h; y += 4) ctx.fillRect(0, y, w, 1.5);
      } else {
        ctx.fillStyle = '#111';
        ctx.fillRect(0, 0, w, h);
      }
    };

    // ── RESIZE ──
    const handleResize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2); // Cap at 2x for performance
      const w = window.innerWidth;
      const h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.scale(dpr, dpr);
      canvasInstanceRef.current = { w, h };
      lastDrawnFrame.current = -1; // Force redraw
      render(smoothFrameRef.current);
    };
    handleResize();
    window.addEventListener('resize', handleResize);

    // ── SMART PRELOAD (Priority + Background) ──
    let loaded = 0;
    const loadImage = (i) => {
      return new Promise((resolve) => {
        const frameNum = String(i + 1).padStart(ZERO_PAD, '0');
        const src = `${FRAMES_DIR}${FILE_PREFIX}${frameNum}${FILE_EXT}`;
        const img = new Image();
        img.src = src;
        img.onload = async () => {
          // Decode off main thread to prevent jank
          try { await img.decode(); } catch {}
          imagesRef.current[i] = img;
          loaded++;
          setLoadedCount(loaded);
          if (loaded === 1) render(0);
          resolve();
        };
        img.onerror = () => {
          loaded++;
          setLoadedCount(loaded);
          resolve();
        };
      });
    };

    const preload = async () => {
      // PHASE 1: Load first batch immediately (for instant hero display)
      const phase1 = [];
      for (let i = 0; i < Math.min(PRIORITY_BATCH_SIZE, TOTAL_FRAMES); i++) {
        phase1.push(loadImage(i));
      }
      await Promise.all(phase1);

      // PHASE 2: Load keyframes (every Nth) for responsive scrubbing
      const phase2 = [];
      for (let i = PRIORITY_BATCH_SIZE; i < TOTAL_FRAMES; i += PRIORITY_STEP) {
        phase2.push(loadImage(i));
      }
      await Promise.all(phase2);

      // PHASE 3: Fill remaining gaps in background (non-blocking)
      for (let i = 0; i < TOTAL_FRAMES; i++) {
        if (!imagesRef.current[i]) {
          await loadImage(i);
        }
      }

      if (triggerRef.current) triggerRef.current.refresh();
    };
    preload();

    // ── SCROLL TRIGGER ──
    const updateOverlay = (progress) => {
      const titleEl = document.getElementById('seq-title');
      if (titleEl) {
        titleEl.style.opacity = Math.max(0, 1 - progress / 0.35).toString();
        titleEl.style.transform = `translateX(-50%) translateY(calc(-54% + ${progress * -80}px))`;
      }
      const botEl = document.getElementById('seq-bottom');
      if (botEl) botEl.style.opacity = Math.max(0, 1 - progress / 0.20).toString();

      const s2El = document.getElementById('seq-scene2-label');
      if (s2El) s2El.style.opacity = Math.max(0, (progress - 0.65) / 0.20).toString();
    };

    triggerRef.current = ScrollTrigger.create({
      trigger: containerRef.current,
      pin: true,
      start: 'top top',
      end: SCRUB_END,
      scrub: true,
      onUpdate: (self) => {
        targetFrameRef.current = self.progress * (TOTAL_FRAMES - 1);
        updateOverlay(self.progress);
      }
    });

    // ── LERP LOOP (GSAP Ticker — runs on rAF internally) ──
    const tickerCallback = () => {
      const diff = targetFrameRef.current - smoothFrameRef.current;
      if (Math.abs(diff) > 0.05) {
        smoothFrameRef.current += diff * LERP_FACTOR;
        render(smoothFrameRef.current);
      }
    };
    gsap.ticker.add(tickerCallback);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (triggerRef.current) triggerRef.current.kill();
      gsap.ticker.remove(tickerCallback);
    };
  }, { scope: containerRef });

  return (
    <section id="seq-container" ref={containerRef} className="seq-layer relative h-screen w-full bg-black overflow-hidden text-cream">
      {/* GPU-accelerated canvas with will-change and translate3d */}
      <canvas 
        id="seq-canvas" 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full object-cover z-0"
        style={{ willChange: 'transform', transform: 'translate3d(0,0,0)' }}
      ></canvas>

      {/* Load Indicator */}
      {loadedCount < TOTAL_FRAMES && (
        <div id="load-indicator" style={{ 
          position: 'absolute', top: '50%', left: '50%', 
          transform: 'translate(-50%, -50%)', zIndex: 50, textAlign: 'center',
          willChange: 'opacity'
        }}>
          <span style={{ fontSize: '0.65rem', letterSpacing: '0.2em', marginBottom: '12px', color: '#2FF4DD', display: 'block' }}>
            LOADING SEQUENCE {loadedCount} / {TOTAL_FRAMES}
          </span>
          <div style={{ width: '180px', height: '2px', background: 'rgba(255,255,255,0.1)', position: 'relative', overflow: 'hidden' }}>
            <div 
               style={{ position: 'absolute', top: 0, left: 0, height: '100%', background: '#2FF4DD', transition: 'width 0.2s linear', width: `${(loadedCount / TOTAL_FRAMES) * 100}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Nav Overlay — GPU accelerated */}
      <div id="seq-nav" className="seq-overlay absolute top-0 left-0 w-full p-6 flex justify-between items-center z-10"
           style={{ willChange: 'transform', transform: 'translate3d(0,0,0)' }}>
        <span className="nav-label text-[0.6rem] tracking-[0.22em] text-cream/60">INTEGRITY</span>
        <div className="nav-links flex gap-8 pointer-events-auto">
          <a href="#verify-section" className="text-[0.68rem] tracking-[0.15em] text-cream/60 hover:text-cyan transition-colors">VERIFY</a>
          <a href="#pipeline" className="text-[0.68rem] tracking-[0.15em] text-cream/60 hover:text-cyan transition-colors">PIPELINE</a>
          <a href="#solutions" className="text-[0.68rem] tracking-[0.15em] text-cream/60 hover:text-cyan transition-colors">SOLUTIONS</a>
        </div>
        <span className="nav-label text-[0.6rem] tracking-[0.22em] text-cream/60">ADVANCEMENT</span>
      </div>

      <h1 
        id="seq-title" 
        style={{ 
          position: 'absolute', top: '50%', left: '50%', 
          transform: 'translateX(-50%) translateY(-54%)', zIndex: 10, 
          fontSize: 'clamp(4rem, 15vw, 16rem)', fontFamily: '"Bebas Neue", sans-serif', 
          color: 'white', whiteSpace: 'nowrap', userSelect: 'none',
          willChange: 'transform, opacity', backfaceVisibility: 'hidden'
        }}
      >
        FACTGUARD
      </h1>

      <p id="seq-scene2-label" 
         className="seq-overlay absolute bottom-20 left-1/2 -translate-x-1/2 text-[clamp(0.65rem,1.1vw,0.85rem)] tracking-[0.32em] uppercase whitespace-nowrap opacity-0 z-10 transition-opacity"
         style={{ willChange: 'opacity', transform: 'translate3d(-50%,0,0)' }}
      >
        WHERE MISINFORMATION MEETS ITS MATCH.
      </p>

      <div id="seq-bottom" className="seq-overlay absolute bottom-0 w-full grid grid-cols-[auto_1fr_auto] border-t border-cream/20 z-10"
           style={{ willChange: 'opacity', transform: 'translate3d(0,0,0)' }}>
        <div className="seq-panel p-6 border-r border-cream/20">
          <div className="panel-tag text-[0.55rem] tracking-[0.22em] text-cyan mb-2">MULTILINGUAL AI</div>
          <p className="panel-h text-sm uppercase leading-relaxed tracking-wider">AI-POWERED<br/>FACT VERIFICATION.<br/><span className="text-cyan">HINDI · ODIA · ENGLISH</span></p>
        </div>
        <div className="seq-panel cta-wrap flex items-center justify-end pr-8 pointer-events-auto border-r border-cream/20">
          <a href="#verify-section" className="cta-btn bg-cream text-black font-bold text-xs tracking-widest py-3 px-8 hover:bg-cyan hover:shadow-[0_0_24px_rgba(47,244,221,0.5)] transition-all">VERIFY A CLAIM ›</a>
        </div>
        <div className="seq-panel p-6 text-right">
          <div className="panel-tag text-[0.55rem] tracking-[0.22em] text-cyan mb-2">THROUGHPUT</div>
          <div className="stat-big font-display text-4xl">1000+</div>
          <div className="stat-label text-[0.56rem] tracking-[0.15em] text-cream/60">CLAIMS / MINUTE</div>
        </div>
      </div>
    </section>
  );
}
