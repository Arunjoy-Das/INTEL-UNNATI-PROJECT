import { motion } from 'framer-motion';

const fadeUp = {
  initial: { opacity: 0, y: 40 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-50px" }
};

export default function HowItWorks() {
  const steps = [
    {
      num: "01",
      title: "INGESTION & NLP LAYER",
      text: "Accepts raw multilingual text. Detects Hindi, Odia, or English and translates it into a uniform processing logic.",
      accent: "text-cyan"
    },
    {
      num: "02",
      title: "CLAIM OPTIMIZATION",
      text: "Strips emotional noise and clickbait framing to extract the verifiable factual core.",
      accent: "text-neon-purple"
    },
    {
      num: "03",
      title: "VECTOR RETRIEVAL",
      text: "Dense embeddings queried against FAISS/Pinecone — WHO and Govt verified truth datasets.",
      accent: "text-neon-green"
    },
    {
      num: "04",
      title: "VERIFICATION ENGINE",
      text: "AI model compares claims vs retrieved facts to determine the final TRUE/FALSE verdict.",
      accent: "text-cyan"
    }
  ];

  return (
    <section className="px-8 border-t border-[#e0e1e3]/8" id="pipeline"
             style={{ background: 'linear-gradient(180deg, #0a0e14 0%, #0b0c10 100%)' }}>
       <div className="max-w-[1240px] mx-auto">
          <motion.div {...fadeUp} transition={{ duration: 0.8 }}>
            <div className="inline-block px-4 py-2 glass-card text-cyan text-[0.8rem] tracking-[0.35em] uppercase mb-8 rounded-sm">
               PIPELINE STACK
            </div>
            <h2 className="text-[clamp(3rem,6vw,5.5rem)] font-display text-[#e0e1e3] leading-none uppercase mb-24">
               HOW IT <span className="text-cyan">WORKS</span>
            </h2>
          </motion.div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12">
             {steps.map((s, i) => (
                <motion.div 
                  key={i}
                  {...fadeUp}
                  transition={{ duration: 0.8, ease: "easeOut", delay: i * 0.15 }}
                  className="group relative pt-14 border-t border-[#e0e1e3]/8 hover:border-cyan/40 transition-all duration-500"
                >
                   <div className={`absolute top-0 left-0 -translate-y-1/2 font-display text-5xl ${s.accent} opacity-30 group-hover:opacity-100 transition-opacity duration-500`}>
                      {s.num}
                   </div>
                   <h3 className="text-sm font-bold tracking-[0.2em] uppercase mb-5 text-[#e0e1e3]/70 group-hover:text-cyan transition-colors duration-300">
                      {s.title}
                   </h3>
                   <p className="text-[#e0e1e3]/40 font-mono text-[0.9rem] leading-relaxed">
                      {s.text}
                   </p>
                </motion.div>
             ))}
          </div>
       </div>
    </section>
  );
}
