#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-seven', 'three-hundred-sixty-nine'),
    ('driehonderdzevenenzestig', 'driehonderdnegenenzestig'),
    ('all_cases[:362]', 'all_cases[:364]'),
    ('{UNKNOWN, TYPO}][:362]', '{UNKNOWN, TYPO}][:364]'),
    ('!= 362', '!= 364'),
    ('355, 356, 357, 358, 359, 360, 361]', '355, 356, 357, 358, 359, 360, 361, 362, 363]'),
]

for name in (
    'generate-validate-three-hundred-sixty-seven.py',
    'validate-three-hundred-sixty-seven-valid-list-cases.py',
    'validate-three-hundred-sixty-seven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-seven', 'three-hundred-sixty-nine')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
