#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-sixty-two'),
    ('driehonderdeenenzestig', 'driehonderdtweeënzestig'),
    ('all_cases[:356]', 'all_cases[:357]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:357]'),
    ('!= 356', '!= 357'),
    (' 353, 354, 355]', ' 353, 354, 355, 356]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-sixty-two-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
