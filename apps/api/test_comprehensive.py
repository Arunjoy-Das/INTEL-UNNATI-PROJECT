"""Test: Can the engine verify ANY claim, not just database entries?"""
import sys
sys.path.insert(0, '.')
sys.stdout = open('test_comprehensive_output.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

from src.services.verification_service import get_verification_service

svc = get_verification_service()

# Test cases: (claim, expected_verdict)
test_cases = [
    # === IN DATABASE (known facts) ===
    ("Water boils at 100 degrees Celsius", "TRUE"),
    ("The sun revolves around the Earth", "FALSE"),
    ("COVID vaccines cause autism", "FALSE"),
    
    # === IN DATABASE (geography) ===
    ("India is the most populous country in the world", "TRUE"),
    ("Mount Everest is the tallest mountain in the world", "TRUE"),
    
    # === NOT IN DATABASE — engine must figure it out ===
    ("The capital of France is Paris", "TRUE"),
    ("The Amazon River is in South America", "TRUE"),
    ("Japan is an island country", "TRUE"),
    ("Bill Gates is going to become next PM of India", "FALSE"),
    ("Elon Musk has been elected president of Japan", "FALSE"),
    ("Drinking bleach cures COVID", "FALSE"),
    ("Barack Obama was the 44th president of the United States", "TRUE"),
    ("The human body has 206 bones", "TRUE"),
    ("Sharks are mammals", "FALSE"),
]

print("=" * 70)
print("  FACTGUARD — UNIVERSAL CLAIM VERIFICATION TEST")
print("  Testing: Database facts + Arbitrary unknown claims")
print("=" * 70)

passed = 0
failed = 0

for claim, expected in test_cases:
    result = svc.process_claim(claim)
    verdict = result['verdict']
    confidence = result['confidence_score']
    sources = len(result['sources'])
    
    is_correct = (
        (expected == "TRUE" and verdict in ["TRUE", "LIKELY TRUE"]) or
        (expected == "FALSE" and verdict in ["FALSE", "MISLEADING"])
    )
    
    status = "✓ PASS" if is_correct else "✗ FAIL"
    if is_correct:
        passed += 1
    else:
        failed += 1
    
    print(f"\n{'='*70}")
    print(f"  {status} | Expected: {expected} | Got: {verdict} ({confidence:.0%})")
    print(f"  Claim: {claim}")
    print(f"  Sources fetched: {sources}")
    print(f"{'='*70}")

print(f"\n\n{'#'*70}")
print(f"  FINAL SCORE: {passed}/{passed+failed} passed ({passed/(passed+failed)*100:.0f}%)")
print(f"  Passed: {passed} | Failed: {failed}")
print(f"{'#'*70}")

sys.stdout.close()
