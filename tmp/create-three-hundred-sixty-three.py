#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-two', 'three-hundred-sixty-three'),
    ('driehonderdtweeënzestig', 'driehonderddrieënzestig'),
    ('all_cases[:357]', 'all_cases[:358]'),
    ('{UNKNOWN, TYPO}][:357]', '{UNKNOWN, TYPO}][:358]'),
    ('!= 357', '!= 358'),
    ('353, 354, 355, 356]', '353, 354, 355, 356, 357]'),
]

for name in (
    'generate-validate-three-hundred-sixty-two.py',
    'validate-three-hundred-sixty-two-valid-list-cases.py',
    'validate-three-hundred-sixty-two-valid-mixed.py',
):
    src = root / 'tmp' / name
    dst = root / 'tmp' / name.replace('three-hundred-sixty-two', 'three-hundred-sixty-three')
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
