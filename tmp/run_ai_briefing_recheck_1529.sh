#!/usr/bin/env bash
set +e
cd /home/clawdy/.openclaw/workspace
python3 scripts/ai-briefing-proof-recheck.py --json > /tmp/ai_proof_recheck_1529.json
rc1=$?
python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3 > /tmp/ai_watchdog_1529.json
rc2=$?
python3 scripts/ai-briefing-watchdog-alert.py --mode proof-target-check --json --consumer-bundle board-suite > /tmp/ai_proof_target_check_1529.json
rc3=$?
printf 'proof_recheck_rc=%s\nwatchdog_rc=%s\nproof_target_check_rc=%s\n' "$rc1" "$rc2" "$rc3"
jq '{result_kind, proof_blocker_kind, proof_progress_text, proof_wait_until_text, proof_recheck_after_text, proof_target_due_at_text, proof_target_due_at_if_next_slot_missed_text, proof_target_check_gate_text, proof_recheck_schedule_kind_text, consumer_requested_outputs_text}' /tmp/ai_proof_recheck_1529.json
printf '%s\n' '---'
jq '{proof_blocker_kind, proof_progress_text, proof_wait_until_text, proof_recheck_after_text, proof_target_due_at_text, proof_target_due_at_if_next_slot_missed_text, proof_target_check_gate_text, proof_recheck_schedule_kind_text}' /tmp/ai_watchdog_1529.json
printf '%s\n' '---'
jq '{mode, no_reply, suppressed_before_proof_deadline, proof_target_check_gate_text, proof_wait_until_text, proof_recheck_after_at, proof_target_due_at_text, proof_target_due_at_if_next_slot_missed_text, proof_recheck_schedule_kind_text, consumer_requested_outputs_text}' /tmp/ai_proof_target_check_1529.json
exit 0
