#!/usr/bin/env python3
from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
repls = [
    ('three-hundred-sixty', 'three-hundred-sixty-one'),
    ('driehonderdzestig', 'driehonderdeenenzestig'),
    ('all_cases[:355]', 'all_cases[:356]'),
    ('{UNKNOWN, TYPO}][:355]', '{UNKNOWN, TYPO}][:356]'),
    ('!= 355', '!= 356'),
    (' 353, 354]', ' 353, 354, 355]'),
]

for kind in ('valid-list-cases', 'valid-mixed'):
    src = root / 'tmp' / f'validate-three-hundred-sixty-{kind}.py'
    dst = root / 'tmp' / f'validate-three-hundred-sixty-one-{kind}.py'
    text = src.read_text()
    for old, new in repls:
        text = text.replace(old, new)
    dst.write_text(text)
