#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-six', 'three-hundred-seventy-seven'),
    ('driehonderdzesenzeventig', 'driehonderdzevenenzeventig'),
    ('all_cases[:371]', 'all_cases[:372]'),
    ('{UNKNOWN, TYPO}][:371]', '{UNKNOWN, TYPO}][:372]'),
    ('!= 371', '!= 372'),
    ('367, 368, 369, 370]', '367, 368, 369, 370, 371]'),
]
for name in (
    'create-three-hundred-seventy-six-files.py',
    'create-three-hundred-seventy-six.py',
    'generate-validate-three-hundred-seventy-six.py',
    'validate-three-hundred-seventy-six-valid-list-cases.py',
    'validate-three-hundred-seventy-six-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-seventy-six', 'three-hundred-seventy-seven')).write_text(text)
