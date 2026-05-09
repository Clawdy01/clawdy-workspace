#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-nine', 'three-hundred-seventy'),
    ('driehonderdnegenenzestig', 'driehonderdzeventig'),
    ('all_cases[:364]', 'all_cases[:365]'),
    ('{UNKNOWN, TYPO}][:364]', '{UNKNOWN, TYPO}][:365]'),
    ('!= 364', '!= 365'),
    ('356, 357, 358, 359, 360, 361, 362, 363]', '356, 357, 358, 359, 360, 361, 362, 363, 364]'),
]

for name in (
    'generate-validate-three-hundred-sixty-nine.py',
    'validate-three-hundred-sixty-nine-valid-list-cases.py',
    'validate-three-hundred-sixty-nine-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-nine', 'three-hundred-seventy')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
