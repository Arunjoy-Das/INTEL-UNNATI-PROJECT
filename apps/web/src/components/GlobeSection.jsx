import { useRef, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, OrbitControls, Float } from '@react-three/drei';
import * as THREE from 'three';

const fadeUp = {
  initial: { opacity: 0, y: 40 },
  whileInView: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: "easeOut" },
  viewport: { once: true, margin: "-50px" }
};

function DataGlobe() {
  const meshRef = useRef();
  
  useFrame((state, delta) => {
    if (meshRef.current) {
        meshRef.current.rotation.y += delta * 0.15;
    }
  });

  const points = useMemo(() => {
    const temp = [];
    for (let i = 0; i < 40; i++) {
        const phi = Math.acos(-1 + (2 * i) / 40);
        const theta = Math.sqrt(40 * Math.PI) * phi;
        temp.push(new THREE.Vector3().setFromSphericalCoords(2.1, phi, theta));
    }
    return temp;
  }, []);

  return (
    <group>
      <mesh ref={meshRef}>
        <sphereGeometry args={[2, 32, 32]} />
        <meshBasicMaterial 
          color="#66fcf1" 
          wireframe 
          transparent 
          opacity={0.15} 
        />
      </mesh>

      <Sphere args={[1.8, 32, 32]}>
        <meshBasicMaterial color="#b202fc" transparent opacity={0.05} />
      </Sphere>

      {points.map((p, i) => (
         <Float key={i} speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
            <mesh position={p}>
                <sphereGeometry args={[0.04, 8, 8]} />
                <meshBasicMaterial color={i % 3 === 0 ? "#39ff14" : "#66fcf1"} />
            </mesh>
         </Float>
      ))}
      
      <mesh rotation={[Math.PI / 2, 0, 0]}>
         <ringGeometry args={[2.05, 2.06, 64]} />
         <meshBasicMaterial color="#66fcf1" transparent opacity={0.3} side={THREE.DoubleSide} />
      </mesh>
    </group>
  );
}

export default function GlobeSection() {
  return (
    <section className="min-h-[700px] w-full relative border-t border-[#e0e1e3]/8 overflow-hidden flex items-center justify-center"
             style={{ background: 'linear-gradient(180deg, #0b0c10 0%, #0a0e14 50%, #0b0c10 100%)' }}>
      <div className="absolute inset-x-0 top-0 h-full w-full opacity-30 z-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(102,252,241,0.04)_0%,transparent_70%)]"></div>
          <div className="absolute inset-0" style={{ backgroundImage: 'linear-gradient(rgba(102,252,241,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(102,252,241,0.02) 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>
      </div>

      <div className="container relative z-10 grid md:grid-cols-2 items-center gap-16 px-8">
        <div className="order-2 md:order-1 h-[500px] cursor-grab active:cursor-grabbing">
           <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} intensity={1} />
              <DataGlobe />
              <OrbitControls enableZoom={false} enablePan={false} autoRotate speed={0.5} />
           </Canvas>
        </div>
        
        <motion.div {...fadeUp} className="order-1 md:order-2 space-y-8">
           <div className="inline-block px-4 py-2 glass-card text-cyan text-[0.8rem] tracking-[0.3em] uppercase rounded-sm">
              GLOBAL NODE NETWORK
           </div>
           <h2 className="text-[clamp(3rem,6vw,5rem)] font-display text-[#e0e1e3] leading-none uppercase">
              DECENTRALIZED<br/><span className="text-cyan">TRUTH INGESTION</span>
           </h2>
           <p className="text-[#e0e1e3]/50 font-mono text-base leading-relaxed max-w-[500px]">
              FactGuard's extraction engine spans thousands of regional social endpoints. 
              Our neural clusters monitor vernacular narratives in real-time, identifying 
              misinformation patterns before they cross dialect boundaries.
           </p>
           
           <div className="flex gap-16 pt-4">
              <motion.div {...fadeUp} transition={{ duration: 0.8, delay: 0.2 }}>
                <div className="text-cyan font-display text-5xl">2.4M</div>
                <div className="text-[#e0e1e3]/35 text-[0.75rem] tracking-widest uppercase mt-2">SITES SCANNED</div>
              </motion.div>
              <motion.div {...fadeUp} transition={{ duration: 0.8, delay: 0.4 }}>
                <div className="text-neon-purple font-display text-5xl">45ms</div>
                <div className="text-[#e0e1e3]/35 text-[0.75rem] tracking-widest uppercase mt-2">GLOBAL LATENCY</div>
              </motion.div>
           </div>
        </motion.div>
      </div>
    </section>
  );
}
