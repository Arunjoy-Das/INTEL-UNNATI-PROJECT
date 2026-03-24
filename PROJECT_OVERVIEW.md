# 🛡️ FactGuard (SATYA) — Project Overview

**FactGuard** is a high-performance, AI-driven fact-verification platform designed to combat disinformation in real-time, with a primary focus on **vernacular languages (Hindi & Odia)**. It combines a cinematic, 3D-interactive user experience with a robust, multi-stage neural verification pipeline.

---

## 🚀 Core Working Principle: The Neural Pipeline

FactGuard doesn't just scan for keywords; it understands the semantic context of claims through a dedicated 4-stage pipeline:

1.  **Language Detection:** Automatically identifies the source script (English, Hindi, or Odia).
2.  **Claim Optimization:** Extracts the core verifiable assertion from complex, noisy social media posts.
3.  **Vector Search:** Queries a high-dimensional vector database (using **FAISS**) for related, verified facts.
4.  **Verification Engine:** Analyzes the similarity and trust-score to assign a final verdict (True/False/Unverified).

---

## 🎨 3D UI & Cinematic Experience

The frontend is designed to feel like a high-tech "intelligence terminal" (The Neural Network Aesthetic).

*   **Cinematic Hero Canvas:** A background sequence powered by **Three.js** and **React-Three-Fiber** that visualizes data packets moving through a neural mesh.
*   **Dynamic Animations:** Orchestrated via **GSAP (GreenSock)** for smooth, scroll-triggered transitions and micro-interactions.
*   **Global Visualization:** A 3D interactive globe showing real-time network status and verification nodes.
*   **Performance:** Built on **Vite** for sub-second hot-reloading and ultra-fast production builds.

---

## 🛠️ Genuine Tech Stack

### **Frontend Layers**
*   **UI Framework:** React 19 + Vite
*   **Styling:** Tailwind CSS 4.0 (Modern utility-first architecture)
*   **Interactivity:** GSAP + @gsap/react
*   **Graphics:** Three.js + @react-three/drei
*   **Icons:** Lucide-React

### **Backend Infrastructure (Powering the API)**
*   **Language:** Python 3.10+
*   **Web Framework:** FastAPI (Asynchronous, high-performance)
*   **Task Management:** Celery (Asynchonous task execution)
*   **Message Broker:** Redis (For real-time message passing)
*   **Database:** PostgreSQL (Metadata) + FAISS (Vector Store for ML)

### **Machine Learning & NLP**
*   **Embeddings:** Sentence-Transformers (for semantic claim analysis)
*   **Library:** SpaCy (Advanced NLP)
*   **Data Validation:** Pydantic V2
*   **Scraping:** BeautifulSoup4 (for live source verification)

---

## 🏗️ Monorepo Architecture

The project is organized into independent microservices for maximum scalability:
*   `/apps/web`: The interactive landing page and verification tool.
*   `/apps/api`: The primary gateway handling authentication and request orchestration.
*   `/apps/worker`: The background "brain" that runs the heavy machine learning models.

---

## ⚙️ Development & DevOps
*   **Orchestration:** Docker Compose (local environment)
*   **Deployment:** 
    *   **Frontend:** Vercel
    *   **API/Worker:** Render / AWS / AppRunner
*   **Versioning:** Git-based workflow with GitHub Actions (CI/CD)

---

© 2026 FACTGUARD — DECENTRALIZED VERIFICATION NETWORK
