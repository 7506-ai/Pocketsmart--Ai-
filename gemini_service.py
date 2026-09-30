"""Gemini integration with validated structured output and a safe fallback."""

from __future__ import annotations

import logging
from typing import Any

from app.config import Settings
from app.models import GeminiDraft, RecommendationRequest, RecommendationResponse
from app.services.budget_engine import build_fallback_plan, build_plan

logger = logging.getLogger(__name__)


class GeminiBudgetService:
    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        self.settings = settings
        self._client = client

    @property
    def configured(self) -> bool:
        return bool(self.settings.gemini_enabled and self.settings.gemini_api_key)

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        from google import genai

        self._client = genai.Client(api_key=self.settings.gemini_api_key)
        return self._client

    def generate(self, request: RecommendationRequest) -> RecommendationResponse:
        if not self.configured and self._client is None:
            return build_fallback_plan(request)

        prompt = f"""
You are PocketSmart AI, a cautious Indian personal-budget planning assistant.
Create a useful recommendation list for this request:
{request.model_dump_json()}

Rules:
- Return 4 to 6 realistic items for the chosen category.
- Use Indian market context, but do not invent exact shop names or live prices.
- Each reason must be short and practical.
- "weight" is a relative allocation weight; all weights must be positive.
- The server will calculate rupee amounts and keep a safety reserve.
- Respect the user's notes when safe and relevant.
""".strip()

        try:
            interaction = self._get_client().interactions.create(
                model=self.settings.gemini_model,
                input=prompt,
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": GeminiDraft.model_json_schema(),
                },
            )
            output_text = getattr(interaction, "output_text", "")
            if not output_text:
                raise ValueError("Gemini returned an empty response")
            draft = GeminiDraft.model_validate_json(output_text)
            return build_plan(
                request,
                draft,
                source="gemini",
                model=self.settings.gemini_model,
            )
        except Exception as exc:  # A live AI failure must not break the user flow.
            logger.warning("Gemini request failed; using the smart fallback (%s)", type(exc).__name__)
            return build_fallback_plan(request)
