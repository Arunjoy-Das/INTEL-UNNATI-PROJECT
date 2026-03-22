# 11. Environment and DevOps

The infrastructure prioritizes reproducibility, ease of deployment, and scalability for machine learning workloads.

## 🌍 Environments

1. **Local Development (Localhost)**
   - Orchestrated entirely via `docker-compose.yml`.
   - Employs hot-reloading for React and FastAPI.
   - Local Redis for message queuing.

2. **Staging Environment**
   - Replica of production using smaller compute instances.
   - Connected to a staging Vector DB to test new embedding models without muddying production data.

3. **Production Environment**
   - High-availability deployment.
   - Managed PostgreSQL database.
   - Managed Vector Database (e.g., Pinecone Serverless).

---

## ☁️ Deployment Strategy (MVP)

For the MVP, a PaaS provider like **Render** or **AWS (ECS/AppRunner)** provides the best balance of speed and control.

- **Frontend:** Deployed as static assets via Vercel or AWS S3/CloudFront for massive edge-caching and high performance.
- **API Gateway (FastAPI):** Deployed on a managed container service (Render Web Service or AWS AppRunner).
- **ML Workers (Celery):** Deployed on compute-heavy background instances. These must have sufficient RAM to load the HuggingFace transformer models into memory.

---

## 🔄 CI/CD Pipeline

**Tool:** GitHub Actions

**Workflows:**
1. **Validation (On Pull Request):**
   - Run Python linters (Black, Flake8).
   - Run React linters (ESLint).
   - Execute Unit Tests for API and ML functions.
   - Build test Docker images to ensure no dependency crashes.

2. **Deployment (On push to `main`):**
   - Build production Docker images.
   - Push images to a Container Registry (e.g., AWS ECR or Docker Hub).
   - Trigger rolling updates on the API and Worker container services to ensure zero downtime.
   - Trigger Vercel/Netlify build for the Frontend.
