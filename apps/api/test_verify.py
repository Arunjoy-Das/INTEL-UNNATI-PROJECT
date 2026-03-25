"""Test with output to file."""
import sys
sys.path.insert(0, '.')
sys.stdout = open('test_output.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

from src.services.verification_service import get_verification_service

svc = get_verification_service()

claims = [
    "Bill Gates is going to become next PM of India",
    "Water boils at 100 degrees Celsius",
    "The sun revolves around the Earth",
    "Earth revolves around the Sun",
    "COVID vaccines cause autism",
]

for claim in claims:
    result = svc.process_claim(claim)
    print(f"\n*** FINAL: {claim}")
    print(f"*** VERDICT: {result['verdict']} ({result['confidence_score']})")
    print(f"*** Sources: {len(result['sources'])}")
    print("---")

sys.stdout.close()
