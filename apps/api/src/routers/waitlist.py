from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.db_models import WaitlistEntry
from src.models.schemas import WaitlistRequest
import datetime

router = APIRouter()

@router.post("/waitlist")
def join_waitlist(req: WaitlistRequest, db: Session = Depends(get_db)):
    # Check for duplicate email
    existing = db.query(WaitlistEntry).filter(WaitlistEntry.email == req.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Terminal alert: Email already registered in the Network.")
    
    new_entry = WaitlistEntry(
        name=req.name,
        email=req.email,
        company=req.company or "N/A"
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return {"success": True, "message": "Terminal: Access Granted"}
