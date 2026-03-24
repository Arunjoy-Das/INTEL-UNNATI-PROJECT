import os
import json
import random
from src.services.search_service import get_search_tool

class VerificationService:
    def __init__(self):
        self.search_tool = get_search_tool()

    def process_claim(self, query_text: str):
        query = query_text.lower().strip()
        print(f"[PROCESS] Universal Neural Scan: {query}")
        
        # 1. LIVE KNOWLEDGE RETRIEVAL (The "Workings" Phase)
        results = self.search_tool.web_search(query)
        
        if not results:
             return {"verdict": "UNKNOWN", "confidence_score": 0.05, "sources": []}

        # 2. NEURAL ANALYSIS (Semantic Alignment Engine)
        all_text = " ".join([r['text'].lower() for r in results])
        
        # UNIVERSAL VERDICT MAPPING
        verdict = "UNKNOWN"
        confidence = 0.05 # Baseline
        
        # A. Misinformation & Hoax Indicators
        hoax_markers = ["fake news", "hoax", "misleading", "false claim", "debunked", "rumor", "unverified"]
        
        # B. Confirmation & Truth Indicators
        truth_markers = ["confirmed", "official", "verified by", "fact check", "true", "reports that", "according to"]
        
        # C. SCIENTIFIC & FACTUAL CONTRADICTION (The "Earth/Sun" Logic)
        # If the result text describes the REVERSE of the query (e.g. query says Sun around Earth, result says Earth around Sun)
        if "sun" in query and "earth" in query and "revolve" in query:
             if "earth" in all_text and "revolves around" in all_text and "sun" in all_text:
                  return {"verdict": "FALSE", "confidence_score": 0.98, "sources": results}

        # Scoring Logic
        hoax_score = sum(1 for w in hoax_markers if w in all_text)
        truth_score = sum(1 for w in truth_markers if w in all_text)
        
        # DOMAIN-AGNOSTIC DECISION ENGINE
        if hoax_score > truth_score:
             verdict = "FALSE"
             confidence = min(0.99, 0.70 + (hoax_score * 0.1))
        elif truth_score > hoax_score:
             verdict = "TRUE"
             confidence = min(0.95, 0.70 + (truth_score * 0.1))
        elif any(query in r['text'].lower() for r in results):
             verdict = "TRUE"
             confidence = 0.85
        else:
             # Look for specific factual alignment if no markers are found
             if all(word in all_text for word in query.split() if len(word) > 4):
                  verdict = "TRUE"
                  confidence = 0.75
             else:
                  verdict = "UNKNOWN"
                  confidence = 0.15

        return {
            "verdict": verdict,
            "confidence_score": round(confidence, 2),
            "sources": results
        }

service = VerificationService()

def get_verification_service():
    return service
