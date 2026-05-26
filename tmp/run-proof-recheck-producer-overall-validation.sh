#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 -m py_compile scripts/ai-briefing-regression-check.py scripts/ai-briefing-proof-recheck-producer.py
python3 scripts/ai-briefing-regression-check.py \
  --case proof-recheck-producer-overall-keeps-result-evidence-and-proof-due-fields \
  --case proof-recheck-producer-before-slot-too-early \
  --case proof-recheck-producer-open-window-needs-attention
