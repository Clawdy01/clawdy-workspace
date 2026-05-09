#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-three', 'three-hundred-sixty-four'),
    ('driehonderddrieënzestig', 'driehonderdvierenzestig'),
    ('all_cases[:358]', 'all_cases[:359]'),
    ('{UNKNOWN, TYPO}][:358]', '{UNKNOWN, TYPO}][:359]'),
    ('!= 358', '!= 359'),
    ('353, 354, 355, 356, 357]', '353, 354, 355, 356, 357, 358]'),
]

for name in (
    'generate-validate-three-hundred-sixty-three.py',
    'validate-three-hundred-sixty-three-valid-list-cases.py',
    'validate-three-hundred-sixty-three-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-three', 'three-hundred-sixty-four')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
