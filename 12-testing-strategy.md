# 12. Testing Strategy

Ensuring accuracy is paramount for a fact-checking application. The testing strategy covers both traditional software engineering reliability and ML model accuracy.

---

## 1. Unit Testing
**Tools:** `pytest` (Python), `Jest` (React)

- **API Layer:** Test endpoint request validation, HTTP status codes, and authorization middleware.
- **NLP Functions:** Test the Claim Optimization layer with mocked "noisy" text to ensure the regex/extraction logic successfully strips filler words.
- **Frontend Components:** Test form submission behavior, state management, and Three.js canvas mounting.

---

## 2. Integration Testing
- **Queue/Worker Comm:** Submit a mock verification request to the API and assert that it successfully reaches the Redis queue.
- **Database Operations:** Verify that CRUD operations on PostgreSQL correctly alter state without race conditions.

---

## 3. End-to-End (E2E) Testing
**Tool:** `Cypress` or `Playwright`

- Automate the primary user journey:
  1. Load the landing page.
  2. Input a known false claim (e.g., "The earth is flat").
  3. Wait for the async loading state to resolve.
  4. Assert that the UI displays a `FALSE` verdict and cites a source.

---

## 4. ML / Accuracy Evaluation (Continuous QA)
Since this is an AI product, standard unit tests aren't enough. We maintain a static "Golden Dataset" of 100 known claims (mixed True, False, and Misleading).

- **Evaluation Script:** A script runs weekly (or upon updating the ML models) to test the engine against the Golden Dataset.
- **Metrics Tracked:**
  - *Precision/Recall:* Is it flagging True claims as False (False Positives)?
  - *Retrieval Hits (MRR):* Is the vector search pulling the *correct* reference fact in the top 3 results?
  - If accuracy drops below 90% on the golden dataset, the CI pipeline fails.

---

## 5. Load and Performance Testing
**Tool:** `Locust` or `k6`

- Simulate 1,000 concurrent users submitting text.
- Monitor:
  - API Gateway response times (should remain < 200ms for acceptance).
  - Worker node throughput and memory usage (ensuring the RAM doesn't spike and crash the containers).
  - Rate-limiting rules triggering correctly.
