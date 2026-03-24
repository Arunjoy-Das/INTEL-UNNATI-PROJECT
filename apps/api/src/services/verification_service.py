import re
from difflib import SequenceMatcher
from src.services.search_service import get_search_tool


class VerificationService:
    """
    Intelligent Fact Verification Engine (No API Keys Required)
    
    Uses multi-query search, sentence-level NLP analysis, extraordinary
    claim detection, and negation proximity to determine truth vs falsehood.
    """

    def __init__(self):
        self.search_tool = get_search_tool()

        # Words that indicate content is DEBUNKING a claim
        self.false_markers = {
            "false", "fake", "hoax", "debunked", "misleading", "incorrect",
            "myth", "conspiracy", "rumor", "unverified", "baseless",
            "unfounded", "fabricated", "disinformation", "misinformation",
            "pseudoscience", "impossible", "no evidence", "not true",
            "there is no", "no proof", "refuted", "denied", "untrue"
        }

        # Words that indicate content is CONFIRMING a claim
        self.true_markers = {
            "confirmed", "verified", "proven", "established",
            "demonstrated", "studies show", "research confirms",
            "officially", "well established", "scientific consensus",
            "is a fact", "it is true"
        }

        # Negation words used for proximity checking
        self.negation_words = {
            "not", "no", "never", "neither", "nobody", "nothing",
            "cannot", "can't", "won't", "doesn't", "don't", "isn't",
            "aren't", "wasn't", "weren't", "hasn't", "haven't",
            "couldn't", "shouldn't", "wouldn't", "impossible", "unlikely"
        }

        # Patterns that indicate EXTRAORDINARY claims requiring strong proof
        self.extraordinary_patterns = [
            r'\b(become|becoming|elected|appointed|next)\b.*\b(president|prime minister|pm|king|queen|minister|ceo)\b',
            r'\b(died|dead|killed|assassinated|passed away)\b',
            r'\b(cure[sd]?|curing)\b.*\b(cancer|aids|hiv|covid|diabetes)\b',
            r'\b(free energy|perpetual motion|time travel)\b',
            r'\b(alien[s]?|ufo[s]?)\b.*\b(confirmed|landed|contact)\b',
        ]

    # ------------------------------------------------------------------ #
    #  HELPER METHODS
    # ------------------------------------------------------------------ #

    def _is_extraordinary(self, claim: str) -> bool:
        """Extraordinary claims need extraordinary evidence."""
        for pat in self.extraordinary_patterns:
            if re.search(pat, claim, re.IGNORECASE):
                return True
        return False

    def _extract_keywords(self, text: str) -> set:
        """Pull out meaningful words (length > 3) from text."""
        return set(re.findall(r'\b[a-zA-Z]{4,}\b', text.lower()))

    def _sentence_relevance(self, sentence: str, claim_kw: set) -> float:
        """What fraction of the claim's keywords appear in this sentence?"""
        if not claim_kw:
            return 0.0
        sent_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', sentence.lower()))
        return len(claim_kw & sent_words) / len(claim_kw)

    def _has_negation_near(self, text: str, keywords: set) -> bool:
        """Check if any negation word sits within 5 words of a keyword."""
        words = text.lower().split()
        for i, w in enumerate(words):
            clean = w.strip(".,!?;:'\"")
            if clean in self.negation_words:
                window = " ".join(words[max(0, i - 4):i + 6])
                for kw in keywords:
                    if kw in window:
                        return True
        return False

    def _count_markers(self, text: str) -> tuple:
        """Count false-markers and true-markers in text."""
        f = sum(1 for m in self.false_markers if m in text)
        t = sum(1 for m in self.true_markers if m in text)
        return f, t

    # ------------------------------------------------------------------ #
    #  CORE VERIFICATION
    # ------------------------------------------------------------------ #

    def process_claim(self, query_text: str) -> dict:
        claim = query_text.strip()
        claim_lower = claim.lower()
        print(f"[VERIFY] Analysing claim: {claim}")

        is_extra = self._is_extraordinary(claim_lower)
        claim_kw = self._extract_keywords(claim)

        # ---- MULTI-QUERY SEARCH (two angles for better coverage) ---- #
        results_main = self.search_tool.web_search(claim)
        results_fc   = self.search_tool.web_search(f"{claim} true or false fact check")

        # Merge and deduplicate
        seen = set()
        all_results = []
        for r in results_main + results_fc:
            key = r.get("url", r["text"][:40])
            if key not in seen:
                seen.add(key)
                all_results.append(r)

        if not all_results:
            return {"verdict": "UNKNOWN", "confidence_score": 0.10, "sources": []}

        # ---- BUILD EVIDENCE CORPUS ---- #
        all_text = " ".join(r["text"].lower() for r in all_results)
        sentences = [s.strip() for s in re.split(r'[.!?]+', all_text) if len(s.strip()) > 15]

        # ---- SCORING ---- #
        false_score = 0
        true_score  = 0
        direct_confirm   = False
        direct_contradict = False

        # 1. Global marker scan
        fm, tm = self._count_markers(all_text)
        false_score += fm * 2
        true_score  += tm * 2

        # 2. Sentence-level deep analysis
        for sent in sentences:
            relevance = self._sentence_relevance(sent, claim_kw)
            if relevance < 0.4:
                continue  # sentence not about the claim

            has_neg = self._has_negation_near(sent, claim_kw)

            if has_neg:
                false_score += 3
                direct_contradict = True
            else:
                # Check if sentence closely mirrors the claim
                sim = SequenceMatcher(None, claim_lower, sent).ratio()
                if sim > 0.45:
                    true_score += 3
                    direct_confirm = True
                else:
                    true_score += 1  # tangentially related

        # 3. Verbatim check – does the claim text appear in results?
        if claim_lower in all_text:
            true_score += 5
            direct_confirm = True

        # 4. Extraordinary claim penalty
        if is_extra:
            if not direct_confirm:
                # No source explicitly states this extraordinary thing
                false_score += 6
            # Require stronger evidence
            true_score = max(0, true_score - 3)

        # ---- VERDICT DECISION ---- #
        total = max(1, false_score + true_score)

        if false_score > true_score:
            verdict = "FALSE"
            confidence = min(0.98, 0.60 + (false_score / total) * 0.35)
        elif true_score > false_score and direct_confirm:
            verdict = "TRUE"
            confidence = min(0.95, 0.60 + (true_score / total) * 0.35)
        elif true_score > false_score:
            verdict = "LIKELY TRUE"
            confidence = min(0.78, 0.50 + (true_score / total) * 0.25)
        else:
            verdict = "UNVERIFIED"
            confidence = 0.20

        print(f"[RESULT] {verdict} ({confidence:.0%}) | F={false_score} T={true_score} extra={is_extra}")

        return {
            "verdict": verdict,
            "confidence_score": round(confidence, 2),
            "sources": all_results[:5]
        }


service = VerificationService()

def get_verification_service():
    return service
