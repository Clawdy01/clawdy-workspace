#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-seven', 'three-hundred-sixty-eight'),
    ('driehonderdzevenenzestig', 'driehonderdachtenzestig'),
    ('all_cases[:362]', 'all_cases[:363]'),
    ('{UNKNOWN, TYPO}][:362]', '{UNKNOWN, TYPO}][:363]'),
    ('!= 362', '!= 363'),
    ('355, 356, 357, 358, 359, 360, 361]', '355, 356, 357, 358, 359, 360, 361, 362]'),
]

for name in (
    'generate-validate-three-hundred-sixty-seven.py',
    'validate-three-hundred-sixty-seven-valid-list-cases.py',
    'validate-three-hundred-sixty-seven-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-seven', 'three-hundred-sixty-eight')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
