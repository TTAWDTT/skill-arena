#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate
skill-arena status
skill-arena ping-model
skill-arena eval-pilot
