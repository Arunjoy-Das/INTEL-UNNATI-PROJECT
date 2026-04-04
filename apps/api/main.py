from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Standard CORS Middleware setup for Production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Temporarily allow all for Vercel -> Render production testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safe database initialization — don't crash if DB is unavailable
try:
    from src.core.database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("[STARTUP] Database tables created successfully.")
except Exception as e:
    print(f"[STARTUP WARNING] Database init failed: {e}")
    print("[STARTUP WARNING] Verify endpoint will still work (stateless mode).")

# Ingest Routers
from src.routers import waitlist, verify
app.include_router(waitlist.router, prefix="/api", tags=["waitlist"])
app.include_router(verify.router, prefix="/api/v1", tags=["verification"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "engine": "FactGuard Triangulation Engine v3",
        "services": {
            "verification": "up",
            "search": "up"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
