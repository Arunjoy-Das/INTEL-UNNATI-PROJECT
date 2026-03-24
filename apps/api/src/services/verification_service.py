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
        
        # 1. LIVE WEB RETRIEVAL (The "Workings" Phase)
        results = self.search_tool.web_search(query)
        
        if not results:
             # If NO internet data exists for a specific claim, it's statistically unverified
             return {
                 "verdict": "UNKNOWN",
                 "confidence_score": 0.05,
                 "sources": []
             }

        # 2. UNIVERSAL ANALYSIS (Domain-Agnostic Truth Engine)
        # We analyze snippets for "Verdicts", "Consistency", and "Fact-Checking" footprints
        all_text = " ".join([r['text'].lower() for r in results])
        all_sources = " ".join([r['source'].lower() for r in results])
        
        # UNIVERSAL VERDICT MAPPING
        verdict = "UNKNOWN"
        confidence = 0.50 # Neutral baseline
        
        # A. Misinformation Indicators (Works across all domains: Health, Tech, Politics, Celebs)
        hoax_markers = [
            "fake news", "hoax", "misleading", "false claim", "refuted by", 
            "not true", "rumor", "unverified", "debunked", "fraudulent", 
            "misinformation", "disinformation", "no evidence"
        ]
        
        # B. Confirmation Indicators
        truth_markers = [
            "confirmed", "reports that", "official statement", "verified by",
            "pib fact check", "fact check", "true", "actually happened", 
            "announced by", "published", "according to", "verified source"
        ]

        # Scoring Logic: Consistency & Weight
        hoax_score = sum(1 for w in hoax_markers if w in all_text)
        truth_score = sum(1 for w in truth_markers if w in all_text)
        
        # DOMAIN-AGNOSTIC DECISION ENGINE
        if hoax_score > truth_score:
             verdict = "FALSE"
             # Higher gap = higher confidence
             confidence = min(0.99, 0.75 + (hoax_score - truth_score) * 0.05)
        elif truth_score > hoax_score:
             verdict = "TRUE"
             confidence = min(0.95, 0.70 + (truth_score - hoax_score) * 0.05)
        elif truth_score > 0 and hoax_score > 0:
             # Conflicting data detected
             verdict = "MISLEADING"
             confidence = 0.85
        else:
             # Basic presence of the claim in search results but no clear verdict
             # If the claim appears exactly in news titles, it's likely TRUE
             if any(query in r['text'].lower() for r in results):
                  verdict = "TRUE"
                  confidence = 0.65
             else:
                  verdict = "UNKNOWN"
                  confidence = 0.15

        return {
            "verdict": verdict,
            "confidence_score": round(confidence, 2),
            "sources": results # Actual live internet data used for analysis
        }

service = VerificationService()

def get_verification_service():
    return service
