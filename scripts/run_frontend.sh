#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../frontend"

if [ ! -d "node_modules" ]; then
  echo "Frontend dependencies not found. Run: npm install" >&2
  exit 1
fi

exec npm run dev
