# PocketSmart AI Viva Questions and Short Answers

## What is PocketSmart AI?

It is a full-stack budget recommendation application. The user selects a category, budget and preference; the backend returns a safe item-wise spending plan with a reserve.

## Why is FastAPI used?

FastAPI provides validated REST endpoints, automatic OpenAPI/Swagger documentation and a simple testing workflow.

## How is Gemini used?

The backend sends the validated user request to Gemini through the official Python SDK. Gemini returns a structured JSON draft that is validated by Pydantic before the server calculates money values.

## Why not let Gemini calculate the final budget directly?

Generative models can make arithmetic or formatting mistakes. PocketSmart AI uses Gemini for recommendation content and a deterministic Python engine for final allocation, ensuring the plan never exceeds the budget.

## What happens if Gemini fails?

The service catches the failure and uses a deterministic category-based fallback. The website therefore remains usable without a key, during quota limits or during a network issue.

## What is Pydantic?

Pydantic validates request and response data. It rejects unsupported categories, invalid preferences and budgets outside the allowed range.

## What endpoints are available?

`GET /api/health`, `GET /api/categories` and `POST /api/recommendations`. Interactive documentation is available at `/docs`.

## How is the project tested?

Pytest tests the budget engine, Gemini success and failure paths, API endpoints, validation errors and static frontend serving. Gemini is mocked, so automated tests do not spend API quota.

## How is the API key protected?

The key is read from a local `.env` file or the hosting provider's secret environment settings. `.env` is excluded by `.gitignore`, and the health endpoint never returns the key.

## What can be added in the future?

User authentication, database-backed saved plans, more budget categories, live product price integrations and multilingual recommendations can be added later.
