#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-seventy'),
    ('driehonderdeenenzestig', 'driehonderdzeventig'),
    ('all_cases[:356]', 'all_cases[:365]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:365]'),
    ('!= 356', '!= 365'),
    (' 353, 354, 355]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-seventy-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
