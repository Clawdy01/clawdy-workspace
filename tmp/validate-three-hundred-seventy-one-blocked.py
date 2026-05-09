#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
EXPECTED_AVAILABLE_COUNT = 365
TARGET_VALID_COUNT = 366

proc = subprocess.run(
    ['python3', str(SCRIPT), '--list-cases'],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
)
if proc.returncode != 0:
    raise SystemExit(f'--list-cases faalde met code {proc.returncode}: {proc.stderr or proc.stdout}')

all_cases = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
if len(all_cases) != EXPECTED_AVAILABLE_COUNT:
    raise SystemExit(
        f'verwacht {EXPECTED_AVAILABLE_COUNT} beschikbare casenamen, kreeg {len(all_cases)}: {all_cases}'
    )

unique_cases = list(dict.fromkeys(all_cases))
if unique_cases != all_cases:
    raise SystemExit('verwacht unieke volgorde in --list-cases uitvoer')

if len(all_cases[:TARGET_VALID_COUNT]) >= TARGET_VALID_COUNT:
    raise SystemExit(
        f'verwacht blokkade onder {TARGET_VALID_COUNT} geldige casenamen, maar slice leverde {len(all_cases[:TARGET_VALID_COUNT])}'
    )

print(json.dumps({
    'ok': True,
    'blocked_target_valid_case_count': TARGET_VALID_COUNT,
    'available_case_count': len(all_cases),
    'missing_case_count': TARGET_VALID_COUNT - len(all_cases),
    'last_available_case_name': all_cases[-1],
}, ensure_ascii=False))
