from celery import Celery
import os
import time

# Standard Celery Config for FactGuard
celery_app = Celery(
    "factguard_worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

@celery_app.task(name="verify_claim")
def verify_claim(request_id: str, text: str):
    """
    Simulated Heavy ML Processing Pipeline
    """
    print(f"[+] Task Started: Processing Request {request_id}")
    
    # 1. Extraction (simulate spaCy delay)
    time.sleep(1)
    
    # 2. Retrieval (simulate vector search delay)
    time.sleep(1)
    
    # 3. Verdict Generation
    print(f"[+] Task Completed: Processed Request {request_id}")
    return {"status": "SUCCESS"}
