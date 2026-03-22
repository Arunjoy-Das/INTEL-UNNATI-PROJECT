# System Design

## 🧠 Overview
A distributed pipeline for high-speed fact-checking.

---

## 🔁 Data Flow

1. Input post received
2. Language detected
3. Text optimized → claim extracted
4. Claim converted to embedding
5. Query vector DB
6. Retrieve top facts
7. Verification engine compares
8. Result returned

---

## 🧩 Key Design Decisions

### 1. Use of Optimization Layer
- Reduces token size
- Improves speed
- Avoids noise

---

### 2. Vector Search Instead of Keyword Search
- Better semantic matching
- Handles multilingual variation

---

### 3. Async Processing
- Ensures high throughput
- Prevents bottlenecks

---

## ⚡ Performance Strategy
- Batch processing
- Caching frequent claims
- Lightweight models

---

## 📦 Scaling Strategy
- Horizontal scaling with containers
- Load balancing APIs

---

## 🔐 Reliability
- Fallback if no facts found
- Confidence scoring

---

## 🚀 Future Improvements
- Real-time social media integration
- Advanced multilingual models
- Continuous learning system