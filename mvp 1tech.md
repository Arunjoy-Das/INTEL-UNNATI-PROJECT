# MVP + Tech Stack

## 🎯 Objective
Build a functional prototype of an AI-powered fact-checking system that:
- Extracts factual claims
- Retrieves verified information
- Outputs verification results
- Presents a premium minimal UI with 3D interaction

---

# 🧩 MVP Features

## 1. Input System
- Accept user input (text/news/social post)
- Optional: simple API endpoint

---

## 2. Claim Optimization (CORE)
- Remove noise (clickbait, emotions, filler text)
- Extract structured factual claim

Example:
Input:
"Breaking! Drinking hot water cures all diseases 😱"

Output:
"Claim: Drinking hot water cures diseases"

---

## 3. Fact Database
- Small curated dataset:
  - WHO
  - Government sources
  - Trusted organizations

---

## 4. Retrieval System
- Convert claim → embedding
- Perform semantic search
- Retrieve top relevant facts

---

## 5. Verification Engine
- Compare:
  Claim vs Retrieved Facts
- Output:
  - TRUE
  - FALSE
  - MISLEADING
  - UNKNOWN

---

## 6. Output Display
- Show:
  - Extracted claim
  - Retrieved fact
  - Final verdict
  - Confidence score

---

## 7. Frontend (UI/UX Focused)
- Single-page website
- Features:
  - 3D floating globe (hero section)
  - Smooth scroll transitions
  - Minimal premium design
  - Sticky navbar (Sign Up / Login)
  - Footer with developer info

---

# ❌ Not Included in MVP
- Real-time social media streaming
- Large-scale distributed infrastructure
- Advanced multilingual fine-tuning

---

# 🛠️ Tech Stack

## 🖥️ Frontend
- React.js
- Tailwind CSS
- Three.js / React Three Fiber
- Framer Motion

---

## ⚙️ Backend
- Python
- FastAPI

---

## 🧠 AI / ML
- HuggingFace Transformers
- Sentence Transformers (embeddings)
- spaCy (text processing)

---

## 🗄️ Database
- PostgreSQL (structured data)
- FAISS / Pinecone (vector database)

---

## 🔄 Async & Scaling (Optional for MVP)
- Redis
- Celery / Kafka

---

## 🌍 Language Processing
- Indic NLP
- Translation APIs (if needed)

---

## ☁️ Deployment
- Docker
- Render / AWS / GCP

---

# ⚡ Key Development Focus

- Lightweight models for speed
- Clean UI with smooth animations
- Efficient claim extraction (optimization layer)
- Modular backend for future scaling

---

# 🚀 MVP Success Criteria

- End-to-end working pipeline
- Accurate basic verification
- Smooth, premium UI experience
- Fast response time for small-scale input