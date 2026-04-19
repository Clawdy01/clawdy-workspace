#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 scripts/ai-briefing-watchdog-alert.py --mode proof-progress --json --reference-ms 1776581880000 > /tmp/ai_watchdog_alert_json_check.json
jq '{mode, no_reply, proof_state, proof_next_action_kind, proof_recheck_schedule_kind, proof_recheck_schedule_kind_text, proof_recheck_schedule_job_name, proof_recheck_schedule_expr, proof_recheck_schedule_tz, alert_text}' /tmp/ai_watchdog_alert_json_check.json
python3 scripts/ai-briefing-regression-check.py --json > /tmp/ai_regression_watchdog_alert_json.json
jq '{ok, summary, failed_count, failing_case_names}' /tmp/ai_regression_watchdog_alert_json.json
