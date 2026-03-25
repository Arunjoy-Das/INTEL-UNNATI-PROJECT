import { motion } from 'framer-motion'
import HeroCanvas from './components/HeroCanvas'
import WaitlistForm from './components/WaitlistForm'
import VerifyTool from './components/VerifyTool'
import GlobeSection from './components/GlobeSection'
import HowItWorks from './components/HowItWorks'

function App() {
  return (
    <div className="bg-gradient-to-b from-[#0a0a0a] to-[#111] min-h-screen text-[#e0e1e3] overflow-x-hidden font-mono">

      {/* 0. Glassmorphism Navbar */}
      <nav id="navbar" className="glass fixed top-0 left-0 w-full flex items-center justify-between px-8 py-4 z-[100]"
           style={{ backdropFilter: 'blur(14px) saturate(150%)', background: 'rgba(10,10,10,0.6)', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
        <div className="flex items-center gap-12">
           <span className="text-[0.75rem] tracking-[0.3em] font-bold text-cyan uppercase">FACTGUARD_NODE_01</span>
           <div className="hidden md:flex gap-8">
              <a href="#verify-section" className="text-[0.7rem] tracking-[0.25em] text-[#e0e1e3]/40 hover:text-cyan transition-colors uppercase">VERIFY</a>
              <a href="#pipeline" className="text-[0.7rem] tracking-[0.25em] text-[#e0e1e3]/40 hover:text-cyan transition-colors uppercase">PIPELINE</a>
              <a href="#join-network" className="text-[0.7rem] tracking-[0.25em] text-[#e0e1e3]/40 hover:text-cyan transition-colors uppercase">ACCESS</a>
           </div>
        </div>
        <div className="flex gap-4 items-center">
           <div className="h-2 w-2 rounded-full bg-neon-green animate-pulse"></div>
           <span className="text-[0.65rem] tracking-[0.3em] text-[#e0e1e3]/40">NETWORK ONLINE</span>
        </div>
      </nav>

      {/* 1. Cinematic Hero Canvas Sequence (GSAP — NOT modified) */}
      <HeroCanvas />

      {/* 2. Marquee with fade-in */}
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 1.2 }}
        viewport={{ once: true }}
        className="marquee-wrap overflow-hidden border-y border-[#45a29e]/15 py-4 bg-gradient-to-r from-[#0a0a0a] via-[#0f1014] to-[#0a0a0a] relative z-20"
      >
        <div className="marquee-track flex w-max gap-8">
          {[...Array(6)].map((_, i) => (
             <span key={i} className="text-[0.75rem] tracking-[0.22em] text-[#e0e1e3]/50 uppercase flex items-center gap-3">
                <span className="text-[#66fcf1]">—</span> COMBATING DISINFORMATION <span className="text-cyan">::</span> VERNACULAR AI PIPELINE <span className="text-cyan">::</span> TRUTH VALIDATION
             </span>
          ))}
        </div>
      </motion.div>

      {/* 3. Neural Verification Tool */}
      <VerifyTool />

      {/* 4. Global Network Visualization (3D Globe) */}
      <GlobeSection />

      {/* 5. How It Works (Pipeline) */}
      <HowItWorks />

      {/* 6. Join the Network Form */}
      <WaitlistForm />

      {/* Footer */}
       <footer className="py-16 px-8 border-t border-[#e0e1e3]/8 bg-gradient-to-b from-[#0a0a0a] to-[#080808] text-[#e0e1e3]/30 text-center font-mono text-[0.7rem] tracking-[0.4em] uppercase">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6 max-w-[1240px] mx-auto">
             <span>© 2026 FACTGUARD — DECENTRALIZED VERIFICATION</span>
             <div className="flex gap-8">
                <a href="#" className="hover:text-cyan transition-colors">OSINT</a>
                <a href="#" className="hover:text-cyan transition-colors">API_DOCS</a>
                <a href="#" className="hover:text-cyan transition-colors">LEGAL</a>
             </div>
          </div>
       </footer>
    </div>
  )
}

export default App
