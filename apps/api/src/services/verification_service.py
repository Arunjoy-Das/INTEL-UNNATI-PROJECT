import re
from difflib import SequenceMatcher
from src.services.search_service import get_search_tool


class VerificationService:
    """
    Cross-Reference Triangulation Verification Engine v3
    
    4-Phase evidence gathering + inversion-aware analysis.
    No API keys. No LLMs. Pure logic + heuristics.
    """

    def __init__(self):
        self.search = get_search_tool()

        self.debunk_markers = [
            "false", "fake", "hoax", "debunked", "misleading", "incorrect",
            "myth", "conspiracy", "rumor", "baseless", "unfounded", "fabricated",
            "disinformation", "misinformation", "pseudoscience", "not true",
            "no evidence", "no proof", "there is no", "refuted", "denied",
            "satire", "parody", "unsubstantiated", "no credible",
            "widely debunked", "has been debunked", "common misconception",
            "geocentric", "flat earth", "pseudoscience"
        ]

        self.confirm_markers = [
            "confirmed", "verified", "proven", "established", "demonstrated",
            "according to", "studies show", "research confirms", "officially",
            "well established", "scientific consensus", "it is true",
            "evidence supports", "data shows"
        ]

        self.negation_words = {
            "not", "no", "never", "neither", "cannot", "can't", "won't",
            "doesn't", "don't", "isn't", "aren't", "wasn't", "weren't",
            "hasn't", "haven't", "couldn't", "shouldn't", "wouldn't",
            "impossible", "unlikely", "unable", "false", "incorrect"
        }

        self.extraordinary_patterns = [
            r'\b(become|becoming|elected|appointed|chosen|named|next)\b.*\b(president|prime.?minister|pm|king|queen|chancellor|minister|ceo|chief)\b',
            r'\b(died|dead|killed|assassinated|passed\s+away)\b',
            r'\b(cure[sd]?|cures?)\b.*\b(cancer|aids|hiv|covid|diabetes|alzheimer)\b',
            r'\b(free\s+energy|perpetual\s+motion|time\s+travel|flat\s+earth)\b',
            r'\b(alien[s]?|ufo)\b.*\b(confirmed|proven|landed|contact|exist)\b',
            r'\b(world\s+war|nuclear\s+war|apocalypse)\b.*\b(started|begun|happening)\b',
        ]

        # Known scientific misconceptions — if the claim matches any of these,
        # it's FALSE regardless of keyword overlap
        self.known_false_patterns = [
            (r'sun\b.*\b(?:revolves?|orbits?|goes?|moves?)\b.*\b(?:around|round)\b.*\bearth\b', "The Earth revolves around the Sun, not vice versa"),
            (r'earth\b.*\bflat\b', "The Earth is an oblate spheroid"),
            (r'(?:moon\b.*\bmade\s+of\s+cheese)', "The Moon is not made of cheese"),
            (r'great\s+wall.*(?:visible|seen)\s+(from\s+)?space', "The Great Wall is not visible from space with the naked eye"),
            (r'humans?\b.*\bonly\s+use\b.*\b(?:10|ten)\s*%?\s*(?:of)?\s*(?:their)?\s*brain', "Humans use virtually every part of their brain"),
            (r'lightning\b.*\bnever\b.*\bstrike[s]?\b.*\btwice', "Lightning can and does strike the same place multiple times"),
            (r'vaccine[s]?\b.*\bcause[s]?\b.*\bautism', "Scientific consensus: vaccines do not cause autism"),
        ]

        # Known TRUE scientific/factual patterns
        self.known_true_patterns = [
            (r'water\b.*\bboils?\b.*\b100\b.*\b(?:celsius|°c|degrees)', "Water boils at 100°C (212°F) at standard atmospheric pressure"),
            (r'earth\b.*\b(?:revolves?|orbits?)\b.*\bsun\b', "Earth revolves around the Sun"),
            (r'earth\b.*\b(?:round|spheri|oblate)', "Earth is an oblate spheroid"),
            (r'speed\s+of\s+light\b.*\b(?:300|299)', "Speed of light is approximately 299,792 km/s"),
            (r'moon\b.*\borbits?\b.*\bearth', "The Moon orbits the Earth"),
            (r'water\b.*\bh2o\b', "Water is H2O"),
            (r'dna\b.*\bdouble\s+helix', "DNA has a double helix structure"),
        ]

    # ------------------------------------------------------------------ #
    #  ENTITY & QUERY HELPERS
    # ------------------------------------------------------------------ #

    def _extract_entities(self, claim: str) -> list:
        multi = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', claim)
        singles = re.findall(r'(?<!^)(?<!\. )[A-Z][a-z]{2,}', claim)
        entities = list(set(multi + singles))
        if not entities:
            words = [w for w in claim.split() if len(w) > 3]
            entities = words[:3]
        return entities[:4]

    def _generate_counter_query(self, claim: str) -> str:
        cl = claim.lower().strip().rstrip('?.')

        m = re.search(r'(.+?)\s+(?:is|will|going to|shall)\s+(?:become|be|becoming)\s+(.+?)(?:\s+of\s+(.+))?$', cl, re.I)
        if m and m.group(3):
            return f"Who is the {m.group(2).strip()} of {m.group(3).strip()}"

        m = re.search(r'(.+?)\s+(?:boils?|melts?|freezes?|burns?)\s+at\s+(.+)', cl, re.I)
        if m:
            action = re.search(r'(boils?|melts?|freezes?|burns?)', cl, re.I).group()
            return f"At what temperature does {m.group(1).strip()} {action}"

        m = re.search(r'(.+?)\s+(?:revolves?|orbits?|rotates?|goes?)\s+(?:around|round)\s+(.+)', cl, re.I)
        if m:
            return f"What revolves around what {m.group(1).strip()} or {m.group(2).strip()}"

        m = re.search(r'(.+?)\s+(?:has\s+)?(?:died|was\s+killed|is\s+dead|passed\s+away)', cl, re.I)
        if m:
            return f"Is {m.group(1).strip()} alive"

        return f"{cl} true or false"

    def _is_extraordinary(self, claim: str) -> bool:
        for pat in self.extraordinary_patterns:
            if re.search(pat, claim, re.IGNORECASE):
                return True
        return False

    def _check_known_false(self, claim: str) -> tuple:
        """Check claim against database of known misconceptions."""
        cl = claim.lower()
        for pattern, explanation in self.known_false_patterns:
            if re.search(pattern, cl, re.IGNORECASE):
                return True, explanation
        return False, ""

    def _check_known_true(self, claim: str) -> tuple:
        """Check claim against database of well-established facts."""
        cl = claim.lower()
        for pattern, explanation in self.known_true_patterns:
            if re.search(pattern, cl, re.IGNORECASE):
                return True, explanation
        return False, ""

    def _extract_keywords(self, text: str) -> set:
        stopwords = {'the', 'that', 'this', 'with', 'from', 'have', 'been',
                      'were', 'will', 'they', 'their', 'about', 'which',
                      'when', 'what', 'where', 'would', 'could', 'should',
                      'also', 'than', 'then', 'some', 'more', 'most', 'such',
                      'very', 'just', 'into', 'only', 'other', 'over', 'after',
                      'before', 'does', 'going'}
        words = set(re.findall(r'\b[a-zA-Z]{4,}\b', text.lower()))
        return words - stopwords

    # ------------------------------------------------------------------ #
    #  INVERSION DETECTION (critical for Sun/Earth type claims)
    # ------------------------------------------------------------------ #

    def _detect_subject_object_inversion(self, claim: str, evidence: str) -> bool:
        """
        Detects if the evidence INVERTS the subject-object relationship.
        
        Claim:    "The Sun revolves around the Earth"
        Evidence: "The Earth revolves around the Sun"
        
        Both have the same keywords, but the subject/object positions are swapped.
        This function detects that swap.
        """
        cl = claim.lower()
        ev = evidence.lower()

        # Find "A [verb] around B" patterns in both claim and evidence
        pattern = r'(\b\w+\b)\s+(?:revolves?|orbits?|goes?|moves?|rotates?)\s+(?:around|round)\s+(?:the\s+)?(\b\w+\b)'
        
        claim_match = re.search(pattern, cl)
        if not claim_match:
            return False
        
        claim_subject = claim_match.group(1)
        claim_object = claim_match.group(2)
        
        # Look for the inverted pattern in evidence
        for sent in re.split(r'[.!?]+', ev):
            ev_match = re.search(pattern, sent)
            if ev_match:
                ev_subject = ev_match.group(1)
                ev_object = ev_match.group(2)
                
                # Check if subject and object are swapped
                if (claim_subject == ev_object and claim_object == ev_subject):
                    print(f"[INVERSION] Detected! Claim: {claim_subject}→{claim_object}, Evidence: {ev_subject}→{ev_object}")
                    return True
        
        return False

    # ------------------------------------------------------------------ #
    #  EVIDENCE ANALYSIS
    # ------------------------------------------------------------------ #

    def _analyze_text_for_claim(self, evidence_text: str, claim: str) -> dict:
        ev = evidence_text.lower()
        cl = claim.lower()
        claim_kw = self._extract_keywords(claim)
        
        debunk_score = 0
        confirm_score = 0
        direct_match = False
        has_contradiction = False
        has_inversion = False

        # 0. Subject-Object Inversion Detection
        if self._detect_subject_object_inversion(claim, evidence_text):
            has_inversion = True
            has_contradiction = True
            debunk_score += 10  # Heavy penalty for inverted relationship

        # 1. Marker counting (ONLY in claim-relevant text)
        # Split evidence into sentences, only count markers in relevant sentences
        ev_sentences = [s.strip() for s in re.split(r'[.!?]+', ev) if len(s.strip()) > 10]
        for sent in ev_sentences:
            sent_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', sent))
            relevance = len(claim_kw & sent_words) / max(len(claim_kw), 1)
            if relevance < 0.25:
                continue  # Skip sentences not about the claim
            
            for m in self.debunk_markers:
                if m in sent:
                    debunk_score += 2
            for m in self.confirm_markers:
                if m in sent:
                    confirm_score += 1

        # 2. Sentence-level analysis
        sentences = [s.strip() for s in re.split(r'[.!?]+', ev) if len(s.strip()) > 15]
        
        for sent in sentences:
            sent_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', sent))
            overlap = len(claim_kw & sent_words) / max(len(claim_kw), 1)
            
            if overlap < 0.35:
                continue

            # Check negation near claim keywords
            words_list = sent.split()
            for i, w in enumerate(words_list):
                if w.strip(".,!?;:'\"") in self.negation_words:
                    window = " ".join(words_list[max(0, i-4):i+6])
                    for kw in claim_kw:
                        if kw in window:
                            has_contradiction = True
                            debunk_score += 3
                            break

            # Only count as direct confirmation if the claim is
            # nearly VERBATIM in the evidence (high bar)
            sim = SequenceMatcher(None, cl, sent).ratio()
            if sim > 0.65:  # Raised from 0.5 — stricter matching
                confirm_score += 4
                direct_match = True
            # Mere keyword overlap gets ZERO confirm points
            # (prevents topically-related but contradicting evidence from confirming)

        # 3. Verbatim claim in evidence
        if cl in ev:
            confirm_score += 5
            direct_match = True

        return {
            "debunk": debunk_score,
            "confirm": confirm_score,
            "direct_match": direct_match,
            "contradiction": has_contradiction,
            "inversion": has_inversion,
        }

    # ------------------------------------------------------------------ #
    #  MAIN VERIFICATION PIPELINE
    # ------------------------------------------------------------------ #

    def process_claim(self, query_text: str) -> dict:
        claim = query_text.strip()
        claim_lower = claim.lower()
        print(f"\n{'='*60}")
        print(f"[VERIFY] CLAIM: {claim}")
        print(f"{'='*60}")

        # ═══════════════════════════════════════════════════════
        #  PRE-CHECK: Known facts databases
        # ═══════════════════════════════════════════════════════
        is_known_false, false_reason = self._check_known_false(claim_lower)
        if is_known_false:
            print(f"[KNOWN FALSE] Matched misconception database: {false_reason}")

        is_known_true, true_reason = self._check_known_true(claim_lower)
        if is_known_true:
            print(f"[KNOWN TRUE] Matched established facts database: {true_reason}")

        is_extraordinary = self._is_extraordinary(claim_lower)
        entities = self._extract_entities(claim)
        counter_query = self._generate_counter_query(claim)

        print(f"[INFO] Extraordinary: {is_extraordinary}")
        print(f"[INFO] Entities: {entities}")
        print(f"[INFO] Counter-query: {counter_query}")

        # ═══════════════════════════════════════════════════════
        #  PHASE 1: MULTI-SOURCE EVIDENCE GATHERING
        # ═══════════════════════════════════════════════════════

        results_direct = self.search.web_search(claim)
        results_fc = self.search.web_search(f"{claim} fact check true or false")
        results_counter = self.search.web_search(counter_query)

        # ═══════════════════════════════════════════════════════
        #  PHASE 1.5: DEEP SCRAPING
        # ═══════════════════════════════════════════════════════
        deep_evidence = ""
        # Combine direct and fact-check results to find the best URLs to visit
        authorities = [r for r in (results_direct + results_fc) if r.get("url")]
        seen_urls = set()
        to_scrape = []
        for r in authorities:
            u = r["url"]
            if u in seen_urls: continue
            seen_urls.add(u)
            # Skip aggregators and internal search results
            if any(x in u for x in ["wikipedia.org", "duckduckgo.com", "bing.com"]):
                continue
            if "google.com" in u and "news.google.com" not in u:
                continue
            to_scrape.append(u)
            if len(to_scrape) >= 2: break  # Cap at 2 articles for speed
        
        for url in to_scrape:
            print(f"[DEEP SCRAPE] Visiting: {url}")
            content = self.search.scrape_article(url)
            if content:
                print(f"  ∟ Scraped {len(content)} chars")
                deep_evidence += f" {content}"

        # ═══════════════════════════════════════════════════════
        #  PHASE 2: CROSS-REFERENCE ANALYSIS
        # ═══════════════════════════════════════════════════════

        # Wikipedia deep summaries (Deep context fallback)
        wiki_context = ""
        wiki_sources = []
        for entity in entities[:2]:
            summary = self.search.wikipedia_summary(entity)
            if summary:
                wiki_context += f" {summary}"
                wiki_sources.append({
                    "text": summary[:300] + "..." if len(summary) > 300 else summary,
                    "source": f"Wikipedia: {entity}",
                    "url": f"https://en.wikipedia.org/wiki/{entity.replace(' ', '_')}"
                })
                print(f"[WIKI] {entity}: {summary[:120]}...")

        # Deduplicate display results
        seen_urls = set()
        all_display_results = []
        for r in results_direct + results_fc + wiki_sources:
            key = r.get("url", r["text"][:50])
            if key not in seen_urls:
                seen_urls.add(key)
                all_display_results.append(r)

        if not all_display_results and not wiki_context:
            return {"verdict": "UNKNOWN", "confidence_score": 0.10, "sources": [],
                    "extracted_claim": claim}

        # ═══════════════════════════════════════════════════════
        #  PHASE 2: CROSS-REFERENCE ANALYSIS
        # ═══════════════════════════════════════════════════════

        direct_text = " ".join(r["text"] for r in results_direct)
        fc_text = " ".join(r["text"] for r in results_fc)
        counter_text = " ".join(r["text"] for r in results_counter)

        direct_analysis = self._analyze_text_for_claim(direct_text, claim)
        fc_analysis = self._analyze_text_for_claim(fc_text, claim)
        deep_analysis = self._analyze_text_for_claim(deep_evidence, claim)
        wiki_analysis = self._analyze_text_for_claim(wiki_context, claim)
        counter_analysis = self._analyze_text_for_claim(counter_text, claim)

        # ═══════════════════════════════════════════════════════
        #  PHASE 3: WEIGHTED VERDICT CALCULATION
        # ═══════════════════════════════════════════════════════

        total_debunk = (
            direct_analysis["debunk"] * 1.0 +
            fc_analysis["debunk"] * 1.5 +
            deep_analysis["debunk"] * 2.0 +   # Deeply scraped content is most reliable
            wiki_analysis["debunk"] * 1.5 +
            counter_analysis["debunk"] * 1.5
        )

        total_confirm = (
            direct_analysis["confirm"] * 1.0 +
            fc_analysis["confirm"] * 1.5 +
            deep_analysis["confirm"] * 1.5 +
            wiki_analysis["confirm"] * 2.0 +  # Wikipedia confirmation is strong
            counter_analysis["confirm"] * 0.5
        )

        has_direct_match = any(a["direct_match"] for a in 
            [direct_analysis, fc_analysis, deep_analysis, wiki_analysis])

        has_contradiction = any(a["contradiction"] for a in
            [direct_analysis, fc_analysis, deep_analysis, wiki_analysis, counter_analysis])

        has_inversion = any(a.get("inversion", False) for a in
            [direct_analysis, fc_analysis, deep_analysis, wiki_analysis, counter_analysis])

        # Known true override (well-established scientific facts)
        if is_known_true:
            total_confirm += 20
            has_direct_match = True  # Known facts count as direct match

        # Known false override
        if is_known_false:
            total_debunk += 20

        # Extraordinary claim penalty
        if is_extraordinary:
            if not has_direct_match:
                total_debunk += 8
                print(f"[EXTRA] +8 debunk penalty (extraordinary, no direct confirmation)")
            total_confirm = max(0, total_confirm - 4)

        # Inversion penalty (e.g., Sun/Earth)
        # BUT ONLY if this is NOT a known-true fact (avoids false flag on correct claims)
        if has_inversion and not is_known_true:
            total_debunk += 8
            total_confirm = max(0, total_confirm - 6)
            print(f"[INVERSION] Subject-object inversion detected → heavy debunk penalty")
        elif has_inversion and is_known_true:
            print(f"[INVERSION] Detected but skipped (claim is in known-true database)")

        # Wikipedia coverage check
        if wiki_context:
            claim_kw = self._extract_keywords(claim)
            wiki_kw = self._extract_keywords(wiki_context)
            coverage = len(claim_kw & wiki_kw) / max(len(claim_kw), 1)
            if coverage < 0.4:
                total_debunk += 3
                print(f"[WIKI] Low coverage ({coverage:.0%}) — topic not well-supported")

        print(f"\n[SCORES] Debunk: {total_debunk:.1f} | Confirm: {total_confirm:.1f}")
        print(f"[FLAGS]  Direct: {has_direct_match} | Contradiction: {has_contradiction} | Inversion: {has_inversion}")

        # ═══════════════════════════════════════════════════════
        #  PHASE 4: VERDICT
        # ═══════════════════════════════════════════════════════

        total = max(1, total_debunk + total_confirm)

        if is_known_false:
            verdict = "FALSE"
            confidence = min(0.97, 0.85 + (total_debunk / total) * 0.12)
        elif is_known_true:
            # Known established fact — short-circuit to TRUE
            verdict = "TRUE"
            confidence = min(0.95, 0.90 + (total_confirm / total) * 0.05)
        elif total_debunk > total_confirm * 1.5:
            # Strong FALSE — debunk significantly outweighs confirm
            verdict = "FALSE"
            raw_conf = 0.60 + (total_debunk / total) * 0.35
            if has_contradiction or has_inversion:
                raw_conf += 0.05
            confidence = min(0.97, raw_conf)
        elif total_debunk > total_confirm:
            # Weak FALSE
            verdict = "FALSE"
            confidence = min(0.75, 0.50 + (total_debunk / total) * 0.20)
        elif total_confirm > total_debunk * 1.5 and has_direct_match:
            # Strong TRUE — confirm significantly outweighs debunk + direct match
            verdict = "TRUE"
            raw_conf = 0.65 + (total_confirm / total) * 0.30
            confidence = min(0.95, raw_conf)
        elif total_confirm > total_debunk and has_direct_match:
            verdict = "LIKELY TRUE"
            confidence = min(0.78, 0.55 + (total_confirm / total) * 0.20)
        elif total_confirm > total_debunk:
            verdict = "LIKELY TRUE"
            confidence = min(0.65, 0.40 + (total_confirm / total) * 0.20)
        elif has_contradiction or has_inversion:
            verdict = "FALSE"
            confidence = 0.65
        else:
            verdict = "UNVERIFIED"
            confidence = 0.20

        print(f"\n[VERDICT] {verdict} — Confidence: {confidence:.0%}")
        print(f"{'='*60}\n")

        return {
            "verdict": verdict,
            "confidence_score": round(confidence, 2),
            "sources": all_display_results[:6],
            "extracted_claim": claim
        }


service = VerificationService()

def get_verification_service():
    return service
