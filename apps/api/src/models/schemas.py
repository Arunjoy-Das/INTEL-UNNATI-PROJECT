from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class WaitlistRequest(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None

class VerificationSubmission(BaseModel):
    text: str

class VerificationJobResponse(BaseModel):
    request_id: str
    status: str
    message: str

class SourceReference(BaseModel):
    text: str
    source: str
    url: str

class VerificationResultData(BaseModel):
    original_text: str
    detected_language: str
    extracted_claim: str
    verdict: str
    confidence_score: float
    sources: List[SourceReference]

class VerificationResultResponse(BaseModel):
    request_id: str
    status: str
    data: Optional[VerificationResultData] = None
    message: Optional[str] = None
