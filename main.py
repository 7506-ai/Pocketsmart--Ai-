"""FastAPI entry point for PocketSmart AI."""

from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings
from app.models import CategoryInfo, HealthResponse, RecommendationRequest, RecommendationResponse
from app.services.budget_engine import CATEGORY_META
from app.services.gemini_service import GeminiBudgetService

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

settings = Settings.from_env()
recommendation_service = GeminiBudgetService(settings)

app = FastAPI(
    title="PocketSmart AI API",
    version=settings.app_version,
    description="Gemini-powered budget recommendations with a deterministic safety fallback.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def get_recommendation_service() -> GeminiBudgetService:
    return recommendation_service


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    configured = recommendation_service.configured
    return HealthResponse(
        app=settings.app_name,
        version=settings.app_version,
        gemini_configured=configured,
        mode="gemini-ready" if configured else "fallback-ready",
    )


@app.get("/api/categories", response_model=list[CategoryInfo], tags=["Budget planner"])
def categories() -> list[CategoryInfo]:
    return [
        CategoryInfo(id=category, title=meta["title"], description=meta["description"])
        for category, meta in CATEGORY_META.items()
    ]


@app.post("/api/recommendations", response_model=RecommendationResponse, tags=["Budget planner"])
def create_recommendation(
    request: RecommendationRequest,
    service: GeminiBudgetService = Depends(get_recommendation_service),
) -> RecommendationResponse:
    return service.generate(request)
