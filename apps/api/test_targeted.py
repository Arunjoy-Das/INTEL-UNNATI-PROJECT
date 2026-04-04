"""Targeted test: Fails from the universal test"""
import sys
sys.path.insert(0, '.')
sys.stdout = open('test_targeted_output.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

from src.services.verification_service import get_verification_service

svc = get_verification_service()

test_cases = [
    ("Drinking bleach cures COVID", "FALSE"),
    ("Sharks are mammals", "FALSE"),
    ("Barack Obama was the 44th president of the United States", "TRUE"),
    ("The human body has 206 bones", "TRUE"),
]

print("=" * 70)
print("  FACTGUARD — TARGETED ACCURACY TEST")
print("=" * 70)

for claim, expected in test_cases:
    result = svc.process_claim(claim)
    verdict = result['verdict']
    confidence = result['confidence_score']
    
    is_correct = (
        (expected == "TRUE" and verdict in ["TRUE", "LIKELY TRUE"]) or
        (expected == "FALSE" and verdict in ["FALSE", "MISLEADING"])
    )
    
    status = "✓ PASS" if is_correct else "✗ FAIL"
    print(f"\nClaim: {claim}")
    print(f"{status} | Expected: {expected} | Got: {verdict} ({confidence:.0%})")
    print("-" * 70)

sys.stdout.close()
