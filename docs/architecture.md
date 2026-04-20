# Architecture

## Final Stack

- Frontend: Angular
- Backend: FastAPI
- Persistence: SQLite for local/demo use
- Document parsing: `pypdf`
- Retrieval: chunked document storage with keyword ranking
- Answer generation: deterministic fallback, optional OpenAI answer synthesis when `OPENAI_API_KEY` is configured

## Top-Level Structure

- `backend/`
  - `app/api/`: REST endpoints
  - `app/core/`: settings, database, auth
  - `app/services/`: ingestion, retrieval, quiz generation
  - `app/data/`: local runtime database and uploaded files
- `frontend/`
  - Angular app for admin and employee workflows
- `docs/`
  - product, architecture, and roadmap docs
- `prompts/`
  - assistant system prompt
- `archive/`
  - preserved legacy backends and superseded assets

## Backend Modules

### Authentication and roles

- Seeded demo users
- JWT-based auth
- Role-based access with `admin` and `employee`

### Document ingestion

- Admin uploads PDF
- Backend stores file locally
- `pypdf` extracts page text
- Pages are chunked into retrieval units with page metadata

### Retrieval and citations

- Questions are matched against stored chunks
- Top-ranked chunks are returned as context
- Answers include citations with document title and page number

### Quiz generation

- Quiz questions are derived from indexed document chunks
- Quiz submissions create progress signals and score summaries

### Progress tracking

- Records training module status
- Captures quiz completion outcomes
- Supports employee-facing progress views

## Implementation Notes

- SQLite keeps local setup simple and demo-friendly.
- The retrieval layer is intentionally modular so it can later be upgraded to pgvector or another vector store.
- OpenAI-backed answer synthesis is optional. Without an API key, the system still works using a deterministic grounded fallback.
