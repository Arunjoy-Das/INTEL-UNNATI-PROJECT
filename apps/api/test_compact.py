import sys
sys.path.insert(0, '.')
from src.services.verification_service import get_verification_service

svc = get_verification_service()
test_cases = [
    "Drinking bleach cures COVID",
    "Sharks are mammals",
    "Barack Obama was the 44th president of the United States",
    "The human body has 206 bones"
]

with open('test_compact_results.txt', 'w', encoding='utf-8') as f:
    f.write("\n" + "="*50 + "\n")
    f.write("  RE-TESTING OPTIMIZED VERIFICATION\n")
    f.write("="*50 + "\n")
    
    for claim in test_cases:
        f.write(f"\nClaim: {claim}\n")
        print(f"Processing: {claim}")
        result = svc.process_claim(claim)
        f.write(f"VERDICT: {result['verdict']} ({result['confidence_score']:.0%})\n")
        f.write(f"Reasoning: {result.get('ai_reasoning', 'No AI reasoning available')}\n")
        f.write("-" * 50 + "\n")
