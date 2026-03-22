from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.db_models import VerificationRequest, VerificationResult
from src.models.schemas import VerificationSubmission, VerificationJobResponse, VerificationResultResponse, VerificationResultData, SourceReference
import datetime
import uuid
from src.services.verification_service import get_verification_service

router = APIRouter()

@router.post("/verify", status_code=202, response_model=VerificationJobResponse)
async def submit_verification(req: VerificationSubmission, db: Session = Depends(get_db)):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Terminal alert: No text provided for processing.")
    
    # Process using the new Backend Service (Workings Phase)
    v_service = get_verification_service()
    result = v_service.process_claim(req.text)
    
    new_req = VerificationRequest(
        raw_input=req.text,
        status="COMPLETED"
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    
    # 4. Save result to DB
    new_result = VerificationResult(
        request_id=new_req.id,
        verdict=result["verdict"],
        confidence_score=result["confidence_score"],
        matched_fact_ids={"indices": [r['text'][:20] for r in result["sources"]]}
    )
    db.add(new_result)
    db.commit()
    
    return {
        "request_id": new_req.id,
        "status": "COMPLETED",
        "message": "Terminal: Verification Sequence Active."
    }

@router.get("/results/{request_id}", response_model=VerificationResultResponse)
async def get_results(request_id: str, db: Session = Depends(get_db)):
    req = db.query(VerificationRequest).filter(VerificationRequest.id == request_id).one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="Request ID not found in Terminal registry.")
    
    if req.status != "COMPLETED":
         return {"request_id": request_id, "status": req.status, "message": "Neural processing in progress..."}

    v_service = get_verification_service()
    result = v_service.process_claim(req.raw_input)

    return {
        "request_id": req.id,
        "status": req.status,
        "data": {
            "original_text": req.raw_input,
            "detected_language": req.language or "en",
            "extracted_claim": req.extracted_claim or req.raw_input[:100],
            "verdict": req.result.verdict if req.result else "UNKNOWN",
            "confidence_score": req.result.confidence_score if req.result else 0.0,
            "sources": result["sources"]
        }
    }
