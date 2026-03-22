import HeroCanvas from './components/HeroCanvas'
import WaitlistForm from './components/WaitlistForm'
import VerifyTool from './components/VerifyTool'
import GlobeSection from './components/GlobeSection'
import HowItWorks from './components/HowItWorks'

function App() {
  return (
    <div className="bg-[#0b0c10] min-h-screen text-[#c5c6c7] overflow-x-hidden font-mono selection:bg-cyan selection:text-black">
      
      {/* 0. Sticky Navbar */}
      <nav id="navbar" className="fixed top-0 left-0 w-full flex items-center justify-between px-8 py-4 border-b border-white/5 bg-[#0b0c10]/80 backdrop-blur-md z-[100]">
        <div className="flex items-center gap-12">
           <span className="text-[0.65rem] tracking-[0.3em] font-bold text-cyan uppercase">FACTGUARD_NODE_01</span>
           <div className="hidden md:flex gap-8">
              <a href="#verify-section" className="text-[0.6rem] tracking-[0.25em] text-cream/40 hover:text-cyan transition-colors uppercase">VERIFY</a>
              <a href="#pipeline" className="text-[0.6rem] tracking-[0.25em] text-cream/40 hover:text-cyan transition-colors uppercase">PIPELINE</a>
              <a href="#join-network" className="text-[0.6rem] tracking-[0.25em] text-cream/40 hover:text-cyan transition-colors uppercase">ACCESS</a>
           </div>
        </div>
        <div className="flex gap-4">
           <div className="h-2 w-2 rounded-full bg-neon-green animate-pulse"></div>
           <span className="text-[0.55rem] tracking-[0.3em] text-cream/40">NETWORK ONLINE</span>
        </div>
      </nav>

      {/* 1. Cinematic Hero Canvas Sequence (Pins) */}
      <HeroCanvas />

      {/* 2. Manifesto / Marquee */}
      <div className="marquee-wrap overflow-hidden border-y border-[#45a29e]/20 py-3 bg-[#0b0c10] relative z-20">
        <div className="marquee-track flex w-max gap-8" style={{ animation: 'marqueeScroll 26s linear infinite' }}>
          {[...Array(6)].map((_, i) => (
             <span key={i} className="text-[0.65rem] tracking-[0.22em] text-[#c5c6c7]/60 uppercase flex items-center gap-3">
                <span className="text-[#66fcf1]">—</span> COMBATING DISINFORMATION <span className="text-cyan">::</span> VERNACULAR AI PIPELINE <span className="text-cyan">::</span> TRUTH VALIDATION
             </span>
          ))}
        </div>
      </div>

      {/* 3. Neural Verification Tool */}
      <VerifyTool />

      {/* 4. Global Network Visualization (3D Globe) */}
      <GlobeSection />

      {/* 5. How It Works (Pipeline) */}
      <HowItWorks />

      {/* 6. Join the Network Form */}
      <WaitlistForm />

      {/* Footer */}
       <footer className="py-12 px-8 border-t border-cream/10 bg-[#0b0c10] text-[#c5c6c7]/40 text-center font-mono text-[0.6rem] tracking-[0.4em] uppercase">
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
