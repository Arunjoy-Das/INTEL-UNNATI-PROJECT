# 08. Scoring Engine Specs

The Verification Engine determines the final verdict by comparing the user's `extracted_claim` against the `retrieved_facts` from the vector database.

## 📊 Evaluation Metrics

The system calculates a `semantic_similarity_score` between the claim and the retrieved fact embeddings as the baseline. It then uses an NLI (Natural Language Inference) model (e.g., a fine-tuned RoBERTa) to determine logical entailment.

A pairwise comparison yields three NLI probabilities:
1. `P(Entailment)`: The fact supports the claim.
2. `P(Contradiction)`: The fact refutes the claim.
3. `P(Neutral)`: The fact is unrelated or lacks sufficient detail.

---

## ⚖️ Verdict Determination Rules

### 1. `TRUE`
* **Condition:** `P(Entailment) > 0.85` AND `semantic_similarity_score > 0.75`
* **Definition:** The retrieved verified fact directly supports the user's extracted claim with high confidence.
* **Fallback:** If `0.70 < P(Entailment) < 0.85`, it may still output `TRUE` but warn the user of a lower confidence score.

### 2. `FALSE`
* **Condition:** `P(Contradiction) > 0.85` AND `semantic_similarity_score > 0.75`
* **Definition:** The retrieved verified fact directly disputes and proves the user's extracted claim wrong.

### 3. `MISLEADING`
* **Condition:** 
  - The claim contains multiple sub-claims where one is TRUE and one is FALSE.
  - OR `P(Neutral)` is high alongside a very high `semantic_similarity_score`, implying the claim takes real facts out of context.
  - OR `0.60 < P(Contradiction) < 0.85`.
* **Definition:** The claim contains elements of truth but omits context or distorts the factual baseline.

### 4. `UNKNOWN`
* **Condition:** `semantic_similarity_score < 0.40` for all retrieved database records.
* **Definition:** The system's trusted database simply does not possess relevant verified information about this specific claim. The AI will gracefully fallback and not attempt to guess.

---

## 📈 Confidence Score Calculation
The final `confidence_score` returned to the user is a weighted aggregate of:
- The base semantic similarity match (30% weight).
- The highest probability output from the NLI model (70% weight).

If multiple facts are retrieved, the engine takes the `MAX()` entailment or contradiction score across the top 3 results to formulate the final verdict.
