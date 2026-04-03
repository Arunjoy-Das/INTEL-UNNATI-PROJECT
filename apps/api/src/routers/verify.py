from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.schemas import VerificationSubmission
from src.services.verification_service import get_verification_service
import uuid

router = APIRouter()

@router.post("/verify", status_code=202)
async def submit_verification(req: VerificationSubmission):
    """
    Stateless verification endpoint.
    Runs the triangulation engine and returns results directly.
    No DB dependency — works even if PostgreSQL is down.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="No text provided for processing.")
    
    v_service = get_verification_service()
    result = v_service.process_claim(req.text)
    
    request_id = str(uuid.uuid4())
    
    # Try to save to DB (best-effort, don't crash if DB is unavailable)
    try:
        from src.models.db_models import VerificationRequest, VerificationResult
        db = next(get_db())
        new_req = VerificationRequest(
            id=request_id,
            raw_input=req.text,
            status="COMPLETED"
        )
        db.add(new_req)
        db.commit()
        
        new_result = VerificationResult(
            request_id=request_id,
            verdict=result["verdict"],
            confidence_score=result["confidence_score"],
            matched_fact_ids={"indices": [r['text'][:20] for r in result["sources"]]}
        )
        db.add(new_result)
        db.commit()
        db.close()
    except Exception as e:
        print(f"[DB WARNING] Could not save to database: {e}")
    
    return {
        "request_id": request_id,
        "status": "COMPLETED",
        "message": "Terminal: Verification Sequence Complete.",
        "data": {
            "original_text": req.text,
            "detected_language": "en",
            "extracted_claim": result.get("extracted_claim", req.text[:100]),
            "verdict": result["verdict"],
            "confidence_score": result["confidence_score"],
            "sources": result["sources"]
        }
    }

@router.get("/results/{request_id}")
async def get_results(request_id: str):
    """
    Retrieve saved results from DB. Falls back gracefully if DB is unavailable.
    """
    try:
        from src.models.db_models import VerificationRequest
        db = next(get_db())
        req = db.query(VerificationRequest).filter(VerificationRequest.id == request_id).one_or_none()
        db.close()
        
        if not req:
            raise HTTPException(status_code=404, detail="Request ID not found.")
        
        v_service = get_verification_service()
        result = v_service.process_claim(req.raw_input)
        
        return {
            "request_id": req.id,
            "status": req.status,
            "data": {
                "original_text": req.raw_input,
                "detected_language": req.language or "en",
                "extracted_claim": req.extracted_claim or req.raw_input[:100],
                "verdict": req.result.verdict if req.result else result["verdict"],
                "confidence_score": req.result.confidence_score if req.result else result["confidence_score"],
                "sources": result["sources"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[DB WARNING] Could not retrieve from database: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable. Use /verify endpoint directly.")
