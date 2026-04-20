#!/usr/bin/env bash
set +e
cd /home/clawdy/.openclaw/workspace
python3 scripts/ai-briefing-proof-recheck.py --json > /tmp/ai_proof_recheck_1629.json
pr=$?
python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3 > /tmp/ai_watchdog_1629.json
wd=$?
python3 scripts/ai-briefing-watchdog-alert.py --mode proof-target-check --json --consumer-bundle board-suite > /tmp/ai_proof_target_check_1629.json
pt=$?
printf 'proof_recheck_exit=%s\nwatchdog_exit=%s\nproof_target_check_exit=%s\n' "$pr" "$wd" "$pt"
printf '\n---PROOF-RECHECK---\n'
jq '{result_kind, proof_blocker_kind, proof_runs_completed, proof_runs_required, proof_next_qualifying_slot_text, proof_recheck_after_text, proof_target_due_at_text, proof_target_due_at_if_next_slot_missed_text, proof_target_check_gate_text, proof_recheck_schedule_kind_text, consumer_requested_outputs_text}' /tmp/ai_proof_recheck_1629.json
printf '\n---WATCHDOG---\n'
jq '{proof_blocker_kind, proof_progress_text, last_run_config_relation_text, proof_next_qualifying_slot_text, proof_recheck_after_text, proof_target_due_at_text, proof_target_due_at_if_next_slot_missed_text}' /tmp/ai_watchdog_1629.json
printf '\n---TARGET-CHECK---\n'
jq '{mode, no_reply, suppressed_before_proof_deadline, proof_target_check_gate_text, proof_recheck_schedule_kind_text, consumer_requested_outputs_text}' /tmp/ai_proof_target_check_1629.json
