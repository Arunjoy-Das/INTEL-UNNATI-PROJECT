import { useState, useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

const API_URL = import.meta.env.VITE_API_URL || "https://intel-unnati-project.onrender.com";

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
    
    // reset steps
    setSteps(s => s.map(item => ({ ...item, state: 'idle' })));

    // Simulating the 4 steps with delay
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
        
        // Final results fetch simulation
        const resFinal = await fetch(`${API_URL}/api/v1/results/${data.request_id}`);
        const finalData = await resFinal.json();
        
        setResult(finalData.data);
    } catch (err) {
        console.error(err);
    } finally {
        setLoading(false);
    }
  };

  return (
    <section className="py-32 px-8 border-t border-cream/20" id="verify-section" ref={containerRef}>
      <div className="max-w-[1000px] mx-auto text-center mb-16">
        <h2 className="text-[clamp(2.5rem,8vw,6rem)] leading-none font-display uppercase tracking-wider mb-2">VERIFY NOW</h2>
        <p className="text-cream/50 tracking-widest text-xs uppercase">[ Neural Verification Pipeline Active ]</p>
      </div>

      <div className="max-w-[800px] mx-auto bg-[#1f2833]/30 border border-cream/10 p-8 relative group">
        {/* Glow corner decorations */}
        <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-cyan -translate-x-1 -translate-y-1 group-hover:scale-110 transition-transform"></div>
        <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-cyan translate-x-1 translate-y-1 group-hover:scale-110 transition-transform"></div>

        <label className="block text-cyan text-[0.65rem] tracking-[0.25em] font-mono mb-4 uppercase">PASTE NEWS / SOCIAL POST / CLAIM</label>
        
        <textarea
          className="w-full bg-transparent border border-cream/20 font-mono text-cream p-4 min-h-[160px] outline-none focus:border-cyan transition-colors placeholder-cream/30 mb-8"
          placeholder="e.g. Breaking! Drinking hot water cures all diseases..."
          value={text}
          onChange={handleInput}
          disabled={loading}
        ></textarea>

        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex gap-4 items-center">
            <span className="text-cream/50 text-[0.65rem] tracking-widest uppercase">Detected Language:</span>
            <span className="text-cyan font-bold tracking-widest text-sm">{lang}</span>
          </div>
          
          <button 
            onClick={handleVerify}
            disabled={loading || !text.trim()}
            className="w-full md:w-auto bg-[#66fcf1] text-black px-12 py-5 font-bold tracking-widest hover:shadow-[0_0_35px_rgba(102,252,241,0.6)] transition-all disabled:opacity-30 disabled:cursor-not-allowed uppercase text-sm border-none cursor-pointer"
          >
            {loading ? 'PROCESSING...' : 'CHECK FACTS ›'}
          </button>
        </div>
      </div>

      {/* Loading Steps */}
      {loading && (
        <div className="max-w-[800px] mx-auto mt-12 space-y-3 font-mono text-[0.7rem] tracking-widest">
          {steps.map((s, i) => (
            <div key={i} className={`flex justify-between items-center ${s.state === 'active' ? 'text-cyan animate-pulse' : s.state === 'done' ? 'text-green' : 'text-cream/30'}`}>
                <span>{s.label}</span>
                <span>{s.state === 'done' ? '██████████ ✓' : s.state === 'active' ? '░░░░░░░░░░' : '----------'}</span>
            </div>
          ))}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="max-w-[800px] mx-auto mt-12 bg-[#0b0c10] border border-green/30 p-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
           <div className="grid md:grid-cols-3 gap-8">
              <div className="space-y-4">
                <span className="text-[0.6rem] text-cream/40 tracking-widest block uppercase">EXTRACTED CLAIM</span>
                <p className="text-sm border-l-2 border-cyan pl-4 italic">{result.extracted_claim}</p>
              </div>
              <div className="flex flex-col items-center justify-center text-center">
                <div className={`text-4xl font-bold tracking-tighter mb-2 ${
                  result.verdict === 'TRUE' ? 'text-green' : 
                  result.verdict === 'FALSE' ? 'text-red' : 
                  result.verdict === 'MISLEADING' ? 'text-amber-500' : 'text-cream/40'
                }`}>{result.verdict}</div>
                <div className="w-full h-1 bg-cream/10 relative overflow-hidden mt-2">
                    <div className="absolute left-0 top-0 h-full bg-cyan transition-all" style={{ width: `${result.confidence_score * 100}%` }}></div>
                </div>
                <span className="text-[0.6rem] text-cyan tracking-widest mt-2 uppercase">Confidence: {Math.round(result.confidence_score * 100)}%</span>
              </div>
              <div className="space-y-4">
                 <span className="text-[0.6rem] text-cream/40 tracking-widest block uppercase">SOURCE REFERENCE</span>
                 {result.sources.map((s, idx) => (
                    <div key={idx} className="text-[0.7rem] bg-white/5 p-3 border border-white/10">
                        <p className="mb-2">{s.text}</p>
                        <a href={s.url} target="_blank" className="text-cyan underline uppercase font-bold">{s.source}</a>
                    </div>
                 ))}
              </div>
           </div>
        </div>
      )}
    </section>
  );
}
