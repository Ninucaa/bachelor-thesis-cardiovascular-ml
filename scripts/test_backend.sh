#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export PYDANTIC_DISABLE_PLUGINS="${PYDANTIC_DISABLE_PLUGINS:-1}"
export PYTEST_DISABLE_PLUGIN_AUTOLOAD="${PYTEST_DISABLE_PLUGIN_AUTOLOAD:-1}"

exec .venv/bin/python -m pytest -q
