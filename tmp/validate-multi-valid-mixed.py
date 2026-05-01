#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
EXPECTED_VALID = 'watchdog-all-routes-full-sweep'
UNKNOWN = 'definitely-not-a-real-regression-case'
TYPO = 'regression-check-list-case-output'
SUGGESTION = 'regression-check-list-cases-output'


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
second_valid = next(
    case_name
    for case_name in all_cases
    if case_name not in {EXPECTED_VALID, UNKNOWN, TYPO}
)

case_names = [
    EXPECTED_VALID,
    UNKNOWN,
    second_valid,
    TYPO,
    second_valid,
    EXPECTED_VALID,
    UNKNOWN,
    TYPO,
]
case_args = [arg for case_name in case_names for arg in ('--case', case_name)]
expected_requested = unique(case_names)
expected_selected = [EXPECTED_VALID, second_valid]
expected_unknown = [UNKNOWN, TYPO]

plain_proc = run(*case_args)
if plain_proc.returncode != 2:
    raise SystemExit(f'plain exitcode verwacht 2, kreeg {plain_proc.returncode}')
if plain_proc.stdout.strip():
    raise SystemExit('plain run hoort geen stdout te geven')
expected_stderr = 'geldige regressiecases in dezelfde aanvraag: ' + ', '.join(expected_selected)
if expected_stderr not in (plain_proc.stderr or ''):
    raise SystemExit('plain stderr noemt niet beide geldige first-seen cases')

json_proc = run('--json', *case_args)
if json_proc.returncode != 2:
    raise SystemExit(f'json exitcode verwacht 2, kreeg {json_proc.returncode}')
json_payload = json.loads((json_proc.stdout or json_proc.stderr).strip())
if json_payload.get('requested_case_names') != expected_requested:
    raise SystemExit(f'json requested_case_names mismatch: {json_payload.get("requested_case_names")} != {expected_requested}')
if json_payload.get('selected_case_names') != expected_selected:
    raise SystemExit(f'json selected_case_names mismatch: {json_payload.get("selected_case_names")} != {expected_selected}')
if json_payload.get('selected_case_count') != len(expected_selected):
    raise SystemExit(f'json selected_case_count mismatch: {json_payload.get("selected_case_count")} != {len(expected_selected)}')
if json_payload.get('unknown_case_names') != expected_unknown:
    raise SystemExit(f'json unknown_case_names mismatch: {json_payload.get("unknown_case_names")} != {expected_unknown}')
if json_payload.get('unknown_case_count') != len(expected_unknown):
    raise SystemExit(f'json unknown_case_count mismatch: {json_payload.get("unknown_case_count")} != {len(expected_unknown)}')
if json_payload.get('available_case_names') != all_cases:
    raise SystemExit('json available_case_names mismatch met volledige --list-cases uitvoer')
if json_payload.get('available_case_count') != len(all_cases):
    raise SystemExit(f'json available_case_count mismatch: {json_payload.get("available_case_count")} != {len(all_cases)}')
suggestions = json_payload.get('suggested_case_names_by_input')
if not isinstance(suggestions, dict):
    raise SystemExit('json suggested_case_names_by_input ontbreekt of is geen dict')
if suggestions.get(UNKNOWN) != []:
    raise SystemExit(f'json suggestions voor echte onbekende hoort [] te zijn, kreeg {suggestions.get(UNKNOWN)}')
if SUGGESTION not in (suggestions.get(TYPO) or []):
    raise SystemExit(f'json suggestions voor typo mist {SUGGESTION}: {suggestions.get(TYPO)}')

plain_list_proc = run('--list-cases', *case_args)
if plain_list_proc.returncode != 2:
    raise SystemExit(f'plain --list-cases exitcode verwacht 2, kreeg {plain_list_proc.returncode}')
if (plain_list_proc.stderr or '') != (plain_proc.stderr or ''):
    raise SystemExit('plain --list-cases stderr wijkt af van gewone run')

json_list_proc = run('--json', '--list-cases', *case_args)
if json_list_proc.returncode != 2:
    raise SystemExit(f'json --list-cases exitcode verwacht 2, kreeg {json_list_proc.returncode}')
json_list_payload = json.loads((json_list_proc.stdout or json_list_proc.stderr).strip())
if json_list_payload.get('requested_case_names') != expected_requested:
    raise SystemExit(f'json --list-cases requested_case_names mismatch: {json_list_payload.get("requested_case_names")} != {expected_requested}')
if json_list_payload.get('selected_case_names') != expected_selected:
    raise SystemExit(f'json --list-cases selected_case_names mismatch: {json_list_payload.get("selected_case_names")} != {expected_selected}')
if json_list_payload.get('selected_case_count') != len(expected_selected):
    raise SystemExit(f'json --list-cases selected_case_count mismatch: {json_list_payload.get("selected_case_count")} != {len(expected_selected)}')
if json_list_payload.get('unknown_case_names') != expected_unknown:
    raise SystemExit(f'json --list-cases unknown_case_names mismatch: {json_list_payload.get("unknown_case_names")} != {expected_unknown}')
if json_list_payload.get('unknown_case_count') != len(expected_unknown):
    raise SystemExit(f'json --list-cases unknown_case_count mismatch: {json_list_payload.get("unknown_case_count")} != {len(expected_unknown)}')
if json_list_payload.get('available_case_names') != all_cases:
    raise SystemExit('json --list-cases available_case_names mismatch met volledige --list-cases uitvoer')
if json_list_payload.get('available_case_count') != len(all_cases):
    raise SystemExit(f'json --list-cases available_case_count mismatch: {json_list_payload.get("available_case_count")} != {len(all_cases)}')
list_suggestions = json_list_payload.get('suggested_case_names_by_input')
if not isinstance(list_suggestions, dict):
    raise SystemExit('json --list-cases suggested_case_names_by_input ontbreekt of is geen dict')
if list_suggestions.get(UNKNOWN) != []:
    raise SystemExit(f'json --list-cases suggestions voor echte onbekende hoort [] te zijn, kreeg {list_suggestions.get(UNKNOWN)}')
if SUGGESTION not in (list_suggestions.get(TYPO) or []):
    raise SystemExit(f'json --list-cases suggestions voor typo mist {SUGGESTION}: {list_suggestions.get(TYPO)}')

json_fields = {
    key: value
    for key, value in json_payload.items()
    if key not in {
        'generated_at',
        'generated_at_text',
        'started_at',
        'started_at_text',
        'duration_ms',
        'duration_seconds',
        'duration_text',
    }
}
json_list_fields = {
    key: value
    for key, value in json_list_payload.items()
    if key not in {
        'generated_at',
        'generated_at_text',
        'started_at',
        'started_at_text',
        'duration_ms',
        'duration_seconds',
        'duration_text',
    }
}
if json_list_fields != json_fields:
    raise SystemExit('json en json --list-cases unknown-cases payloads horen buiten runtime-metadata identiek te zijn')

print(json.dumps({
    'ok': True,
    'second_valid_case_name': second_valid,
    'requested_case_names': expected_requested,
    'selected_case_names_json': expected_selected,
    'selected_case_names_json_list_cases': expected_selected,
    'unknown_case_names': expected_unknown,
}, ensure_ascii=False))
