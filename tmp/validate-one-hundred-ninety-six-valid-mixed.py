#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
UNKNOWN = 'definitely-not-a-real-regression-case'
TYPO = 'regression-check-list-case-output'
SUGGESTION = 'regression-check-list-cases-output'
ORDER = [58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 26, 28, 24, 27, 22, 25, 20, 23, 18, 21, 16, 19, 14, 17, 12, 15, 10, 13, 8, 11, 6, 9, 4, 7, 2, 5, 0, 3, 1, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193]


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
valid_cases = [case_name for case_name in all_cases if case_name not in {UNKNOWN, TYPO}][:195]
if len(valid_cases) != 195:
    raise SystemExit(f'kon geen honderdzesennegentig geldige casenamen vinden, kreeg {valid_cases}')

valid_order = [valid_cases[index] for index in ORDER]
case_names = valid_order[:1] + [UNKNOWN] + valid_order[1:3] + [TYPO] + valid_order[3:] + valid_order[:1] + [UNKNOWN] + valid_order[1:3] + [TYPO] + valid_order[3:]
case_args = [arg for case_name in case_names for arg in ('--case', case_name)]
expected_requested = unique(case_names)
expected_selected = valid_order
expected_unknown = [UNKNOWN, TYPO]

plain_proc = run(*case_args)
if plain_proc.returncode != 2:
    raise SystemExit(f'plain exitcode verwacht 2, kreeg {plain_proc.returncode}')
if plain_proc.stdout.strip():
    raise SystemExit('plain run hoort geen stdout te geven')
expected_stderr = 'geldige regressiecases in dezelfde aanvraag: ' + ', '.join(expected_selected)
if expected_stderr not in (plain_proc.stderr or ''):
    raise SystemExit('plain stderr noemt niet alle honderdzesennegentig geldige first-seen cases')

json_proc = run('--json', *case_args)
if json_proc.returncode != 2:
    raise SystemExit(f'json exitcode verwacht 2, kreeg {json_proc.returncode}')
json_payload = json.loads((json_proc.stdout or json_proc.stderr).strip())
json_list_proc = run('--json', '--list-cases', *case_args)
if json_list_proc.returncode != 2:
    raise SystemExit(f'json --list-cases exitcode verwacht 2, kreeg {json_list_proc.returncode}')
json_list_payload = json.loads((json_list_proc.stdout or json_list_proc.stderr).strip())
plain_list_proc = run('--list-cases', *case_args)
if plain_list_proc.returncode != 2:
    raise SystemExit(f'plain --list-cases exitcode verwacht 2, kreeg {plain_list_proc.returncode}')
if (plain_list_proc.stderr or '') != (plain_proc.stderr or ''):
    raise SystemExit('plain --list-cases stderr wijkt af van gewone run')

for label, payload in ((('json'), json_payload), (('json --list-cases'), json_list_payload)):
    if payload.get('requested_case_names') != expected_requested:
        raise SystemExit(f'{label} requested_case_names mismatch: {payload.get("requested_case_names")} != {expected_requested}')
    if payload.get('requested_case_count') != len(expected_requested):
        raise SystemExit(f'{label} requested_case_count mismatch: {payload.get("requested_case_count")} != {len(expected_requested)}')
    if payload.get('selected_case_names') != expected_selected:
        raise SystemExit(f'{label} selected_case_names mismatch: {payload.get("selected_case_names")} != {expected_selected}')
    if payload.get('selected_case_count') != len(expected_selected):
        raise SystemExit(f'{label} selected_case_count mismatch: {payload.get("selected_case_count")} != {len(expected_selected)}')
    if payload.get('unknown_case_names') != expected_unknown:
        raise SystemExit(f'{label} unknown_case_names mismatch: {payload.get("unknown_case_names")} != {expected_unknown}')
    if payload.get('unknown_case_count') != len(expected_unknown):
        raise SystemExit(f'{label} unknown_case_count mismatch: {payload.get("unknown_case_count")} != {len(expected_unknown)}')
    if payload.get('available_case_names') != all_cases:
        raise SystemExit(f'{label} available_case_names mismatch met volledige --list-cases uitvoer')
    if payload.get('available_case_count') != len(all_cases):
        raise SystemExit(f'{label} available_case_count mismatch: {payload.get("available_case_count")} != {len(all_cases)}')
    suggestions = payload.get('suggested_case_names_by_input')
    if not isinstance(suggestions, dict):
        raise SystemExit(f'{label} suggested_case_names_by_input ontbreekt of is geen dict')
    if suggestions.get(UNKNOWN) != []:
        raise SystemExit(f'{label} suggestions voor echte onbekende hoort [] te zijn, kreeg {suggestions.get(UNKNOWN)}')
    if SUGGESTION not in (suggestions.get(TYPO) or []):
        raise SystemExit(f'{label} suggestions voor typo mist {SUGGESTION}: {suggestions.get(TYPO)}')

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
    'valid_case_names': valid_cases,
    'requested_case_names': expected_requested,
    'selected_case_names': expected_selected,
    'unknown_case_names': expected_unknown,
}, ensure_ascii=False))
