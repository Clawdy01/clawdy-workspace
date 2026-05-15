#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
SERIES_OFFSET = 15

proc = subprocess.run(
    ['python3', str(SCRIPT), '--list-cases'],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
)
if proc.returncode != 0:
    raise SystemExit(proc.stderr or proc.stdout or f'--list-cases faalde met code {proc.returncode}')

all_cases = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
discoverable_count = len(all_cases)
max_feasible_series = discoverable_count + SERIES_OFFSET
next_blocked_series = max_feasible_series + 1
required_valid_for_next_blocked = next_blocked_series - SERIES_OFFSET

print(
    '\n'.join(
        [
            f'discoverable_count={discoverable_count}',
            f'max_feasible_series={max_feasible_series}',
            f'next_blocked_series={next_blocked_series}',
            f'required_valid_for_next_blocked={required_valid_for_next_blocked}',
            f'available_last_case={all_cases[-1] if all_cases else "NONE"}',
        ]
    )
)
