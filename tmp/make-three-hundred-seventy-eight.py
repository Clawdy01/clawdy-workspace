#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-seven', 'three-hundred-seventy-eight'),
    ('driehonderdzevenenzeventig', 'driehonderdachtenzeventig'),
    ('all_cases[:372]', 'all_cases[:373]'),
    ('{UNKNOWN, TYPO}][:372]', '{UNKNOWN, TYPO}][:373]'),
    ('!= 372', '!= 373'),
    ('367, 368, 369, 370, 371]', '367, 368, 369, 370, 371, 372]'),
]
for name in (
    'create-three-hundred-seventy-seven-files.py',
    'create-three-hundred-seventy-seven.py',
    'generate-validate-three-hundred-seventy-seven.py',
    'validate-three-hundred-seventy-seven-valid-list-cases.py',
    'validate-three-hundred-seventy-seven-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-seventy-seven', 'three-hundred-seventy-eight')).write_text(text)
