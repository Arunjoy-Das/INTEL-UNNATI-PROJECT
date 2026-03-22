# 07. Monorepo Structure

The project uses a monorepo setup to cleanly organize the frontend, backend APIs, and the ML background workers.

```text
automated-fact-checker/
│
├── .github/                   # CI/CD pipelines and GitHub Actions
├── docker-compose.yml         # Local development orchestration
├── README.md                  # Root project documentation
│
├── apps/                      # Main applications
│   ├── web/                   # Frontend SPA (React + Three.js)
│   │   ├── package.json
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/    # Reusable UI elements (Three.js canvas, Forms)
│   │   │   ├── pages/         # Page layouts
│   │   │   └── services/      # API client wrappers
│   │   └── Dockerfile
│   │
│   ├── api/                   # FastAPI Backend Gateway
│   │   ├── requirements.txt
│   │   ├── main.py            # Entry point for FastAPI
│   │   ├── src/
│   │   │   ├── routers/       # API endpoints (/verify, /results)
│   │   │   ├── models/        # Pydantic schema / DB models
│   │   │   └── core/          # Config, DB connection, Auth
│   │   └── Dockerfile
│   │
│   └── worker/                # Async ML Worker Node (Celery/Kafka consumer)
│       ├── requirements.txt
│       ├── main.py            # Worker entry point
│       ├── src/
│       │   ├── optimization/  # Core claim extraction scripts (spaCy)
│       │   ├── retrieval/     # Sentence Transformers & FAISS/Pinecone logic
│       │   └── verification/  # Verdict logic and scoring
│       └── Dockerfile
│
├── packages/                  # Shared internal libraries (optional but good for scaling)
│   ├── database/              # Shared SQLAlchemy ORM models (used by api & worker)
│   └── types/                 # Shared schema definitions
│
└── tests/                     # Global E2E tests
    ├── integration/
    └── load_tests/
```

## 🐳 Docker Orchestration (`docker-compose.yml` Overview)
For local MVP development, the system runs 5 distinct containers:
1. `web` - Frontend React development server (Port 3000)
2. `api` - FastAPI Uvicorn server (Port 8000)
3. `worker` - Celery Worker consuming from Redis
4. `redis` - Message broker
5. `postgres` - Relational database (Port 5432)
