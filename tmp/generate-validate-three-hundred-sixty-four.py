#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty-one', 'three-hundred-sixty-four'),
    ('driehonderdeenenzestig', 'driehonderdvierenzestig'),
    ('all_cases[:356]', 'all_cases[:359]'),
    ('{UNKNOWN, TYPO}][:356]', '{UNKNOWN, TYPO}][:359]'),
    ('!= 356', '!= 359'),
    (' 353, 354, 355]', ' 353, 354, 355, 356, 357, 358]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-sixty-four-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
