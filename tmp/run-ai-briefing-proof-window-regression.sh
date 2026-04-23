#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-regression-check.py
python3 scripts/ai-briefing-regression-check.py --json \
  --case status-stdout-json-before-slot-has-runtime-metadata \
  --case status-stdout-json-open-window-has-runtime-metadata \
  --case watchdog-stdout-json-before-slot-keeps-proof-config-context \
  --case watchdog-stdout-json-open-window-keeps-proof-config-context \
  --case proof-recheck-before-slot-too-early \
  --case proof-recheck-grace-window-too-early \
  --case proof-recheck-open-window-needs-attention
