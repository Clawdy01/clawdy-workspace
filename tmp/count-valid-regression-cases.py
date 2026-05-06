#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
UNKNOWN = 'definitely-not-a-real-regression-case'
TYPO = 'regression-check-list-case-output'

proc = subprocess.run(
    ['python3', str(SCRIPT), '--list-cases'],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
)
if proc.returncode != 0:
    raise SystemExit(proc.stderr or proc.stdout)
all_cases = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
valid_cases = [case for case in all_cases if case not in {UNKNOWN, TYPO}]
print(f'all_cases={len(all_cases)}')
print(f'valid_cases_excluding_unknown_and_typo={len(valid_cases)}')
print(f'last_valid_case={valid_cases[-1]}')
