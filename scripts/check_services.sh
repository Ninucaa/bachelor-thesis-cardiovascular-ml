#!/usr/bin/env bash
set -euo pipefail

backend_url="${BACKEND_URL:-http://127.0.0.1:8765/health}"
frontend_url="${FRONTEND_URL:-http://127.0.0.1:5173/}"

echo "Checking backend: ${backend_url}"
curl -fsS "${backend_url}"
echo

echo "Checking frontend: ${frontend_url}"
curl -fsSI "${frontend_url}" >/dev/null
echo "Frontend is reachable."
