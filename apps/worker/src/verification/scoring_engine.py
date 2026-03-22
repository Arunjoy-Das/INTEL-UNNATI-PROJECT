import os
import random

class ScoringEngine:
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            "TRUE": 0.85, # High similarity => TRUE
            "FALSE": 0.80, # High similarity AND contradiction logic? 
            # In MVP, we'll use a simplified logic: 
            # If matches a "false-claim" truth fact (like "Drinking hot water doesn't cure"), 
            # then it's FALSE. 
            "MISLEADING": 0.60
        }

    def determine_verdict(self, results):
        if not results:
            return "UNKNOWN", 0.0
        
        # Take best match
        best_match = results[0]
        similarity = best_match['similarity']
        matched_fact_text = best_match['fact']['text']
        
        # Simple Logic for "Workings Phase"
        if similarity < 0.45:
            return "UNKNOWN", float(similarity)
        
        if similarity >= self.thresholds["TRUE"]:
            return "TRUE", float(similarity)
        
        if similarity >= self.thresholds["MISLEADING"]:
            return "MISLEADING", float(similarity)
            
        return "FALSE", float(similarity)

# Singleton instance
engine = None

def get_scoring_engine():
    global engine
    if engine is None:
        engine = ScoringEngine()
    return engine
