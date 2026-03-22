import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, OrbitControls, Float } from '@react-three/drei';
import * as THREE from 'three';

function DataGlobe() {
  const meshRef = useRef();
  
  // Rotate the globe
  useFrame((state, delta) => {
    if (meshRef.current) {
        meshRef.current.rotation.y += delta * 0.15;
    }
  });

  const points = useMemo(() => {
    // Generate some "data nodes" on the surface
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
      {/* Main Wireframe Globe */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[2, 32, 32]} />
        <meshBasicMaterial 
          color="#66fcf1" 
          wireframe 
          transparent 
          opacity={0.15} 
        />
      </mesh>

      {/* Core Glow */}
      <Sphere args={[1.8, 32, 32]}>
        <meshBasicMaterial color="#b202fc" transparent opacity={0.05} />
      </Sphere>

      {/* Interactive Data Nodes */}
      {points.map((p, i) => (
         <Float key={i} speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
            <mesh position={p}>
                <sphereGeometry args={[0.04, 8, 8]} />
                <meshBasicMaterial color={i % 3 === 0 ? "#39ff14" : "#66fcf1"} />
            </mesh>
         </Float>
      ))}
      
      {/* Connective pulses (Optional glow) */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
         <ringGeometry args={[2.05, 2.06, 64]} />
         <meshBasicMaterial color="#66fcf1" transparent opacity={0.3} side={THREE.DoubleSide} />
      </mesh>
    </group>
  );
}

export default function GlobeSection() {
  return (
    <section className="h-[700px] w-full relative bg-[#0b0c10] border-t border-cream/10 overflow-hidden flex items-center justify-center">
      <div className="absolute inset-x-0 top-0 h-full w-full opacity-30 z-0">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(102,252,241,0.05)_0%,transparent_70%)]"></div>
          {/* Grid Background */}
          <div className="absolute inset-0" style={{ backgroundImage: 'linear-gradient(rgba(102,252,241,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(102,252,241,0.03) 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>
      </div>

      <div className="container relative z-10 grid md:grid-cols-2 items-center gap-12 px-8">
        <div className="order-2 md:order-1 h-[500px] cursor-grab active:cursor-grabbing">
           <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} intensity={1} />
              <DataGlobe />
              <OrbitControls enableZoom={false} enablePan={false} autoRotate speed={0.5} />
           </Canvas>
        </div>
        
        <div className="order-1 md:order-2 space-y-6">
           <div className="inline-block px-3 py-1 border border-cyan/30 text-cyan text-[0.6rem] tracking-[0.3em] uppercase bg-cyan/5">
              GLOBAL NODE NETWORK
           </div>
           <h2 className="text-[clamp(3rem,6vw,5rem)] font-display text-cream leading-none uppercase">
              DECENTRALIZED<br/><span className="text-cyan">TRUTH INGESTION</span>
           </h2>
           <p className="text-cream/60 font-mono text-sm leading-relaxed max-w-[500px]">
              FactGuard’s extraction engine spans thousands of regional social endpoints. 
              Our neural clusters monitor vernacular narratives in real-time, identifying 
              misinformation patterns before they cross dialect boundaries.
           </p>
           
           <div className="flex gap-12 pt-4">
              <div>
                <div className="text-cyan font-display text-4xl">2.4M</div>
                <div className="text-cream/40 text-[0.55rem] tracking-widest uppercase mt-1">SITES SCANNED</div>
              </div>
              <div>
                <div className="text-neon-purple font-display text-4xl">45ms</div>
                <div className="text-cream/40 text-[0.55rem] tracking-widest uppercase mt-1">GLOBAL LATENCY</div>
              </div>
           </div>
        </div>
      </div>
    </section>
  );
}
