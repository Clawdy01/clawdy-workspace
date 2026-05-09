#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-sixty-three'),
    ('driehonderdeenenzestig', 'driehonderddrieënzestig'),
    ('all_cases[:356]', 'all_cases[:358]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:358]'),
    ('!= 356', '!= 358'),
    (' 353, 354, 355]', ' 353, 354, 355, 356, 357]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-sixty-three-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
