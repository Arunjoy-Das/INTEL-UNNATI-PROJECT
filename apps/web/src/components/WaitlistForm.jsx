import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(ScrollTrigger, useGSAP);

const API_URL = import.meta.env.VITE_API_URL || "https://intel-unnati-project.onrender.com";

const fadeUp = {
  initial: { opacity: 0, y: 40 },
  whileInView: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: "easeOut" },
  viewport: { once: true, margin: "-50px" }
};

export default function WaitlistForm() {
  const [status, setStatus] = useState({ state: 'idle', message: '' });
  const formRef = useRef(null);

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
    <section className="border-t border-[#e0e1e3]/10 px-8" id="join-network" ref={formRef}
             style={{ background: 'linear-gradient(180deg, #0b0c10 0%, #0a0a0a 100%)' }}>
      
      <motion.div {...fadeUp} style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h2 className="text-[clamp(3rem,8vw,8rem)] leading-[0.92] uppercase tracking-[0.03em] font-display text-[#e0e1e3]">
          <span>JOIN THE NETWORK</span>
        </h2>
      </motion.div>
      
      <motion.form 
        {...fadeUp}
        transition={{ duration: 0.8, delay: 0.15 }}
        onSubmit={handleSubmit} 
        className="max-w-[600px] mx-auto flex flex-col gap-6"
      >
        <div className="relative group p-2">
          <div className="absolute inset-x-0 top-0 h-10 border-x border-cyan opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none -translate-x-2 group-hover:translate-x-0 duration-500"></div>
          <input
            name="name"
            type="text"
            className="w-full bg-transparent border border-[#e0e1e3]/15 text-cyan p-5 text-lg font-mono outline-none focus:border-[#b202fc] focus:shadow-[inset_0_0_20px_rgba(178,2,252,0.08),_0_0_20px_rgba(178,2,252,0.15)] transition-all placeholder-[#e0e1e3]/30 rounded-sm"
            placeholder="[ ENTER_NAME ]"
            required
            disabled={status.state === 'transmitting' || status.state === 'success'}
          />
        </div>
        
        <div className="relative group p-2">
          <input
            name="email"
            type="email"
            className="w-full bg-transparent border border-[#e0e1e3]/15 text-cyan p-5 text-lg font-mono outline-none focus:border-[#b202fc] focus:shadow-[inset_0_0_20px_rgba(178,2,252,0.08),_0_0_20px_rgba(178,2,252,0.15)] transition-all placeholder-[#e0e1e3]/30 rounded-sm"
            placeholder="[ ENTER_EMAIL_ADDRESS ]"
            required
            disabled={status.state === 'transmitting' || status.state === 'success'}
          />
        </div>

        <div className="relative group p-2">
          <input
            name="company"
            type="text"
            className="w-full bg-transparent border border-[#e0e1e3]/15 text-cyan p-5 text-lg font-mono outline-none focus:border-[#b202fc] focus:shadow-[inset_0_0_20px_rgba(178,2,252,0.08),_0_0_20px_rgba(178,2,252,0.15)] transition-all placeholder-[#e0e1e3]/30 rounded-sm"
            placeholder="[ AUTHORIZED_COMPANY_OR_ORG ]"
            disabled={status.state === 'transmitting' || status.state === 'success'}
          />
        </div>

        <button
          type="submit"
          disabled={status.state === 'transmitting' || status.state === 'success'}
          className="btn-hover bg-transparent text-[#39ff14] font-bold text-lg tracking-[0.2em] uppercase p-5 mt-4 border border-[#39ff14] hover:bg-[#39ff14] hover:text-[#0a0a0a] hover:shadow-[0_0_30px_rgba(57,255,20,0.4)] transition-all flex justify-center disabled:opacity-50 disabled:cursor-not-allowed rounded-sm"
        >
          {status.state === 'transmitting' ? 'TRANSMITTING...' : status.state === 'success' ? 'ACCESS GRANTED [ OK ]' : 'REQUEST ACCESS >_'}
        </button>

        {status.message && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mt-4 text-center text-base font-mono tracking-widest ${status.state === 'success' ? 'text-[#39ff14]' : 'text-[#ff003c]'}`}
          >
            {status.message}
          </motion.div>
        )}
      </motion.form>
    </section>
  );
}
