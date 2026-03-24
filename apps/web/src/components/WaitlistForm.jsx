import { useState, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

const API_URL = import.meta.env.VITE_API_URL || "https://intel-unnati-project.onrender.com";

export default function WaitlistForm() {
  const [status, setStatus] = useState({ state: 'idle', message: '' }); // idle | transmitting | success | error
  const formRef = useRef(null);

  useGSAP(() => {
    gsap.from(formRef.current, {
      opacity: 0,
      y: 30,
      ease: 'power3.out',
      duration: 0.9,
      scrollTrigger: {
        trigger: formRef.current,
        start: 'top 85%',
        toggleActions: 'play none none reset'
      }
    });
  }, { scope: formRef });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    if (!data.name || !data.email) return;

    setStatus({ state: 'transmitting', message: '' });

    try {
      const res = await fetch(`${API_URL}/api/waitlist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await res.json();

      if (res.ok) {
        setStatus({ state: 'success', message: '> ' + result.message });
        e.target.reset();
      } else {
        setStatus({ state: 'error', message: '> Error: ' + result.detail });
      }
    } catch (err) {
      setStatus({ 
        state: 'error', 
        message: '> System Error: Connection Refused. Is the FastAPI backend online on port 8000?' 
      });
    }
  };

  return (
    <section className="border-t border-cream/20 py-32 px-8" id="join-network" ref={formRef}>
      <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h2 className="text-[clamp(3rem,8vw,8rem)] leading-[0.92] uppercase tracking-[0.03em] font-display" style={{ fontFamily: '"Bebas Neue", sans-serif' }}>
          <span>JOIN THE NETWORK</span>
        </h2>
      </div>
      
      <form onSubmit={handleSubmit} className="max-w-[600px] mx-auto flex flex-col gap-6">
        <div className="relative group p-2">
          {/* Bracket borders effect */}
          <div className="absolute inset-x-0 top-0 h-10 border-x border-cyan opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none -translate-x-2 group-hover:translate-x-0"></div>
          <input
            name="name"
            type="text"
            className="w-full bg-transparent border border-cream/20 text-cyan p-4 font-mono outline-none focus:border-[#b202fc] focus:shadow-[inset_0_0_15px_rgba(178,2,252,0.1),_0_0_15px_rgba(178,2,252,0.2)] transition-all placeholder-cream/60"
            placeholder="[ ENTER_NAME ]"
            required
            disabled={status.state === 'transmitting' || status.state === 'success'}
          />
        </div>
        
        <div className="relative group p-2">
          <input
            name="email"
            type="email"
            className="w-full bg-transparent border border-cream/20 text-cyan p-4 font-mono outline-none focus:border-[#b202fc] focus:shadow-[inset_0_0_15px_rgba(178,2,252,0.1),_0_0_15px_rgba(178,2,252,0.2)] transition-all placeholder-cream/60"
            placeholder="[ ENTER_EMAIL_ADDRESS ]"
            required
            disabled={status.state === 'transmitting' || status.state === 'success'}
          />
        </div>

        <div className="relative group p-2">
          <input
            name="company"
            type="text"
            className="w-full bg-transparent border border-cream/20 text-cyan p-4 font-mono outline-none focus:border-[#b202fc] focus:shadow-[inset_0_0_15px_rgba(178,2,252,0.1),_0_0_15px_rgba(178,2,252,0.2)] transition-all placeholder-cream/60"
            placeholder="[ AUTHORIZED_COMPANY_OR_ORG ]"
            disabled={status.state === 'transmitting' || status.state === 'success'}
          />
        </div>

        <button
          type="submit"
          disabled={status.state === 'transmitting' || status.state === 'success'}
          className="bg-transparent text-[#39ff14] font-bold text-base tracking-[0.2em] uppercase p-4 mt-4 border border-[#39ff14] hover:bg-[#39ff14] hover:text-black hover:shadow-[0_0_25px_rgba(57,255,20,0.5)] transition-all flex justify-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {status.state === 'transmitting' ? 'TRANSMITTING...' : status.state === 'success' ? 'ACCESS GRANTED [ OK ]' : 'REQUEST ACCESS >_'}
        </button>

        {status.message && (
          <div className={`mt-4 text-center text-sm font-mono tracking-widest ${status.state === 'success' ? 'text-[#39ff14]' : 'text-[#ff003c]'}`}>
            {status.message}
          </div>
        )}
      </form>
    </section>
  );
}
