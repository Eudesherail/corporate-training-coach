from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class DocumentResponse(BaseModel):
    id: int
    title: str
    category: str
    description: str
    filename: str
    uploaded_at: datetime
    total_pages: int

    class Config:
        from_attributes = True


class Citation(BaseModel):
    document_name: str
    page_number: int
    excerpt: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=3)


class ChatResponse(BaseModel):
    title: str
    answer: str
    citations: list[Citation]
    mode: str = "EXPLAIN"


class QuizQuestionResponse(BaseModel):
    id: int
    prompt: str
    explanation: str
    source_document: str
    source_page: int

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: int
    title: str
    document_id: int
    questions: list[QuizQuestionResponse]


class GenerateQuizRequest(BaseModel):
    document_id: int
    title: str = "Onboarding Knowledge Check"
    question_count: int = Field(default=5, ge=3, le=8)


class SubmitQuizRequest(BaseModel):
    answers: dict[int, str]


class QuizAttemptResponse(BaseModel):
    score_percent: float
    total_questions: int
    correct_answers: int


class ProgressUpdateRequest(BaseModel):
    module_name: str
    document_id: int | None = None
    status: str = "in_progress"
    completion_percent: int = Field(default=0, ge=0, le=100)
    notes: str = ""


class ProgressRecordResponse(BaseModel):
    id: int
    module_name: str
    status: str
    completion_percent: int
    notes: str
    updated_at: datetime

    class Config:
        from_attributes = True


class AdminDashboardResponse(BaseModel):
    total_documents: int
    total_quizzes: int
    total_employees: int
    active_progress_records: int


class EmployeeDashboardResponse(BaseModel):
    assigned_modules: int
    completed_modules: int
    recent_quiz_average: float
