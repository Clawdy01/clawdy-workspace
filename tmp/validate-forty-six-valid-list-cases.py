#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
ORDER = [45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 26, 28, 24, 27, 22, 25, 20, 23, 18, 21, 16, 19, 14, 17, 12, 15, 10, 13, 8, 11, 6, 9, 4, 7, 2, 5, 0, 3, 1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ['python3', str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def unique(seq):
    out = []
    for item in seq:
        if item not in out:
            out.append(item)
    return out


list_proc = run('--list-cases')
if list_proc.returncode != 0:
    raise SystemExit(f'--list-cases faalde met code {list_proc.returncode}: {list_proc.stderr or list_proc.stdout}')
all_cases = [line.strip() for line in list_proc.stdout.splitlines() if line.strip()]
valid_cases = all_cases[:46]
if len(valid_cases) != 46:
    raise SystemExit(f'kon geen zesenveertig geldige casenamen vinden, kreeg {valid_cases}')

case_names = [valid_cases[index] for index in ORDER] + [valid_cases[index] for index in ORDER]
case_args = [arg for case_name in case_names for arg in ('--case', case_name)]
expected_requested = unique(case_names)
expected_discoverable = sorted(expected_requested)

plain_list_proc = run('--list-cases', *case_args)
if plain_list_proc.returncode != 0:
    raise SystemExit(f'plain --list-cases exitcode verwacht 0, kreeg {plain_list_proc.returncode}')
if plain_list_proc.stderr.strip():
    raise SystemExit(f'plain --list-cases hoort geen stderr te geven, kreeg: {plain_list_proc.stderr}')
plain_list_cases = [line.strip() for line in plain_list_proc.stdout.splitlines() if line.strip()]
if plain_list_cases != expected_discoverable:
    raise SystemExit(f'plain --list-cases mismatch: {plain_list_cases} != {expected_discoverable}')

json_list_proc = run('--json', '--list-cases', *case_args)
if json_list_proc.returncode != 0:
    raise SystemExit(f'json --list-cases exitcode verwacht 0, kreeg {json_list_proc.returncode}')
if json_list_proc.stderr.strip():
    raise SystemExit(f'json --list-cases hoort geen stderr te geven, kreeg: {json_list_proc.stderr}')
json_list_payload = json.loads(json_list_proc.stdout)
if json_list_payload.get('requested_case_names') != expected_requested:
    raise SystemExit(
        'json --list-cases requested_case_names mismatch: '
        f'{json_list_payload.get("requested_case_names")} != {expected_requested}'
    )
if json_list_payload.get('requested_case_count') != len(expected_requested):
    raise SystemExit(
        'json --list-cases requested_case_count mismatch: '
        f'{json_list_payload.get("requested_case_count")} != {len(expected_requested)}'
    )
if json_list_payload.get('selected_case_names') != expected_discoverable:
    raise SystemExit(
        'json --list-cases selected_case_names mismatch: '
        f'{json_list_payload.get("selected_case_names")} != {expected_discoverable}'
    )
if json_list_payload.get('selected_case_count') != len(expected_discoverable):
    raise SystemExit(
        'json --list-cases selected_case_count mismatch: '
        f'{json_list_payload.get("selected_case_count")} != {len(expected_discoverable)}'
    )
if json_list_payload.get('cases') != expected_discoverable:
    raise SystemExit(f'json --list-cases cases mismatch: {json_list_payload.get("cases")} != {expected_discoverable}')
if json_list_payload.get('case_count') != len(expected_discoverable):
    raise SystemExit(
        'json --list-cases case_count mismatch: '
        f'{json_list_payload.get("case_count")} != {len(expected_discoverable)}'
    )
if json_list_payload.get('available_case_names') != all_cases:
    raise SystemExit('json --list-cases available_case_names mismatch met volledige --list-cases uitvoer')
if json_list_payload.get('available_case_count') != len(all_cases):
    raise SystemExit(
        'json --list-cases available_case_count mismatch: '
        f'{json_list_payload.get("available_case_count")} != {len(all_cases)}'
    )
if json_list_payload.get('ok') is not True:
    raise SystemExit(f'json --list-cases ok verwacht True, kreeg {json_list_payload.get("ok")}')

print(json.dumps({
    'ok': True,
    'valid_case_names': valid_cases,
    'requested_case_names': expected_requested,
    'discoverable_case_names': expected_discoverable,
}, ensure_ascii=False))
