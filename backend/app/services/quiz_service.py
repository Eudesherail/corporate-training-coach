import re

from sqlalchemy.orm import Session

from app.models import Document, Quiz, QuizQuestion, User


def _sentence_candidates(text: str) -> list[str]:
    sentences = [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]
    return [sentence for sentence in sentences if len(sentence.split()) > 7]


def generate_quiz(
    db: Session, document: Document, created_by: User, title: str, question_count: int
) -> Quiz:
    quiz = Quiz(title=title, document_id=document.id, created_by_id=created_by.id)
    db.add(quiz)
    db.flush()

    question_index = 0
    for chunk in document.chunks:
        for sentence in _sentence_candidates(chunk.content):
            if question_index >= question_count:
                break
            question = f"What does {document.title} say about {sentence.split()[0:6]}?"
            db.add(
                QuizQuestion(
                    quiz_id=quiz.id,
                    prompt=question.replace("[", "").replace("]", "").replace("'", ""),
                    correct_answer=sentence,
                    explanation=(
                        f"According to {document.title} (Page {chunk.page_number}), {sentence}"
                    ),
                    source_document=document.title,
                    source_page=chunk.page_number,
                )
            )
            question_index += 1
        if question_index >= question_count:
            break

    db.commit()
    db.refresh(quiz)
    return quiz
