#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 scripts/ai-briefing-regression-check.py --json \
  --case watchdog-stdout-json-before-slot-keeps-proof-config-context \
  --case watchdog-stdout-json-open-window-keeps-proof-config-context
