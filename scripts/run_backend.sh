#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export PYDANTIC_DISABLE_PLUGINS="${PYDANTIC_DISABLE_PLUGINS:-1}"

if [ ! -x ".venv/bin/python" ]; then
  echo "Virtual environment not found. Run: python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt" >&2
  exit 1
fi

exec .venv/bin/python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8765 --reload
