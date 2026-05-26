#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 -m py_compile scripts/ai-briefing-watchdog-producer.py scripts/ai-briefing-regression-check.py
python3 scripts/ai-briefing-regression-check.py \
  --case watchdog-producer-overall-keeps-direct-status-and-proof-due-fields \
  --case watchdog-producer-before-slot-keeps-proof-recheck-cronstatus \
  --case watchdog-producer-open-window-keeps-proof-recheck-cronstatus \
  --case status-proof-context-all-routes
