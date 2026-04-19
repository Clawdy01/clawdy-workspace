#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 scripts/ai-briefing-regression-check.py --json > /tmp/ai_regression_watchdog_alert_json.json
jq '{ok, summary, failed_count, failing_case_names}' /tmp/ai_regression_watchdog_alert_json.json
