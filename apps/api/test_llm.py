import os
import sys
sys.path.insert(0, '.')
from src.services.llm_service import get_llm_service
from dotenv import load_dotenv

load_dotenv()

llm = get_llm_service()
print(f"API Key present: {bool(llm.api_key)}")
print(f"Model: {llm.model}")

claim = "The Moon is made of cheese"
evidence = "Common knowledge says the moon is composed of rock and dust. No reputable source claims it is made of dairy."

result = llm.evaluate_claim(claim, evidence)
print("\n--- TEST RESULT ---")
print(f"Verdict: {result.get('verdict')}")
print(f"Confidence: {result.get('confidence_score')}")
print(f"Reasoning: {result.get('brief_reasoning')}")
