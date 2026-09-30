"""Environment-based settings for PocketSmart AI."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _as_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "PocketSmart AI"
    app_version: str = "2.0.0"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    gemini_enabled: bool = True
    allowed_origins: tuple[str, ...] = ("http://localhost:8000", "http://127.0.0.1:8000")

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        raw_origins = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:8000,http://127.0.0.1:8000",
        )
        origins = tuple(origin.strip() for origin in raw_origins.split(",") if origin.strip())
        api_key = os.getenv("GEMINI_API_KEY", "").strip() or None
        return cls(
            gemini_api_key=api_key,
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip() or "gemini-3.8-flash",
            gemini_enabled=_as_bool(os.getenv("GEMINI_ENABLED"), default=True),
            allowed_origins=origins,
        )
