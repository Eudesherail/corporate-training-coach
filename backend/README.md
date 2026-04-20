# Backend

FastAPI backend for Corporate Training Coach.

## Responsibilities

- JWT authentication with seeded demo users
- admin-only PDF upload and indexing
- retrieval-backed assistant answers
- quiz generation from indexed documents
- employee progress tracking

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Requirements:

- Python 3.11
- `bcrypt==3.2.2` is pinned for passlib compatibility in local demo environments
