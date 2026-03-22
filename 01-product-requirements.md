# 01. Product Requirements Document (PRD)

## 📌 Product Name
Automated Fact Checker for Vernacular News

---

## 🎯 Objective
Enable fast, scalable detection of misinformation in multilingual content using AI. The system should provide a premium user experience while functionally verifying claims extracted from text, particularly in vernacular languages like Hindi and Odia.

---

## 👥 Target Audience
- **General Public:** Users looking to verify questionable news or claims from social media platforms.
- **Journalists:** Professionals needing quick verification of facts before publishing.
- **Government Agencies:** Entities monitoring misinformation and public sentiment.
- **Fact-checking Organizations:** Groups looking for an automated first-pass filtering of claims.

---

## 🧩 Core Features

### 1. Functional Features
- **Input Processing:** Accept raw text input (from news snippets, social media posts).
- **Language Detection & Translation:** Identify input languages (Hindi, Odia, English) and translate them to a standard processing language (typically English) if required.
- **Claim Optimization & Extraction:** Strip out noise (ads, emotions, clickbait) from the raw input and extract a structured factual claim (e.g., "Claim: XYZ happened").
- **Fact Retrieval:** Convert the extracted claim into embeddings and query a vector database (containing facts from WHO, Govt. sources, etc.) for semantic matches.
- **Verification Engine:** Compare the extracted claim with retrieved facts.
- **Result Output:** Clearly output the verification result as `TRUE`, `FALSE`, `MISLEADING`, or `UNKNOWN` along with confidence scores and retrieved context.

### 2. UI/UX Features
- **Minimalist 3D Landing Page:** An interactive and premium entry point featuring a 3D HTML canvas (e.g., floating globe) using Three.js.
- **Smooth Navigation:** Implement smooth scrolling transitions.
- **Clean Interface:** Non-cluttered design focusing strictly on the input and results.
- **Standard Navigation UI:** Sticky navbar with 'Sign Up' / 'Login' functionality, and a footer featuring developer information.

---

## ⚡ Non-Functional Requirements
- **High Throughput:** Need to support processing 1000+ items/minute in a scalable production environment (batch inference, Celery/Kafka).
- **Low Latency:** Fast response time, especially crucial for the MVP.
- **Scalability:** Horizontal scaling using containerized microservices (Docker) and load balancing.
- **Reliability:** Fallbacks implemented for scenarios with zero retrieved facts.
- **Security:** API rate limiting and rigorous input sanitization.

---

## 📊 Success Metrics
- **Accuracy:** Precision and recall of the verification engine.
- **Processing Speed:** End-to-end latency from input submission to result viewing.
- **User Engagement:** High interaction rates with the 3D elements and low bounce rates on the main verification tool. 
- **System Uptime:** Maintain near 100% uptime through load-balanced scaling.

---

## 🔐 System Constraints
- **Limited Compute Resources:** Dictates the necessity for lightweight models optimized for speed over pure size.
- **Optimization Necessity:** Emphasizes the creation of a 'claim optimization layer' to avoid passing unnecessarily large contexts or emotional noise into expensive embedding models.
