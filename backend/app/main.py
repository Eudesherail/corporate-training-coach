from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.database import Base, engine
from app.seed import seed_demo_data


settings = get_settings()
Base.metadata.create_all(bind=engine)
seed_demo_data()

app = FastAPI(
    title="Corporate Training Coach API",
    version="0.1.0",
    summary="Document-grounded onboarding and compliance training platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router, prefix="/api")
