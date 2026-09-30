# SkillWallet Epic Requirement Mapping

This file shows where every visible SkillWallet requirement is implemented in the repository.

| SkillWallet section | Evidence in this project | What to demonstrate |
| --- | --- | --- |
| Prerequisites | `requirements.txt`, `.env.example`, `START_HERE_TAMIL.md` | Python environment, dependencies and safe API-key setup |
| Project Workflow | `README.md` architecture and project structure | Explain UI → FastAPI → Gemini/fallback → validated response |
| Epic 1: Gemini AI Initialization | `app/config.py`, `app/services/gemini_service.py` | Environment key, official SDK client, model and structured JSON schema |
| Epic 2: Core Functionalities Development | `app/models.py`, `app/services/budget_engine.py` | Categories, preferences, budget calculation, reserve and fallback |
| Epic 3: Backend – FastAPI Integration | `app/main.py` | Health, categories and recommendation endpoints plus `/docs` |
| Epic 4: UI Development | `app/static/index.html`, `app/static/css/style.css`, `app/static/js/app.js` | Responsive form, backend fetch, results and saved plans |
| Epic 5: Testing and Deployment | `tests/`, `.github/workflows/tests.yml`, `Dockerfile`, `render.yaml` | Passing pytest output, GitHub Actions and deployed URL |
| Conclusion | `README.md`, running app and submission screenshots | Final demonstration and project learning summary |

## Functional acceptance criteria

- A valid budget request returns HTTP 200 and a list of recommendations.
- Invalid category, preference or out-of-range budget returns HTTP 422.
- The sum of all item amounts equals `total`.
- `total + remaining` always equals the user budget.
- Gemini output is validated before use.
- Missing key, quota failure or network failure switches to `smart_fallback`.
- No secret key is returned by the health API or committed to source control.
- The frontend remains usable on mobile and desktop.
