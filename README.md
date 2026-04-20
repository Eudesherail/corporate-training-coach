# Corporate Training Coach

Angular + FastAPI demo for document-grounded onboarding, SOP training, compliance learning, and internal knowledge support.
It demonstrates a practical workflow from PDF upload and retrieval-backed answers to quiz generation and progress tracking.

Corporate Training Coach is an internal enablement platform for onboarding, SOP training, compliance education, and company knowledge support.

It is designed for a common operational problem: important onboarding documents, process guides, and policy PDFs often exist, but they are hard to search, hard to teach from consistently, and rarely turned into repeatable training workflows. This project turns those materials into a grounded assistant experience with document upload, retrieval-backed answers, generated quizzes, and basic progress tracking.

This repository is intended as a clear, working foundation for a corporate training product. It highlights product thinking, implementation choices, and tradeoffs without presenting itself as a fully hardened enterprise system.

## Quick Start

```bash
git clone https://github.com/Eudesherail/corporate-training-coach.git
cd corporate-training-coach
docker compose up --build
```

Open:

- http://localhost:4200

Sign in with:

- admin@coach.com / Admin123!
- employee@coach.com / Employee123!


## Why This Project Exists

Many teams have the same training gap:

- onboarding knowledge is scattered across handbooks, SOPs, policy PDFs, and internal docs
- employees often ask repeat questions because the source material is hard to navigate
- training quality varies by manager or department
- compliance and process learning are hard to reinforce consistently

Corporate Training Coach exists to make internal knowledge easier to access and easier to teach from. Instead of treating documents as static files, it treats them as training assets that can support search, explanation, quizzes, and progress visibility.

## What It Does

- Upload internal PDFs such as handbooks, SOPs, policy guides, and onboarding manuals
- Parse and chunk those documents for retrieval
- Answer employee questions using uploaded document content
- Return citation-backed responses with document and page references
- Generate quizzes from indexed company material
- Support separate admin and employee workflows
- Track basic training and onboarding progress

## Who It Is For

- HR teams running onboarding programs
- operations teams maintaining SOP training
- compliance and policy owners who need consistent education
- internal enablement teams supporting company knowledge access

## Product Scope

This is not a generic chatbot or consumer learning app.

The product is focused on:

- onboarding
- training
- SOP guidance
- compliance learning
- internal knowledge support

## Feature Overview

### Implemented Now

- Angular frontend with dedicated admin and employee screens
- FastAPI backend with JWT-based demo authentication
- Admin-only PDF upload and indexing flow
- PDF parsing with `pypdf`
- Chunk storage for retrieval
- Document-grounded assistant endpoint
- Citation payloads with document title, page number, and excerpt
- Quiz generation from indexed document text
- Quiz submission and basic scoring
- Employee progress records and dashboard summaries
- Docker setup for local demo use

### Planned Improvements

- vector-search retrieval instead of keyword-only ranking
- richer quiz grading and evaluation
- document management actions like delete and re-index
- stronger production persistence and migration support
- enterprise auth / SSO

## Architecture Summary

- `frontend/`
  Angular application for login, admin document workflows, employee training views, assistant interaction, and progress tracking.

- `backend/`
  FastAPI API for authentication, document ingestion, retrieval, quiz generation, and progress persistence.

- `docs/`
  Supporting project documentation:
  - [Product Overview](docs/product-overview.md)
  - [Architecture](docs/architecture.md)
  - [Roadmap](docs/roadmap.md)

- `prompts/`
  Assistant behavior prompt:
  - [System Prompt](prompts/system_prompt.txt)

- `archive/`
  Preserved legacy code from the original multi-backend prototype, kept for reference rather than active use.

## Setup

### Requirements

- Node.js 18+
- Python 3.11+
- npm

Compatibility note:

- `bcrypt` is pinned to `3.2.2` in the backend requirements to avoid passlib compatibility issues during local setup.

### Backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`.

Fresh-clone note:

- Use `python3.11` explicitly for backend setup.
- `.env.example` only contains settings accepted by the FastAPI config.
- The backend now creates the SQLite `app/data` directory automatically on first startup.

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:4200`.

### Docker

```bash
docker compose up --build
```

This starts:

- FastAPI on `http://localhost:8000`
- Angular via nginx on `http://localhost:4200`

## Demo Credentials

- Admin: `admin@coach.com` / `Admin123!`
- Employee: `employee@coach.com` / `Employee123!`

These are seeded automatically by the backend for local demo use.

## Usage Flow

1. Sign in as admin.
2. Upload a PDF such as an employee handbook, SOP, or compliance guide.
3. Let the backend parse and chunk the document.
4. Generate a quiz from the indexed document.
5. Sign in as employee.
6. Ask grounded questions in the assistant.
7. Review citations returned from the uploaded material.
8. Take quizzes and review progress updates.

## API Summary

### Auth

- `POST /api/auth/login`
- `GET /api/auth/me`

### Dashboards

- `GET /api/dashboard/admin`
- `GET /api/dashboard/employee`

### Documents

- `POST /api/documents/upload`
- `GET /api/documents`

### Assistant

- `POST /api/assistant/ask`

### Quizzes

- `POST /api/quizzes/generate`
- `GET /api/quizzes`
- `POST /api/quizzes/{quiz_id}/submit`

### Progress

- `GET /api/progress/me`
- `POST /api/progress`

## Environment Variables

See [.env.example](.env.example).

Important values:

- `JWT_SECRET`
- `OPENAI_API_KEY`
- `CHAT_MODEL`
- `DATABASE_URL`
- `CORS_ORIGINS`

## Current Limitations

This repository is intentionally honest about current scope.

- Retrieval is keyword-based today, not full vector search yet.
- Quiz grading is simple and currently relies on lightweight answer matching.
- Persistence is demo-oriented and uses SQLite by default.
- Background processing for large document ingestion is not implemented yet.
- Role handling is basic and limited to seeded `admin` and `employee` flows.
- The system is not production-hardened yet for multi-tenant, enterprise, or regulated deployment.
- Local setup expects Python 3.11 and the pinned bcrypt version in `backend/requirements.txt`.
- No real-time collaboration or multi-user sync yet.

## Repository Notes

- clear product identity
- one chosen backend architecture
- separated frontend/backend/docs/prompts layout
- preserved legacy code in `archive/` instead of mixing it into active runtime paths
- explicit roadmap and limitations
- easy local demo setup

## Suggested Demo Narrative

If you are showing this project to a reviewer, hiring manager, or teammate:

1. Log in as admin.
2. Upload a corporate handbook or SOP PDF.
3. Generate a quiz from that material.
4. Ask the assistant a policy or process question.
5. Show the citation-backed response.
6. Log in as employee and complete the quiz.
7. Show the progress update.

## Example Use Case

A new employee joins a company.

Instead of reading static PDFs:

- they upload onboarding materials
- ask questions in plain language
- get answers with citations
- take quizzes generated from real documents
- track their progress

This reduces onboarding time and improves knowledge retention.
