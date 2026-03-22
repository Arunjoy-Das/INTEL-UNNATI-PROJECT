# Architecture Overview

## 🧠 System Goal
Build a scalable AI-powered pipeline that processes high-volume multilingual news/social posts and verifies factual claims efficiently.

---

## 🏗️ High-Level Architecture

[ Data Sources ]
   ↓
[ Ingestion Layer ]
   ↓
[ Optimization Layer (Claim Extraction) ]
   ↓
[ Fact Retrieval Engine ]
   ↓
[ Verification Engine ]
   ↓
[ Storage + API Layer ]
   ↓
[ Frontend (3D Website UI) ]

---

## 🔹 Components

### 1. Data Ingestion Layer
- Collects posts from:
  - Social media APIs
  - News feeds
- Uses queue system (Kafka / Redis)

---

### 2. Language Processing Layer
- Detects language (Hindi, Odia, English)
- Translates to English for uniform processing

---

### 3. Optimization Layer (CORE)
- Removes noise (ads, emotions, clickbait)
- Extracts structured factual claims

Output:
> "Claim: XYZ happened"

---

### 4. Fact Retrieval Engine
- Uses vector database (FAISS / Pinecone)
- Retrieves most relevant verified facts
- Applies:
  - Time filtering
  - Source ranking

---

### 5. Verification Engine
- Compares claim vs retrieved facts
- Outputs:
  - TRUE / FALSE / MISLEADING / UNKNOWN

---

### 6. Storage Layer
- PostgreSQL → metadata
- Vector DB → embeddings

---

### 7. API Layer
- FastAPI backend
- Exposes endpoints:
  - /verify
  - /results

---

### 8. Frontend
- React + Three.js
- Minimal 3D landing experience
- Smooth scroll + globe interaction

---

## ⚡ Scalability Strategy
- Async processing (Celery/Kafka)
- Batch inference
- Caching repeated claims

---

## 🔐 Security
- API rate limiting
- Input sanitization