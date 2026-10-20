#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
cp -n .env.example .env || true
skill-arena seed
skill-arena filter
skill-arena status
echo "Bootstrap done. Fill .env then: skill-arena ping-model && skill-arena eval-pilot"
