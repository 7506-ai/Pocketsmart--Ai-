import pytest
from fastapi.testclient import TestClient

from app.main import app, get_recommendation_service
from app.services.budget_engine import build_fallback_plan


class StubRecommendationService:
    def generate(self, request):
        return build_fallback_plan(request)


@pytest.fixture(autouse=True)
def deterministic_service():
    app.dependency_overrides[get_recommendation_service] = lambda: StubRecommendationService()
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "PocketSmart AI" in response.text


def test_health_endpoint_does_not_expose_a_secret():
    response = client.get("/api/health")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert "api_key" not in data


def test_categories_endpoint():
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {"home", "party", "jewellery"}


def test_recommendation_endpoint():
    response = client.post(
        "/api/recommendations",
        json={
            "category": "home",
            "budget": 25_000,
            "preference": "Balanced",
            "notes": "modern student room",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["source"] == "smart_fallback"
    assert data["total"] + data["remaining"] == data["budget"]
    assert len(data["items"]) >= 3


@pytest.mark.parametrize(
    "payload",
    [
        {"category": "home", "budget": 4_999, "preference": "Balanced"},
        {"category": "travel", "budget": 25_000, "preference": "Balanced"},
        {"category": "home", "budget": 25_000, "preference": "Luxury"},
        {"category": "home", "budget": 200_001, "preference": "Balanced"},
    ],
)
def test_invalid_input_returns_422(payload):
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422


def test_static_css_is_served():
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "--primary" in response.text
