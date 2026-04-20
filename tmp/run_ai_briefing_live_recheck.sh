#!/usr/bin/env bash
set +e
cd /home/clawdy/.openclaw/workspace
python3 scripts/ai-briefing-proof-recheck.py --json > /tmp/ai_proof_recheck_live_cron.json
rc1=$?
python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3 > /tmp/ai_watchdog_live_cron.json
rc2=$?
python3 scripts/ai-briefing-watchdog-alert.py --mode proof-target-check --json --consumer-bundle board-suite > /tmp/ai_proof_target_check_live_cron.json
rc3=$?
printf 'proof_recheck_rc=%s\nwatchdog_rc=%s\nproof_target_check_rc=%s\n' "$rc1" "$rc2" "$rc3"
jq '{result_kind, proof_blocker_kind, proof_wait_until_text, proof_recheck_after_at, proof_target_due_at, proof_target_due_at_if_next_slot_missed, proof_recheck_schedule_kind_text, proof_recheck_schedule_text, proof_config_hash, last_run_config_relation, last_run_config_relation_text}' /tmp/ai_proof_recheck_live_cron.json
echo '---'
jq '{proof_state, proof_blocker_kind, proof_runs_remaining, proof_target_met, proof_wait_until_text, proof_next_qualifying_slot_at, proof_recheck_after_at, proof_target_due_at, proof_target_due_at_if_next_slot_missed, proof_target_check_gate, proof_target_check_gate_text, proof_recheck_schedule_kind_text, proof_recheck_schedule_text, proof_config_hash, last_run_config_relation, last_run_config_relation_text}' /tmp/ai_watchdog_live_cron.json
echo '---'
jq '{mode, no_reply, suppressed_before_proof_deadline, proof_target_check_gate, proof_target_check_gate_text, proof_wait_until_text, proof_recheck_after_at, proof_target_due_at, proof_target_due_at_if_next_slot_missed, proof_recheck_schedule_kind_text, proof_recheck_schedule_text, consumer_requested_output_count, consumer_requested_output_channel_count, consumer_requested_outputs_status_kind, consumer_requested_outputs_text}' /tmp/ai_proof_target_check_live_cron.json
exit 0
