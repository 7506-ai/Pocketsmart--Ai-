#!/usr/bin/env sh
set -eu
python3 -m pip install -r requirements-dev.txt
if [ ! -f .env ]; then cp .env.example .env; fi
python3 -m uvicorn app.main:app --reload
