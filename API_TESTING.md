# API and Testing Guide

## Start the server

```bash
python -m uvicorn app.main:app --reload
```

## Swagger testing

Open `http://127.0.0.1:8000/docs`, select `POST /api/recommendations`, choose **Try it out**, paste the request below and press **Execute**.

```json
{
  "category": "party",
  "budget": 25000,
  "preference": "Balanced",
  "notes": "30 guests and a blue theme"
}
```

Expected checks:

- HTTP status is `200`.
- `source` is `gemini` when the key works, otherwise `smart_fallback`.
- `total` is not greater than `budget`.
- `total + remaining` equals `budget`.
- `items` contains practical recommendations.

## Command-line API test

```bash
curl -X POST http://127.0.0.1:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"category":"home","budget":25000,"preference":"Balanced","notes":"modern style"}'
```

## Automated tests

```bash
pytest -v
pytest --cov=app --cov-report=term-missing
```

The test suite covers:

- Budget allocation for every category and preference.
- Budget safety invariant.
- Notes normalization.
- Valid Gemini structured JSON.
- Gemini failure fallback.
- Home page and static file serving.
- Health and category endpoints.
- Valid and invalid API requests.

## Common issues

| Problem | Fix |
| --- | --- |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements-dev.txt`. |
| Gemini badge shows fallback | Add a valid `GEMINI_API_KEY` to `.env`, restart the server and generate again. |
| Port 8000 already in use | Run `uvicorn app.main:app --reload --port 8001`. |
| API returns 422 | Use a supported category, exact preference spelling and a budget from 5,000 to 200,000. |
| GitHub Pages shows only static content | Deploy the repository to a Python/Docker hosting service. |
