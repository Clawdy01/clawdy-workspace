#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 -m py_compile scripts/creative-review.py
TEST_ROOT=tmp/creative-review-cleanup-log-test
REPORTS="$TEST_ROOT/reports"
LOGS="$TEST_ROOT/logs"
rm -rf "$TEST_ROOT"
mkdir -p "$REPORTS" "$LOGS"
OLD_REPORT="$REPORTS/creative-review-mixed-review.json"
OLD_DAYLOG="$REPORTS/creative-review-daylog-20260320.jsonl"
NEW_REPORT="$REPORTS/creative-review-mixed-review-recent.json"
printf '{"old":true}\n' > "$OLD_REPORT"
printf '{"old_daylog":true}\n' > "$OLD_DAYLOG"
printf '{"recent":true}\n' > "$NEW_REPORT"
touch -d '10 days ago' "$OLD_REPORT"
touch -d '20 days ago' "$OLD_DAYLOG"
touch -d '1 day ago' "$NEW_REPORT"
python3 scripts/creative-review.py cleanup-only --cleanup-preset balanced --cleanup-log --cleanup-log-dir "$LOGS" --report-dir "$REPORTS" --format json > /tmp/creative_cleanup_dryrun.json
python3 scripts/creative-review.py weekly-cleanup --cleanup-log --cleanup-log-dir "$LOGS" --report-dir "$REPORTS" --format json > /tmp/creative_cleanup_apply.json
printf '\nDRYRUN\n'
cat /tmp/creative_cleanup_dryrun.json
printf '\nAPPLY\n'
cat /tmp/creative_cleanup_apply.json
printf '\nFILES\n'
find "$TEST_ROOT" -maxdepth 2 -type f | sort
