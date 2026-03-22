from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from src.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class VerificationRequest(Base):
    __tablename__ = "verification_requests"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    raw_input = Column(String, nullable=False)
    language = Column(String(10), nullable=True) # can be null during initialization
    extracted_claim = Column(String, nullable=True)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    result = relationship("VerificationResult", uselist=False, back_populates="request")

class VerificationResult(Base):
    __tablename__ = "verification_results"
    request_id = Column(String, ForeignKey("verification_requests.id"), primary_key=True)
    verdict = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    matched_fact_ids = Column(JSON, nullable=True)
    
    request = relationship("VerificationRequest", back_populates="result")

class WaitlistEntry(Base):
    __tablename__ = "waitlist"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    company = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
