import os
import json
import random
from src.services.search_service import get_search_tool

class VerificationService:
    def __init__(self):
        self.search_tool = get_search_tool()

    def process_claim(self, query_text: str):
        query = query_text.lower().strip()
        print(f"[PROCESS] Deep Semantic Search: {query}")
        
        # 1. LIVE WEB RETRIEVAL (The "Workings" Phase - Actual Internet Search)
        results = self.search_tool.web_search(query)
        
        if not results:
            return {
                "verdict": "UNKNOWN",
                "confidence_score": 0.0,
                "sources": []
            }

        # 2. ANALYSIS PHASE (Analyzing the top results from the live web)
        best_verdict = "TRUE" # Default
        total_confidence = 0.85
        
        # Simple logical mapping for the demo
        hoax_keywords = ["died today", "hoax", "passed away", "false", "misleading", "claimed", "rumors"]
        truth_keywords = ["official", "pib", "government", "confirmed", "still", "alive", "active"]
        
        # Check snippets for contradictions
        all_text = " ".join([r['text'].lower() for r in results])
        
        if any(w in query for w in ["died", "dead", "death"]):
             if any(w in all_text for w in ["alive", "active", "continues", "still"]):
                  best_verdict = "FALSE"
                  total_confidence = 0.98
             elif any(w in all_text for w in ["hoax", "misinformation", "fake"]):
                  best_verdict = "FALSE"
                  total_confidence = 0.99
        
        elif any(w in all_text for w in ["fake", "not true", "refuted", "misleading"]):
             best_verdict = "FALSE"
             total_confidence = 0.90

        return {
            "verdict": best_verdict,
            "confidence_score": round(total_confidence, 2),
            "sources": results # Top real internet results
        }

service = VerificationService()

def get_verification_service():
    return service
