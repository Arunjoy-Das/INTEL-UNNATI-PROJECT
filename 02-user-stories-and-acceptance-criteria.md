# 02. User Stories and Acceptance Criteria

## 👤 User Persona 1: General User
**User Story:** As a general user, I want to paste a questionable social media post into the website so that I can quickly find out if the claim being made is true, false, or misleading.

**Acceptance Criteria:**
- The landing page has a clear, prominent text input area.
- The user can input an unstructured text segment (including clickbait or emotional language).
- Upon submission, the user receives a verdict (`TRUE`, `FALSE`, `MISLEADING`, `UNKNOWN`) within a few seconds.
- The UI displays the optimized claim (what the system actually checked) alongside the final verdict.

---

## 👤 User Persona 2: Journalist
**User Story:** As a journalist, I want to input vernacular news snippets (e.g., in Hindi or Odia) so that I can verify regional facts before writing my article.

**Acceptance Criteria:**
- The system automatically detects the input language (Hindi or Odia).
- The text is cleanly processed without requiring the user to manually translate it.
- The system extracts the factual claim and queries the trusted database accurately, outputting a referenced verdict.
- The result includes retrieved relevant facts from trusted sources (e.g., WHO, Government databases) to provide context for the verdict.

---

## 👤 User Persona 3: System Administrator / Fact-checking Partner
**User Story:** As an administrator or partner, I want the system to process a high volume of claims asynchronously so that it doesn't crash during breaking news events.

**Acceptance Criteria:**
- The backend employs a job queue (like Celery or Kafka) for processing inputs.
- The system can batch process inputs for embedding and retrieval.
- APIs have rate limiting implemented to prevent abuse.
- The system maintains low latency even when dealing with concurrent requests.

---

## 👤 User Persona 4: UI/UX Enthusiast
**User Story:** As a user visiting the platform, I expect a modern, premium experience with 3D interactions so that I feel engaged and trust the platform's technological capability.

**Acceptance Criteria:**
- The homepage features a 3D interactive element (like a floating globe) using Three.js/React Three Fiber.
- Scrolling through the site is smooth (using tools like Framer Motion).
- The UI relies on a minimalist design, removing clutter and focusing entirely on user input and results.
- There is a sticky navigation bar that remains highly accessible during scrolling.
