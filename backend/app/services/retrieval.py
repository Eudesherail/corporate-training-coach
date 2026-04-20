import re
from collections import Counter

from openai import OpenAI
from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.models import DocumentChunk
from app.schemas import Citation


settings = get_settings()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9']+", text.lower())


def rank_chunks(db: Session, question: str, limit: int = 4) -> list[DocumentChunk]:
    query_terms = tokenize(question)
    if not query_terms:
        return []

    term_counter = Counter(query_terms)
    scored: list[tuple[float, DocumentChunk]] = []
    chunks = db.query(DocumentChunk).options(joinedload(DocumentChunk.document)).all()

    for chunk in chunks:
        content_terms = Counter(tokenize(chunk.content))
        overlap = sum(min(content_terms[token], count) for token, count in term_counter.items())
        score = overlap / max(len(query_terms), 1)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:limit]]


def build_citations(chunks: list[DocumentChunk]) -> list[Citation]:
    citations: list[Citation] = []
    for chunk in chunks:
        citations.append(
            Citation(
                document_name=chunk.document.title,
                page_number=chunk.page_number,
                excerpt=chunk.content[:240].strip(),
            )
        )
    return citations


def _fallback_answer(chunks: list[DocumentChunk]) -> str:
    if not chunks:
        return "I could not find this information in the provided materials."

    bullets = []
    for chunk in chunks[:2]:
        snippet = chunk.content[:280].strip()
        bullets.append(
            f"- According to {chunk.document.title} (Page {chunk.page_number}), {snippet}"
        )
    return "\n".join(bullets)


def generate_answer(question: str, chunks: list[DocumentChunk]) -> str:
    if not chunks:
        return "I could not find this information in the provided materials."

    if not settings.openai_api_key:
        return _fallback_answer(chunks)

    context = "\n\n".join(
        [
            f"[{chunk.document.title} | Page {chunk.page_number}]\n{chunk.content}"
            for chunk in chunks
        ]
    )
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.chat_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a document-grounded corporate training assistant. "
                    "Answer only from provided context. If the answer is not in the context, "
                    "say exactly: I could not find this information in the provided materials."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Context:\n{context}\n\n"
                    "Return a short professional answer with no hallucinated policies."
                ),
            },
        ],
    )
    return response.output_text.strip()
