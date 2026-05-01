#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
script = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
case_name = 'regression-check-list-case-output'
commands = {
    'list_cases': ['python3', str(script), '--json', '--list-cases', '--case', case_name],
    'run': ['python3', str(script), '--json', '--case', case_name],
}
results = {}
for label, cmd in commands.items():
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 2:
        raise SystemExit(f'{label} returncode expected 2, got {proc.returncode}')
    payload = json.loads((proc.stdout or proc.stderr).strip())
    results[label] = payload

runtime_fields = {
    'generated_at', 'generated_at_text', 'started_at', 'started_at_text',
    'duration_ms', 'duration_seconds', 'duration_text',
}

def strip_runtime_metadata(payload):
    return {k: v for k, v in payload.items() if k not in runtime_fields}

if strip_runtime_metadata(results['list_cases']) != strip_runtime_metadata(results['run']):
    raise SystemExit('list-cases typo payload differs from regular run typo payload')

payload = results['list_cases']
assert payload['ok'] is False
assert payload['error'] == 'unknown-cases'
assert payload['requested_case_names'] == [case_name]
assert payload['requested_case_count'] == 1
assert payload['selected_case_names'] == []
assert payload['selected_case_count'] == 0
assert payload['unknown_case_names'] == [case_name]
assert payload['unknown_case_count'] == 1
assert payload['available_case_count'] == len(payload['available_case_names'])
assert 'regression-check-list-cases-output' in (payload['suggested_case_names_by_input'] or {}).get(case_name, [])
print('ok')
