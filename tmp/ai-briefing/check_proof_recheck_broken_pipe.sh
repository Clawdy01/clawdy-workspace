#!/usr/bin/env bash
set -eu
python3 /home/clawdy/.openclaw/workspace/scripts/ai-briefing-proof-recheck.py --json | head -n 1 >/dev/null
python3 /home/clawdy/.openclaw/workspace/scripts/ai-briefing-proof-recheck.py | head -n 1 >/dev/null
