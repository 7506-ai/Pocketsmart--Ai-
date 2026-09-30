# Verified Build Results

Verification date: 30 September 2026 (UTC)

## Automated tests

```text
23 passed in 1.06s
Total application coverage: 91%
```

Covered areas:

- Frontend and static asset delivery
- Health and category endpoints
- Recommendation endpoint
- Invalid request validation (HTTP 422)
- Every category and preference combination
- Budget total and reserve invariants
- Gemini structured-response path with a mock client
- Gemini error and missing-key fallback paths

## Additional checks

```text
JavaScript syntax: OK
Python compile: OK
OpenAPI schema: OK
HTTP health endpoint: OK
HTTP categories endpoint: OK
HTTP recommendation endpoint: OK
```

The live Gemini call is intentionally not part of automated tests because a secret API key must never be stored in the repository and tests should not consume API quota.
