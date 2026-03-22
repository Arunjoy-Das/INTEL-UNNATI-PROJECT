# 05. Database Schema

The system utilizes a dual-database approach to handle structured metadata and high-dimensional vector embeddings separately.

## 🗄️ Relational Database (PostgreSQL)

Used for structured data storage, user management, and transactional metadata.

### Table: `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique user identifier |
| `email` | VARCHAR | UNIQUE, NOT NULL | User account email |
| `password_hash` | VARCHAR | NOT NULL | Hashed password |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Account creation time |

### Table: `verification_requests`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique request ID |
| `user_id` | UUID | FOREIGN KEY (`users.id`) | Submitter ID (Nullable for anonymous) |
| `raw_input` | TEXT | NOT NULL | The original text/post submitted |
| `language` | VARCHAR(10) | NOT NULL | Detected language (e.g., 'hi', 'or', 'en') |
| `extracted_claim` | TEXT | | The optimized core claim after noise reduction |
| `status` | VARCHAR | DEFAULT 'PENDING' | Status (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`) |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Time of submission |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Time of last status update |

### Table: `verification_results`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `request_id` | UUID | PRIMARY KEY, FK | Links to `verification_requests` |
| `verdict` | VARCHAR | NOT NULL | `TRUE`, `FALSE`, `MISLEADING`, `UNKNOWN` |
| `confidence_score`| FLOAT | NOT NULL | ML confidence score (0.0 to 1.0) |
| `matched_fact_ids`| JSONB | | Array of IDs linking to the Vector DB records |

---

## 🧠 Vector Database (FAISS / Pinecone)

Used for fast semantic search based on dense vector embeddings.

### Storage: `verified_facts_index`
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | STRING / UUID | Unique fact identifier |
| `vector` | FLOAT ARRAY (e.g., 384d or 768d)| Dense text embedding of the verified claim |
| `metadata` | JSON | Accompanying contextual data |

**Metadata JSON Structure:**
```json
{
  "text": "Drinking hot water does not cure COVID-19 or all diseases.",
  "source_name": "World Health Organization",
  "source_url": "https://who.int/...",
  "published_date": "2023-01-15T00:00:00Z",
  "language": "en"
}
```
