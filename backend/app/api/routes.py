from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_current_user,
    require_admin,
    verify_password,
)
from app.models import Document, ProgressRecord, Quiz, QuizAttempt, User
from app.schemas import (
    AdminDashboardResponse,
    AuthResponse,
    ChatRequest,
    ChatResponse,
    DocumentResponse,
    EmployeeDashboardResponse,
    GenerateQuizRequest,
    LoginRequest,
    ProgressRecordResponse,
    ProgressUpdateRequest,
    QuizAttemptResponse,
    QuizQuestionResponse,
    QuizResponse,
    SubmitQuizRequest,
    UserResponse,
)
from app.services.document_pipeline import ingest_document
from app.services.quiz_service import generate_quiz
from app.services.retrieval import build_citations, generate_answer, rank_chunks


router = APIRouter()
settings = get_settings()


@router.post("/auth/login", response_model=AuthResponse, tags=["auth"])
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user.email)
    return AuthResponse(access_token=token, user=user)


@router.get("/auth/me", response_model=UserResponse, tags=["auth"])
def me(user: User = Depends(get_current_user)) -> User:
    return user


@router.get("/users", response_model=list[UserResponse], tags=["admin"])
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).order_by(User.role.desc(), User.full_name.asc()).all()


@router.get("/dashboard/admin", response_model=AdminDashboardResponse, tags=["dashboard"])
def admin_dashboard(
    _: User = Depends(require_admin), db: Session = Depends(get_db)
) -> AdminDashboardResponse:
    return AdminDashboardResponse(
        total_documents=db.query(func.count(Document.id)).scalar() or 0,
        total_quizzes=db.query(func.count(Quiz.id)).scalar() or 0,
        total_employees=db.query(func.count(User.id)).filter(User.role == "employee").scalar() or 0,
        active_progress_records=(
            db.query(func.count(ProgressRecord.id))
            .filter(ProgressRecord.status != "completed")
            .scalar()
            or 0
        ),
    )


@router.get(
    "/dashboard/employee", response_model=EmployeeDashboardResponse, tags=["dashboard"]
)
def employee_dashboard(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> EmployeeDashboardResponse:
    records = db.query(ProgressRecord).filter(ProgressRecord.user_id == user.id).all()
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user.id).all()
    avg_score = round(sum(item.score for item in attempts) / len(attempts), 1) if attempts else 0.0
    return EmployeeDashboardResponse(
        assigned_modules=len(records),
        completed_modules=len([record for record in records if record.status == "completed"]),
        recent_quiz_average=avg_score,
    )


@router.post("/documents/upload", response_model=DocumentResponse, tags=["documents"])
async def upload_document(
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Document:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported right now")
    return await ingest_document(
        db=db,
        upload_dir=settings.upload_path,
        file=file,
        title=title,
        category=category,
        description=description,
        user=user,
    )


@router.get("/documents", response_model=list[DocumentResponse], tags=["documents"])
def list_documents(
    _: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Document]:
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


@router.post("/assistant/ask", response_model=ChatResponse, tags=["assistant"])
def ask_assistant(
    payload: ChatRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChatResponse:
    chunks = rank_chunks(db, payload.question)
    answer = generate_answer(payload.question, chunks)
    citations = build_citations(chunks)
    title = "Document-Grounded Answer" if citations else "No Relevant Source Found"
    return ChatResponse(title=title, answer=answer, citations=citations)


@router.post("/quizzes/generate", response_model=QuizResponse, tags=["quizzes"])
def create_quiz(
    payload: GenerateQuizRequest,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> QuizResponse:
    document = (
        db.query(Document)
        .options(joinedload(Document.chunks))
        .filter(Document.id == payload.document_id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    quiz = generate_quiz(db, document, user, payload.title, payload.question_count)
    questions = [
        QuizQuestionResponse.model_validate(question) for question in quiz.questions
    ]
    return QuizResponse(
        id=quiz.id, title=quiz.title, document_id=quiz.document_id, questions=questions
    )


@router.get("/quizzes", response_model=list[QuizResponse], tags=["quizzes"])
def list_quizzes(
    _: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[QuizResponse]:
    quizzes = db.query(Quiz).options(joinedload(Quiz.questions)).order_by(Quiz.created_at.desc()).all()
    return [
        QuizResponse(
            id=quiz.id,
            title=quiz.title,
            document_id=quiz.document_id,
            questions=[QuizQuestionResponse.model_validate(question) for question in quiz.questions],
        )
        for quiz in quizzes
    ]


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizAttemptResponse, tags=["quizzes"])
def submit_quiz(
    quiz_id: int,
    payload: SubmitQuizRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QuizAttemptResponse:
    quiz = db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    correct = 0
    for question in quiz.questions:
        submitted = payload.answers.get(question.id, "").strip().lower()
        expected = question.correct_answer.strip().lower()
        if submitted and submitted in expected:
            correct += 1

    total = len(quiz.questions)
    score_percent = round((correct / total) * 100, 1) if total else 0.0
    db.add(
        QuizAttempt(
            quiz_id=quiz.id,
            user_id=user.id,
            score=score_percent,
            total_questions=total,
        )
    )

    progress = (
        db.query(ProgressRecord)
        .filter(ProgressRecord.user_id == user.id, ProgressRecord.module_name == quiz.title)
        .first()
    )
    if not progress:
        progress = ProgressRecord(user_id=user.id, module_name=quiz.title)
        db.add(progress)
    progress.status = "completed" if score_percent >= 70 else "in_progress"
    progress.completion_percent = 100 if score_percent >= 70 else 70
    progress.notes = f"Last quiz score: {score_percent}%"
    progress.updated_at = datetime.utcnow()

    db.commit()
    return QuizAttemptResponse(
        score_percent=score_percent,
        total_questions=total,
        correct_answers=correct,
    )


@router.get("/progress/me", response_model=list[ProgressRecordResponse], tags=["progress"])
def my_progress(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[ProgressRecord]:
    return (
        db.query(ProgressRecord)
        .filter(ProgressRecord.user_id == user.id)
        .order_by(ProgressRecord.updated_at.desc())
        .all()
    )


@router.post("/progress", response_model=ProgressRecordResponse, tags=["progress"])
def update_progress(
    payload: ProgressUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProgressRecord:
    progress = (
        db.query(ProgressRecord)
        .filter(ProgressRecord.user_id == user.id, ProgressRecord.module_name == payload.module_name)
        .first()
    )
    if not progress:
        progress = ProgressRecord(user_id=user.id, module_name=payload.module_name)
        db.add(progress)

    progress.document_id = payload.document_id
    progress.status = payload.status
    progress.completion_percent = payload.completion_percent
    progress.notes = payload.notes
    progress.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(progress)
    return progress
