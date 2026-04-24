#!/usr/bin/env bash
set -euo pipefail
sleep 75
python3 scripts/open-deliverables.py list --open-only
printf '\n---STATUS---\n'
python3 scripts/ai-briefing-status.py --json
printf '\n---WATCHDOG---\n'
python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3
printf '\n---PROOF-RECHECK---\n'
python3 scripts/ai-briefing-proof-recheck.py --json
printf '\n---ALERT---\n'
python3 scripts/ai-briefing-watchdog-alert.py --mode proof-target-check --json --consumer-bundle board-suite
