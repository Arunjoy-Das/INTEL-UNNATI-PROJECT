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
    <section className="py-32 px-8 border-t border-cream/10 bg-[#0b0c10]" id="pipeline">
       <div className="max-w-[1240px] mx-auto">
          <div className="inline-block px-3 py-1 border border-cyan/30 text-cyan text-[0.6rem] tracking-[0.35em] uppercase bg-cyan/5 mb-6">
             PIPELINE STACK
          </div>
          <h2 className="text-[clamp(3rem,6vw,5.5rem)] font-display text-cream leading-none uppercase mb-20">
             HOW IT <span className="text-cyan">WORKS</span>
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12">
             {steps.map((s, i) => (
                <div key={i} className="group relative pt-12 border-t border-cream/10 hover:border-cyan/50 transition-colors">
                   <div className={`absolute top-0 left-0 -translate-y-1/2 font-display text-4xl ${s.accent} opacity-50 group-hover:opacity-100 transition-opacity`}>
                      {s.num}
                   </div>
                   <h3 className="text-xs font-bold tracking-[0.2em] uppercase mb-4 text-cream/80 group-hover:text-cyan">
                      {s.title}
                   </h3>
                   <p className="text-cream/50 font-mono text-[0.75rem] leading-relaxed">
                      {s.text}
                   </p>
                </div>
             ))}
          </div>
       </div>
    </section>
  );
}
