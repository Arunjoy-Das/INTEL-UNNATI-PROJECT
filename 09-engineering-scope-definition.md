# 09. Engineering Scope Definition

## 🎯 In-Scope for MVP
The Minimum Viable Product focuses on delivering a functional, end-to-end fact-checking pipeline with a premium user interface.

- **Frontend:**
  - Single-page application using React.js and Tailwind CSS.
  - Interactive 3D globe hero section using Three.js/React Three Fiber.
  - Input form and results display.
- **Backend & API:**
  - FastAPI server with a single `/verify` endpoint and polling mechanism for results.
  - Basic rate-limiting.
- **Data & AI Pipeline:**
  - Basic language detection and translation (using existing APIs or lightweight models).
  - Claim Optimization Layer (extracting structured claims using spaCy/Transformers).
  - Vector Embedding (Sentence Transformers).
  - Fact Retrieval (FAISS/Pinecone) using a small, curated initial dataset (WHO, Govt sources).
  - Verification Engine determining logical entailment.
- **Infrastructure:**
  - Dockerized containers for local orchestration.
  - Deployment on accessible cloud platforms like Render, AWS, or GCP.

---

## ❌ Out of Scope for MVP
These features are explicitly deferred to future iterations to maintain development velocity for the core product.

1. **Real-time Social Media Streaming:**
   - No direct firehose ingestion from X (Twitter), Facebook, or Instagram APIs. Users must manually paste text or links.
2. **Large-scale Distributed Infrastructure:**
   - Complex Kubernetes (K8s) clusters and advanced multi-region load balancing are excluded. Docker Compose is sufficient for the MVP.
3. **Advanced Multilingual Fine-tuning:**
   - Training bespoke LLMs on specific dialects or rare vernacular languages. We will rely on translation to English for the initial semantic searches.
4. **User Accounts & Dashboards:**
   - MVP will focus on anonymous or basic token usage. Full user history dashboards and OAuth are deferred.
5. **Continuous Learning System:**
   - Automated ingestion of new facts into the vector database. The MVP vector DB will be pre-populated statically.
