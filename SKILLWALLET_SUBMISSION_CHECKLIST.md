# SkillWallet Submission Checklist

The 0% shown on the Workspace page is a portal completion state, not a code error. Use this order and tick each item only after saving its proof.

## Before submission

- [ ] Extract the ZIP and run the project locally.
- [ ] Create a fresh Gemini API key and keep it only in `.env` or the hosting secret settings.
- [ ] Open the website and generate one plan that shows the `Gemini AI` badge.
- [ ] Open `/docs` and test `POST /api/recommendations` successfully.
- [ ] Run `pytest -v` and confirm every test passes.
- [ ] Upload the complete project to a public or faculty-accessible GitHub repository.
- [ ] Deploy the FastAPI app and confirm `/api/health` returns HTTP 200.

## Proof screenshots to capture

Use clear filenames so faculty can understand them immediately.

1. `01-home-page.png` — PocketSmart AI main page.
2. `02-gemini-result.png` — Generated plan with Gemini badge and budget totals.
3. `03-swagger-docs.png` — `/docs` showing the three API endpoints.
4. `04-api-response.png` — Successful recommendation JSON response.
5. `05-pytest-passed.png` — Terminal with all tests passed.
6. `06-github-repository.png` — Repository file structure.
7. `07-live-deployment.png` — Deployed website with browser URL visible.

## Portal completion order

### Prerequisites

- [ ] Open the section, read every item and complete any acknowledgement or quiz.
- [ ] Use `.env.example` and the setup commands as implementation evidence.

### Project Workflow

- [ ] Explain the architecture from the README.
- [ ] Attach the repository link if a URL field is provided.

### Epic 1 — Gemini AI Initialization

- [ ] Show `app/config.py` and `app/services/gemini_service.py`.
- [ ] Explain that the API key is loaded from the environment, not hard-coded.
- [ ] Show one response where `source` is `gemini`.

### Epic 2 — Core Functionalities Development

- [ ] Demonstrate all three categories.
- [ ] Demonstrate Essential, Balanced and Premium preferences.
- [ ] Show that total spending stays below the selected budget.

### Epic 3 — FastAPI Integration

- [ ] Open `/docs`.
- [ ] Run `GET /api/health`, `GET /api/categories` and `POST /api/recommendations`.
- [ ] Save the API response screenshot.

### Epic 4 — UI Development

- [ ] Show mobile or responsive layout.
- [ ] Generate and save a plan.
- [ ] Open Saved Plans and show the stored result.

### Epic 5 — Testing and Deployment

- [ ] Run `pytest -v` and attach the result.
- [ ] Show the green GitHub Actions test run.
- [ ] Paste the live deployment URL.

### Conclusion

- [ ] Add a short learning summary.
- [ ] Confirm every internal task is marked completed/submitted.

## Final links to paste

```text
GitHub repository: ADD_LINK_HERE
Live demo: ADD_LINK_HERE
Swagger docs: ADD_LIVE_LINK_HERE/docs
```

After pasting the links, return to Workspace and refresh. If a section is still 0%, expand that section; one internal task, quiz or acknowledgement is still incomplete.
