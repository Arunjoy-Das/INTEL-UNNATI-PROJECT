import os
import re
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
        
        self.client = None

    def evaluate_claim(self, claim: str, evidence: str) -> dict:
        """
        Uses an LLM to perform a high-level semantic evaluation of the claim 
        against the gathered evidence.
        """
        if not self.api_key:
            return {
                "verdict": "UNVERIFIED",
                "confidence_score": 0.1,
                "brief_reasoning": "AI Evaluation skipped: No API Key provided."
            }

        # Cap evidence to avoid hitting token limits
        evidence = evidence[:5000]

        prompt = f"""
        Role: Expert Fact-Checker
        Task: Evaluate the truthfulness of a CLAIM based ONLY on the provided EVIDENCE snippets.
        
        CLAIM: "{claim}"
        
        EVIDENCE:
        {evidence}
        
        INSTRUCTIONS:
        1. Analyze if the evidence directly confirms, refutes, or is insufficient for the claim.
        2. Pay attention to specific dates, names, and quantities.
        3. Identify if the evidence is debunking a rumor (e.g. "The claim that X is true is actually false").
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "verdict": "TRUE" | "FALSE" | "MISLEADING" | "UNVERIFIED",
            "confidence_score": 0.0 to 1.0,
            "brief_reasoning": "One sentence explaining why."
        }}
        """
        import requests
        import json

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://factguard.ai", 
            "X-Title": "FactGuard AI Verification",
        }
        
        try:
            # Use requests with verify=False to bypass SSL check
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                verify=False,
                timeout=30
            )
            if resp.status_code == 200:
                result_json = resp.json()["choices"][0]["message"]["content"]
                # Try to clean up markdown if present
                if "```json" in result_json:
                    result_json = re.search(r"```json\s*(.*?)\s*```", result_json, re.DOTALL).group(1)
                elif "```" in result_json:
                    result_json = re.search(r"```\s*(.*?)\s*```", result_json, re.DOTALL).group(1)
                return json.loads(result_json.strip())
            else:
                error_body = resp.text
                print(f"[LLM ERROR] Status {resp.status_code}: {error_body}")
                return {"verdict": "UNVERIFIED", "confidence_score": 0.2, "brief_reasoning": f"HTTP Error {resp.status_code}: {error_body[:100]}"}
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return {
                "verdict": "UNVERIFIED",
                "confidence_score": 0.2,
                "brief_reasoning": f"AI Evaluation failed: {str(e)}"
            }

_service = LLMService()

def get_llm_service():
    return _service
