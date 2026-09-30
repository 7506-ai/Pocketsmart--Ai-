import pytest

from app.models import Category, Preference, RecommendationRequest
from app.services.budget_engine import build_fallback_plan


@pytest.mark.parametrize("category", list(Category))
@pytest.mark.parametrize("preference", list(Preference))
def test_fallback_plan_is_always_inside_budget(category, preference):
    request = RecommendationRequest(
        category=category,
        budget=25_000,
        preference=preference,
        notes="student-friendly",
    )

    plan = build_fallback_plan(request)

    assert 3 <= len(plan.items) <= 8
    assert plan.total + plan.remaining == plan.budget
    assert plan.total <= plan.budget
    assert plan.remaining > 0
    assert sum(item.amount for item in plan.items) == plan.total
    assert all(item.amount >= 100 for item in plan.items)
    assert plan.source == "smart_fallback"


def test_preference_changes_spending_level():
    essential = build_fallback_plan(
        RecommendationRequest(category="home", budget=50_000, preference="Essential")
    )
    premium = build_fallback_plan(
        RecommendationRequest(category="home", budget=50_000, preference="Premium")
    )

    assert essential.total < premium.total
    assert essential.remaining > premium.remaining


def test_notes_are_cleaned():
    request = RecommendationRequest(
        category="party",
        budget=20_000,
        preference="Balanced",
        notes="  30   guests   and blue theme  ",
    )
    assert request.notes == "30 guests and blue theme"
