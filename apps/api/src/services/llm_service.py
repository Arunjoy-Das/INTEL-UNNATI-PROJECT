import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-preview-02-05:free")
        
        if self.api_key:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        else:
            self.client = None

    def evaluate_claim(self, claim: str, evidence: str) -> dict:
        """
        Uses an LLM to perform a high-level semantic evaluation of the claim 
        against the gathered evidence.
        """
        if not self.client:
            return {
                "verdict": "UNVERIFIED",
                "confidence": 0.1,
                "reasoning": "AI Evaluation skipped: No API Key provided."
            }

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

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return {
                "verdict": "UNVERIFIED",
                "confidence": 0.2,
                "reasoning": f"AI Evaluation failed: {str(e)}"
            }

_service = LLMService()

def get_llm_service():
    return _service
