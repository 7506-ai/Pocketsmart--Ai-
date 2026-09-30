"""Validated API and Gemini data models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Category(str, Enum):
    HOME = "home"
    PARTY = "party"
    JEWELLERY = "jewellery"


class Preference(str, Enum):
    ESSENTIAL = "Essential"
    BALANCED = "Balanced"
    PREMIUM = "Premium"


class RecommendationRequest(BaseModel):
    category: Category
    budget: int = Field(ge=5_000, le=200_000)
    preference: Preference = Preference.BALANCED
    notes: str = Field(default="", max_length=500)

    @field_validator("notes")
    @classmethod
    def clean_notes(cls, value: str) -> str:
        return " ".join(value.strip().split())


class GeminiDraftItem(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    reason: str = Field(min_length=2, max_length=180)
    weight: float = Field(gt=0, le=100)
    icon: str | None = Field(default=None, max_length=8)


class GeminiDraft(BaseModel):
    summary: str = Field(min_length=8, max_length=240)
    items: list[GeminiDraftItem] = Field(min_length=3, max_length=8)


class BudgetItem(BaseModel):
    icon: str
    name: str
    reason: str
    amount: int = Field(ge=0)


class RecommendationResponse(BaseModel):
    plan_id: str
    category: Category
    title: str
    preference: Preference
    budget: int
    notes: str
    summary: str
    items: list[BudgetItem]
    total: int
    remaining: int
    currency: Literal["INR"] = "INR"
    source: Literal["gemini", "smart_fallback"]
    model: str | None = None
    generated_at: datetime


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    app: str
    version: str
    gemini_configured: bool
    mode: Literal["gemini-ready", "fallback-ready"]


class CategoryInfo(BaseModel):
    id: Category
    title: str
    description: str
