#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 -m py_compile scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-watchdog-producer.py
python3 scripts/ai-briefing-watchdog-alert.py --mode proof-progress --reference-ms 1776495540000
python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet --reference-ms 1776495540000
