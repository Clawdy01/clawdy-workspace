#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-sixty-nine'),
    ('driehonderdeenenzestig', 'driehonderdnegenenzestig'),
    ('all_cases[:356]', 'all_cases[:364]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:364]'),
    ('!= 356', '!= 364'),
    (' 353, 354, 355]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-sixty-nine-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
