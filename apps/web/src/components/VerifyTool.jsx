import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

const API_URL = import.meta.env.VITE_API_URL || "https://intel-unnati-project.onrender.com";

const fadeUp = {
  initial: { opacity: 0, y: 40 },
  whileInView: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: "easeOut" },
  viewport: { once: true, margin: "-50px" }
};

export default function VerifyTool() {
  const [text, setText] = useState('');
  const [lang, setLang] = useState('—');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [steps, setSteps] = useState([
    { label: '[ LANGUAGE DETECTION     ]', state: 'idle' },
    { label: '[ CLAIM OPTIMIZATION     ]', state: 'idle' },
    { label: '[ VECTOR SEARCH          ]', state: 'idle' },
    { label: '[ VERIFICATION ENGINE    ]', state: 'idle' }
  ]);

  const containerRef = useRef(null);

  const detectLang = (val) => {
    const isHindi = /[\u0900-\u097F]/.test(val);
    const isOdia = /[\u0B00-\u0B7F]/.test(val);
    if (isHindi) return 'HINDI [HI]';
    if (isOdia) return 'ODIA [OR]';
    return val.length > 0 ? 'ENGLISH [EN]' : '—';
  };

  const handleInput = (e) => {
    const val = e.target.value;
    setText(val);
    setLang(detectLang(val));
  };

  const handleVerify = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    setSteps(s => s.map(item => ({ ...item, state: 'idle' })));

    for (let i = 0; i < 4; i++) {
        setSteps(prev => prev.map((s, idx) => idx === i ? { ...s, state: 'active' } : s));
        await new Promise(r => setTimeout(r, 800 + Math.random() * 500));
        setSteps(prev => prev.map((s, idx) => idx === i ? { ...s, state: 'done' } : s));
    }

    try {
        const res = await fetch(`${API_URL}/api/v1/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        // Results now come directly from /verify (stateless mode)
        setResult(data.data);
    } catch (err) {
        console.error(err);
    } finally {
        setLoading(false);
    }
  };

  return (
    <section className="px-8 border-t border-[#e0e1e3]/10" id="verify-section" ref={containerRef}
             style={{ background: 'linear-gradient(180deg, #0b0c10 0%, #0e1015 100%)' }}>
      
      <motion.div {...fadeUp} className="max-w-[1000px] mx-auto text-center mb-16">
        <h2 className="text-[clamp(2.5rem,8vw,6rem)] leading-none font-display uppercase tracking-wider mb-3">VERIFY NOW</h2>
        <p className="text-[#e0e1e3]/40 tracking-widest text-sm uppercase">[ Neural Verification Pipeline Active ]</p>
      </motion.div>

      <motion.div 
        {...fadeUp}
        transition={{ duration: 0.8, ease: "easeOut", delay: 0.15 }}
        className="max-w-[800px] mx-auto glass-card p-10 relative group rounded-sm"
      >
        {/* Glow corner decorations */}
        <div className="absolute top-0 left-0 w-5 h-5 border-t-2 border-l-2 border-cyan -translate-x-1 -translate-y-1 group-hover:scale-125 transition-transform duration-500"></div>
        <div className="absolute bottom-0 right-0 w-5 h-5 border-b-2 border-r-2 border-cyan translate-x-1 translate-y-1 group-hover:scale-125 transition-transform duration-500"></div>

        <label className="block text-cyan text-base tracking-[0.25em] font-mono mb-6 uppercase">
          PASTE NEWS / SOCIAL POST / CLAIM
        </label>
        
        <textarea
          className="w-full bg-transparent border border-[#e0e1e3]/15 font-mono text-[#e0e1e3] p-8 text-xl min-h-[260px] outline-none focus:border-cyan/60 focus:shadow-[0_0_30px_rgba(102,252,241,0.1)] transition-all placeholder-[#e0e1e3]/15 mb-8 leading-relaxed rounded-sm"
          placeholder="e.g. Breaking! Drinking hot water cures all diseases..."
          value={text}
          onChange={handleInput}
          disabled={loading}
        ></textarea>

        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex gap-6 items-center">
            <span className="text-[#e0e1e3]/40 text-[0.85rem] tracking-widest uppercase">Detected Language:</span>
            <span className="text-cyan font-bold tracking-widest text-base">{lang}</span>
          </div>
          
          <button 
            onClick={handleVerify}
            disabled={loading || !text.trim()}
            className="btn-hover w-full md:w-auto bg-[#66fcf1] text-[#0a0a0a] px-16 py-7 font-bold tracking-[0.25em] hover:shadow-[0_0_50px_rgba(102,252,241,0.5)] transition-all disabled:opacity-30 disabled:cursor-not-allowed uppercase text-base border-none cursor-pointer rounded-sm"
          >
            {loading ? 'PROCESSING...' : 'CHECK FACTS >>'}
          </button>
        </div>
      </motion.div>

      {/* Loading Steps */}
      {loading && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="max-w-[800px] mx-auto mt-12 space-y-4 font-mono text-[0.9rem] tracking-widest"
        >
          {steps.map((s, i) => (
            <div key={i} className={`flex justify-between items-center ${s.state === 'active' ? 'text-cyan animate-pulse' : s.state === 'done' ? 'text-green' : 'text-[#e0e1e3]/25'}`}>
                <span>{s.label}</span>
                <span>{s.state === 'done' ? '██████████ ✓' : s.state === 'active' ? '░░░░░░░░░░' : '----------'}</span>
            </div>
          ))}
        </motion.div>
      )}

      {/* Results */}
      {result && (
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
          className="max-w-[800px] mx-auto mt-12 glass-card p-12 rounded-sm"
          style={{ borderColor: 'rgba(69, 162, 158, 0.25)' }}
        >
           <div className="grid md:grid-cols-3 gap-10">
              <div className="space-y-4">
                <span className="text-[0.8rem] text-[#e0e1e3]/35 tracking-widest block uppercase mb-2">EXTRACTED CLAIM</span>
                <p className="text-base border-l-2 border-cyan pl-5 italic leading-relaxed text-[#e0e1e3]/70">{result.extracted_claim}</p>
              </div>
              <div className="flex flex-col items-center justify-center text-center">
                <div className={`text-5xl font-bold tracking-tighter mb-3 ${
                  result.verdict === 'TRUE' ? 'text-green' : 
                  result.verdict === 'LIKELY TRUE' ? 'text-green' : 
                  result.verdict === 'FALSE' ? 'text-red' : 
                  result.verdict === 'MISLEADING' ? 'text-amber-500' : 
                  result.verdict === 'UNVERIFIED' ? 'text-amber-500' : 'text-[#e0e1e3]/30'
                }`}>{result.verdict}</div>
                <div className="w-full h-2 bg-[#e0e1e3]/8 relative overflow-hidden mt-3 rounded-full">
                    <div className="absolute left-0 top-0 h-full bg-cyan transition-all rounded-full" style={{ width: `${result.confidence_score * 100}%` }}></div>
                </div>
                <span className="text-[0.9rem] text-cyan tracking-widest mt-3 uppercase font-bold">Confidence: {Math.round(result.confidence_score * 100)}%</span>
              </div>
              <div className="space-y-4">
                 <span className="text-[0.8rem] text-[#e0e1e3]/35 tracking-widest block uppercase mb-2">SOURCE REFERENCE</span>
                 {result.sources.map((s, idx) => (
                     <div key={idx} className="text-base glass-card p-6 leading-relaxed rounded-sm">
                        <p className="mb-4 text-[#e0e1e3]/70">{s.text}</p>
                        <a href={s.url} target="_blank" className="text-cyan underline uppercase font-bold text-sm tracking-widest hover:text-[#e0e1e3]/90">{s.source}</a>
                    </div>
                 ))}
              </div>
           </div>
        </motion.div>
      )}
    </section>
  );
}
