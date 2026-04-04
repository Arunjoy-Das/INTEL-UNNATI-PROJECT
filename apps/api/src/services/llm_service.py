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
        Role: Ruthless Fact-Checker
        Task: Evaluate the truthfulness of a CLAIM based ONLY on the provided EVIDENCE snippets.
        
        CLAIM: "{claim}"
        
        EVIDENCE:
        {evidence}
        
        STRICT INSTRUCTIONS:
        1. You must strictly identify the SUBJECT of the claim.
        2. If the claim states Person A died, but the sources state Person A is reacting to Person B's death, the claim is FALSE.
        3. You must think step-by-step. Write out a 2-sentence logical deduction before reaching your final conclusion.
        4. Do not be fooled by related keywords if the context (subject/object relationship) is different.
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "logical_deduction": "Your 2-sentence step-by-step reasoning.",
            "verdict": "TRUE" | "FALSE" | "MISLEADING" | "UNVERIFIED",
            "confidence_score": 0.0 to 1.0,
            "brief_reasoning": "Final one-sentence summary for the user interface."
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
                    match = re.search(r"```json\s*(.*?)\s*```", result_json, re.DOTALL)
                    if match:
                        result_json = match.group(1)
                elif "```" in result_json:
                    match = re.search(r"```\s*(.*?)\s*```", result_json, re.DOTALL)
                    if match:
                        result_json = match.group(1)
                
                parsed_result = json.loads(result_json.strip())
                # Ensure compatibility with legacy field names if necessary
                if "brief_reasoning" not in parsed_result and "logical_deduction" in parsed_result:
                    parsed_result["brief_reasoning"] = parsed_result["logical_deduction"]
                
                return parsed_result
            else:
                error_body = resp.text
                print(f"[LLM ERROR] Status {resp.status_code}: {error_body}")
                return {"verdict": "UNVERIFIED", "confidence_score": 0.2, "brief_reasoning": f"HTTP Error {resp.status_code}"}
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
