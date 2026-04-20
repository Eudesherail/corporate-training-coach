import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models import Document, DocumentChunk, User


def sanitize_filename(filename: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", filename).strip("-")


def extract_pdf_pages(file_path: Path) -> list[dict[str, int | str]]:
    reader = PdfReader(str(file_path))
    pages: list[dict[str, int | str]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        clean_text = re.sub(r"\s+", " ", text).strip()
        if clean_text:
            pages.append({"page_number": index, "text": clean_text})
    return pages


def chunk_page_text(page_text: str, max_chars: int = 1400, overlap: int = 220) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(page_text):
        end = min(len(page_text), start + max_chars)
        chunks.append(page_text[start:end].strip())
        if end == len(page_text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


async def ingest_document(
    db: Session,
    upload_dir: Path,
    file: UploadFile,
    title: str,
    category: str,
    description: str,
    user: User,
) -> Document:
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = sanitize_filename(file.filename or "document.pdf")
    stored_name = f"{uuid4().hex}-{safe_name}"
    stored_path = upload_dir / stored_name

    with stored_path.open("wb") as output:
        output.write(await file.read())

    pages = extract_pdf_pages(stored_path)

    document = Document(
        title=title,
        category=category,
        description=description,
        filename=file.filename or safe_name,
        stored_path=str(stored_path),
        uploaded_by_id=user.id,
        total_pages=len(pages),
    )
    db.add(document)
    db.flush()

    chunk_counter = 0
    for page in pages:
        for chunk in chunk_page_text(str(page["text"])):
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    page_number=int(page["page_number"]),
                    chunk_index=chunk_counter,
                    content=chunk,
                )
            )
            chunk_counter += 1

    db.commit()
    db.refresh(document)
    return document
