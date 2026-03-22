# 06. API Contracts

The backend exposes a RESTful API using FastAPI to handle user inputs and asynchronous job status polling.

---

## 1. Submit Verification Request

**Endpoint:** `POST /api/v1/verify`  
**Description:** Accepts unstructured text input, enqueues it for asynchronous processing, and returns a job/request ID.

### Request
**Headers:** 
- `Content-Type: application/json`
- `Authorization: Bearer <token>` (Optional)

**Body:**
```json
{
  "text": "Breaking! Drinking hot water cures all diseases 😱"
}
```

### Response (202 Accepted)
```json
{
  "request_id": "8f8a11a2-63b7-4402-ba4a-a719d67bcb28",
  "status": "PENDING",
  "message": "Claim submitted successfully and is being processed."
}
```

---

## 2. Check Verification Status / Retrieve Results

**Endpoint:** `GET /api/v1/results/{request_id}`  
**Description:** Polls the server for the result of a submitted request. Given the async nature, clients should poll this (e.g., every 2 seconds) until completion.

### Request
**URL Params:**
- `request_id` (UUID)

### Response (200 OK) - Processing in progress
```json
{
  "request_id": "8f8a11a2-63b7-4402-ba4a-a719d67bcb28",
  "status": "PROCESSING",
  "message": "Extracting claims and querying database."
}
```

### Response (200 OK) - Completed
```json
{
  "request_id": "8f8a11a2-63b7-4402-ba4a-a719d67bcb28",
  "status": "COMPLETED",
  "data": {
    "original_text": "Breaking! Drinking hot water cures all diseases 😱",
    "detected_language": "en",
    "extracted_claim": "Drinking hot water cures diseases",
    "verdict": "FALSE",
    "confidence_score": 0.95,
    "sources": [
      {
        "text": "Drinking hot water does not cure COVID-19 or all diseases.",
        "source": "World Health Organization",
        "url": "https://who.int/..."
      }
    ]
  }
}
```

---

## 3. System Health Check

**Endpoint:** `GET /health`  
**Description:** Provides basic uptime and dependency health (DB, Cache) for load balancers.

### Response (200 OK)
```json
{
  "status": "healthy",
  "services": {
    "postgres": "up",
    "redis": "up",
    "vector_db": "up"
  }
}
```
