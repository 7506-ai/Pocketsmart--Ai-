from types import SimpleNamespace

from app.config import Settings
from app.models import RecommendationRequest
from app.services.gemini_service import GeminiBudgetService


class FakeInteractions:
    def __init__(self, output_text=None, error=None):
        self.output_text = output_text
        self.error = error
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        if self.error:
            raise self.error
        return SimpleNamespace(output_text=self.output_text)


class FakeClient:
    def __init__(self, interactions):
        self.interactions = interactions


def test_valid_gemini_json_becomes_a_safe_plan():
    output = """{
      "summary": "A student-friendly celebration plan with a protected backup amount.",
      "items": [
        {"name": "Venue", "reason": "Affordable local hall", "weight": 25, "icon": "🏛️"},
        {"name": "Food", "reason": "Simple menu for guests", "weight": 40, "icon": "🍽️"},
        {"name": "Decor", "reason": "Reusable themed decoration", "weight": 20, "icon": "🎈"},
        {"name": "Photos", "reason": "Capture the important moments", "weight": 15, "icon": "📸"}
      ]
    }"""
    interactions = FakeInteractions(output_text=output)
    service = GeminiBudgetService(
        Settings(gemini_api_key="test-key"),
        client=FakeClient(interactions),
    )
    request = RecommendationRequest(category="party", budget=30_000, preference="Balanced")

    plan = service.generate(request)

    assert plan.source == "gemini"
    assert plan.model == "gemini-3.8-flash"
    assert plan.total + plan.remaining == 30_000
    assert interactions.last_kwargs["response_format"]["mime_type"] == "application/json"
    assert "schema" in interactions.last_kwargs["response_format"]


def test_gemini_failure_uses_fallback_instead_of_crashing():
    service = GeminiBudgetService(
        Settings(gemini_api_key="test-key"),
        client=FakeClient(FakeInteractions(error=RuntimeError("network unavailable"))),
    )
    request = RecommendationRequest(category="home", budget=25_000, preference="Essential")

    plan = service.generate(request)

    assert plan.source == "smart_fallback"
    assert plan.total <= plan.budget


def test_missing_key_uses_fallback_without_calling_gemini():
    service = GeminiBudgetService(Settings(gemini_api_key=None))
    request = RecommendationRequest(category="jewellery", budget=40_000, preference="Premium")
    assert service.generate(request).source == "smart_fallback"
