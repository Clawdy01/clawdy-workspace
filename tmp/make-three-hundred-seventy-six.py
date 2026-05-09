#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace/tmp')
repls = [
    ('three-hundred-seventy-five', 'three-hundred-seventy-six'),
    ('driehonderdvijfenzeventig', 'driehonderdzesenzeventig'),
    ('all_cases[:370]', 'all_cases[:371]'),
    ('{UNKNOWN, TYPO}][:370]', '{UNKNOWN, TYPO}][:371]'),
    ('!= 370', '!= 371'),
    ('366, 367, 368, 369]', '366, 367, 368, 369, 370]'),
]
for name in (
    'create-three-hundred-seventy-five-files.py',
    'create-three-hundred-seventy-five.py',
    'generate-validate-three-hundred-seventy-five.py',
    'validate-three-hundred-seventy-five-valid-list-cases.py',
    'validate-three-hundred-seventy-five-valid-mixed.py',
):
    text = (root / name).read_text()
    for old, new in repls:
        text = text.replace(old, new)
    (root / name.replace('three-hundred-seventy-five', 'three-hundred-seventy-six')).write_text(text)
