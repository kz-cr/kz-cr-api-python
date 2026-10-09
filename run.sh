#!/usr/bin/env bash
# Run the API locally: creates a virtualenv if needed, installs deps, starts uvicorn.
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

exec uvicorn main:app --reload --host "${HOST:-127.0.0.1}" --port "${PORT:-8000}"
