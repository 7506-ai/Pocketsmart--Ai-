# PocketSmart AI — Gemini + FastAPI Edition

PocketSmart AI is a full-stack student project that creates safe, category-based budget recommendations. It uses Gemini structured output when a valid API key is configured and automatically switches to a deterministic smart fallback when AI is unavailable.

## What is included

- Responsive HTML, CSS and JavaScript interface
- FastAPI REST backend with Swagger and ReDoc
- Gemini API integration through the official `google-genai` Python SDK
- Pydantic input and output validation
- Safe budget normalization so a plan never exceeds the selected budget
- Offline/server-side fallback when an API key, quota or network is unavailable
- Pytest unit and API tests using FastAPI `TestClient`
- GitHub Actions continuous testing
- Dockerfile, Procfile and `render.yaml` deployment options
- Epic-by-Epic SkillWallet evidence checklist

## Architecture

```text
Browser UI
   │  POST /api/recommendations
   ▼
FastAPI + Pydantic validation
   │
   ├── Gemini structured response (when configured)
   │
   └── Smart deterministic fallback
             │
             ▼
      Safe budget normalizer
             │
             ▼
       Validated JSON plan
```

## Project structure

```text
PocketSmart-AI-Gemini-FastAPI/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── services/
│   │   ├── budget_engine.py
│   │   └── gemini_service.py
│   └── static/
│       ├── index.html
│       ├── css/style.css
│       ├── js/app.js
│       └── images/favicon.svg
├── tests/
├── docs/
├── .github/workflows/tests.yml
├── .env.example
├── Dockerfile
├── Procfile
├── render.yaml
├── requirements.txt
└── requirements-dev.txt
```

## Run locally

Python 3.10 or newer is required. Python 3.12 is recommended.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
cp .env.example .env
python3 -m uvicorn app.main:app --reload
```

Open:

- App: <http://127.0.0.1:8000>
- Swagger API testing: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Enable Gemini AI

1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Open `.env`.
3. Replace the placeholder value:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env` or paste a real API key into GitHub. The application still works in smart fallback mode without a key.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Backend and Gemini configuration status |
| `GET` | `/api/categories` | Supported planning categories |
| `POST` | `/api/recommendations` | Generate a validated budget plan |
| `GET` | `/docs` | Interactive Swagger API documentation |
| `GET` | `/redoc` | ReDoc API documentation |

Example request:

```json
{
  "category": "party",
  "budget": 25000,
  "preference": "Balanced",
  "notes": "30 guests and a blue theme"
}
```

## Run automated tests

```bash
pytest -v
pytest --cov=app --cov-report=term-missing
```

Tests never require a real Gemini key. Gemini responses are mocked, and the fallback path is tested separately.

## Deployment

The project can run on any Python or Docker host. Configure `GEMINI_API_KEY` as a secret environment variable in the hosting dashboard. GitHub Pages cannot run this FastAPI backend; it can host only a static frontend.

For submission evidence and the exact SkillWallet order, read:

- [Tamil start guide](START_HERE_TAMIL.md)
- [Epic requirement mapping](docs/EPIC_MAPPING.md)
- [SkillWallet submission checklist](docs/SKILLWALLET_SUBMISSION_CHECKLIST.md)
- [API and testing guide](docs/API_TESTING.md)
- [Viva questions and answers](docs/VIVA_QUESTIONS.md)

## Technical references

- [Gemini API getting started](https://ai.google.dev/gemini-api/docs/get-started)
- [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI static files](https://fastapi.tiangolo.com/tutorial/static-files/)

## Author

Aswin E — B.Sc. Computer Science
