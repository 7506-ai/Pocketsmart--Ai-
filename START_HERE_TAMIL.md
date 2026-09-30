# முதலில் இதைப் படிக்கவும் — PocketSmart AI Full Project

Machi, இது பழைய static website மட்டும் இல்லை. இந்த version-ல் **Gemini AI + FastAPI backend + validation + automated testing + deployment files** எல்லாமே இருக்கு.

## Screenshot-ல் ஏன் 0% காட்டுகிறது?

SkillWallet progress தானாக GitHub code-ஐ பார்த்து update ஆகாது. ஒவ்வொரு section-ஐ open செய்து அதில் கேட்ட task/quiz/proof-ஐ submit அல்லது complete செய்த பிறகுதான் percentage மாறும்.

இந்த project code ready ஆனாலும் கீழே உள்ள proof-களை நீ portal-ல் add செய்ய வேண்டும்:

1. GitHub repository link
2. Running demo link
3. `/docs` Swagger screenshot
4. `pytest -v` result screenshot
5. Frontend result screenshot
6. ஒவ்வொரு Epic task-க்கும் completion click/submit

Exact checklist: `docs/SKILLWALLET_SUBMISSION_CHECKLIST.md`

## Laptop-ல் run செய்வது

### முதல் முறை மட்டும்

1. Python 3.12 install பண்ணு.
2. ZIP extract பண்ணு.
3. Extract செய்த project folder-ஐ VS Code-ல் open பண்ணு.
4. VS Code Terminal open பண்ணு.
5. இந்த commands run பண்ணு:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
copy .env.example .env
```

### Gemini key add செய்வது

1. Google AI Studio-ல் ஒரு புதிய API key create பண்ணு.
2. Project-ல் உள்ள `.env` file open பண்ணு.
3. இந்த line-ல் மட்டும் உன் key paste பண்ணு:

```env
GEMINI_API_KEY=your_real_key_here
```

API key-ஐ GitHub-ல் upload பண்ணக் கூடாது. ஏற்கனவே public-ஆ share செய்த key இருந்தால் அதை revoke/rotate செய்து புதிய key use பண்ணுவது safe.

### Website start செய்வது

```powershell
python -m uvicorn app.main:app --reload
```

Browser-ல்:

- Website: `http://127.0.0.1:8000`
- API testing: `http://127.0.0.1:8000/docs`

## Tests run செய்வது

```powershell
pytest -v
```

எல்லா tests-க்கும் `PASSED` வந்த screen-ஐ screenshot எடுத்து வைத்துக்கோ. இது Epic 5 proof.

## GitHub-க்கு upload செய்வது

Project folder உள்ளே இருக்கும் files/folders அனைத்தையும் repository root-க்கு upload பண்ணு. `.env` file மட்டும் upload பண்ணக்கூடாது. `.env.example` upload ஆக வேண்டும்.

Upload ஆனதும் repository-ல் இவை இருப்பதை check பண்ணு:

- `app` folder
- `tests` folder
- `docs` folder
- `requirements.txt`
- `Dockerfile`
- `README.md`
- `.github/workflows/tests.yml`

## முக்கியம்

GitHub Pages Python/FastAPI backend-ஐ run பண்ணாது. Full Gemini project demo-க்கு Python/Docker hosting தேவை. Hosting dashboard-ல் `GEMINI_API_KEY`-ஐ secret environment variable-ஆ add பண்ணு; source code-ல் எழுதாதே.

## SkillWallet complete order

`Prerequisites → Project Workflow → Epic 1 → Epic 2 → Epic 3 → Epic 4 → Epic 5 → Conclusion`

ஒவ்வொரு section-ஐ expand செய்து உள்ளே இருக்கிற task-ஐ complete பண்ணாமல் main screen-ல் percentage update ஆகாது.
