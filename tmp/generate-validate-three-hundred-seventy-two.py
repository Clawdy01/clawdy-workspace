#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-seventy-two'),
    ('driehonderdeenenzestig', 'driehonderdtweeënzeventig'),
    ('all_cases[:356]', 'all_cases[:367]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:367]'),
    ('!= 356', '!= 367'),
    (' 353, 354, 355]', ' 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-seventy-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
