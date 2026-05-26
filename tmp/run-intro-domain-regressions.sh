#!/usr/bin/env bash
set -euo pipefail
python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-regression-check.py
python3 scripts/ai-briefing-regression-check.py \
  --case explicit-no-briefingitems-with-intro-domain-reference-sample \
  --case status-summary-audit-cli-keeps-explicit-no-briefingitems-with-intro-domain-reference-audit \
  --case explicit-no-briefingitems-with-domain-reference-sample \
  --case status-summary-audit-cli-keeps-explicit-no-briefingitems-with-domain-reference-audit \
  --case explicit-no-briefingitems-with-summary-evidence-sample \
  --case status-summary-audit-cli-keeps-explicit-no-briefingitems-summary-evidence-audit \
  --json
