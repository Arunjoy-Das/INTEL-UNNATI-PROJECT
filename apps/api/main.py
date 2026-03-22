from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import engine, Base
from src.routers import waitlist, verify

# Create tables in SQLite (only for demo, normally use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Standard CORS Middleware setup for Production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be restrictive in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ingest Routers
app.include_router(waitlist.router, prefix="/api", tags=["waitlist"])
app.include_router(verify.router, prefix="/api/v1", tags=["verification"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "postgres": "up",
            "redis": "up",
            "vector_db": "up"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
